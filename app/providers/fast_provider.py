import asyncio
import random

from fastapi import FastAPI

from app.models.model import (
    FastTranscribeRequest,
    FastTranscribeResponse
)


app = FastAPI()


# Fake FastTranscribe API. It accepts the provider-specific request shape and returns a simulated transcription response.
@app.post("/transcribe", response_model=FastTranscribeResponse)
async def transcribe(request: FastTranscribeRequest):
    
    random_confidence_score = random.randint(70, 99) # Simulate a random confidence score between 70% and 99%.
    random_processing_time_ms = random.randint(100, 300)

    # Add a fake delay of 100 to 300ms.
    await asyncio.sleep(random_processing_time_ms / 1000)

    return FastTranscribeResponse(
        text="Hello, this is a fake transcription from FastTranscribe.",
        confidence_score=random_confidence_score,
        processing_ms=random_processing_time_ms
    )
