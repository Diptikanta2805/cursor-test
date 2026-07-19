# VeritasAI API — runs on any free CPU host (HF Spaces Docker, Render, Fly).
# HF Spaces expects the app to listen on port 7860.
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    HF_HOME=/data/hf-cache \
    PORT=7860

WORKDIR /srv

COPY apps/api/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY packages/detection ./packages/detection
RUN pip install --no-cache-dir ./packages/detection

COPY apps/api/app ./app

# Non-root user (required by HF Spaces)
RUN useradd -m -u 1000 appuser && mkdir -p /data/hf-cache && chown -R appuser /data /srv
USER appuser

EXPOSE 7860
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
