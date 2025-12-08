# Test configuration and fixtures
import pytest
import asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import text
from httpx import AsyncClient, ASGITransport

from main import create_application
from core.database import DatabaseSessionManager, sessionmanager
from db_models import Base
from workers.async_worker import worker

# Use test database in the same PostgreSQL instance
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@postgres:5432/postgres_test"


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def test_db_engine():
    """Create a test database engine with isolated test database."""
    # Create engine connected to default postgres db to create test database
    admin_engine = create_async_engine(
        "postgresql+asyncpg://postgres:postgres@postgres:5432/postgres",
        isolation_level="AUTOCOMMIT",
    )
    
    # Drop and create test database
    async with admin_engine.connect() as conn:
        await conn.execute(text("DROP DATABASE IF EXISTS postgres_test"))
        await conn.execute(text("CREATE DATABASE postgres_test"))
    
    await admin_engine.dispose()
    
    # Create engine for test database
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        pool_pre_ping=True,
    )
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    # Cleanup
    await engine.dispose()
    
    # Drop test database
    admin_engine = create_async_engine(
        "postgresql+asyncpg://postgres:postgres@postgres:5432/postgres",
        isolation_level="AUTOCOMMIT",
    )
    async with admin_engine.connect() as conn:
        await conn.execute(text("DROP DATABASE IF EXISTS postgres_test"))
    await admin_engine.dispose()


@pytest.fixture(scope="function")
async def test_session(test_db_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session."""
    async_session = async_sessionmaker(
        bind=test_db_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    async with async_session() as session:
        yield session


@pytest.fixture(scope="function")
async def client(test_db_engine):
    """Create a test client with test database."""
    # Override the database session manager for tests
    original_engine = sessionmanager.engine
    original_factory = sessionmanager._session_factory
    
    sessionmanager.engine = test_db_engine
    sessionmanager._session_factory = async_sessionmaker(
        bind=test_db_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    app = create_application()
    
    # Don't start the worker during tests
    transport = ASGITransport(app=app)
    
    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as ac:
        yield ac
    
    # Restore original session manager
    sessionmanager.engine = original_engine
    sessionmanager._session_factory = original_factory


@pytest.fixture
def mock_image_urls():
    """Mock image URLs for testing."""
    return [
        "https://test.com/image1.png",
        "https://test.com/image2.png",
        "https://test.com/image3.png",
    ]


@pytest.fixture
def sample_job_data():
    """Sample job data for testing."""
    return {
        "numImages": 3
    }
