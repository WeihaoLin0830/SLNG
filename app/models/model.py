from pydantic import BaseModel

# =========================================================

class ModelsResponse(BaseModel):
    models: list[str]

# =========================================================

class FastTranscribeRequest(BaseModel):
    audio_data: str
    lang: str
    model_type: str
    add_punctuation: bool = True


class FastTranscribeResponse(BaseModel):
    text: str
    confidence_score: int
    processing_ms: int

# =========================================================

class AccurateSTTRequest(BaseModel):
    audio_file: str
    language_code: str
    accuracy_level: str


class AccurateSTTResponse(BaseModel):
    transcript: str
    confidence: float
    duration_sec: float

# =========================================================

class GatewayRequest(BaseModel):
    audio_url: str
    provider: str | None = None
    language: str
    model: str


class GatewayResponse(BaseModel):
    transcript: str
    provider: str
    confidence: float
    metadata: dict