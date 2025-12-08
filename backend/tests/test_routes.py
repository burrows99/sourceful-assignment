# Unit tests for API endpoints
import pytest
from httpx import AsyncClient

from models import JobStatus


@pytest.mark.unit
class TestGenerationsEndpoints:
    """Test generation API endpoints."""
    
    async def test_create_generation_success(self, client: AsyncClient, sample_job_data):
        """Test successful job creation."""
        response = await client.post("/generations", json=sample_job_data)
        
        assert response.status_code == 202
        data = response.json()
        assert "jobId" in data
        assert data["status"] == "pending"
        assert isinstance(data["jobId"], str)
    
    async def test_create_generation_invalid_num_images_too_low(self, client: AsyncClient):
        """Test job creation with too few images."""
        response = await client.post("/generations", json={"numImages": 0})
        
        assert response.status_code == 400
        assert "numImages must be between 1 and 10" in response.json()["detail"]
    
    async def test_create_generation_invalid_num_images_too_high(self, client: AsyncClient):
        """Test job creation with too many images."""
        response = await client.post("/generations", json={"numImages": 15})
        
        assert response.status_code == 400
        assert "numImages must be between 1 and 10" in response.json()["detail"]
    
    async def test_create_generation_missing_field(self, client: AsyncClient):
        """Test job creation with missing required field."""
        response = await client.post("/generations", json={})
        
        assert response.status_code == 422
    
    async def test_get_generation_not_found(self, client: AsyncClient):
        """Test getting a non-existent job."""
        response = await client.get("/generations/non-existent-id")
        
        assert response.status_code == 404
        assert response.json()["detail"] == "Job not found"
    
    async def test_get_generation_success(self, client: AsyncClient, sample_job_data):
        """Test getting an existing job."""
        # Create a job first
        create_response = await client.post("/generations", json=sample_job_data)
        job_id = create_response.json()["jobId"]
        
        # Get the job
        response = await client.get(f"/generations/{job_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["jobId"] == job_id
        assert data["status"] in ["pending", "processing", "completed", "failed"]
        assert data["numImages"] == 3
    
    async def test_list_generations_empty(self, client: AsyncClient):
        """Test listing jobs when none exist."""
        response = await client.get("/generations")
        
        assert response.status_code == 200
        assert response.json() == []
    
    async def test_list_generations_with_jobs(self, client: AsyncClient, sample_job_data):
        """Test listing jobs after creating some."""
        # Create multiple jobs
        job_ids = []
        for i in range(3):
            create_response = await client.post("/generations", json={"numImages": i + 1})
            job_ids.append(create_response.json()["jobId"])
        
        # List all jobs
        response = await client.get("/generations")
        
        assert response.status_code == 200
        jobs = response.json()
        assert len(jobs) == 3
        assert all(job["jobId"] in job_ids for job in jobs)
