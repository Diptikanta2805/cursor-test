"""API key management (admin-token gated)."""

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.config import get_settings
from app.db import get_db
from app.models import ApiKey
from app.schemas import CreateKeyRequest, CreateKeyResponse
from app.security import hash_key, mint_key

router = APIRouter(prefix="/v1/keys", tags=["keys"])


def _require_admin(authorization: str | None = Header(default=None)) -> None:
    settings = get_settings()
    if not settings.admin_token:
        raise HTTPException(
            status_code=403,
            detail="Key management disabled (set VERITAS_ADMIN_TOKEN to enable)",
        )
    if authorization != f"Bearer {settings.admin_token}":
        raise HTTPException(status_code=401, detail="Invalid admin token")


@router.post("", response_model=CreateKeyResponse)
def create_key(
    body: CreateKeyRequest,
    db: Session = Depends(get_db),
    _: None = Depends(_require_admin),
) -> CreateKeyResponse:
    settings = get_settings()
    raw = mint_key()
    key = ApiKey(
        key_hash=hash_key(raw),
        name=body.name,
        daily_limit=settings.api_key_daily_limit,
    )
    db.add(key)
    db.commit()
    db.refresh(key)
    return CreateKeyResponse(
        api_key=raw, key_id=key.id, name=key.name, daily_limit=key.daily_limit
    )


@router.delete("/{key_id}")
def revoke_key(
    key_id: str,
    db: Session = Depends(get_db),
    _: None = Depends(_require_admin),
) -> dict:
    key = db.get(ApiKey, key_id)
    if key is None:
        raise HTTPException(status_code=404, detail="Key not found")
    key.revoked = 1
    db.commit()
    return {"revoked": key_id}
