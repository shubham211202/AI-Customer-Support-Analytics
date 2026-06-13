FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Install curl for health checking
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy pyproject.toml first to cache dependency installation
COPY pyproject.toml /app/

# Copy the rest of the application files needed for pip install
COPY app /app/app
COPY alembic /app/alembic
COPY alembic.ini /app/alembic.ini

# Install the app dependencies and the app package itself
RUN pip install --upgrade pip && \
    pip install .

EXPOSE 8000

# Default command to run FastAPI app. We will override this in docker-compose
# to run migrations on container startup.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
