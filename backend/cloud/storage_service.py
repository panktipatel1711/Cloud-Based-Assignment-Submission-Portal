import os
import shutil
from pathlib import Path
from fastapi import UploadFile, HTTPException
from backend.config import settings

class StorageService:
    def __init__(self):
        self.storage_type = settings.STORAGE_TYPE
        if self.storage_type == "local":
            self.base_dir = Path(settings.LOCAL_STORAGE_DIR)
            self.base_dir.mkdir(parents=True, exist_ok=True)
        elif self.storage_type == "s3":
            import boto3
            self.s3_client = boto3.client(
                "s3",
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION
            )
            self.bucket_name = settings.S3_BUCKET_NAME

    def upload_file(self, file: UploadFile, relative_path: str) -> str:
        if self.storage_type == "local":
            destination = self.base_dir / relative_path
            destination.parent.mkdir(parents=True, exist_ok=True)
            with open(destination, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            return str(relative_path).replace("\\", "/")
        elif self.storage_type == "s3":
            try:
                self.s3_client.upload_fileobj(
                    file.file,
                    self.bucket_name,
                    relative_path,
                    ExtraArgs={"ContentType": file.content_type}
                )
                return relative_path
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Cloud storage failure: {str(e)}")

    def get_file_path(self, relative_path: str) -> Path:
        if self.storage_type == "local":
            path = self.base_dir / relative_path
            if not path.exists():
                raise HTTPException(status_code=404, detail="File not found in storage bucket.")
            return path
        else:
            raise NotImplementedError("Direct paths are not applicable for S3 objects.")

storage_service = StorageService()
