# FastAPI Backend

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

## Run

Start the development server:
```bash
fastapi dev main.py
```

The server will run at `http://127.0.0.1:8000`

## API Documentation

- Interactive docs (Swagger UI): `http://127.0.0.1:8000/docs`
- Alternative docs (ReDoc): `http://127.0.0.1:8000/redoc`

## Endpoints

- `GET /` - Root endpoint returning a hello world message
- `GET /health` - Health check endpoint
