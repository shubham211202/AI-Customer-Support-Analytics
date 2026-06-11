# AI-Powered Customer Support Analytics Platform

Production-grade web application project for learning AI/ML, MLOps, Docker,
Kubernetes, Terraform, GitOps, monitoring, and cloud-native architecture.

## Roadmap

1. FastAPI + PostgreSQL + AI models
2. Docker + Docker Compose
3. MLflow + Airflow
4. Prometheus + Grafana + Loki
5. Kubernetes
6. ArgoCD GitOps
7. Terraform

This repository currently implements **Phase 1**.

## Phase 1 Architecture

```text
Future Web Frontend
        |
        v
FastAPI Backend
        |
        |-- API layer
        |-- Service layer
        |-- ML inference layer
        |-- Repository layer
        |
        v
PostgreSQL Database
```

## Repository Structure

```text
backend/   FastAPI backend and tests
frontend/  Placeholder for the future web UI
docs/      Architecture notes
```

## Local Setup

<<<<<<< HEAD
Requires Python 3.10 or newer.
=======
Requires Python 3.10 or newer. If VS Code is using Python 3.10.11, create the
virtual environment with that interpreter:
>>>>>>> 66babbfa (Support Python 3.10 development environment)

```powershell
cd backend
py -3.10 -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
copy ..\.env.example .env
alembic upgrade head
uvicorn app.main:app --reload
```

## Tests

```powershell
cd backend
pytest
```

## VS Code

Use this order:

```text
Terminal > Run Task > Backend: install dependencies
Terminal > Run Task > Backend: migrate local SQLite
Run and Debug > Backend: FastAPI localhost
```

## API Docs

```text
http://127.0.0.1:8000/docs
```

Tests use SQLite in memory for fast feedback. Local development and production use PostgreSQL through `DATABASE_URL`.