from abc import ABC, abstractmethod

from pydantic import BaseModel


class AudioSynthesisResult(BaseModel):
    b64_audio: str
    mime_type: str = "audio/mp3"
    duration_seconds: float = 3.0
    model: str = "juhi-tts-v1"
    voice_id: str = "juhi-warm"


class BaseAudioProvider(ABC):
    @abstractmethod
    async def synthesize_speech(
        self,
        text: str,
        voice_id: str | None = None,
        speed: float = 1.0,
    ) -> AudioSynthesisResult:
        pass
