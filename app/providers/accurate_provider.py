from fastapi import FastAPI
import asyncio
import random

from app.models.model import AccurateSTTRequest, AccurateSTTResponse



app = FastAPI()



@app.post("/transcribe", response_model=AccurateSTTResponse)
async def transcribe(request: AccurateSTTRequest):
    
    random_processing_time_ms = random.randint(200, 500)
    
    await asyncio.sleep(random_processing_time_ms / 1000)  # Convert ms to seconds
    
    return AccurateSTTResponse(
        transcript="Hello, this is a fake transcription from AccurateSTT.",
        confidence=0.93,
        duration_sec=5.2
    )