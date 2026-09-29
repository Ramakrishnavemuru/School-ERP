import os
import shutil
from pathlib import Path
from fastapi import HTTPException, UploadFile, status
from backend.app.config import settings
from backend.app.utils.validators import validate_file_upload, generate_safe_filename

class FileService:
    @staticmethod
    def ensure_upload_dirs():
        base = Path(settings.UPLOAD_DIR)
        for sub in ["profiles", "assignments", "study-materials", "documents", "reports"]:
            (base / sub).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def save_upload_file(file: UploadFile, subfolder: str = "documents") -> str:
        FileService.ensure_upload_dirs()
        validate_file_upload(file)

        safe_filename = generate_safe_filename(file.filename)
        destination_folder = Path(settings.UPLOAD_DIR) / subfolder
        destination_folder.mkdir(parents=True, exist_ok=True)
        file_path = destination_folder / safe_filename

        # Write file with size check
        max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
        size = 0
        try:
            with open(file_path, "wb") as buffer:
                while chunk := file.file.read(1024 * 1024):  # 1MB chunks
                    size += len(chunk)
                    if size > max_bytes:
                        # Clean up and raise
                        file_path.unlink(missing_ok=True)
                        raise HTTPException(
                            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                            detail=f"File exceeds maximum allowed size of {settings.MAX_UPLOAD_SIZE_MB}MB"
                        )
                    buffer.write(chunk)
        finally:
            file.file.close()

        # Return relative or normalized file path for storage
        return str(Path(subfolder) / safe_filename)

    @staticmethod
    def get_absolute_path(stored_path: str) -> Path:
        base = Path(settings.UPLOAD_DIR).resolve()
        target = (base / stored_path).resolve()
        if not str(target).startswith(str(base)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file path"
            )
        if not target.exists() or not target.is_file():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File not found"
            )
        return target

    @staticmethod
    def delete_file(stored_path: str):
        try:
            target = FileService.get_absolute_path(stored_path)
            if target.exists():
                target.unlink()
        except HTTPException:
            pass

file_service = FileService()
