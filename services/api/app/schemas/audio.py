import uuid

from pydantic import BaseModel, Field


class SpeakTextRequest(BaseModel):
    text: str = Field(min_length=1, max_length=2000)
    voice_id: str = "juhi-warm"
    speed: float = 1.0


class SpeakMessageRequest(BaseModel):
    voice_id: str | None = None
    speed: float = 1.0


class AudioSpeechResponse(BaseModel):
    asset_id: uuid.UUID | None = None
    b64_audio: str
    mime_type: str = "audio/mp3"
    duration_seconds: float
    voice_id: str
