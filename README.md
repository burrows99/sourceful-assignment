# sourceful-assignment

## Docker Setup

### Prerequisites
- Docker installed on your system
- Docker Compose installed

### Running with Docker Compose

1. **Build and start all services:**
```bash
docker-compose up --build
```

2. **Run in detached mode (background):**
```bash
docker-compose up -d
```

3. **Stop all services:**
```bash
docker-compose down
```

4. **View logs:**
```bash
docker-compose logs -f
```

### Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **PostgreSQL**: localhost:5432 (user: sourceful, password: sourceful123)
- **pgAdmin**: http://localhost:5050 (email: admin@sourceful.com, password: admin123)

### pgAdmin Setup

1. Open http://localhost:5050
2. Login with email: `admin@sourceful.com` and password: `admin123`
3. Add server:
   - Name: Sourceful DB
   - Host: postgres
   - Port: 5432
   - Database: sourceful_db
   - Username: sourceful
   - Password: sourceful123

### Database Migrations

The database is automatically initialized on startup. To manually run migrations:

```bash
docker-compose exec backend bash -c "cd /app && alembic upgrade head"
```

To create a new migration:

```bash
docker-compose exec backend bash -c "cd /app && alembic revision -m 'your migration message'"
```

### Development Mode
For development with hot reload, you can still run the services locally:
- Frontend: `cd frontend && npm run dev`
- Backend: `cd backend && venv/bin/python -m fastapi dev main.py`

## Improvements Implemented

### Mobile Dialog - Selected State Indicator
The mobile category selection dialog displays the currently selected category with visual highlighting, allowing users to see their active selection while browsing all available options. This improves user awareness and provides clear context when choosing a new category.

### Responsive Dialog Visibility Fix
Fixed an issue where the mobile dialog would remain visible when resizing from mobile to desktop view. The dialog now properly hides when switching to desktop breakpoint, ensuring clean transitions between mobile and desktop interfaces.

### Carousel Navigation Button Visibility
Implemented proper scroll navigation button visibility logic. The left navigation button now disappears when at the leftmost position, and the right navigation button disappears when at the rightmost position. This provides intuitive visual feedback about scroll boundaries and prevents unnecessary interaction with disabled navigation controls.

### Product Mockups Button Glitch Fix
Fixed an unintentional layout glitch where clicking the "Product mockups" button caused the entire page to shift horizontally from left to right. This behavior was unique to this button and not present in other category buttons. The implementation now ensures consistent behavior across all category selections without any unwanted page movement. This implementation does not include the background animations, which is likely the reason of the layout shift issue's fix.

### Consistent Prompt Box Height
Implemented minimum height constraint for the prompt box to ensure consistent sizing across all categories. Whether displaying a textarea input or info message badge, the prompt box now maintains a fixed height of 168px, preventing visual jumps when switching between different category types.

![Carousel Navigation](./public/images/improvements/carousel-navigation.png)
