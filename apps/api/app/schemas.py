"""Pydantic request/response schemas for the public API."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class ScanRequest(BaseModel):
    text: str = Field(min_length=1, max_length=120_000)
    mode: Literal["fast", "deep"] = "fast"
    operating_point: Literal["strict", "balanced"] = "balanced"


class BatchScanRequest(BaseModel):
    items: list[ScanRequest] = Field(min_length=1)


class SentenceOut(BaseModel):
    text: str
    start: int
    end: int
    score: float


class ScanResponse(BaseModel):
    scan_id: str
    created_at: datetime
    verdict: str
    ai_probability: float
    confidence: str
    operating_point: str
    mode_used: str
    word_count: int
    duration_ms: int
    warning: str | None = None
    sentences: list[SentenceOut]
    signals: dict
    model_version: str


class ScanSummary(BaseModel):
    scan_id: str
    created_at: datetime
    verdict: str
    ai_probability: float
    word_count: int
    text_preview: str


class BatchScanResponse(BaseModel):
    results: list[ScanResponse]


class UsageResponse(BaseModel):
    requester: str
    date: str
    used: int
    daily_limit: int


class CreateKeyRequest(BaseModel):
    name: str = Field(min_length=1, max_length=120)


class CreateKeyResponse(BaseModel):
    api_key: str  # returned once, only the hash is stored
    key_id: str
    name: str
    daily_limit: int


class HealthResponse(BaseModel):
    status: str
    fast_model: str
    deep_model: str | None
    perplexity_model: str | None
    version: str
