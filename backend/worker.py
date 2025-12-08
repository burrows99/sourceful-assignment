# Background worker for processing image generation jobs
import asyncio
import threading
import random
from database import db
from models import JobStatus
from providers import get_image_provider
from config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# List of animals to randomly select from
ANIMALS = [
    "cat", "dog", "elephant", "lion", "tiger", "bear", "giraffe",
    "zebra", "panda", "koala", "fox", "wolf", "rabbit", "deer",
    "penguin", "owl", "eagle", "dolphin", "whale", "octopus"
]


class ImageGenerationWorker:
    """
    Background worker that processes pending image generation jobs
    
    This worker:
    1. Polls the database for pending jobs
    2. Selects a random animal for each job
    3. Calls the image provider to generate images
    4. Updates the job with results or errors
    """
    
    def __init__(self, poll_interval: float | None = None):
        """
        Initialize the worker
        
        Args:
            poll_interval: Time in seconds between polling for new jobs
        """
        self.poll_interval = poll_interval if poll_interval is not None else settings.WORKER_POLL_INTERVAL
        self.provider = get_image_provider(delay_seconds=settings.IMAGE_PROVIDER_DELAY)
        self._running = False
        self._thread = None
    
    def start(self):
        """Start the worker in a background thread"""
        if self._running:
            logger.warning("Worker is already running")
            return
        
        self._running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        logger.info("Image generation worker started")
    
    def stop(self):
        """Stop the worker"""
        self._running = False
        if self._thread:
            self._thread.join()
        logger.info("Image generation worker stopped")
    
    def _run(self):
        """Main worker loop - runs in background thread"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        while self._running:
            try:
                # Get pending jobs from database
                pending_jobs = db.get_pending_jobs()
                
                if pending_jobs:
                    logger.info(f"Found {len(pending_jobs)} pending jobs")
                
                # Process each pending job
                for job in pending_jobs:
                    loop.run_until_complete(self._process_job(job.id))
                
                # Sleep before next poll
                asyncio.run(asyncio.sleep(self.poll_interval))
                
            except Exception as e:
                logger.error(f"Error in worker loop: {e}", exc_info=True)
                asyncio.run(asyncio.sleep(self.poll_interval))
    
    async def _process_job(self, job_id: str):
        """
        Process a single job
        
        Args:
            job_id: The ID of the job to process
        """
        try:
            # Mark job as processing
            job = db.update_job(job_id, status=JobStatus.PROCESSING)
            if not job:
                logger.error(f"Job {job_id} not found")
                return
            
            logger.info(f"Processing job {job_id} - generating {job.numImages} images")
            
            # Select random animal
            animal = random.choice(ANIMALS)
            prompt = f"a cute {animal}"
            
            logger.info(f"Job {job_id} - selected animal: {animal}")
            
            # Generate images using the provider
            image_urls = await self.provider.generate_images(prompt, job.numImages)
            
            # Update job with results
            db.update_job(
                job_id,
                status=JobStatus.COMPLETED,
                animal=animal,
                imageUrls=image_urls
            )
            
            logger.info(f"Job {job_id} completed successfully with {len(image_urls)} images")
            
        except Exception as e:
            # Update job with error
            error_msg = str(e)
            logger.error(f"Job {job_id} failed: {error_msg}", exc_info=True)
            db.update_job(
                job_id,
                status=JobStatus.FAILED,
                error=error_msg
            )


# Global worker instance
worker = ImageGenerationWorker()
