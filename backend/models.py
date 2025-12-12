# Image generation provider models
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum


class JobStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class GenerationRequest(BaseModel):
    numImages: int

    class Config:
        json_schema_extra = {
            "example": {
                "numImages": 3
            }
        }


class GenerationResponse(BaseModel):
    jobId: str
    status: JobStatus


class Job(BaseModel):
    id: str
    status: JobStatus
    numImages: int
    animal: Optional[str] = None
    imageUrls: Optional[List[str]] = None
    error: Optional[str] = None
    createdAt: str
    updatedAt: str


class JobDetailResponse(BaseModel):
    jobId: str
    status: JobStatus
    numImages: int
    animal: Optional[str] = None
    imageUrls: Optional[List[str]] = None
    error: Optional[str] = None
    createdAt: str
    updatedAt: str


class ClassifyRequest(BaseModel):
    imgUrl: str

    class Config:
        json_schema_extra = {
            "example": {
                "imgUrl": "https://example.com/image.jpg"
            }
        }


class ClassifyResponse(BaseModel):
    animals: List[str]
    error: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "animals": ["cat", "dog"],
                "error": None
            }
        }
