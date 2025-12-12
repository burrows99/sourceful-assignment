# Integration tests - end-to-end flows
import pytest
import asyncio
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock

from models import JobStatus


@pytest.mark.integration
class TestEndToEndFlows:
    """Test complete end-to-end workflows."""
    
    async def test_complete_job_lifecycle(self, client: AsyncClient):
        """Test complete job creation and retrieval flow."""
        # Create a job
        create_response = await client.post(
            "/generations",
            json={"numImages": 3}
        )
        assert create_response.status_code == 202
        
        job_data = create_response.json()
        job_id = job_data["jobId"]
        assert job_data["status"] == "pending"
        
        # Get the job details
        get_response = await client.get(f"/generations/{job_id}")
        assert get_response.status_code == 200
        
        job_details = get_response.json()
        assert job_details["jobId"] == job_id
        assert job_details["status"] == "pending"
        assert job_details["numImages"] == 3
        assert job_details["animal"] is None
        assert job_details["imageUrls"] is None
        
        # List all jobs
        list_response = await client.get("/generations")
        assert list_response.status_code == 200
        
        jobs = list_response.json()
        assert len(jobs) >= 1
        assert any(job["jobId"] == job_id for job in jobs)
    
    async def test_multiple_concurrent_jobs(self, client: AsyncClient):
        """Test creating multiple jobs concurrently."""
        # Create multiple jobs in parallel
        tasks = [
            client.post("/generations", json={"numImages": i + 1})
            for i in range(5)
        ]
        responses = await asyncio.gather(*tasks)
        
        # Verify all jobs were created
        assert all(r.status_code == 202 for r in responses)
        job_ids = [r.json()["jobId"] for r in responses]
        assert len(set(job_ids)) == 5  # All unique
        
        # Verify all jobs appear in list
        list_response = await client.get("/generations")
        all_jobs = list_response.json()
        assert len(all_jobs) >= 5
        
        for job_id in job_ids:
            assert any(job["jobId"] == job_id for job in all_jobs)
    
    @patch('workers.async_worker.AsyncImageWorker._process_job')
    async def test_job_processing_simulation(self, mock_process, client: AsyncClient):
        """Test simulating job processing."""
        # Make the mock async
        mock_process.return_value = None
        
        # Create a job
        response = await client.post(
            "/generations",
            json={"numImages": 2}
        )
        job_id = response.json()["jobId"]
        
        # Simulate processing
        # In real scenario, worker would pick this up
        # For test, we verify the job is queryable
        get_response = await client.get(f"/generations/{job_id}")
        assert get_response.status_code == 200
        assert get_response.json()["status"] in [
            "pending", "processing", "completed", "failed"
        ]
    
    async def test_validation_errors(self, client: AsyncClient):
        """Test various validation error scenarios."""
        # Missing required field
        response = await client.post("/generations", json={})
        assert response.status_code == 422
        
        # Invalid type
        response = await client.post("/generations", json={"numImages": "abc"})
        assert response.status_code == 422
        
        # Out of range (too low)
        response = await client.post("/generations", json={"numImages": 0})
        assert response.status_code == 400
        
        # Out of range (too high)
        response = await client.post("/generations", json={"numImages": 100})
        assert response.status_code == 400
        
        # Negative number
        response = await client.post("/generations", json={"numImages": -1})
        assert response.status_code == 400
