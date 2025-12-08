# Repository pattern for database operations
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from datetime import datetime, timezone

from db_models import JobModel
from models import Job, JobStatus


class JobRepository:
    """
    Repository pattern for Job database operations
    Encapsulates all database queries for jobs
    """
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, job: Job) -> Job:
        """Create a new job"""
        db_job = JobModel(
            id=job.id,
            status=job.status.value,
            num_images=job.numImages,
            animal=job.animal,
            image_urls=job.imageUrls,
            error=job.error,
            created_at=datetime.fromisoformat(job.createdAt),
            updated_at=datetime.fromisoformat(job.updatedAt)
        )
        self.session.add(db_job)
        await self.session.flush()
        await self.session.refresh(db_job)
        return self._to_domain_model(db_job)
    
    async def get_by_id(self, job_id: str) -> Optional[Job]:
        """Get job by ID"""
        result = await self.session.execute(
            select(JobModel).where(JobModel.id == job_id)
        )
        db_job = result.scalar_one_or_none()
        return self._to_domain_model(db_job) if db_job else None
    
    async def update(self, job_id: str, **kwargs) -> Optional[Job]:
        """Update job fields"""
        update_data = {}
        
        if "status" in kwargs:
            update_data["status"] = kwargs["status"].value if isinstance(kwargs["status"], JobStatus) else kwargs["status"]
        if "animal" in kwargs:
            update_data["animal"] = kwargs["animal"]
        if "imageUrls" in kwargs:
            update_data["image_urls"] = kwargs["imageUrls"]
        if "error" in kwargs:
            update_data["error"] = kwargs["error"]
        
        update_data["updated_at"] = datetime.now(timezone.utc)
        
        await self.session.execute(
            update(JobModel)
            .where(JobModel.id == job_id)
            .values(**update_data)
        )
        await self.session.flush()
        
        return await self.get_by_id(job_id)
    
    async def get_pending_jobs(self) -> List[Job]:
        """Get all pending jobs"""
        result = await self.session.execute(
            select(JobModel).where(JobModel.status == JobStatus.PENDING.value)
        )
        db_jobs = result.scalars().all()
        return [self._to_domain_model(job) for job in db_jobs]
    
    async def get_all(self) -> List[Job]:
        """Get all jobs"""
        result = await self.session.execute(select(JobModel))
        db_jobs = result.scalars().all()
        return [self._to_domain_model(job) for job in db_jobs]
    
    @staticmethod
    def _to_domain_model(db_job: JobModel) -> Job:
        """Convert SQLAlchemy model to Pydantic domain model"""
        return Job(
            id=db_job.id,
            status=JobStatus(db_job.status),
            numImages=db_job.num_images,
            animal=db_job.animal,
            imageUrls=db_job.image_urls,
            error=db_job.error,
            createdAt=db_job.created_at.isoformat(),
            updatedAt=db_job.updated_at.isoformat()
        )
