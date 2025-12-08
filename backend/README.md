# Image Generation API - Backend

Production-grade FastAPI application with async job processing, PostgreSQL database, and containerized deployment.

## 🏗️ Architecture

**Layered Architecture** with proper separation of concerns:
- `routes.py` - API endpoints (presentation layer)
- `services.py` - Business logic (service layer)  
- `repositories/` - Data access (persistence layer)
- `workers/` - Background job processing

**Key Production Patterns:**
- Repository Pattern for data access
- Dependency Injection via FastAPI Depends
- Session Management with connection pooling
- Async Worker in main event loop (no threading)

## 📁 Project Structure

```
backend/
├── main.py                     # Application factory & lifespan
├── config.py                   # Settings with environment variables
├── models.py                   # Pydantic domain models
├── db_models.py                # SQLAlchemy ORM models
├── routes.py                   # API endpoints
├── services.py                 # Business logic layer
├── providers.py                # Image generation provider interface
├── core/
│   └── database.py             # Session manager & DI
├── repositories/
│   └── job_repository.py       # Database operations
└── workers/
    └── async_worker.py         # Async job processor
```

See `PRODUCTION_ARCHITECTURE.md` for detailed architecture documentation.

## 🚀 Quick Start

### Docker (Recommended)

```bash
# Start all services
docker-compose up -d

# View logs
docker logs sourceful-backend -f

# Stop services
docker-compose down
```

**Services:**
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- PostgreSQL: localhost:5432 (postgres:postgres)
- pgAdmin: http://localhost:5050
  - Login: `admin@admin.com` / `admin`
  - Server auto-configured: "Sourceful PostgreSQL"
  - DB Password when prompted: `postgres`

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set database URL (uses default postgres credentials)
export DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"

# Run migrations
alembic upgrade head

# Start server
fastapi dev main.py
```

### Accessing pgAdmin

1. Navigate to http://localhost:5050
2. Login with: `admin@admin.com` / `admin`
3. In left sidebar, expand **"Servers"**
4. Click **"Sourceful PostgreSQL"** 
5. When prompted for password, enter: `postgres`
6. Check "Save Password" to avoid future prompts
7. Browse to **Databases → postgres → Schemas → public → Tables → jobs**

## 🔌 API Endpoints

### Create Job
```bash
POST /generations
Content-Type: application/json

{
  "numImages": 3
}

# Response (202 Accepted):
{
  "jobId": "uuid",
  "status": "pending"
}
```

### Get Job Status
```bash
GET /generations/{jobId}

# Response (200 OK):
{
  "jobId": "uuid",
  "status": "completed",
  "numImages": 3,
  "animal": "bear",
  "imageUrls": ["url1", "url2", "url3"],
  "createdAt": "2025-12-08T02:14:39+00:00",
  "updatedAt": "2025-12-08T02:14:42+00:00"
}
```

### List All Jobs
```bash
GET /generations

# Response: Array of job objects
```

## 💾 Database

- **PostgreSQL** with asyncpg driver
- **SQLAlchemy** async ORM
- **Alembic** migrations

```bash
# Create migration
alembic revision -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## 🔧 Configuration

Environment variables (create `.env` file):

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@postgres:5432/postgres
WORKER_POLL_INTERVAL=1.0
IMAGE_PROVIDER_DELAY=2.0
MAX_IMAGES_PER_JOB=10
```

## 🧪 Testing

```bash
# Create job
curl -X POST http://localhost:8000/generations \
  -H "Content-Type: application/json" \
  -d '{"numImages": 3}'

# Check status (wait ~3 seconds)
curl http://localhost:8000/generations/{jobId}

# List all jobs
curl http://localhost:8000/generations
```

## 📚 Documentation

- **Architecture Details**: See `PRODUCTION_ARCHITECTURE.md`
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🐛 Debugging

Remote debugging enabled on port 5678. Attach VS Code debugger using the provided launch configuration.
