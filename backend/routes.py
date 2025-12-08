# API Routes for image generation endpoints
from fastapi import APIRouter, HTTPException
from typing import List

from models import GenerationRequest, GenerationResponse, JobDetailResponse
from services import GenerationService

router = APIRouter(
    prefix="/generations",
    tags=["generations"]
)

# Dependency injection - service instance
generation_service = GenerationService()


@router.post("", response_model=GenerationResponse, status_code=202)
async def create_generation(request: GenerationRequest):
    """
    Create a new image generation job
    
    This endpoint creates a job and returns immediately with a jobId.
    The actual image generation happens asynchronously in the background.
    
    Args:
        request: Request body containing numImages
        
    Returns:
        Job ID and initial status (pending)
    """
    if request.numImages < 1 or request.numImages > 10:
        raise HTTPException(
            status_code=400,
            detail="numImages must be between 1 and 10"
        )
    
    return await generation_service.create_job(request.numImages)


@router.get("/{job_id}", response_model=JobDetailResponse)
async def get_generation(job_id: str):
    """
    Get the status and results of a generation job
    
    Args:
        job_id: The ID of the job to retrieve
        
    Returns:
        Complete job details including status, images (if completed), or error
    """
    job = await generation_service.get_job(job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return job


@router.get("", response_model=List[JobDetailResponse])
async def list_generations():
    """
    List all generation jobs
    
    Returns:
        List of all jobs in the system
    """
    return await generation_service.list_jobs()
