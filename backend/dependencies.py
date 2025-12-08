# Application dependencies for dependency injection
from typing import Generator
from database import JobDatabase, db


def get_db() -> Generator[JobDatabase, None, None]:
    """
    Database dependency for dependency injection
    
    Usage in routes:
        @router.get("/example")
        async def example(db: JobDatabase = Depends(get_db)):
            # Use db here
            pass
    """
    try:
        yield db
    finally:
        pass  # Cleanup if needed
