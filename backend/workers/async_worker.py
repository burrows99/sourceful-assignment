# Async background worker service for processing jobs
import asyncio
import random
import logging
from typing import Optional

from models import JobStatus
from providers import get_image_provider
from config import settings
from core.database import sessionmanager
from repositories.job_repository import JobRepository

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# List of animals to randomly select from
ANIMALS = [
    "cat", "dog", "elephant", "lion", "tiger", "bear", "giraffe",
    "zebra", "panda", "koala", "fox", "wolf", "rabbit", "deer",
    "penguin", "owl", "eagle", "dolphin", "whale", "octopus"
]


class AsyncImageWorker:
    """
    Async background worker that processes pending image generation jobs
    Runs as asyncio task in the main event loop (production pattern)
    """
    
    def __init__(self, poll_interval: Optional[float] = None):
        """
        Initialize the worker
        
        Args:
            poll_interval: Time in seconds between polling for new jobs
        """
        self.poll_interval = poll_interval if poll_interval is not None else settings.WORKER_POLL_INTERVAL
        self.provider = get_image_provider(delay_seconds=settings.IMAGE_PROVIDER_DELAY)
        self._task: Optional[asyncio.Task] = None
        self._running = False
    
    def start(self):
        """Start the worker as an asyncio task"""
        if self._running:
            logger.warning("Worker is already running")
            return
        
        self._running = True
        self._task = asyncio.create_task(self._run())
        logger.info("✅ Async image worker started")
    
    async def stop(self):
        """Stop the worker gracefully"""
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("✅ Async image worker stopped")
    
    async def _run(self):
        """Main worker loop - runs as asyncio task"""
        while self._running:
            try:
                await self._process_pending_jobs()
                await asyncio.sleep(self.poll_interval)
                
            except asyncio.CancelledError:
                logger.info("Worker task cancelled")
                break
            except Exception as e:
                logger.error(f"Error in worker loop: {e}", exc_info=True)
                await asyncio.sleep(self.poll_interval)
    
    async def _process_pending_jobs(self):
        """Get and process all pending jobs"""
        async with sessionmanager.session() as session:
            repository = JobRepository(session)
            pending_jobs = await repository.get_pending_jobs()
            
            if pending_jobs:
                logger.info(f"Found {len(pending_jobs)} pending job(s)")
            
            # Process jobs concurrently
            if pending_jobs:
                tasks = [self._process_job(job.id) for job in pending_jobs]
                await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _process_job(self, job_id: str):
        """
        Process a single job
        
        Args:
            job_id: The ID of the job to process
        """
        # Use a fresh session for each job
        async with sessionmanager.session() as session:
            repository = JobRepository(session)
            
            try:
                # Mark job as processing
                job = await repository.update(job_id, status=JobStatus.PROCESSING)
                if not job:
                    logger.error(f"Job {job_id} not found")
                    return
                
                logger.info(f"⚙️  Processing job {job_id} - generating {job.numImages} images")
                
                # Select random animal
                animal = random.choice(ANIMALS)
                prompt = f"a cute {animal}"
                
                logger.info(f"🐾 Job {job_id} - selected animal: {animal}")
                
                # Generate images using the provider
                image_urls = await self.provider.generate_images(prompt, job.numImages)
                
                # Update job with results
                await repository.update(
                    job_id,
                    status=JobStatus.COMPLETED,
                    animal=animal,
                    imageUrls=image_urls
                )
                
                logger.info(f"✅ Job {job_id} completed with {len(image_urls)} images")
                
            except Exception as e:
                # Update job with error
                error_msg = str(e)
                logger.error(f"❌ Job {job_id} failed: {error_msg}", exc_info=True)
                
                try:
                    await repository.update(
                        job_id,
                        status=JobStatus.FAILED,
                        error=error_msg
                    )
                except Exception as update_error:
                    logger.error(f"Failed to update job {job_id} error status: {update_error}")


# Global worker instance
worker = AsyncImageWorker()
