import asyncio
import random

from fastapi import FastAPI

from app.models.model import (
    AccurateSTTRequest, 
    AccurateSTTResponse
)   


app = FastAPI()


# Fake AccurateSTT API. It accepts the provider-specific request shape and returns a simulated transcription response.
@app.post("/transcribe", response_model=AccurateSTTResponse)
async def transcribe(request: AccurateSTTRequest):
    
    random_processing_time_ms = random.randint(200, 500)

    # Add a fake delay of 200 to 500ms.
    await asyncio.sleep(random_processing_time_ms / 1000)

    return AccurateSTTResponse(
        transcript="Hello, this is a fake transcription from AccurateSTT.",
        confidence=0.93,
        duration_sec=5.2
    )
