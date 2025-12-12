# API Routes for image generation endpoints
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from models import GenerationRequest, GenerationResponse, JobDetailResponse, ClassifyRequest, ClassifyResponse
from services import GenerationService
from core.database import get_db
from providers import get_vision_provider
from config import settings

router = APIRouter(
    prefix="/generations",
    tags=["generations"]
)

classify_router = APIRouter(
    tags=["classification"]
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


@classify_router.post("/classify", response_model=ClassifyResponse)
async def classify_image(request: ClassifyRequest):
    """
    Classify animals in an image using vision AI
    
    Uses a vision language model to identify animals in the provided image.
    If no animals are detected, returns an empty list with an error message.
    
    The provider is configurable via environment variables:
    - VISION_PROVIDER: "openrouter", "openai", or "mock"
    - VISION_MODEL: Specific model to use (optional, uses provider default)
    
    Args:
        request: Request body containing imgUrl
        
    Returns:
        List of animals detected and optional error message
    """
    # Validate URL format
    if not request.imgUrl.startswith(("http://", "https://")):
        raise HTTPException(
            status_code=400,
            detail="Invalid image URL. Must start with http:// or https://"
        )
    
    # Determine API key based on provider
    provider_type = settings.VISION_PROVIDER.lower()
    
    if provider_type == "mock":
        api_key = ""  # Mock doesn't need an API key
    elif provider_type == "openrouter":
        api_key = settings.OPENROUTER_API_KEY
        if not api_key:
            raise HTTPException(
                status_code=500,
                detail="OpenRouter API key not configured. Please set OPENROUTER_API_KEY in environment variables."
            )
    elif provider_type == "openai":
        api_key = settings.OPENAI_API_KEY
        if not api_key:
            raise HTTPException(
                status_code=500,
                detail="OpenAI API key not configured. Please set OPENAI_API_KEY in environment variables."
            )
    else:
        raise HTTPException(
            status_code=500,
            detail=f"Unknown vision provider: {provider_type}. Supported: openrouter, openai, mock"
        )
    
    # Get vision provider and classify image
    provider = get_vision_provider(
        provider_type=provider_type,
        api_key=api_key,
        model=settings.VISION_MODEL,
        site_url=settings.OPENROUTER_SITE_URL,
        site_name=settings.OPENROUTER_SITE_NAME,
        timeout=settings.VISION_TIMEOUT
    )
    
    result = await provider.classify_image(request.imgUrl)
    
    return ClassifyResponse(
        animals=result.get("animals", []),
        error=result.get("error")
    )
