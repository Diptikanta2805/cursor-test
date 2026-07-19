"""SQLAlchemy ORM models."""

import uuid
from datetime import datetime, timezone

from sqlalchemy import JSON, DateTime, Float, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _new_id() -> str:
    return uuid.uuid4().hex


class Base(DeclarativeBase):
    pass


class Scan(Base):
    __tablename__ = "scans"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=_new_id)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)
    verdict: Mapped[str] = mapped_column(String(16))
    ai_probability: Mapped[float] = mapped_column(Float)
    confidence: Mapped[str] = mapped_column(String(8))
    operating_point: Mapped[str] = mapped_column(String(16))
    mode_used: Mapped[str] = mapped_column(String(8))
    word_count: Mapped[int] = mapped_column(Integer)
    duration_ms: Mapped[int] = mapped_column(Integer)
    text_preview: Mapped[str] = mapped_column(Text)  # first 280 chars for history lists
    payload: Mapped[dict] = mapped_column(JSON)  # full result incl. sentences/signals
    requester: Mapped[str] = mapped_column(String(64), index=True)  # key id or ip hash


class ApiKey(Base):
    __tablename__ = "api_keys"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=_new_id)
    key_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)
    daily_limit: Mapped[int] = mapped_column(Integer)
    revoked: Mapped[int] = mapped_column(Integer, default=0)


class DailyUsage(Base):
    __tablename__ = "daily_usage"

    id: Mapped[str] = mapped_column(String(80), primary_key=True)  # f"{requester}:{date}"
    requester: Mapped[str] = mapped_column(String(64), index=True)
    date: Mapped[str] = mapped_column(String(10))
    count: Mapped[int] = mapped_column(Integer, default=0)
