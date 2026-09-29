import os
import re
import uuid
from pathlib import Path
from fastapi import HTTPException, UploadFile, status
from backend.app.config import settings

def get_allowed_extensions() -> set:
    return {ext.strip().lower() for ext in settings.ALLOWED_EXTENSIONS.split(",")}

def sanitize_filename(filename: str) -> str:
    # Remove directory separators and unsafe characters
    base = os.path.basename(filename)
    clean = re.sub(r'[^a-zA-Z0-9_.-]', '_', base)
    return clean

def generate_safe_filename(original_filename: str) -> str:
    clean = sanitize_filename(original_filename)
    extension = Path(clean).suffix.lower()
    prefix = uuid.uuid4().hex[:12]
    stem = Path(clean).stem[:30]
    return f"{prefix}_{stem}{extension}"

def validate_file_upload(file: UploadFile) -> None:
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename cannot be empty"
        )
    
    ext = Path(file.filename).suffix.lstrip(".").lower()
    allowed = get_allowed_extensions()
    if ext not in allowed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File extension '.{ext}' is not permitted. Allowed extensions: {', '.join(sorted(allowed))}"
        )
