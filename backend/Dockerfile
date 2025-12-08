FROM python:3.13-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose ports
EXPOSE 8000
EXPOSE 5678

# Run the application in development mode with hot reload
CMD ["fastapi", "dev", "main.py", "--host", "0.0.0.0", "--port", "8000"]
