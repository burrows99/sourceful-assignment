# Unit tests for business logic services
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from services import GenerationService
from models import JobStatus


@pytest.mark.unit
class TestGenerationService:
    """Test generation service business logic."""
    
    async def test_create_job(self, test_session: AsyncSession):
        """Test creating a new job."""
        service = GenerationService(test_session)
        
        result = await service.create_job(num_images=3)
        
        assert result.jobId is not None
        assert result.status == JobStatus.PENDING
    
    async def test_get_job_not_found(self, test_session: AsyncSession):
        """Test getting a non-existent job."""
        service = GenerationService(test_session)
        
        result = await service.get_job("non-existent-id")
        
        assert result is None
    
    async def test_get_job_success(self, test_session: AsyncSession):
        """Test getting an existing job."""
        service = GenerationService(test_session)
        
        # Create a job
        created = await service.create_job(num_images=2)
        
        # Get the job
        result = await service.get_job(created.jobId)
        
        assert result is not None
        assert result.jobId == created.jobId
        assert result.numImages == 2
        assert result.status == JobStatus.PENDING
    
    async def test_list_jobs_empty(self, test_session: AsyncSession):
        """Test listing jobs when none exist."""
        service = GenerationService(test_session)
        
        result = await service.list_jobs()
        
        assert result == []
    
    async def test_list_jobs_with_data(self, test_session: AsyncSession):
        """Test listing multiple jobs."""
        service = GenerationService(test_session)
        
        # Create multiple jobs
        for i in range(3):
            await service.create_job(num_images=i + 1)
        
        # List all jobs
        result = await service.list_jobs()
        
        assert len(result) == 3
        assert all(job.status == JobStatus.PENDING for job in result)
