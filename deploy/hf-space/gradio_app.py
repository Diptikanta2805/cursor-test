"""Gradio Space entrypoint — mounts VeritasAI FastAPI at the root ASGI app."""

import gradio as gr

from app.main import app as fastapi_app

with gr.Blocks(title="VeritasAI API", fill_height=True) as demo:
    gr.Markdown(
        """
# VeritasAI API

Open, calibrated AI-generated text detection.

| Resource | URL |
|----------|-----|
| OpenAPI docs | [/docs](/docs) |
| Health | [/v1/health](/v1/health) |
| Scan | `POST /v1/scan` |

```bash
curl -X POST /v1/scan \\
  -H "Content-Type: application/json" \\
  -d '{"text": "...50+ words...", "mode": "deep"}'
```
"""
    )

app = gr.mount_gradio_app(fastapi_app, demo, path="/")
