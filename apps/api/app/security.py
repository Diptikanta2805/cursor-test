"""API-key auth and daily quota accounting."""

from __future__ import annotations

import hashlib
import secrets
from datetime import datetime, timezone

from fastapi import Depends, Header, HTTPException, Request
from sqlalchemy.orm import Session

from app.config import get_settings
from app.db import get_db
from app.models import ApiKey, DailyUsage


def hash_key(raw_key: str) -> str:
    return hashlib.sha256(raw_key.encode()).hexdigest()


def mint_key() -> str:
    return "vk_" + secrets.token_urlsafe(32)


def _client_id(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for", "")
    ip = forwarded.split(",")[0].strip() if forwarded else (
        request.client.host if request.client else "unknown"
    )
    return "ip:" + hashlib.sha256(ip.encode()).hexdigest()[:24]


class Requester:
    def __init__(self, identifier: str, daily_limit: int) -> None:
        self.identifier = identifier
        self.daily_limit = daily_limit


def get_requester(
    request: Request,
    db: Session = Depends(get_db),
    x_api_key: str | None = Header(default=None),
) -> Requester:
    settings = get_settings()
    if x_api_key:
        key = (
            db.query(ApiKey)
            .filter(ApiKey.key_hash == hash_key(x_api_key), ApiKey.revoked == 0)
            .first()
        )
        if key is None:
            raise HTTPException(status_code=401, detail="Invalid API key")
        return Requester("key:" + key.id, key.daily_limit)
    return Requester(_client_id(request), settings.anonymous_daily_limit)


def charge_quota(db: Session, requester: Requester, amount: int = 1) -> int:
    """Increment today's usage; raise 429 when over the daily limit."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    row_id = f"{requester.identifier}:{today}"
    usage = db.get(DailyUsage, row_id)
    if usage is None:
        usage = DailyUsage(
            id=row_id, requester=requester.identifier, date=today, count=0
        )
        db.add(usage)
    if usage.count + amount > requester.daily_limit:
        raise HTTPException(
            status_code=429,
            detail=(
                f"Daily quota exceeded ({requester.daily_limit} scans/day). "
                "Use an API key for a higher limit."
            ),
        )
    usage.count += amount
    db.commit()
    return usage.count
