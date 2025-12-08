# In-memory database for job storage
# NOTE: This is an in-memory implementation. In production, replace with SQLite/Postgres:
# - Use SQLAlchemy ORM with async support
# - Create proper database tables with migrations
# - Implement connection pooling for better performance
# - Add proper indexing on jobId for faster lookups

from typing import Dict, Optional, Any
from models import Job, JobStatus
from datetime import datetime, timezone
import threading


class JobDatabase:
    def __init__(self):
        self._jobs: Dict[str, Job] = {}
        self._lock = threading.Lock()

    def create_job(self, job: Job) -> Job:
        """Create a new job in the database"""
        with self._lock:
            self._jobs[job.id] = job
        return job

    def get_job(self, job_id: str) -> Optional[Job]:
        """Retrieve a job by ID"""
        with self._lock:
            return self._jobs.get(job_id)

    def update_job(self, job_id: str, **kwargs: Any) -> Optional[Job]:
        """Update job fields"""
        with self._lock:
            job = self._jobs.get(job_id)
            if job:
                job_dict = job.model_dump()
                job_dict.update(kwargs)
                job_dict['updatedAt'] = datetime.now(timezone.utc).isoformat()
                updated_job = Job(**job_dict)
                self._jobs[job_id] = updated_job
                return updated_job
        return None

    def get_pending_jobs(self) -> list[Job]:
        """Get all jobs with pending status"""
        with self._lock:
            return [
                job for job in self._jobs.values() 
                if job.status == JobStatus.PENDING
            ]

    def get_all_jobs(self) -> list[Job]:
        """Get all jobs"""
        with self._lock:
            return list(self._jobs.values())


# Global database instance
db = JobDatabase()
