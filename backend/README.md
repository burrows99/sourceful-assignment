# FastAPI Backend

A FastAPI-based image generation API with asynchronous job processing, following proper design patterns and separation of concerns.

## Architecture & Design Patterns

### 📁 Project Structure

```
backend/
├── main.py              # Application factory & setup
├── config.py            # Configuration management (Settings pattern)
├── routes.py            # API route handlers (Controller layer)
├── services.py          # Business logic (Service layer)
├── models.py            # Pydantic models (DTO pattern)
├── database.py          # Data access layer (Repository pattern)
├── providers.py         # Provider interface (Strategy pattern)
├── worker.py            # Background job processor
└── dependencies.py      # Dependency injection
```

### 🏗️ Design Patterns Used

1. **Application Factory Pattern** (`main.py`)
   - `create_application()` function for testable app creation
   - Centralized middleware and router registration

2. **Layered Architecture**
   - **Routes Layer**: HTTP request/response handling
   - **Service Layer**: Business logic and orchestration
   - **Data Layer**: Database operations

3. **Repository Pattern** (`database.py`)
   - Abstracted data access
   - Easy to swap implementations (in-memory → SQL)

4. **Strategy Pattern** (`providers.py`)
   - `ImageProvider` abstract interface
   - Pluggable image generation backends

5. **Settings Pattern** (`config.py`)
   - Environment-based configuration
   - Pydantic settings with validation
   - `.env` file support

6. **Dependency Injection** (`dependencies.py`)
   - FastAPI's `Depends()` ready
   - Testable and mockable dependencies

### Features

- **Async Job Processing**: Image generation jobs are processed in the background
- **Provider Pattern**: Easily swap between different image generation providers
- **Job Queue System**: Track job status and retrieve results
- **Configuration Management**: Environment-based settings
- **Proper Separation of Concerns**: Routes, services, and data access are cleanly separated
- **In-Memory Database**: Simple storage with clear migration path to SQL databases

## Setup

1. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment (optional):
```bash
cp .env.example .env
# Edit .env with your settings
```

## Run

Start the development server:
```bash
fastapi dev main.py
```

The server will run at `http://127.0.0.1:8000`

## Configuration

Edit `.env` file or set environment variables:

```env
APP_NAME="Image Generation API"
VERSION="1.0.0"
DEBUG=true
WORKER_POLL_INTERVAL=1.0
IMAGE_PROVIDER_DELAY=2.0
MAX_IMAGES_PER_JOB=10
```

## API Documentation

- Interactive docs (Swagger UI): `http://127.0.0.1:8000/docs`
- Alternative docs (ReDoc): `http://127.0.0.1:8000/redoc`

## Endpoints

### POST /generations
Create a new image generation job.

**Request:**
```json
{
  "numImages": 3
}
```

**Response (202 Accepted):**
```json
{
  "jobId": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending"
}
```

### GET /generations/{jobId}
Get the status and results of a specific job.

**Response:**
```json
{
  "jobId": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "numImages": 3,
  "animal": "cat",
  "imageUrls": [
    "https://example.com/image1.png",
    "https://example.com/image2.png",
    "https://example.com/image3.png"
  ],
  "createdAt": "2025-12-08T01:23:45.678Z",
  "updatedAt": "2025-12-08T01:23:48.123Z"
}
```

### GET /generations
List all generation jobs.

**Response:**
```json
{
  "jobs": [
    {
      "jobId": "...",
      "status": "completed",
      "numImages": 3,
      "animal": "cat",
      "imageUrls": ["..."],
      "createdAt": "...",
      "updatedAt": "..."
    }
  ]
}
```

## Job Statuses

- `pending`: Job created, waiting to be processed
- `processing`: Worker is generating images
- `completed`: Images generated successfully
- `failed`: Error occurred during generation

## Migration to Production Database

The current in-memory database can be easily replaced with SQLite or Postgres:

1. Install SQLAlchemy: `pip install sqlalchemy[asyncio]`
2. Create database models using SQLAlchemy ORM
3. Replace the `JobDatabase` class methods with SQL queries
4. Update the connection in `database.py`

Comments in `database.py` provide guidance on this migration.
