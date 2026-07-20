"""Runtime configuration, all overridable via environment variables."""

from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Models
    fast_model_id: str = "MayZhou/e5-small-lora-ai-generated-detector"
    deep_model_id: str = "desklib/ai-text-detector-v1.01"
    perplexity_model_id: str = "distilgpt2"
    embedder_model_id: str = "intfloat/e5-small-v2"
    enable_deep_tier: bool = True
    enable_perplexity: bool = True
    enable_retrieval: bool = True
    enable_binoculars: bool = True
    enable_raidar: bool = True
    binoculars_observer_id: str = "Qwen/Qwen2.5-0.5B"
    binoculars_performer_id: str = "Qwen/Qwen2.5-0.5B-Instruct"
    raidar_rewrite_model_id: str = "HuggingFaceTB/SmolLM2-360M-Instruct"
    style_index_path: str = ""  # empty = packaged default
    device: str = "cpu"

    # Storage
    database_url: str = "sqlite:///./veritas.db"

    # API behavior
    cors_origins: str = "*"
    anonymous_daily_limit: int = 50
    api_key_daily_limit: int = 2000
    rate_limit: str = "20/minute"
    admin_token: str = ""  # required to mint API keys; empty disables the endpoint
    max_batch_size: int = 20
    max_upload_bytes: int = 5 * 1024 * 1024

    model_config = {"env_prefix": "VERITAS_", "env_file": ".env", "extra": "ignore"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
