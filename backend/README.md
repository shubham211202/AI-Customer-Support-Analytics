# Backend

FastAPI backend for the AI-Powered Customer Support Analytics Platform.

## Commands

Requires Python 3.10 or newer. If VS Code is using Python 3.10.11, create the
virtual environment with that interpreter:

```powershell
py -3.10 -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
copy ..\.env.example .env
alembic upgrade head
uvicorn app.main:app --reload
```

Run tests:

```powershell
pytest
```
