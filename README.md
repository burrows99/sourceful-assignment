# Sourceful Assignment

Full-stack image generation application with FastAPI backend, Next.js frontend, and PostgreSQL database.

---

## Quick Start

```bash
# Copy environment file and add your OpenRouter API key
cp .env.example .env
# Edit .env and set OPENROUTER_API_KEY

# Start all services (migrations run automatically on backend start)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Startup Times & Expected Logs

**PostgreSQL** (~5 seconds):
```
✅ Ready: "database system is ready to accept connections"
```

**Backend** (~10-15 seconds):
```
✅ Ready: "✅ Database initialized"
✅ Ready: "✅ Database migrations applied"  
✅ Ready: "✅ Async image worker started"
✅ Ready: "Uvicorn running on http://0.0.0.0:8000"
```
⚠️ Note: You may see a migration warning about duplicate tables - this is normal if the database already exists.

**Frontend** (~20-30 seconds):
```
✅ Ready: "✓ Ready in 4.5s"
✅ Ready: "Local: http://localhost:3000"
```

**pgAdmin** (~30-40 seconds):
```
✅ Ready: "Booting worker with pid"
✅ Ready: "Added 0 Server Group(s) and 1 Server(s)"
```

### Access Services

| Service | URL | Credentials |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 | - |
| **Backend API** | http://localhost:8000 | - |
| **API Docs** | http://localhost:8000/docs | - |
| **MinIO Console** | http://localhost:9001 | minioadmin:minioadmin |
| **MinIO API** | http://localhost:9000 | - |
| **pgAdmin** | http://localhost:5050 | admin@admin.com:admin |

**Note**: Images are automatically uploaded to MinIO S3 storage and returned as public HTTP URLs instead of base64 data URLs.

---

## API Endpoints

### Image Generation

**POST /generations**

Generate images of random animals asynchronously using AI models. Images are automatically stored in MinIO S3 and returned as public HTTP URLs.

**Request:**
```json
{
  "numImages": 3
}
```

**Response:**
```json
{
  "jobId": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending"
}
```

**GET /generations/{jobId}**

Get job status and generated image URLs.

**Response:**
```json
{
  "jobId": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "numImages": 3,
  "animal": "cat",
  "imageUrls": [
    "http://localhost:9000/generated-images/jobs/550e8400/image1.png",
    "http://localhost:9000/generated-images/jobs/550e8400/image2.png",
    "http://localhost:9000/generated-images/jobs/550e8400/image3.png"
  ],
  "createdAt": "2025-12-12T10:30:00Z",
  "updatedAt": "2025-12-12T10:30:15Z"
}
```

### Image Classification

**POST /classify**

Classify animals in an image using AI vision models. The system supports multiple providers with easy switching via configuration.

**Request:**
```json
{
  "imgUrl": "https://example.com/animal-image.jpg"
}
```

**Response:**
```json
{
  "animals": ["cat", "dog"],
  "error": null
}
```

**Example with cURL:**
```bash
curl -X POST http://localhost:8000/classify \
  -H "Content-Type: application/json" \
  -d '{"imgUrl": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/1200px-Cat03.jpg"}'
```

### Supported Vision Providers

The classification endpoint uses an **extensible provider system** that allows easy switching between AI services:

| Provider | Configuration | API Key Required | Models Available |
|----------|--------------|------------------|------------------|
| **OpenRouter** | `VISION_PROVIDER=openrouter` | Yes ([Get key](https://openrouter.ai/keys)) | GPT-4o, GPT-4o-mini, Claude, Gemini, etc. |
| **Mock** | `VISION_PROVIDER=mock` | No | Pattern-based (for testing) |

**Switching Providers:**

Edit `.env` and set `VISION_PROVIDER`:
```bash
# Use OpenRouter (default, multiple models available)
VISION_PROVIDER=openrouter
VISION_MODEL=openai/gpt-4o-mini
OPENROUTER_API_KEY=sk-or-v1-your-key

# Use mock for testing (no API key needed)
VISION_PROVIDER=mock
```

Then restart: `docker-compose restart backend`

---

## Image Storage (MinIO S3)

The system uses **MinIO** - an S3-compatible object storage service - to convert base64-encoded images from AI providers into publicly accessible HTTP URLs.

### How It Works

1. **Image Generation**: OpenRouter's Riverflow model generates images as base64 data URLs
2. **Automatic Upload**: Background worker uploads images to MinIO S3 storage
3. **Public URLs**: Images are accessible via HTTP URLs (e.g., `http://localhost:9000/generated-images/...`)
4. **Organized Storage**: Images stored in folders by job ID for easy management

### MinIO Configuration

**Environment Variables** (`.env`):
```bash
# Storage backend: "minio" or "none" (keeps base64)
STORAGE_BACKEND=minio

# MinIO S3 settings
MINIO_ENDPOINT=minio:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET=generated-images
MINIO_PUBLIC_URL=http://localhost:9000
```

### MinIO Console

Access the MinIO web console at http://localhost:9001

**Login**: `minioadmin` / `minioadmin`

**Features**:
- Browse uploaded images by job ID
- View storage usage and metrics
- Manage buckets and access policies
- Download or delete images
- Monitor upload activity

### Storage Structure

```
generated-images/
├── jobs/
│   ├── 550e8400-e29b-41d4-a716-446655440000/
│   │   ├── abc123.png
│   │   ├── def456.png
│   │   └── ghi789.png
│   └── 661f9511-f3ac-52e5-b827-557766551111/
│       └── jkl012.png
└── test/
    └── validation-images.png
```

### Disable S3 Storage (Keep Base64)

To return base64 data URLs instead of HTTP URLs:

```bash
# In .env
STORAGE_BACKEND=none
```

Then restart: `docker-compose restart backend`

---

## Database Visualization (pgAdmin)

1. Open http://localhost:5050
2. Login: `admin@admin.com` / `admin`
3. Expand **"Servers"** → Click **"Sourceful PostgreSQL"**
4. Enter server password: `postgres` (check "Save Password")
5. Navigate to: **Databases → postgres → Schemas → public → Tables → jobs**

---

## Testing

**Coverage**: 77 tests, 87% overall

**Test Files:** (organized by type)
- **Unit Tests:**
  - `test_routes_unit.py` - API endpoint tests
  - `test_services_unit.py` - Business logic tests
  - `test_repository_unit.py` - Database operation tests
  - `test_classify_unit.py` - Vision classification unit tests (22 tests)

- **Integration Tests:**
  - `test_worker_integration.py` - Async worker tests
  - `test_integration_e2e.py` - End-to-end workflow tests
  - `test_classify_integration.py` - Classification integration tests (7 tests)

**Test Coverage by Component:**
- **Routes (87%)** - API endpoints (create job, get job, list jobs, classify)
- **Services (100%)** - Business logic (job creation, status updates)
- **Repositories (100%)** - Database operations (CRUD, queries)
- **Workers (82%)** - Async job processing (concurrent execution)
- **Providers (69%)** - Unified provider system (OpenRouter, Mock)
- **Integration (100%)** - End-to-end workflows

**Key Aspects Tested:**
- ✅ Unified provider architecture (text-to-image + image-to-text)
- ✅ OpenRouter integration with Riverflow model
- ✅ Vision classification with multiple providers
- ✅ Provider factory pattern and easy switching
- ✅ Mock provider for testing without API costs
- ✅ Base64 to S3 URL conversion with MinIO
- ✅ URL validation and error handling
- ✅ Concurrent job processing with `asyncio.gather()`
- ✅ Async worker without threading conflicts
- ✅ Database session management with connection pooling
- ✅ Error handling and rollback mechanisms
- ✅ Job status transitions (pending → processing → completed/failed)

```bash
# Run all tests
docker exec sourceful-backend pytest

# Run with coverage report
docker exec sourceful-backend pytest --cov=. --cov-report=html
open backend/htmlcov/index.html

# Run specific test types
docker exec sourceful-backend pytest -m unit
docker exec sourceful-backend pytest -m integration

# Run specific test files
docker exec sourceful-backend pytest tests/test_classify_unit.py
docker exec sourceful-backend pytest tests/test_classify_integration.py
```

---

## UI Improvements Implemented

### Mobile Dialog - Selected State Indicator
The mobile category selection dialog displays the currently selected category with visual highlighting, allowing users to see their active selection while browsing all available options. This improves user awareness and provides clear context when choosing a new category.

### Responsive Dialog Visibility Fix
Fixed an issue where the mobile dialog would remain visible when resizing from mobile to desktop view. The dialog now properly hides when switching to desktop breakpoint, ensuring clean transitions between mobile and desktop interfaces.

### Carousel Navigation Button Visibility
Implemented proper scroll navigation button visibility logic. The left navigation button now disappears when at the leftmost position, and the right navigation button disappears when at the rightmost position. This provides intuitive visual feedback about scroll boundaries and prevents unnecessary interaction with disabled navigation controls.

### Product Mockups Button Glitch Fix
Fixed an unintentional layout glitch where clicking the "Product mockups" button caused the entire page to shift horizontally from left to right. This behavior was unique to this button and not present in other category buttons. The implementation now ensures consistent behavior across all category selections without any unwanted page movement.

### Consistent Prompt Box Height
Implemented minimum height constraint for the prompt box to ensure consistent sizing across all categories. Whether displaying a textarea input or info message badge, the prompt box now maintains a fixed height of 168px, preventing visual jumps when switching between different category types.

![Carousel Navigation](./frontend/public/images/improvements/carousel-navigation.png)

---

## Architecture Highlights

### Unified Provider System

All AI providers extend from a single `BaseProvider` class supporting both capabilities:
- **Text-to-Image**: Generate images from text prompts
- **Image-to-Text**: Classify/analyze images

```python
# Single provider instance for both tasks
provider = get_provider("openrouter", 
    api_key="...",
    image_model="sourceful/riverflow-v2-max-preview",
    vision_model="openai/gpt-4o-mini"
)

# Generate images
images = await provider.generate_images("a cute cat", 3)

# Classify images
result = await provider.classify_image(images[0])
```

**Benefits**:
- Single configuration for all AI tasks
- Easy to add new providers
- Consistent error handling
- Simplified testing

### Storage Service Architecture

**Abstraction Layer**: Worker doesn't need to know about storage implementation

```python
# Worker simply generates images
image_urls = await provider.generate_images(prompt, num_images)

# Storage service handles conversion automatically
if settings.STORAGE_BACKEND == "minio":
    image_urls = storage_service.upload_multiple_base64_images(image_urls)
```

**Flexibility**: Switch between base64 and S3 URLs with a config change

### Async Background Processing

- **AsyncIO-based**: No threading, pure async/await
- **Database Pooling**: Efficient connection management
- **Error Recovery**: Jobs marked as failed with error messages
- **Concurrent Processing**: Multiple jobs processed in parallel

---

## Troubleshooting

```bash
# View container logs
docker logs sourceful-backend -f
docker logs sourceful-frontend -f
docker logs sourceful-minio -f

# Rebuild containers
docker-compose build --no-cache
docker-compose up -d

# Check container status
docker ps

# Reset MinIO storage
docker-compose down -v
docker-compose up -d
```

### Common Issues

**Images not uploading to MinIO**:
```bash
# Check MinIO is running
docker ps | grep minio

# Check MinIO logs
docker logs sourceful-minio

# Verify bucket exists
curl http://localhost:9000/minio/health/live
```

**Base64 URLs instead of HTTP URLs**:
- Check `STORAGE_BACKEND=minio` in `.env`
- Restart backend: `docker-compose restart backend`
