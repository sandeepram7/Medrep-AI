FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PORT=7860

# Set working directory
WORKDIR /code

# Copy dependencies first for caching layer
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy the rest of the backend and data
COPY backend/ ./backend/
COPY data/ ./data/

# Switch to backend directory
WORKDIR /code/backend

# Pre-build the ChromaDB local vector database during the Docker build
RUN python data_loader.py

# Expose Hugging Face Space's default port
EXPOSE 7860

# Run the Flask app with Gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:7860", "--workers", "1", "--timeout", "120"]