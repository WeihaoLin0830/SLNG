from fastapi import FastAPI
from fastapi.responses import JSONResponse
import httpx
import time

from app.models.model import (
    FastTranscribeRequest,
    AccurateSTTRequest,
    GatewayRequest,
    GatewayResponse,
    ModelsResponse
)



app = FastAPI()



FAST_TRANSCRIBE_URL = "http://localhost:8001/transcribe"
ACCURATE_STT_URL = "http://localhost:8002/transcribe"



FAST_MODEL_MAPPING = {
    "general": "base",
    "phone_call": "telephony"
}

ACCURATE_LANGUAGE_MAPPING = {
    "en": "en-US"
}

ACCURATE_MODEL_MAPPING = {
    "general": "standard",
    "phone_call": "phone"
}



def build_fast_payload(request: GatewayRequest) -> FastTranscribeRequest:
    return FastTranscribeRequest(
        audio_data=request.audio_url,
        lang=request.language,
        model_type=FAST_MODEL_MAPPING[request.model],
        add_punctuation=True
    )

def build_accurate_payload(request: GatewayRequest) -> AccurateSTTRequest:
    return AccurateSTTRequest(
        audio_file=request.audio_url,
        language_code=ACCURATE_LANGUAGE_MAPPING[request.language],
        accuracy_level=ACCURATE_MODEL_MAPPING[request.model]
    )

def normalize_fast_response(provider_data: dict) -> GatewayResponse:
    return GatewayResponse(
        transcript=provider_data["text"],
        provider="fast_transcribe",
        confidence=provider_data["confidence_score"] / 100,
        metadata={"processing_time_ms": provider_data["processing_ms"]}
    )

def normalize_accurate_response(provider_data: dict, processing_time_ms: int) -> GatewayResponse:
    return GatewayResponse(
        transcript=provider_data["transcript"],
        provider="accurate_stt",
        confidence=provider_data["confidence"],
        metadata={"processing_time_ms": processing_time_ms}
    )



@app.post("/transcribe", response_model=GatewayResponse)
async def post_transcribe(request: GatewayRequest):
    
    if request.provider == "fast_transcribe":
        
        if request.model not in FAST_MODEL_MAPPING:
            return JSONResponse(
                status_code=400,
                content={"error": f"Unknown model: {request.model}"}
            )
        
        payload = build_fast_payload(request)
        
        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                provider_response = await client.post(
                FAST_TRANSCRIBE_URL,
                json=payload.model_dump()
                )
                
        except httpx.RequestError:
            return JSONResponse(
                status_code=502,
                content={"error": f"Provider {request.provider} unavailable"}
            )
        
        if provider_response.status_code != 200:
            return JSONResponse(
                status_code=502,
                content={"error": f"Provider {request.provider} returned an error"}
            )
            
        provider_data = provider_response.json()
        
        response = normalize_fast_response(provider_data)
        
        return response
    
    
    elif request.provider == "accurate_stt":
        
        if request.language not in ACCURATE_LANGUAGE_MAPPING:
            return JSONResponse(
                status_code=400,
                content={"error": f"Unsupported language: {request.language}"}
            )
        
        if request.model not in ACCURATE_MODEL_MAPPING:
            return JSONResponse(
                status_code=400,
                content={"error": f"Unknown model: {request.model}"}
            )
        
        payload = build_accurate_payload(request)
        
        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                
                start_time = time.perf_counter()

                provider_response = await client.post(
                ACCURATE_STT_URL,
                json=payload.model_dump()
                )
                
                processing_time_ms = round((time.perf_counter() - start_time) * 1000)
                
        except httpx.RequestError:
            return JSONResponse(
                status_code=502,
                content={"error": f"Provider {request.provider} unavailable"}
            )
        
        if provider_response.status_code != 200:
            return JSONResponse(
                status_code=502,
                content={"error": f"Provider {request.provider} returned an error"}
            )
            
        provider_data = provider_response.json()
        
        response = normalize_accurate_response(provider_data, processing_time_ms)
        
        return response
    
    
    if request.provider is None:
        return JSONResponse(
            status_code=400,
            content={"error": "Unknown provider: missing"}
        )
    
    
    else:
        return JSONResponse(
            status_code=400,
            content={"error": f"Unknown provider: {request.provider}"}
)



@app.get("/health")
async def get_health():
    return {"status": "ok"}



@app.get("/models")
async def get_models():
    return ModelsResponse(models=["fast_transcribe", "accurate_stt"])