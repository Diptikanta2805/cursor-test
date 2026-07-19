"""Scan endpoints: single, file upload, batch, retrieval, usage."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal

from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile
from fastapi.concurrency import run_in_threadpool
from sqlalchemy.orm import Session

from app.config import get_settings
from app.db import get_db
from app.engine import get_pipeline
from app.files import extract_text
from app.models import Scan
from app.schemas import (
    BatchScanRequest,
    BatchScanResponse,
    ScanRequest,
    ScanResponse,
    ScanSummary,
    UsageResponse,
)
from app.security import Requester, charge_quota, get_requester
from veritas_detection.pipeline import ScanResult

router = APIRouter(prefix="/v1", tags=["scan"])


def _persist(
    db: Session, result: ScanResult, text: str, requester: Requester
) -> Scan:
    payload = {
        "sentences": [s.__dict__ for s in result.sentences],
        "signals": result.signals,
        "warning": result.warning,
    }
    scan = Scan(
        verdict=result.verdict,
        ai_probability=result.ai_probability,
        confidence=result.confidence,
        operating_point=result.operating_point,
        mode_used=result.mode_used,
        word_count=result.word_count,
        duration_ms=result.duration_ms,
        text_preview=text[:280],
        payload=payload,
        requester=requester.identifier,
    )
    db.add(scan)
    db.commit()
    db.refresh(scan)
    return scan


def _to_response(scan: Scan) -> ScanResponse:
    settings = get_settings()
    return ScanResponse(
        scan_id=scan.id,
        created_at=scan.created_at,
        verdict=scan.verdict,
        ai_probability=scan.ai_probability,
        confidence=scan.confidence,
        operating_point=scan.operating_point,
        mode_used=scan.mode_used,
        word_count=scan.word_count,
        duration_ms=scan.duration_ms,
        warning=scan.payload.get("warning"),
        sentences=scan.payload.get("sentences", []),
        signals=scan.payload.get("signals", {}),
        model_version=settings.fast_model_id,
    )


def _run_scan(
    db: Session, requester: Requester, body: ScanRequest
) -> Scan:
    pipeline = get_pipeline()
    result = pipeline.scan(
        body.text, mode=body.mode, operating_point=body.operating_point
    )
    return _persist(db, result, body.text, requester)


@router.post("/scan", response_model=ScanResponse)
async def scan_text(
    request: Request,
    body: ScanRequest,
    db: Session = Depends(get_db),
    requester: Requester = Depends(get_requester),
) -> ScanResponse:
    charge_quota(db, requester)
    scan = await run_in_threadpool(_run_scan, db, requester, body)
    return _to_response(scan)


@router.post("/scan/file", response_model=ScanResponse)
async def scan_file(
    request: Request,
    file: UploadFile = File(...),
    mode: Literal["fast", "deep"] = Form("fast"),
    operating_point: Literal["strict", "balanced"] = Form("balanced"),
    db: Session = Depends(get_db),
    requester: Requester = Depends(get_requester),
) -> ScanResponse:
    settings = get_settings()
    charge_quota(db, requester)
    text = await extract_text(file, settings.max_upload_bytes)
    body = ScanRequest(text=text, mode=mode, operating_point=operating_point)
    scan = await run_in_threadpool(_run_scan, db, requester, body)
    return _to_response(scan)


@router.post("/scan/batch", response_model=BatchScanResponse)
async def scan_batch(
    request: Request,
    body: BatchScanRequest,
    db: Session = Depends(get_db),
    requester: Requester = Depends(get_requester),
) -> BatchScanResponse:
    settings = get_settings()
    if len(body.items) > settings.max_batch_size:
        raise HTTPException(
            status_code=422,
            detail=f"Batch too large (max {settings.max_batch_size} items)",
        )
    charge_quota(db, requester, amount=len(body.items))
    scans = [
        await run_in_threadpool(_run_scan, db, requester, item)
        for item in body.items
    ]
    return BatchScanResponse(results=[_to_response(s) for s in scans])


@router.get("/scan/{scan_id}", response_model=ScanResponse)
def get_scan(scan_id: str, db: Session = Depends(get_db)) -> ScanResponse:
    scan = db.get(Scan, scan_id)
    if scan is None:
        raise HTTPException(status_code=404, detail="Scan not found")
    return _to_response(scan)


@router.get("/history", response_model=list[ScanSummary])
def history(
    request: Request,
    db: Session = Depends(get_db),
    requester: Requester = Depends(get_requester),
    limit: int = 20,
) -> list[ScanSummary]:
    rows = (
        db.query(Scan)
        .filter(Scan.requester == requester.identifier)
        .order_by(Scan.created_at.desc())
        .limit(min(limit, 100))
        .all()
    )
    return [
        ScanSummary(
            scan_id=r.id,
            created_at=r.created_at,
            verdict=r.verdict,
            ai_probability=r.ai_probability,
            word_count=r.word_count,
            text_preview=r.text_preview,
        )
        for r in rows
    ]


@router.get("/usage", response_model=UsageResponse)
def usage(
    request: Request,
    db: Session = Depends(get_db),
    requester: Requester = Depends(get_requester),
) -> UsageResponse:
    from app.models import DailyUsage

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    row = db.get(DailyUsage, f"{requester.identifier}:{today}")
    return UsageResponse(
        requester=requester.identifier,
        date=today,
        used=row.count if row else 0,
        daily_limit=requester.daily_limit,
    )
