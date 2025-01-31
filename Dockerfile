# Use Python as base image
FROM python:3.9

# Set working directory
WORKDIR /ai-agent-backend

# Copy project files
COPY . /ai-agent-backend/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]