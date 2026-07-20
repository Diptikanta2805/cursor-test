FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    HF_HOME=/data/hf-cache \
    PORT=8000

WORKDIR /srv

COPY apps/api/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY packages/detection ./packages/detection
RUN pip install --no-cache-dir ./packages/detection

COPY apps/api/app ./app

RUN mkdir -p /data/hf-cache
EXPOSE 8000
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
