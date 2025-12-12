"""
Storage service for converting base64 images to S3 URLs
"""
import base64
import uuid
from typing import Optional
from minio import Minio
from minio.error import S3Error
import logging

from config import settings

logger = logging.getLogger(__name__)


class StorageService:
    """Service for storing images in MinIO S3-compatible storage"""
    
    def __init__(self):
        """Initialize MinIO client"""
        if settings.STORAGE_BACKEND == "minio":
            self.client = Minio(
                settings.MINIO_ENDPOINT,
                access_key=settings.MINIO_ACCESS_KEY,
                secret_key=settings.MINIO_SECRET_KEY,
                secure=settings.MINIO_SECURE
            )
            self._ensure_bucket_exists()
        else:
            self.client = None
    
    def _ensure_bucket_exists(self):
        """Ensure the bucket exists, create if not"""
        try:
            if not self.client.bucket_exists(settings.MINIO_BUCKET):
                self.client.make_bucket(settings.MINIO_BUCKET)
                # Set bucket policy to public read
                policy = {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": {"AWS": "*"},
                            "Action": ["s3:GetObject"],
                            "Resource": [f"arn:aws:s3:::{settings.MINIO_BUCKET}/*"]
                        }
                    ]
                }
                import json
                self.client.set_bucket_policy(
                    settings.MINIO_BUCKET,
                    json.dumps(policy)
                )
                logger.info(f"Created bucket: {settings.MINIO_BUCKET}")
        except S3Error as e:
            logger.error(f"Error ensuring bucket exists: {e}")
    
    def upload_base64_image(self, base64_data: str, prefix: str = "images") -> Optional[str]:
        """
        Upload a base64-encoded image to MinIO and return the public URL
        
        Args:
            base64_data: Base64-encoded image data (with or without data URI prefix)
            prefix: Folder prefix for organizing images
            
        Returns:
            Public HTTP URL to access the image, or None if upload fails
        """
        if not self.client or settings.STORAGE_BACKEND != "minio":
            return base64_data  # Return original if storage disabled
        
        try:
            # Extract base64 data and content type
            if base64_data.startswith("data:"):
                # Format: data:image/png;base64,<data>
                header, encoded = base64_data.split(",", 1)
                content_type = header.split(":")[1].split(";")[0]
            else:
                encoded = base64_data
                content_type = "image/png"  # Default
            
            # Decode base64 to bytes
            image_bytes = base64.b64decode(encoded)
            
            # Generate unique filename
            extension = content_type.split("/")[1]
            filename = f"{prefix}/{uuid.uuid4()}.{extension}"
            
            # Upload to MinIO
            from io import BytesIO
            self.client.put_object(
                settings.MINIO_BUCKET,
                filename,
                BytesIO(image_bytes),
                length=len(image_bytes),
                content_type=content_type
            )
            
            # Generate public URL
            url = f"{settings.MINIO_PUBLIC_URL}/{settings.MINIO_BUCKET}/{filename}"
            logger.info(f"Uploaded image to: {url}")
            return url
            
        except Exception as e:
            logger.error(f"Failed to upload image to MinIO: {e}")
            return base64_data  # Fallback to base64
    
    def upload_multiple_base64_images(self, base64_images: list[str], prefix: str = "images") -> list[str]:
        """
        Upload multiple base64-encoded images
        
        Args:
            base64_images: List of base64-encoded images
            prefix: Folder prefix for organizing images
            
        Returns:
            List of public HTTP URLs
        """
        return [self.upload_base64_image(img, prefix) for img in base64_images]


# Global storage service instance
storage_service = StorageService()


def convert_to_public_url(base64_or_url: str) -> str:
    """
    Convert base64 data URL to public HTTP URL, or return as-is if already HTTP
    
    Args:
        base64_or_url: Either a base64 data URL or HTTP URL
        
    Returns:
        Public HTTP URL
    """
    if base64_or_url.startswith("http"):
        return base64_or_url
    
    if base64_or_url.startswith("data:"):
        return storage_service.upload_base64_image(base64_or_url)
    
    return base64_or_url
