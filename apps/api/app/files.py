"""Extract plain text from uploaded PDF / DOCX / TXT / MD files."""

from __future__ import annotations

import io

from fastapi import HTTPException, UploadFile


async def extract_text(upload: UploadFile, max_bytes: int) -> str:
    raw = await upload.read()
    if len(raw) > max_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"File too large (max {max_bytes // (1024 * 1024)} MB)",
        )
    name = (upload.filename or "").lower()
    if name.endswith(".pdf"):
        return _from_pdf(raw)
    if name.endswith(".docx"):
        return _from_docx(raw)
    if name.endswith((".txt", ".md", ".text")):
        return raw.decode("utf-8", errors="replace")
    raise HTTPException(
        status_code=415,
        detail="Unsupported file type. Use PDF, DOCX, TXT, or MD.",
    )


def _from_pdf(raw: bytes) -> str:
    from pypdf import PdfReader

    try:
        reader = PdfReader(io.BytesIO(raw))
        pages = [page.extract_text() or "" for page in reader.pages]
    except Exception as exc:  # noqa: BLE001 - surface parse errors as 422
        raise HTTPException(status_code=422, detail=f"Could not parse PDF: {exc}")
    text = "\n\n".join(pages).strip()
    if not text:
        raise HTTPException(
            status_code=422,
            detail="No extractable text in PDF (scanned documents need OCR).",
        )
    return text


def _from_docx(raw: bytes) -> str:
    from docx import Document

    try:
        document = Document(io.BytesIO(raw))
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=422, detail=f"Could not parse DOCX: {exc}")
    text = "\n".join(p.text for p in document.paragraphs).strip()
    if not text:
        raise HTTPException(status_code=422, detail="No text found in DOCX file.")
    return text
