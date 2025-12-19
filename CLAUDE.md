# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Employee attrition prediction platform with FastAPI backend and Streamlit frontend. Supports dual database backends (PostgreSQL for local dev, SQLite for production deployment on Hugging Face Spaces).

## Architecture

### Two-Tier Application Structure

**Backend (API)**:
- `main.py` - FastAPI application entry point
- `api/schemas.py` - Pydantic models for API contracts
- `database/models.py` - SQLAlchemy ORM models
- `database/config.py` - Database connection management with dual backend support

**Frontend (Streamlit)**:
- `app.py` - Main entry point (home page)
- `pages/` - Multi-page app structure (Explorer, Recherche, Statistiques)
- `utils/api_client.py` - HTTP client for API communication
- `utils/ui_components.py` - Reusable Streamlit components
- `config.py` - Centralized frontend configuration (API_URL, colors, etc.)

### Database Configuration Pattern

The app dynamically switches between databases via `DB_TYPE` environment variable:

```python
# PostgreSQL (local development)
export DB_TYPE=postgres
docker-compose up -d

# SQLite (production/HF Spaces)
export DB_TYPE=sqlite  # or unset, default is sqlite
```

Database URLs are constructed in `database/config.py` based on this variable.

### API Client Pattern

Streamlit pages don't directly import database models. They use `utils/api_client.py` which makes HTTP requests to the FastAPI backend. This maintains separation of concerns and allows frontend/backend to scale independently.

## Development Commands

### Running the Application

```bash
# Full stack (recommended for development)
uv run streamlit_launcher.py
# Launches both API (port 8000) and Streamlit (port 8501)

# API only
uv run uvicorn main:app --reload --port 8000

# Streamlit only (requires API running)
uv run streamlit run app.py
```

### Database Setup

```bash
# PostgreSQL (Docker)
docker-compose up -d
uv run database/import_data.py

# SQLite (no Docker needed)
export DB_TYPE=sqlite
uv run database/migrate_to_sqlite.py
# Creates database.db with all data
```

### Testing

```bash
# All tests (13 tests total)
pytest tests/

# Unit tests only (8 tests - fast, mocked)
pytest tests/unit -v

# Functional tests only (5 tests - slower, integration)
pytest tests/functional -v

# With coverage
pytest tests/ --cov=utils --cov-report=term-missing

# Single test file
pytest tests/unit/test_api_client.py -v

# Single test
pytest tests/unit/test_api_client.py::TestAPIClient::test_health_check_success -v
```

### Code Quality

```bash
# Linting
ruff check .

# Formatting
black . --line-length=100

# Format check (CI mode)
black --check . --line-length=100
```

## CI/CD Pipeline

Single unified GitHub Actions workflow:

**`ci-cd.yml`** - Runs on pushes to `app.py`, `config.py`, `pages/**`, `utils/**`, `tests/**`

**Job `test`** (runs always):
- Linting (Ruff, Black)
- Unit + functional tests
- Coverage reports to Codecov

**Job `deploy`** (runs only on push to `main`):
- Deploys to Hugging Face Spaces via git push
- Requires `HF_TOKEN` secret in GitHub

## Key Implementation Patterns

### Environment-Based Configuration

```python
# In database/config.py
DB_TYPE = os.getenv("DB_TYPE", "sqlite")  # Defaults to sqlite
if DB_TYPE == "postgres":
    DATABASE_URL = f"postgresql://{user}:{password}@{host}/{db}"
else:
    DATABASE_URL = "sqlite:///./database.db"
```

### Streamlit Multi-Page App

Pages follow Streamlit's naming convention:
- `app.py` - Home page (no number prefix)
- `pages/1_📊_Explorer.py` - Auto-discovered, appears in sidebar
- `pages/2_🔍_Recherche.py`
- `pages/3_📈_Statistiques.py`

All pages import shared utilities from `utils/` and config from `config.py` (both at project root).

### API Client Singleton Pattern

The API client is initialized once in `app.py` session state:

```python
if "api_client" not in st.session_state:
    st.session_state.api_client = APIClient()
```

Pages access it via `st.session_state.api_client` to avoid re-instantiation.

## Deployment

### Local Development
- PostgreSQL via Docker Compose
- API on http://localhost:8000 (docs at /docs)
- Streamlit on http://localhost:8501

### Production (Hugging Face Spaces)
- SQLite database (database.db committed in repo)
- Single port (7860) running Streamlit
- API runs on localhost:8000 (internal)
- Deployed automatically on push to `main` after tests pass

## Project Dependencies

Managed via `uv` (pyproject.toml):
- FastAPI + Uvicorn (API)
- Streamlit + Plotly (Frontend)
- SQLAlchemy + psycopg2-binary (Database)
- Pandas + NumPy (Data)
- Pytest + pytest-cov (Testing)

Install: `uv sync` or use existing requirements.txt
