# Backend

FastAPI backend for the AI-Powered Customer Support Analytics Platform.

## Commands

Requires Python 3.11 or newer. On this machine, use Python 3.13:

```powershell
py -3.13 -m venv .venv
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
