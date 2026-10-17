import uuid

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.authorization import get_current_active_user, verify_conversation_access
from app.core.errors import NotFoundException
from app.domain.models.conversation import Conversation, Message
from app.domain.models.media import MediaAsset
from app.domain.models.user import User
from app.infrastructure.database.session import get_db
from app.infrastructure.providers.audio.tts_provider import VeniceTTSProvider
from app.schemas.audio import AudioSpeechResponse, SpeakMessageRequest, SpeakTextRequest

router = APIRouter(prefix="/audio", tags=["Audio & Speech"])


def get_tts_provider() -> VeniceTTSProvider:
    return VeniceTTSProvider()


@router.post("/speak", response_model=AudioSpeechResponse)
async def synthesize_text_speech(
    data: SpeakTextRequest,
    user: User = Depends(get_current_active_user),
    tts_provider: VeniceTTSProvider = Depends(get_tts_provider),
):
    """
    Direct text-to-speech synthesis endpoint.
    """
    result = await tts_provider.synthesize_speech(
        text=data.text,
        voice_id=data.voice_id,
        speed=data.speed,
    )
    return AudioSpeechResponse(
        b64_audio=result.b64_audio,
        mime_type=result.mime_type,
        duration_seconds=result.duration_seconds,
        voice_id=result.voice_id,
    )


@router.post(
    "/conversations/{conversation_id}/messages/{message_id}/speak",
    response_model=AudioSpeechResponse,
)
async def synthesize_message_speech(
    message_id: uuid.UUID,
    request: SpeakMessageRequest = SpeakMessageRequest(),
    conversation: Conversation = Depends(verify_conversation_access),
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
    tts_provider: VeniceTTSProvider = Depends(get_tts_provider),
):
    """
    Synthesizes speech for an existing conversation message and attaches an audio media asset.
    """
    stmt = select(Message).where(
        Message.id == message_id,
        Message.conversation_id == conversation.id,
    )
    msg_res = await db.execute(stmt)
    message = msg_res.scalar_one_or_none()
    if not message:
        raise NotFoundException("Message not found in conversation")

    # Extract text from message envelope
    text = ""
    if isinstance(message.content_json, dict) and "parts" in message.content_json:
        for p in message.content_json["parts"]:
            if p.get("type") == "text":
                text += p.get("text", "")
    elif isinstance(message.content_json, dict) and "text" in message.content_json:
        text = message.content_json["text"]

    if not text.strip():
        raise NotFoundException("Message does not contain speakable text")

    # Synthesize speech
    result = await tts_provider.synthesize_speech(
        text=text,
        voice_id=request.voice_id or "juhi-warm",
        speed=request.speed,
    )

    asset_id = uuid.uuid4()
    asset = MediaAsset(
        id=asset_id,
        user_id=user.id,
        conversation_id=conversation.id,
        message_id=message.id,
        asset_kind="audio",
        origin="ai_generated",
        storage_bucket="juhi-private-media",
        object_key=f"audio/{user.id}/{asset_id}.mp3",
        mime_type=result.mime_type,
        processing_status="ready",
        moderation_status="allowed",
        visibility="private",
        metadata_json={
            "duration_seconds": result.duration_seconds,
            "voice_id": result.voice_id,
            "model": result.model,
            "text_snippet": text[:100],
        },
    )
    db.add(asset)
    await db.commit()
    await db.refresh(asset)

    return AudioSpeechResponse(
        asset_id=asset.id,
        b64_audio=result.b64_audio,
        mime_type=result.mime_type,
        duration_seconds=result.duration_seconds,
        voice_id=result.voice_id,
    )
