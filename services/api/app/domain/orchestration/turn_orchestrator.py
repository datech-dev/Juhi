from collections.abc import AsyncGenerator

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.companion import CompanionProfile, PersonaVersion
from app.domain.models.conversation import Conversation, Message
from app.domain.models.memory import MemoryItem
from app.domain.models.user import User
from app.infrastructure.providers.llm.base import BaseLLMProvider, LLMMessage
from app.infrastructure.providers.llm.factory import get_llm_provider


class TurnOrchestrator:
    def __init__(self, provider: BaseLLMProvider | None = None):
        self.provider = provider or get_llm_provider()

    async def compile_context(
        self,
        user: User,
        conversation: Conversation,
        db: AsyncSession,
        recent_limit: int = 15,
    ) -> list[LLMMessage]:
        # 1. Fetch persona version
        persona_stmt = select(PersonaVersion).where(
            PersonaVersion.id == conversation.active_persona_version_id
        )
        persona_res = await db.execute(persona_stmt)
        persona = persona_res.scalar_one_or_none()

        companion_name = "Juhi"
        relationship_mode = "companion"
        if conversation.companion_profile_id:
            comp_stmt = select(CompanionProfile).where(
                CompanionProfile.id == conversation.companion_profile_id
            )
            comp_res = await db.execute(comp_stmt)
            companion = comp_res.scalar_one_or_none()
            if companion:
                companion_name = companion.display_name
                relationship_mode = companion.relationship_mode

        # 2. Fetch active memories for this user
        mem_stmt = (
            select(MemoryItem)
            .where(
                MemoryItem.user_id == user.id,
                MemoryItem.status == "active",
                MemoryItem.scope == "real_life",
            )
            .order_by(MemoryItem.importance.desc(), MemoryItem.created_at.desc())
            .limit(10)
        )
        mem_res = await db.execute(mem_stmt)
        memories = mem_res.scalars().all()

        memory_bullets = (
            "\n".join([f"- {m.content_text}" for m in memories])
            if memories
            else "None recorded yet."
        )

        persona_desc = (
            persona.description
            if persona and persona.description
            else "Warm, empathetic, and culturally fluent AI companion."
        )

        # 3. Assemble system prompt
        system_content = (
            f"You are {companion_name}, a world-class AI companion.\n"
            f"Persona identity: {persona_desc}\n"
            f"Relationship style: {relationship_mode}.\n"
            f"User display name: {user.display_name or 'Friend'}.\n"
            f"Preferred language: {user.preferred_language}.\n"
            "Interaction guidelines:\n"
            "- Be warm, empathetic, respectful, attentive, and authentic.\n"
            "- Speak naturally in the user's language or mixed-language style (English, Hindi, Tamil, Hinglish, Tanglish).\n"
            "- Never pretend to be a human, a therapist, or a doctor.\n"
            "- Do not use guilt, possessiveness, or emotional coercion.\n\n"
            "User's remembered context:\n"
            f"{memory_bullets}\n"
        )

        llm_messages: list[LLMMessage] = [LLMMessage(role="system", content=system_content)]

        # 4. Fetch recent messages
        msg_stmt = (
            select(Message)
            .where(
                Message.conversation_id == conversation.id,
                Message.status == "complete",
            )
            .order_by(Message.sequence_no.desc())
            .limit(recent_limit)
        )
        msg_res = await db.execute(msg_stmt)
        history = list(reversed(msg_res.scalars().all()))

        for m in history:
            role = "user" if m.role == "user" else "assistant"
            # Extract text from content_json
            text_part = ""
            if isinstance(m.content_json, dict) and "parts" in m.content_json:
                for part in m.content_json["parts"]:
                    if part.get("type") == "text":
                        text_part += part.get("text", "")
            elif isinstance(m.content_json, dict) and "text" in m.content_json:
                text_part = m.content_json["text"]

            if text_part:
                llm_messages.append(LLMMessage(role=role, content=text_part))

        return llm_messages

    async def generate_turn(
        self,
        user: User,
        conversation: Conversation,
        db: AsyncSession,
    ) -> str:
        messages = await self.compile_context(user, conversation, db)
        response = await self.provider.generate_response(messages)
        return response.content

    async def stream_turn(
        self,
        user: User,
        conversation: Conversation,
        db: AsyncSession,
    ) -> AsyncGenerator[str, None]:
        messages = await self.compile_context(user, conversation, db)
        async for chunk in self.provider.stream_response(messages):
            if chunk.delta:
                yield chunk.delta
