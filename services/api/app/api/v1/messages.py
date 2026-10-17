import json
import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.authorization import get_current_active_user, verify_conversation_access
from app.domain.models.conversation import Conversation, Message
from app.domain.models.memory import MemoryItem
from app.domain.models.user import User
from app.domain.orchestration.turn_orchestrator import TurnOrchestrator
from app.infrastructure.database.session import get_db
from app.schemas.conversation import (
    ChatTurnResponse,
    MessageResponse,
    SendMessageRequest,
)

router = APIRouter(prefix="/conversations/{conversation_id}/messages", tags=["Messages & Chat"])


@router.get("", response_model=list[MessageResponse])
async def list_messages(
    conversation: Conversation = Depends(verify_conversation_access),
    limit: int = Query(default=50, ge=1, le=100),
    before_sequence_no: int | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Message).where(
        Message.conversation_id == conversation.id,
        Message.status != "deleted",
    )
    if before_sequence_no is not None:
        stmt = stmt.where(Message.sequence_no < before_sequence_no)

    stmt = stmt.order_by(Message.sequence_no.asc()).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.post("", response_model=ChatTurnResponse)
async def send_message(
    data: SendMessageRequest,
    conversation: Conversation = Depends(verify_conversation_access),
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    # 1. Check idempotency for user message
    existing_user_msg_stmt = select(Message).where(
        Message.conversation_id == conversation.id,
        Message.idempotency_key == data.idempotency_key,
    )
    existing_user_res = await db.execute(existing_user_msg_stmt)
    existing_user_msg = existing_user_res.scalar_one_or_none()

    if existing_user_msg:
        # User message was already created. Look for subsequent assistant reply.
        assistant_stmt = select(Message).where(
            Message.conversation_id == conversation.id,
            Message.reply_to_message_id == existing_user_msg.id,
        )
        assistant_res = await db.execute(assistant_stmt)
        existing_assistant = assistant_res.scalar_one_or_none()
        if existing_assistant:
            return ChatTurnResponse(
                user_message=MessageResponse.model_validate(existing_user_msg),
                assistant_message=MessageResponse.model_validate(existing_assistant),
            )

    # 2. Lock conversation and allocate sequence numbers safely
    # If SQLite, FOR UPDATE is not supported, so standard transactional locking applies
    conv_stmt = (
        select(Conversation).where(Conversation.id == conversation.id).with_for_update()
        if not db.bind.url.drivername.startswith("sqlite")
        else select(Conversation).where(Conversation.id == conversation.id)
    )
    conv_res = await db.execute(conv_stmt)
    locked_conv = conv_res.scalar_one()

    user_seq = locked_conv.next_sequence_no
    locked_conv.next_sequence_no += 1

    # 3. Save User Message
    user_content = {
        "schema_version": 1,
        "parts": [{"type": "text", "text": data.text}],
    }
    user_msg = Message(
        id=uuid.uuid4(),
        conversation_id=locked_conv.id,
        sequence_no=user_seq,
        role="user",
        status="complete",
        content_json=user_content,
        client_message_id=data.client_message_id,
        idempotency_key=data.idempotency_key,
        accepted_at=datetime.utcnow(),
        completed_at=datetime.utcnow(),
    )
    db.add(user_msg)
    await db.flush()

    # 4. Generate AI Assistant Turn
    orchestrator = TurnOrchestrator()
    assistant_text = await orchestrator.generate_turn(user, locked_conv, db)

    assistant_seq = locked_conv.next_sequence_no
    locked_conv.next_sequence_no += 1
    locked_conv.last_message_at = datetime.utcnow()

    assistant_content = {
        "schema_version": 1,
        "parts": [{"type": "text", "text": assistant_text}],
    }
    assistant_idempotency = f"assist_{user_msg.id}"
    assistant_msg = Message(
        id=uuid.uuid4(),
        conversation_id=locked_conv.id,
        sequence_no=assistant_seq,
        role="assistant",
        status="complete",
        content_json=assistant_content,
        idempotency_key=assistant_idempotency,
        reply_to_message_id=user_msg.id,
        accepted_at=datetime.utcnow(),
        completed_at=datetime.utcnow(),
    )
    db.add(assistant_msg)

    # 5. Extract candidate memory if user explicitly stated a preference/name
    # Lightweight extraction for immediate user memory continuity
    if any(
        p in data.text.lower()
        for p in [
            "i like ",
            "my favorite ",
            "i love ",
            "my name is ",
            "mera naam ",
            "enakku pidikum ",
        ]
    ):
        memory_item = MemoryItem(
            id=uuid.uuid4(),
            user_id=user.id,
            conversation_id=locked_conv.id,
            source_message_id=user_msg.id,
            memory_type="preference"
            if "favorite" in data.text.lower() or "like" in data.text.lower()
            else "profile_fact",
            content_text=data.text.strip(),
            importance=4,
            status="active",
        )
        db.add(memory_item)

    await db.commit()
    await db.refresh(user_msg)
    await db.refresh(assistant_msg)

    return ChatTurnResponse(
        user_message=MessageResponse.model_validate(user_msg),
        assistant_message=MessageResponse.model_validate(assistant_msg),
    )


@router.post("/stream")
async def stream_message(
    data: SendMessageRequest,
    conversation: Conversation = Depends(verify_conversation_access),
    user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    # Lock conversation and insert user message
    conv_stmt = (
        select(Conversation).where(Conversation.id == conversation.id).with_for_update()
        if not db.bind.url.drivername.startswith("sqlite")
        else select(Conversation).where(Conversation.id == conversation.id)
    )
    conv_res = await db.execute(conv_stmt)
    locked_conv = conv_res.scalar_one()

    user_seq = locked_conv.next_sequence_no
    locked_conv.next_sequence_no += 1

    user_content = {
        "schema_version": 1,
        "parts": [{"type": "text", "text": data.text}],
    }
    user_msg = Message(
        id=uuid.uuid4(),
        conversation_id=locked_conv.id,
        sequence_no=user_seq,
        role="user",
        status="complete",
        content_json=user_content,
        client_message_id=data.client_message_id,
        idempotency_key=data.idempotency_key,
        accepted_at=datetime.utcnow(),
        completed_at=datetime.utcnow(),
    )
    db.add(user_msg)
    await db.commit()

    orchestrator = TurnOrchestrator()

    async def event_generator():
        collected_chunks = []
        async for chunk in orchestrator.stream_turn(user, locked_conv, db):
            collected_chunks.append(chunk)
            payload = json.dumps({"delta": chunk, "is_finished": False})
            yield f"data: {payload}\n\n"

        # On completion, save assistant message
        full_reply = "".join(collected_chunks)
        assistant_seq = locked_conv.next_sequence_no
        locked_conv.next_sequence_no += 1
        locked_conv.last_message_at = datetime.utcnow()

        assistant_msg = Message(
            id=uuid.uuid4(),
            conversation_id=locked_conv.id,
            sequence_no=assistant_seq,
            role="assistant",
            status="complete",
            content_json={"schema_version": 1, "parts": [{"type": "text", "text": full_reply}]},
            idempotency_key=f"assist_{user_msg.id}",
            reply_to_message_id=user_msg.id,
        )
        db.add(assistant_msg)
        await db.commit()

        end_payload = json.dumps(
            {
                "delta": "",
                "is_finished": True,
                "message_id": str(assistant_msg.id),
                "sequence_no": assistant_seq,
            }
        )
        yield f"data: {end_payload}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
