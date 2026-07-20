#!/usr/bin/env python3
"""Upload VeritasAI API to a Hugging Face Docker Space.

Requires HF_TOKEN with write access:
  export HF_TOKEN=hf_...
  python deploy/push_space.py

Creates (or updates) dipu2805/veritas-ai-api as a public Docker Space on cpu-basic.
"""

from __future__ import annotations

import os
import shutil
import tempfile
from pathlib import Path

from huggingface_hub import HfApi, create_repo

REPO_ID = os.environ.get("HF_SPACE_REPO", "dipu2805/veritas-ai-api")
ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    token = os.environ.get("HF_TOKEN")
    if not token:
        raise SystemExit("Set HF_TOKEN (write token from https://huggingface.co/settings/tokens)")

    api = HfApi(token=token)
    create_repo(REPO_ID, repo_type="space", space_sdk="docker", exist_ok=True, token=token)
    api.set_space_settings(REPO_ID, hardware="cpu-basic", secrets={}, variables={}, token=token)

    with tempfile.TemporaryDirectory() as tmp:
        staging = Path(tmp)
        shutil.copy(ROOT / "deploy/hf-space/README.md", staging / "README.md")
        shutil.copy(ROOT / "deploy/hf-space/Dockerfile", staging / "Dockerfile")
        shutil.copytree(ROOT / "apps/api/app", staging / "app")
        shutil.copytree(ROOT / "packages/detection", staging / "packages/detection")
        shutil.copy(ROOT / "apps/api/requirements.txt", staging / "requirements.txt")
        # Dockerfile expects apps/api layout — patch paths for flat staging
        dockerfile = (staging / "Dockerfile").read_text()
        dockerfile = dockerfile.replace("COPY apps/api/requirements.txt", "COPY requirements.txt")
        dockerfile = dockerfile.replace("COPY packages/detection", "COPY packages/detection")
        dockerfile = dockerfile.replace("COPY apps/api/app", "COPY app")
        (staging / "Dockerfile").write_text(dockerfile)

        api.upload_folder(
            folder_path=str(staging),
            repo_id=REPO_ID,
            repo_type="space",
            commit_message="Deploy VeritasAI API",
            token=token,
        )

    print(f"Deployed: https://huggingface.co/spaces/{REPO_ID}")
    print(f"API URL (after build): https://{REPO_ID.replace('/', '-')}.hf.space")


if __name__ == "__main__":
    main()
