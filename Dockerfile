# Marketing Guild Runtime
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Install dependencies
# In a real scenario, we'd install 'mumega-core' here
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . .

ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1

# Start the agent
CMD ["python", "src/agents/marketing_standup.py"]
