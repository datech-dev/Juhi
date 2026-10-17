import httpx
import pytest

from app.infrastructure.providers.image.venice_image_provider import (
    MOCK_PNG_B64,
    VeniceImageProvider,
)


@pytest.mark.asyncio
async def test_venice_image_provider_mock_fallback():
    provider = VeniceImageProvider(api_key="")
    result = await provider.generate_image(
        prompt="Juhi in a modern cafe in Bangalore",
        width=512,
        height=512,
    )
    assert result.b64_image == MOCK_PNG_B64
    assert result.mime_type == "image/png"
    assert result.width == 512
    assert result.height == 512
    assert "mock" in result.model


@pytest.mark.asyncio
async def test_venice_image_provider_success():
    def mock_transport(request: httpx.Request):
        assert str(request.url) == "https://api.venice.ai/api/v1/image/generate"
        assert request.headers["Authorization"] == "Bearer test-venice-key"
        content = request.read().decode("utf-8")
        assert "fluently-xl" in content
        assert "A sunny park" in content

        return httpx.Response(
            200,
            json={
                "images": [
                    MOCK_PNG_B64
                ]
            },
        )

    mock_client = httpx.AsyncClient(transport=httpx.MockTransport(mock_transport))
    provider = VeniceImageProvider(
        api_key="test-venice-key",
        http_client=mock_client,
    )

    result = await provider.generate_image(
        prompt="A sunny park",
        model="fluently-xl",
    )
    assert result.b64_image == MOCK_PNG_B64
    assert result.model == "fluently-xl"
