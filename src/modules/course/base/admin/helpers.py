import os

from fastapi import HTTPException, UploadFile

UPLOAD_DIR = "uploads/course_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

MB = 1024 * 1024

MAX_SIZES = {
    "image/jpeg": 5 * MB,
    "image/png": 5 * MB,
    "image/webp": 5 * MB,
    "application/pdf": 10 * MB,
    "video/mp4": 50 * MB,
}


def _matches_signature(content_type: str, data: bytes) -> bool:
    if content_type == "image/jpeg":
        return data.startswith(b"\xff\xd8\xff")
    if content_type == "image/png":
        return data.startswith(b"\x89PNG\r\n\x1a\n")
    if content_type == "image/webp":
        return data[:4] == b"RIFF" and data[8:12] == b"WEBP"
    if content_type == "application/pdf":
        return data.startswith(b"%PDF")
    if content_type == "video/mp4":
        return data[4:8] == b"ftyp"
    return False


async def validate_documents(document: UploadFile):
    content_type = document.content_type

    if content_type not in MAX_SIZES:
        raise HTTPException(
            status_code=400,
            detail="Only JPEG, PNG, WEBP, PDF, MP4 are allowed",
        )

    max_size = MAX_SIZES[content_type]

    data = await document.read(max_size + 1)

    if len(data) > max_size:
        raise HTTPException(
            status_code=400,
            detail=f"File must be less than {max_size // MB} MB",
        )

    if not _matches_signature(content_type, data):
        raise HTTPException(
            status_code=400,
            detail="File content does not match its declared type",
        )

    await document.seek(0)