import base64
import logging

import httpx

from app.core.config import settings
from app.core.errors import JuhiAPIException
from app.infrastructure.providers.audio.base import AudioSynthesisResult, BaseAudioProvider

logger = logging.getLogger(__name__)

# Minimal valid MP3 header/frame in base64 for offline fallback & tests
MOCK_MP3_B64 = (
    "//uQxAAAAANIAAAAAExBTUUzLjEwMFVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV"
    "VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV"
    "VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV"
)


class VeniceTTSProvider(BaseAudioProvider):
    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        default_voice: str = "juhi-warm",
        http_client: httpx.AsyncClient | None = None,
    ):
        self.api_key = api_key or settings.VENICE_API_KEY
        self.base_url = (base_url or settings.VENICE_BASE_URL).rstrip("/")
        self.default_voice = default_voice
        self._custom_client = http_client

    async def synthesize_speech(
        self,
        text: str,
        voice_id: str | None = None,
        speed: float = 1.0,
    ) -> AudioSynthesisResult:
        chosen_voice = voice_id or self.default_voice
        est_duration = max(1.0, round(len(text.split()) / 2.5, 1))

        # Offline / Test fallback when API key is not configured
        if not self.api_key:
            logger.warning("Venice API key not configured for TTS. Returning mock audio synthesis.")
            return AudioSynthesisResult(
                b64_audio=MOCK_MP3_B64,
                mime_type="audio/mp3",
                duration_seconds=est_duration,
                model="mock-tts-1",
                voice_id=chosen_voice,
            )

        url = f"{self.base_url}/audio/speech"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": "tts-1",
            "input": text,
            "voice": chosen_voice,
            "speed": speed,
            "response_format": "mp3",
        }

        client = self._custom_client or httpx.AsyncClient(timeout=60.0)
        try:
            response = await client.post(url, json=payload, headers=headers)
            if response.status_code != 200:
                raise JuhiAPIException(
                    status_code=502,
                    error_code="VENICE_TTS_ERROR",
                    message=f"Venice TTS synthesis failed ({response.status_code}): {response.text}",
                )

            audio_bytes = response.content
            b64_audio = base64.b64encode(audio_bytes).decode("utf-8")

            return AudioSynthesisResult(
                b64_audio=b64_audio,
                mime_type="audio/mp3",
                duration_seconds=est_duration,
                model="tts-1",
                voice_id=chosen_voice,
            )
        finally:
            if not self._custom_client:
                await client.aclose()
