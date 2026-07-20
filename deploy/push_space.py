#!/usr/bin/env python3
"""Upload VeritasAI API to a Hugging Face Space.

Requires HF_TOKEN with write access:
  export HF_TOKEN=hf_...
  python deploy/push_space.py

Creates (or updates) dipu2805/veritas-ai-api.
- PRO accounts: Docker Space (cpu-basic)
- Free accounts: Gradio Space (cpu-basic) — same FastAPI, no PRO required
"""

from __future__ import annotations

import os
import shutil
import tempfile
from pathlib import Path

from huggingface_hub import HfApi, create_repo

REPO_ID = os.environ.get("HF_SPACE_REPO", "dipu2805/veritas-ai-api")
ROOT = Path(__file__).resolve().parents[1]
FORCE_SDK = os.environ.get("HF_SPACE_SDK", "").lower()  # "docker" | "gradio"


def _use_docker(api: HfApi, token: str) -> bool:
    if FORCE_SDK == "docker":
        return True
    if FORCE_SDK == "gradio":
        return False
    try:
        info = api.whoami(token=token)
        return bool(info.get("isPro"))
    except Exception:
        return False


def _stage_docker(staging: Path) -> None:
    shutil.copy(ROOT / "deploy/hf-space/README.md", staging / "README.md")
    shutil.copy(ROOT / "deploy/hf-space/Dockerfile", staging / "Dockerfile")
    shutil.copytree(ROOT / "apps/api/app", staging / "app")
    shutil.copytree(ROOT / "packages/detection", staging / "packages/detection")
    shutil.copy(ROOT / "apps/api/requirements.txt", staging / "requirements.txt")
    dockerfile = (staging / "Dockerfile").read_text()
    dockerfile = dockerfile.replace("COPY apps/api/requirements.txt", "COPY requirements.txt")
    dockerfile = dockerfile.replace("COPY packages/detection", "COPY packages/detection")
    dockerfile = dockerfile.replace("COPY apps/api/app", "COPY app")
    (staging / "Dockerfile").write_text(dockerfile)


def _stage_gradio(staging: Path) -> None:
    shutil.copy(ROOT / "deploy/hf-space/README-gradio.md", staging / "README.md")
    shutil.copy(ROOT / "deploy/hf-space/gradio_app.py", staging / "app.py")
    shutil.copytree(ROOT / "apps/api/app", staging / "app")
    shutil.copytree(ROOT / "packages/detection", staging / "packages/detection")
    reqs = (ROOT / "apps/api/requirements.txt").read_text().strip()
    reqs += "\ngradio>=5.50.0\n"
    (staging / "requirements.txt").write_text(reqs + "\n")


def main() -> None:
    token = os.environ.get("HF_TOKEN")
    if not token:
        raise SystemExit("Set HF_TOKEN (write token from https://huggingface.co/settings/tokens)")

    api = HfApi(token=token)
    use_docker = _use_docker(api, token)
    sdk = "docker" if use_docker else "gradio"

    try:
        create_repo(REPO_ID, repo_type="space", space_sdk=sdk, exist_ok=True, token=token)
    except Exception as exc:
        err = str(exc)
        if "402" in err or "PRO" in err.upper():
            raise SystemExit(
                "Hugging Face Spaces (Docker and Gradio) require a PRO subscription ($9/mo).\n"
                "Subscribe at https://huggingface.co/pro then re-run:\n"
                "  export HF_TOKEN=hf_... && python deploy/push_space.py\n\n"
                "Free alternative: deploy on Render (no PRO needed):\n"
                "  1. Push this repo to GitHub\n"
                "  2. https://dashboard.render.com → New → Blueprint → select repo\n"
                "  3. Uses render.yaml (API at veritas-ai-api.onrender.com)\n"
            ) from exc
        if use_docker and "sdk" in err.lower():
            print("Docker SDK unavailable — falling back to Gradio.")
            use_docker = False
            sdk = "gradio"
            create_repo(REPO_ID, repo_type="space", space_sdk=sdk, exist_ok=True, token=token)
        else:
            raise

    try:
        api.set_space_settings(REPO_ID, hardware="cpu-basic", secrets={}, variables={}, token=token)
    except Exception:
        pass

    with tempfile.TemporaryDirectory() as tmp:
        staging = Path(tmp)
        if use_docker:
            _stage_docker(staging)
        else:
            _stage_gradio(staging)

        api.upload_folder(
            folder_path=str(staging),
            repo_id=REPO_ID,
            repo_type="space",
            commit_message=f"Deploy VeritasAI API ({sdk})",
            token=token,
        )

    print(f"Deployed ({sdk}): https://huggingface.co/spaces/{REPO_ID}")
    print(f"API URL (after build): https://{REPO_ID.replace('/', '-')}.hf.space")
    if not use_docker:
        print("Note: Gradio SDK used (free tier). Upgrade to HF PRO + HF_SPACE_SDK=docker for Docker.")


if __name__ == "__main__":
    main()
