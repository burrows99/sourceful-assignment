# Business logic service layer
from datetime import datetime, timezone
import uuid
from typing import Optional, List

from models import GenerationResponse, JobDetailResponse, Job, JobStatus
from database import db


class GenerationService:
    """
    Service layer for image generation business logic
    Separates business logic from API routes
    """
    
    def __init__(self):
        self.db = db
    
    async def create_job(self, num_images: int) -> GenerationResponse:
        """
        Create a new image generation job
        
        Args:
            num_images: Number of images to generate
            
        Returns:
            GenerationResponse with jobId and status
        """
        # Generate unique job ID
        job_id = str(uuid.uuid4())
        
        # Create job in database
        now = datetime.now(timezone.utc).isoformat()
        job = Job(
            id=job_id,
            status=JobStatus.PENDING,
            numImages=num_images,
            createdAt=now,
            updatedAt=now
        )
        
        self.db.create_job(job)
        
        return GenerationResponse(
            jobId=job_id,
            status=JobStatus.PENDING
        )
    
    async def get_job(self, job_id: str) -> Optional[JobDetailResponse]:
        """
        Retrieve a job by ID
        
        Args:
            job_id: The job identifier
            
        Returns:
            JobDetailResponse if found, None otherwise
        """
        job = self.db.get_job(job_id)
        
        if not job:
            return None
        
        return JobDetailResponse(
            jobId=job.id,
            status=job.status,
            numImages=job.numImages,
            animal=job.animal,
            imageUrls=job.imageUrls,
            error=job.error,
            createdAt=job.createdAt,
            updatedAt=job.updatedAt
        )
    
    async def list_jobs(self) -> List[JobDetailResponse]:
        """
        List all jobs in the system
        
        Returns:
            List of JobDetailResponse objects
        """
        jobs = self.db.get_all_jobs()
        
        return [
            JobDetailResponse(
                jobId=job.id,
                status=job.status,
                numImages=job.numImages,
                animal=job.animal,
                imageUrls=job.imageUrls,
                error=job.error,
                createdAt=job.createdAt,
                updatedAt=job.updatedAt
            )
            for job in jobs
        ]
