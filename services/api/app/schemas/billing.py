import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class CreditBalanceResponse(BaseModel):
    user_id: uuid.UUID
    available_balance: int
    reserved_balance: int
    credit_unit: str = "credits"
    tier: str = "free"
    rate_cards: dict[str, int] = {
        "image_generation": 10,
        "voice_minute": 5,
    }


class CreditLedgerEntryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    credit_account_id: uuid.UUID
    entry_type: str
    available_delta: int
    reserved_delta: int
    reason: str
    reference_id: uuid.UUID | None = None
    metadata_json: dict[str, Any] = {}
    created_at: datetime
