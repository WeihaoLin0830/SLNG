from fastapi import FastAPI
import asyncio
import random

from app.models.model import FastTranscribeRequest, FastTranscribeResponse



app = FastAPI()



@app.post("/transcribe", response_model=FastTranscribeResponse)
async def transcribe(request: FastTranscribeRequest):
    
    random_confidence_score = random.randint(70, 99)
    random_processing_time_ms = random.randint(100, 300)
    
    await asyncio.sleep(random_processing_time_ms / 1000)  # Convert ms to seconds
    
    return FastTranscribeResponse(
        text="Hello, this is a fake transcription from FastTranscribe.",
        confidence_score=random_confidence_score,
        processing_ms=random_processing_time_ms
    )