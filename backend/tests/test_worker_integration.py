# Integration tests for worker
import pytest
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import Mock, patch, AsyncMock

from workers.async_worker import AsyncImageWorker, ANIMALS
from repositories.job_repository import JobRepository
from models import Job, JobStatus
from datetime import datetime, timezone


@pytest.mark.integration
class TestAsyncImageWorker:
    """Test async image worker functionality."""
    
    async def test_worker_initialization(self):
        """Test worker can be initialized."""
        worker = AsyncImageWorker(poll_interval=0.1)
        
        assert worker.poll_interval == 0.1
        assert worker._running is False
        assert worker._task is None
    
    async def test_worker_start_stop(self):
        """Test worker can start and stop."""
        worker = AsyncImageWorker(poll_interval=0.1)
        
        # Start worker
        worker.start()
        assert worker._running is True
        assert worker._task is not None
        
        # Give it a moment to run
        await asyncio.sleep(0.2)
        
        # Stop worker
        await worker.stop()
        assert worker._running is False
    
    @patch('workers.async_worker.sessionmanager')
    async def test_worker_processes_pending_job(self, mock_sessionmanager, test_session: AsyncSession):
        """Test worker processes a pending job."""
        # Setup mock session manager
        mock_session_context = AsyncMock()
        mock_session_context.__aenter__.return_value = test_session
        mock_session_context.__aexit__.return_value = None
        mock_sessionmanager.session.return_value = mock_session_context
        
        # Create a pending job
        repo = JobRepository(test_session)
        now = datetime.now(timezone.utc).isoformat()
        job = Job(
            id="test-job-1",
            status=JobStatus.PENDING,
            numImages=2,
            createdAt=now,
            updatedAt=now
        )
        await repo.create(job)
        
        # Create worker and process jobs
        worker = AsyncImageWorker(poll_interval=0.1)
        
        # Mock the image provider to return immediately
        with patch.object(worker.provider, 'generate_images', new_callable=AsyncMock) as mock_generate:
            mock_generate.return_value = ["url1", "url2"]
            
            # Process the job
            await worker._process_job("test-job-1")
        
        # Verify job was updated
        updated_job = await repo.get_by_id("test-job-1")
        assert updated_job.status == JobStatus.COMPLETED
        assert updated_job.animal in ANIMALS
        assert len(updated_job.imageUrls) == 2
    
    @patch('workers.async_worker.sessionmanager')
    async def test_worker_handles_job_error(self, mock_sessionmanager, test_session: AsyncSession):
        """Test worker handles job processing errors."""
        # Setup mock session manager
        mock_session_context = AsyncMock()
        mock_session_context.__aenter__.return_value = test_session
        mock_session_context.__aexit__.return_value = None
        mock_sessionmanager.session.return_value = mock_session_context
        
        # Create a pending job
        repo = JobRepository(test_session)
        now = datetime.now(timezone.utc).isoformat()
        job = Job(
            id="test-job-2",
            status=JobStatus.PENDING,
            numImages=2,
            createdAt=now,
            updatedAt=now
        )
        await repo.create(job)
        
        # Create worker
        worker = AsyncImageWorker(poll_interval=0.1)
        
        # Mock the image provider to raise an error
        with patch.object(worker.provider, 'generate_images', new_callable=AsyncMock) as mock_generate:
            mock_generate.side_effect = Exception("Provider error")
            
            # Process the job
            await worker._process_job("test-job-2")
        
        # Verify job was marked as failed
        updated_job = await repo.get_by_id("test-job-2")
        assert updated_job.status == JobStatus.FAILED
        assert updated_job.error == "Provider error"
    
    async def test_worker_selects_random_animal(self):
        """Test worker selects from available animals."""
        worker = AsyncImageWorker(poll_interval=0.1)
        
        # Check animals list is populated
        assert len(ANIMALS) == 20
        assert "cat" in ANIMALS
        assert "dog" in ANIMALS
        assert "elephant" in ANIMALS
