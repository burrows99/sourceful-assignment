# Sourceful Assignment

Full-stack image generation application with FastAPI backend, Next.js frontend, and PostgreSQL database.

---

## Quick Start

```bash
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

## Database Visualization (pgAdmin)

1. Open http://localhost:5050
2. Login: `admin@admin.com` / `admin`
3. Expand **"Servers"** → Click **"Sourceful PostgreSQL"**
4. Enter server password: `postgres` (check "Save Password")
5. Navigate to: **Databases → postgres → Schemas → public → Tables → jobs**

---

## Testing

**Coverage**: 28 tests, 93% overall

**Test Coverage by Component:**
- **Routes (95%)** - API endpoints (create job, get job, list jobs)
- **Services (96%)** - Business logic (job creation, status updates)
- **Repositories (100%)** - Database operations (CRUD, queries)
- **Workers (82%)** - Async job processing (concurrent job execution, image generation)
- **Integration (100%)** - End-to-end workflows (job creation → parallel processing → completion)

**Key Aspects Tested:**
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
