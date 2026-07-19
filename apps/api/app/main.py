"""VeritasAI API — AI-generated text detection service."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app import engine as engine_module
from app.config import get_settings
from app.db import engine
from app.models import Base
from app.routes import keys, scan
from app.schemas import HealthResponse

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(message)s")
logger = logging.getLogger("veritas")

settings = get_settings()
limiter = Limiter(key_func=get_remote_address, default_limits=[settings.rate_limit])


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    engine_module.load_pipeline()
    yield


app = FastAPI(
    title="VeritasAI API",
    description=(
        "Open, calibrated AI-generated text detection. "
        "Ensemble of RAID-benchmark-leading open models with transparent signals. "
        "Detection scores are probabilistic and must not be used as sole evidence "
        "of misconduct."
    ),
    version="0.1.0",
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=(
        ["*"]
        if settings.cors_origins == "*"
        else [o.strip() for o in settings.cors_origins.split(",")]
    ),
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(scan.router)
app.include_router(keys.router)


@app.get("/v1/health", response_model=HealthResponse, tags=["meta"])
def health(request: Request) -> HealthResponse:
    return HealthResponse(
        status="ok" if engine_module._pipeline is not None else "loading",
        fast_model=settings.fast_model_id,
        deep_model=settings.deep_model_id if settings.enable_deep_tier else None,
        perplexity_model=(
            settings.perplexity_model_id if settings.enable_perplexity else None
        ),
        version="0.1.0",
    )


@app.get("/", include_in_schema=False)
def root() -> dict:
    return {"service": "VeritasAI API", "docs": "/docs", "health": "/v1/health"}
