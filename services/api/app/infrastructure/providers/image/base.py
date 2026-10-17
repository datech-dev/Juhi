from abc import ABC, abstractmethod

from pydantic import BaseModel


class ImageGenerationResult(BaseModel):
    b64_image: str
    mime_type: str = "image/png"
    width: int = 1024
    height: int = 1024
    model: str
    seed: int | None = None


class BaseImageProvider(ABC):
    @abstractmethod
    async def generate_image(
        self,
        prompt: str,
        negative_prompt: str | None = None,
        width: int = 1024,
        height: int = 1024,
        model: str | None = None,
    ) -> ImageGenerationResult:
        pass
