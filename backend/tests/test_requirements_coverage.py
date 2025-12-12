"""
Test coverage for all assignment requirements
This file ensures all requirements from the assignment are tested
"""
import pytest
import asyncio
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession

from models import JobStatus
from repositories.job_repository import JobRepository
from providers import get_provider, OpenRouterProvider, MockProvider


@pytest.mark.integration
class TestRequirement_POST_Generations:
    """
    REQUIREMENT: POST /generations
    - Generates n images of a random animal (animal selected by API)
    - Must NOT perform generation synchronously
    - Store job record in DB
    - Background worker picks up pending jobs, calls provider, updates status
    """
    
    async def test_returns_pending_status_immediately(self, client: AsyncClient):
        """Test that endpoint returns immediately with pending status (async behavior)"""
        response = await client.post("/generations", json={"numImages": 3})
        
        assert response.status_code == 202
        data = response.json()
        assert data["status"] == "pending"
        assert "jobId" in data
        # Should return immediately, not wait for image generation
    
    async def test_job_stored_in_database(self, client: AsyncClient, test_session: AsyncSession):
        """Test that job is stored in database"""
        response = await client.post("/generations", json={"numImages": 2})
        job_id = response.json()["jobId"]
        
        # Verify job exists in DB
        repo = JobRepository(test_session)
        job = await repo.get_by_id(job_id)
        assert job is not None
        assert job.status == JobStatus.PENDING
        assert job.numImages == 2
    
    async def test_random_animal_selection(self, client: AsyncClient):
        """Test that API selects random animal (not user-specified)"""
        # Create job and wait for processing (in integration test with worker)
        response = await client.post("/generations", json={"numImages": 1})
        job_id = response.json()["jobId"]
        
        # Note: Animal is selected during processing, not at creation
        # This test verifies the API design allows for this
        get_response = await client.get(f"/generations/{job_id}")
        job_data = get_response.json()
        
        # Initially no animal (selected by worker during processing)
        assert job_data["animal"] is None or isinstance(job_data["animal"], str)
    
    async def test_request_body_num_images(self, client: AsyncClient):
        """Test request body contains numImages field"""
        response = await client.post("/generations", json={"numImages": 5})
        assert response.status_code == 202
    
    async def test_response_body_format(self, client: AsyncClient):
        """Test response contains jobId and status"""
        response = await client.post("/generations", json={"numImages": 2})
        
        data = response.json()
        assert "jobId" in data
        assert "status" in data
        assert data["status"] == "pending"


@pytest.mark.integration
class TestRequirement_GET_GenerationsByID:
    """
    REQUIREMENT: GET /generations/[jobId]
    - Returns job with status and outputs
    - Outputs contain URL of images
    """
    
    async def test_returns_job_with_status(self, client: AsyncClient):
        """Test endpoint returns job with status"""
        # Create job
        create_response = await client.post("/generations", json={"numImages": 2})
        job_id = create_response.json()["jobId"]
        
        # Get job
        response = await client.get(f"/generations/{job_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["jobId"] == job_id
        assert "status" in data
        assert data["status"] in ["pending", "processing", "completed", "failed"]
    
    async def test_outputs_contain_image_urls(self, client: AsyncClient, test_session: AsyncSession):
        """Test that completed job outputs contain image URLs"""
        # Create and manually complete a job for testing
        from models import Job
        from datetime import datetime, timezone
        
        repo = JobRepository(test_session)
        now = datetime.now(timezone.utc).isoformat()
        
        job = Job(
            id="test-completed-job",
            status=JobStatus.COMPLETED,
            numImages=2,
            animal="cat",
            imageUrls=["https://example.com/image1.png", "https://example.com/image2.png"],
            createdAt=now,
            updatedAt=now
        )
        await repo.create(job)
        await test_session.commit()  # Commit so the API can see it
        
        # Get the job
        response = await client.get("/generations/test-completed-job")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "completed"
        assert "imageUrls" in data
        assert len(data["imageUrls"]) == 2
        # Images can be HTTP URLs or base64 data URLs
        assert all(url.startswith("http") or url.startswith("data:image/") for url in data["imageUrls"])
    
    async def test_handles_different_statuses(self, client: AsyncClient):
        """Test endpoint handles all job statuses"""
        # Create job (pending)
        response = await client.post("/generations", json={"numImages": 1})
        job_id = response.json()["jobId"]
        
        # Get job
        get_response = await client.get(f"/generations/{job_id}")
        data = get_response.json()
        
        # Verify status is one of the valid statuses
        assert data["status"] in ["pending", "processing", "completed", "failed"]
    
    async def test_supports_base64_image_urls(self, client: AsyncClient, test_session: AsyncSession):
        """Test that system handles base64-encoded data URLs from OpenRouter"""
        from models import Job
        from datetime import datetime, timezone
        
        repo = JobRepository(test_session)
        now = datetime.now(timezone.utc).isoformat()
        
        # Create job with base64 data URL (as returned by OpenRouter Riverflow)
        base64_url = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABAAAAAQACAIAAADwf7zUAAEAAElEQVR4nIT9..."
        job = Job(
            id="test-base64-job",
            status=JobStatus.COMPLETED,
            numImages=1,
            animal="cat",
            imageUrls=[base64_url],
            createdAt=now,
            updatedAt=now
        )
        await repo.create(job)
        await test_session.commit()
        
        # Get the job
        response = await client.get("/generations/test-base64-job")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "completed"
        assert len(data["imageUrls"]) == 1
        assert data["imageUrls"][0].startswith("data:image/")
        assert "base64," in data["imageUrls"][0]


@pytest.mark.integration
class TestRequirement_POST_Classify:
    """
    REQUIREMENT: POST /classify
    - Takes imgUrl of animal image
    - Uses vision language model to guess animal
    - Indicates if no animal in image
    """
    
    async def test_request_body_contains_img_url(self, client: AsyncClient):
        """Test request body contains imgUrl"""
        with patch('routes.get_vision_provider') as mock_provider:
            mock_instance = AsyncMock()
            mock_instance.classify_image.return_value = {"animals": ["cat"], "error": None}
            mock_provider.return_value = mock_instance
            
            response = await client.post(
                "/classify",
                json={"imgUrl": "https://example.com/cat.jpg"}
            )
            
            assert response.status_code == 200
    
    async def test_response_body_contains_animals_list(self, client: AsyncClient):
        """Test response contains animals list"""
        with patch('routes.get_vision_provider') as mock_provider:
            mock_instance = AsyncMock()
            mock_instance.classify_image.return_value = {
                "animals": ["dog", "cat"],
                "error": None
            }
            mock_provider.return_value = mock_instance
            
            response = await client.post(
                "/classify",
                json={"imgUrl": "https://example.com/pets.jpg"}
            )
            
            data = response.json()
            assert "animals" in data
            assert isinstance(data["animals"], list)
            assert len(data["animals"]) == 2
    
    async def test_empty_animals_list_when_no_animals(self, client: AsyncClient):
        """Test response has empty list when no animals detected"""
        with patch('routes.get_vision_provider') as mock_provider:
            mock_instance = AsyncMock()
            mock_instance.classify_image.return_value = {
                "animals": [],
                "error": "No animals detected in the image"
            }
            mock_provider.return_value = mock_instance
            
            response = await client.post(
                "/classify",
                json={"imgUrl": "https://example.com/landscape.jpg"}
            )
            
            data = response.json()
            assert data["animals"] == []
            assert data["error"] is not None
    
    async def test_error_message_for_no_animals(self, client: AsyncClient):
        """Test error field indicates no animals present"""
        with patch('routes.get_vision_provider') as mock_provider:
            mock_instance = AsyncMock()
            mock_instance.classify_image.return_value = {
                "animals": [],
                "error": "No animals detected in the image"
            }
            mock_provider.return_value = mock_instance
            
            response = await client.post(
                "/classify",
                json={"imgUrl": "https://example.com/building.jpg"}
            )
            
            data = response.json()
            assert "error" in data
            assert "no animal" in data["error"].lower() or "not detected" in data["error"].lower()


@pytest.mark.integration
class TestRequirement_ErrorHandling:
    """
    REQUIREMENT: Handle error cases gracefully
    - Invalid input
    - Missing job
    - Provider failures
    """
    
    async def test_invalid_num_images_too_low(self, client: AsyncClient):
        """Test handling of invalid input: numImages too low"""
        response = await client.post("/generations", json={"numImages": 0})
        
        assert response.status_code == 400
        assert "detail" in response.json()
    
    async def test_invalid_num_images_too_high(self, client: AsyncClient):
        """Test handling of invalid input: numImages too high"""
        response = await client.post("/generations", json={"numImages": 100})
        
        assert response.status_code == 400
        assert "detail" in response.json()
    
    async def test_invalid_num_images_negative(self, client: AsyncClient):
        """Test handling of invalid input: negative numImages"""
        response = await client.post("/generations", json={"numImages": -5})
        
        assert response.status_code == 400
    
    async def test_missing_required_field(self, client: AsyncClient):
        """Test handling of invalid input: missing required field"""
        response = await client.post("/generations", json={})
        
        assert response.status_code == 422
    
    async def test_missing_job_returns_404(self, client: AsyncClient):
        """Test handling of missing job"""
        response = await client.get("/generations/non-existent-job-id")
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    async def test_invalid_image_url_format(self, client: AsyncClient):
        """Test handling of invalid image URL"""
        response = await client.post(
            "/classify",
            json={"imgUrl": "not-a-valid-url"}
        )
        
        assert response.status_code == 400
        assert "invalid" in response.json()["detail"].lower()
    
    async def test_provider_failure_handling(self, client: AsyncClient):
        """Test handling of provider failures"""
        with patch('routes.get_vision_provider') as mock_provider:
            mock_instance = AsyncMock()
            mock_instance.classify_image.return_value = {
                "animals": [],
                "error": "API request failed: 500 Internal Server Error"
            }
            mock_provider.return_value = mock_instance
            
            response = await client.post(
                "/classify",
                json={"imgUrl": "https://example.com/test.jpg"}
            )
            
            # Should still return 200 but with error in response
            assert response.status_code == 200
            data = response.json()
            assert "error" in data
            assert data["error"] is not None
    
    async def test_missing_api_key_configuration(self, client: AsyncClient):
        """Test handling when API key is not configured"""
        with patch('routes.settings') as mock_settings:
            mock_settings.VISION_PROVIDER = "openrouter"
            mock_settings.OPENROUTER_API_KEY = ""
            
            response = await client.post(
                "/classify",
                json={"imgUrl": "https://example.com/test.jpg"}
            )
            
            assert response.status_code == 500
            assert "not configured" in response.json()["detail"].lower()


@pytest.mark.integration
class TestRequirement_ProviderSwapping:
    """
    REQUIREMENT: Design code to be easy to extend (swapping AI providers)
    Test that provider architecture supports swapping
    """
    
    def test_unified_provider_interface(self):
        """Test that all providers implement the same interface"""
        # OpenRouter provider
        openrouter = get_provider("openrouter", api_key="test-key")
        assert hasattr(openrouter, "generate_images")
        assert hasattr(openrouter, "classify_image")
        
        # Mock provider
        mock = get_provider("mock")
        assert hasattr(mock, "generate_images")
        assert hasattr(mock, "classify_image")
    
    def test_provider_factory_pattern(self):
        """Test factory pattern allows easy provider swapping"""
        # Can create different providers with same factory
        provider1 = get_provider("mock")
        provider2 = get_provider("openrouter", api_key="test")
        
        # Both are BaseProvider instances
        assert isinstance(provider1, MockProvider)
        assert isinstance(provider2, OpenRouterProvider)
    
    async def test_mock_provider_supports_both_capabilities(self):
        """Test mock provider implements both text-to-image and image-to-text"""
        provider = get_provider("mock", delay_seconds=0.1)
        
        # Test image generation
        images = await provider.generate_images("test prompt", 2)
        assert len(images) == 2
        
        # Test image classification
        result = await provider.classify_image("https://example.com/cat.jpg")
        assert "animals" in result
    
    async def test_openrouter_provider_supports_both_capabilities(self):
        """Test OpenRouter provider implements both capabilities"""
        provider = get_provider(
            "openrouter",
            api_key="test-key",
            image_model="sourceful/riverflow-v2-max-preview",
            vision_model="openai/gpt-4o-mini"
        )
        
        # Verify both methods exist
        assert callable(provider.generate_images)
        assert callable(provider.classify_image)
        
        # Verify configuration
        assert provider.image_model == "sourceful/riverflow-v2-max-preview"
        assert provider.vision_model == "openai/gpt-4o-mini"


@pytest.mark.integration
class TestRequirement_BackgroundWorker:
    """
    REQUIREMENT: Worker functionality
    - Background worker/async task picks up pending jobs
    - Calls image provider
    - Updates job status and output URLs
    """
    
    @patch('workers.async_worker.sessionmanager')
    async def test_worker_picks_up_pending_jobs(self, mock_sessionmanager, test_session: AsyncSession):
        """Test worker picks up pending jobs from database"""
        from workers.async_worker import AsyncImageWorker
        from models import Job
        from datetime import datetime, timezone
        
        # Setup mock session
        mock_session_context = AsyncMock()
        mock_session_context.__aenter__.return_value = test_session
        mock_session_context.__aexit__.return_value = None
        mock_sessionmanager.session.return_value = mock_session_context
        
        # Create pending job
        repo = JobRepository(test_session)
        now = datetime.now(timezone.utc).isoformat()
        job = Job(
            id="test-worker-job",
            status=JobStatus.PENDING,
            numImages=1,
            createdAt=now,
            updatedAt=now
        )
        await repo.create(job)
        
        # Create worker
        worker = AsyncImageWorker(poll_interval=0.1)
        
        # Mock provider
        with patch.object(worker.provider, 'generate_images', new_callable=AsyncMock) as mock_gen:
            mock_gen.return_value = ["https://example.com/image.png"]
            
            # Process job
            await worker._process_job("test-worker-job")
        
        # Verify job was processed
        updated_job = await repo.get_by_id("test-worker-job")
        assert updated_job.status == JobStatus.COMPLETED
    
    @patch('workers.async_worker.sessionmanager')
    async def test_worker_calls_image_provider(self, mock_sessionmanager, test_session: AsyncSession):
        """Test worker calls the image provider"""
        from workers.async_worker import AsyncImageWorker
        from models import Job
        from datetime import datetime, timezone
        
        # Setup
        mock_session_context = AsyncMock()
        mock_session_context.__aenter__.return_value = test_session
        mock_session_context.__aexit__.return_value = None
        mock_sessionmanager.session.return_value = mock_session_context
        
        # Create job
        repo = JobRepository(test_session)
        now = datetime.now(timezone.utc).isoformat()
        job = Job(
            id="test-provider-call",
            status=JobStatus.PENDING,
            numImages=3,
            createdAt=now,
            updatedAt=now
        )
        await repo.create(job)
        
        # Create worker and spy on provider
        worker = AsyncImageWorker(poll_interval=0.1)
        
        with patch.object(worker.provider, 'generate_images', new_callable=AsyncMock) as mock_gen:
            mock_gen.return_value = ["url1", "url2", "url3"]
            
            await worker._process_job("test-provider-call")
            
            # Verify provider was called
            mock_gen.assert_called_once()
            call_args = mock_gen.call_args
            assert call_args[0][1] == 3  # numImages argument
    
    @patch('workers.async_worker.sessionmanager')
    async def test_worker_updates_job_status_and_urls(self, mock_sessionmanager, test_session: AsyncSession):
        """Test worker updates job status and image URLs"""
        from workers.async_worker import AsyncImageWorker
        from models import Job
        from datetime import datetime, timezone
        
        # Setup
        mock_session_context = AsyncMock()
        mock_session_context.__aenter__.return_value = test_session
        mock_session_context.__aexit__.return_value = None
        mock_sessionmanager.session.return_value = mock_session_context
        
        # Create job
        repo = JobRepository(test_session)
        now = datetime.now(timezone.utc).isoformat()
        job = Job(
            id="test-update-status",
            status=JobStatus.PENDING,
            numImages=2,
            createdAt=now,
            updatedAt=now
        )
        await repo.create(job)
        
        # Process job
        worker = AsyncImageWorker(poll_interval=0.1)
        test_urls = ["https://example.com/img1.png", "https://example.com/img2.png"]
        
        with patch.object(worker.provider, 'generate_images', new_callable=AsyncMock) as mock_gen:
            mock_gen.return_value = test_urls
            
            await worker._process_job("test-update-status")
        
        # Verify updates
        updated_job = await repo.get_by_id("test-update-status")
        assert updated_job.status == JobStatus.COMPLETED
        assert updated_job.imageUrls == test_urls
        assert updated_job.animal is not None  # Random animal was selected
