# Unit tests for repository layer
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone

from repositories.job_repository import JobRepository
from models import Job, JobStatus


@pytest.mark.unit
class TestJobRepository:
    """Test job repository data access."""
    
    async def test_create_job(self, test_session: AsyncSession):
        """Test creating a job in database."""
        repo = JobRepository(test_session)
        
        now = datetime.now(timezone.utc).isoformat()
        job = Job(
            id="test-job-1",
            status=JobStatus.PENDING,
            numImages=3,
            createdAt=now,
            updatedAt=now
        )
        
        result = await repo.create(job)
        
        assert result.id == "test-job-1"
        assert result.status == JobStatus.PENDING
        assert result.numImages == 3
    
    async def test_get_by_id_not_found(self, test_session: AsyncSession):
        """Test getting non-existent job."""
        repo = JobRepository(test_session)
        
        result = await repo.get_by_id("non-existent")
        
        assert result is None
    
    async def test_get_by_id_success(self, test_session: AsyncSession):
        """Test getting existing job by ID."""
        repo = JobRepository(test_session)
        
        # Create a job
        now = datetime.now(timezone.utc).isoformat()
        job = Job(
            id="test-job-2",
            status=JobStatus.PENDING,
            numImages=2,
            createdAt=now,
            updatedAt=now
        )
        await repo.create(job)
        
        # Get the job
        result = await repo.get_by_id("test-job-2")
        
        assert result is not None
        assert result.id == "test-job-2"
        assert result.numImages == 2
    
    async def test_update_job(self, test_session: AsyncSession):
        """Test updating a job."""
        repo = JobRepository(test_session)
        
        # Create a job
        now = datetime.now(timezone.utc).isoformat()
        job = Job(
            id="test-job-3",
            status=JobStatus.PENDING,
            numImages=3,
            createdAt=now,
            updatedAt=now
        )
        await repo.create(job)
        
        # Update the job
        result = await repo.update(
            "test-job-3",
            status=JobStatus.COMPLETED,
            animal="cat",
            imageUrls=["url1", "url2", "url3"]
        )
        
        assert result is not None
        assert result.status == JobStatus.COMPLETED
        assert result.animal == "cat"
        assert len(result.imageUrls) == 3
    
    async def test_get_pending_jobs(self, test_session: AsyncSession):
        """Test getting all pending jobs."""
        repo = JobRepository(test_session)
        
        # Create jobs with different statuses
        now = datetime.now(timezone.utc).isoformat()
        for i, status in enumerate([JobStatus.PENDING, JobStatus.COMPLETED, JobStatus.PENDING]):
            job = Job(
                id=f"test-job-{i}",
                status=status,
                numImages=1,
                createdAt=now,
                updatedAt=now
            )
            await repo.create(job)
        
        # Get pending jobs
        result = await repo.get_pending_jobs()
        
        assert len(result) == 2
        assert all(job.status == JobStatus.PENDING for job in result)
    
    async def test_get_all_jobs(self, test_session: AsyncSession):
        """Test getting all jobs."""
        repo = JobRepository(test_session)
        
        # Create multiple jobs
        now = datetime.now(timezone.utc).isoformat()
        for i in range(5):
            job = Job(
                id=f"test-job-{i}",
                status=JobStatus.PENDING,
                numImages=i + 1,
                createdAt=now,
                updatedAt=now
            )
            await repo.create(job)
        
        # Get all jobs
        result = await repo.get_all()
        
        assert len(result) == 5
