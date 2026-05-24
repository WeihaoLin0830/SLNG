# STT Gateway Assessment

Small REST API that simulates a speech-to-text gateway. The project runs three FastAPI servers:

- Gateway on port `8000`
- FastTranscribe fake provider on port `8001`
- AccurateSTT fake provider on port `8002`

The gateway receives a unified transcription request, translates it to the selected provider format, forwards the request, and returns a normalized response.

## Project Structure

```text
app/
├── gateway/
│   └── main.py
├── models/
│   └── model.py
└── providers/
    ├── accurate_provider.py
    └── fast_provider.py
```

## Setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run The Services

Open three terminal windows from the project root.

Terminal 1:

```bash
uvicorn app.providers.fast_provider:app --reload --port 8001
```

Terminal 2:

```bash
uvicorn app.providers.accurate_provider:app --reload --port 8002
```

Terminal 3:

```bash
uvicorn app.gateway.main:app --reload --port 8000
```

## Example Requests

Health check:

```bash
curl http://localhost:8000/health
```

Available providers:

```bash
curl http://localhost:8000/models
```

Transcription through the gateway:

```bash
curl -X POST http://localhost:8000/transcribe \
  -H "Content-Type: application/json" \
  -d '{
    "audio_url": "https://example.com/audio.wav",
    "provider": "fast_transcribe",
    "language": "en",
    "model": "general"
  }'
```

Example response:

```json
{
  "transcript": "Hello, this is a fake transcription from FastTranscribe.",
  "provider": "fast_transcribe",
  "confidence": 0.87,
  "metadata": {
    "processing_time_ms": 142
  }
}
```

## Supported Providers

- `fast_transcribe`
- `accurate_stt`

## Supported Models

- `general`
- `phone_call`
