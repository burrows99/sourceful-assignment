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
| **pgAdmin** | http://localhost:5050 | admin@admin.com:admin |

**Note**: Mock image generation takes ~5 seconds per image to simulate realistic API behavior. Generating 10 images will take approximately 50 seconds.

---

## API Endpoints

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
| **OpenAI** | `VISION_PROVIDER=openai` | Yes ([Get key](https://platform.openai.com/api-keys)) | GPT-4o, GPT-4o-mini |
| **Mock** | `VISION_PROVIDER=mock` | No | Pattern-based (for testing) |

**Switching Providers:**

Edit `.env` and set `VISION_PROVIDER`:
```bash
# Use OpenRouter (default, multiple models available)
VISION_PROVIDER=openrouter
VISION_MODEL=openai/gpt-4o-mini
OPENROUTER_API_KEY=sk-or-v1-your-key

# Use OpenAI directly
VISION_PROVIDER=openai
VISION_MODEL=gpt-4o-mini
OPENAI_API_KEY=sk-your-key

# Use mock for testing (no API key needed)
VISION_PROVIDER=mock
```

Then restart: `docker-compose restart backend`

**See [PROVIDER_ARCHITECTURE.md](PROVIDER_ARCHITECTURE.md) for:**
- Adding new providers (Anthropic, Google, etc.)
- Custom model configuration
- Fallback strategies
- Architecture details

---

## Database Visualization (pgAdmin)

1. Open http://localhost:5050
2. Login: `admin@admin.com` / `admin`
3. Expand **"Servers"** → Click **"Sourceful PostgreSQL"**
4. Enter server password: `postgres` (check "Save Password")
5. Navigate to: **Databases → postgres → Schemas → public → Tables → jobs**

---

## Testing

**Coverage**: 51 tests, 86% overall

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
- **Providers (69%)** - Vision provider system (OpenRouter, OpenAI, Mock)
- **Integration (100%)** - End-to-end workflows

**Key Aspects Tested:**
- ✅ Vision classification with multiple providers
- ✅ Provider factory pattern and switching
- ✅ Mock provider for testing without API costs
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

## Troubleshooting

```bash
# View container logs
docker logs sourceful-backend -f
docker logs sourceful-frontend -f

# Rebuild containers
docker-compose build --no-cache
docker-compose up -d

# Check container status
docker ps
```
