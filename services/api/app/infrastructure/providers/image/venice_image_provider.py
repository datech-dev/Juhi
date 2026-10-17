import logging

import httpx

from app.core.config import settings
from app.core.errors import JuhiAPIException
from app.infrastructure.providers.image.base import BaseImageProvider, ImageGenerationResult

logger = logging.getLogger(__name__)

# 1x1 transparent PNG fallback for offline testing
MOCK_PNG_B64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="


class VeniceImageProvider(BaseImageProvider):
    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        default_model: str = "fluently-xl",
        http_client: httpx.AsyncClient | None = None,
    ):
        self.api_key = api_key or settings.VENICE_API_KEY
        self.base_url = (base_url or settings.VENICE_BASE_URL).rstrip("/")
        self.default_model = default_model
        self._custom_client = http_client

    async def generate_image(
        self,
        prompt: str,
        negative_prompt: str | None = None,
        width: int = 1024,
        height: int = 1024,
        model: str | None = None,
    ) -> ImageGenerationResult:
        chosen_model = model or self.default_model

        # Offline / Test fallback when API key is not configured
        if not self.api_key:
            logger.warning("Venice API key not set for image generation. Returning mock image.")
            return ImageGenerationResult(
                b64_image=MOCK_PNG_B64,
                mime_type="image/png",
                width=width,
                height=height,
                model=f"mock-{chosen_model}",
            )

        url = f"{self.base_url}/image/generate"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        payload = {
            "model": chosen_model,
            "prompt": prompt,
            "negative_prompt": negative_prompt or "ugly, blurry, distorted, low quality, artifacts",
            "width": width,
            "height": height,
            "steps": 30,
            "hide_watermark": True,
            "return_binary": False,
        }

        client = self._custom_client or httpx.AsyncClient(timeout=90.0)
        try:
            response = await client.post(url, json=payload, headers=headers)
            if response.status_code != 200:
                raise JuhiAPIException(
                    status_code=502,
                    error_code="VENICE_IMAGE_ERROR",
                    message=f"Venice image generation failed ({response.status_code}): {response.text}",
                )

            data = response.json()
            images = data.get("images", [])
            if not images:
                raise JuhiAPIException(
                    status_code=502,
                    error_code="VENICE_IMAGE_EMPTY",
                    message="Venice returned empty image list",
                )

            b64_img = images[0]
            # Strip data:image/...;base64, prefix if returned
            if b64_img.startswith("data:"):
                b64_img = b64_img.split(",", 1)[-1]

            return ImageGenerationResult(
                b64_image=b64_img,
                mime_type="image/png",
                width=width,
                height=height,
                model=chosen_model,
            )
        finally:
            if not self._custom_client:
                await client.aclose()
