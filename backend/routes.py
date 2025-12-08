# API Routes for image generation endpoints
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from models import GenerationRequest, GenerationResponse, JobDetailResponse
from services import GenerationService
from core.database import get_db

router = APIRouter(
    prefix="/generations",
    tags=["generations"]
)


@router.post("", response_model=GenerationResponse, status_code=202)
async def create_generation(
    request: GenerationRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new image generation job
    
    This endpoint creates a job and returns immediately with a jobId.
    The actual image generation happens asynchronously in the background.
    
    Args:
        request: Request body containing numImages
        db: Database session (injected)
        
    Returns:
        Job ID and initial status (pending)
    """
    if request.numImages < 1 or request.numImages > 10:
        raise HTTPException(
            status_code=400,
            detail="numImages must be between 1 and 10"
        )
    
    service = GenerationService(db)
    return await service.create_job(request.numImages)


@router.get("/{job_id}", response_model=JobDetailResponse)
async def get_generation(
    job_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get the status and results of a generation job
    
    Args:
        job_id: The ID of the job to retrieve
        db: Database session (injected)
        
    Returns:
        Complete job details including status, images (if completed), or error
    """
    service = GenerationService(db)
    job = await service.get_job(job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return job


@router.get("", response_model=List[JobDetailResponse])
async def list_generations(db: AsyncSession = Depends(get_db)):
    """
    List all generation jobs
    
    Args:
        db: Database session (injected)
        
    Returns:
        List of all jobs in the system
    """
    service = GenerationService(db)
    return await service.list_jobs()
