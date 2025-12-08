# Production Architecture Documentation

## 🎯 Overview

This backend implements a production-grade FastAPI application with:
- **Async job processing** using asyncio (not threading)
- **PostgreSQL** with SQLAlchemy async ORM
- **Repository pattern** for clean data access
- **Dependency injection** for testability
- **Proper session management** with connection pooling

## 🏗️ Architecture Layers

```
┌─────────────────────────────────────────┐
│         routes.py (API Layer)           │  ← HTTP endpoints
├─────────────────────────────────────────┤
│       services.py (Business Logic)      │  ← Domain logic
├─────────────────────────────────────────┤
│  repositories/ (Data Access Layer)      │  ← Database ops
├─────────────────────────────────────────┤
│    core/database.py (Session Manager)   │  ← Connection pool
├─────────────────────────────────────────┤
│      db_models.py (ORM Models)          │  ← SQLAlchemy
└─────────────────────────────────────────┘

       workers/async_worker.py             │  ← Background jobs
```

## 📂 File Structure

```
backend/
├── main.py                      # App factory + lifespan
├── config.py                    # Environment settings
├── models.py                    # Pydantic DTOs
├── db_models.py                 # SQLAlchemy models
├── routes.py                    # API endpoints
├── services.py                  # Business logic
├── providers.py                 # Image provider interface
│
├── core/
│   ├── __init__.py
│   └── database.py              # ✨ Session manager + DI
│
├── repositories/
│   ├── __init__.py
│   └── job_repository.py        # ✨ Data access layer
│
└── workers/
    ├── __init__.py
    ├── async_worker.py          # ✨ Production worker
    └── image_worker.py          # ❌ Deprecated (threading)
```

## 🔑 Key Production Patterns

### 1. Session Management (`core/database.py`)

**Problem**: Sharing database connections across event loops causes errors.

**Solution**: Singleton session manager with context manager.

```python
class DatabaseSessionManager:
    def __init__(self, database_url: str):
        self.engine = create_async_engine(
            database_url,
            pool_size=20,
            pool_pre_ping=True,
            pool_recycle=3600
        )
        self._session_factory = async_sessionmaker(...)
    
    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self._session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

# Global singleton
sessionmanager = DatabaseSessionManager(settings.DATABASE_URL)
```

### 2. Dependency Injection

**Problem**: Routes shouldn't create their own database sessions.

**Solution**: FastAPI Depends with async generator.

```python
# In core/database.py
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with sessionmanager.session() as session:
        yield session

# In routes.py
@router.post("/generations")
async def create_generation(
    request: GenerationRequest,
    db: AsyncSession = Depends(get_db)  # ✨ Injected
):
    service = GenerationService(db)
    return await service.create_job(request.numImages)
```

### 3. Repository Pattern

**Problem**: Database logic scattered across services.

**Solution**: Dedicated repository per entity.

```python
class JobRepository:
    def __init__(self, session: AsyncSession):
        self.session = session  # Injected session
    
    async def create(self, job: Job) -> Job:
        db_job = JobModel(...)
        self.session.add(db_job)
        await self.session.flush()
        return self._to_domain_model(db_job)
    
    async def get_by_id(self, job_id: str) -> Optional[Job]:
        result = await self.session.execute(
            select(JobModel).where(JobModel.id == job_id)
        )
        return self._to_domain_model(result.scalar_one_or_none())
```

### 4. Async Worker (NO THREADING!)

**Problem**: Worker thread with own event loop can't share async connections.

**Solution**: Worker runs as asyncio task in main event loop.

```python
class AsyncImageWorker:
    def start(self):
        self._running = True
        # ✨ Create task in main event loop (not thread!)
        self._task = asyncio.create_task(self._run())
    
    async def _run(self):
        while self._running:
            await self._process_pending_jobs()
            await asyncio.sleep(self.poll_interval)
    
    async def _process_pending_jobs(self):
        # ✨ Each call gets fresh session
        async with sessionmanager.session() as session:
            repository = JobRepository(session)
            jobs = await repository.get_pending_jobs()
            
            # Process concurrently
            await asyncio.gather(*[
                self._process_job(job.id) for job in jobs
            ])
```

## 🚀 Request Flow

### Creating a Job

```
1. Client → POST /generations {"numImages": 3}
                ↓
2. routes.py → Depends(get_db) injects session
                ↓
3. GenerationService(session) → creates service with session
                ↓
4. JobRepository(session) → creates job in DB
                ↓
5. Worker polls → finds pending job
                ↓
6. Worker processes → updates job to "completed"
                ↓
7. Client → GET /generations/{id} → returns results
```

## 🔧 Configuration

### Environment Variables

```env
# Database (use 'postgres' for container name)
DATABASE_URL=postgresql+asyncpg://sourceful:sourceful123@postgres:5432/sourceful_db

# Worker
WORKER_POLL_INTERVAL=1.0
IMAGE_PROVIDER_DELAY=2.0

# API
MAX_IMAGES_PER_JOB=10

# Debug
ENABLE_DEBUG=true
DEBUG_PORT=5678
```

## 📊 Database Schema

```sql
CREATE TABLE jobs (
    id VARCHAR PRIMARY KEY,
    status VARCHAR NOT NULL,        -- indexed
    num_images INTEGER NOT NULL,
    animal VARCHAR,
    image_urls VARCHAR[],           -- PostgreSQL array
    error TEXT,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL
);

CREATE INDEX ix_jobs_status ON jobs(status);
```

## 🧪 Testing the API

```bash
# Create job
curl -X POST http://localhost:8000/generations \
  -H "Content-Type: application/json" \
  -d '{"numImages": 3}'

# Response: {"jobId": "...", "status": "pending"}

# Wait ~3 seconds for processing

# Check status
curl http://localhost:8000/generations/{jobId}

# Response: 
# {
#   "jobId": "...",
#   "status": "completed",
#   "animal": "bear",
#   "imageUrls": ["url1", "url2", "url3"],
#   ...
# }
```

## ⚠️ Common Pitfalls (Avoided)

### ❌ Threading with Async DB
```python
# DON'T: Worker in thread with own event loop
def _run_in_thread():
    loop = asyncio.new_event_loop()
    loop.run_until_complete(db_operation())  # ❌ Event loop conflict!
```

### ✅ Async Worker
```python
# DO: Worker as async task in main loop
async def _run():
    while running:
        await process_jobs()  # ✅ Same event loop
```

### ❌ Shared Sessions
```python
# DON'T: Create session once and reuse
session = sessionmanager._session_factory()
# Use everywhere ❌
```

### ✅ Context Managers
```python
# DO: New session per operation
async with sessionmanager.session() as session:
    # Use session ✅
# Automatically closed
```

## 🎓 Key Takeaways

1. **Use asyncio tasks, not threads** for async operations
2. **Create fresh sessions** for each operation
3. **Inject dependencies** via FastAPI Depends
4. **Separate concerns** with repositories
5. **Use connection pooling** at engine level
6. **Context managers** for automatic cleanup

## 📚 References

- FastAPI Async SQL: https://fastapi.tiangolo.com/tutorial/sql-databases/
- SQLAlchemy Async: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
- Repository Pattern: https://martinfowler.com/eaaCatalog/repository.html
