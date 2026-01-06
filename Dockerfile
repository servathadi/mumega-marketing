# Marketing Guild Runtime
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . .

ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1

# Start the Master Loop
CMD ["python", "src/main.py"]