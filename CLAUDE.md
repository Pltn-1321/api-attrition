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

**`ci-cd.yml`** - Triggers on:
- **Branches**: `main`, `dev`
- **Paths**: `app.py`, `config.py`, `pages/**`, `utils/**`, `tests/**`, `.streamlit/**`, `main.py`, `api/**`, `database/**`, `requirements.txt`, `.github/workflows/ci-cd.yml`
- **Manual**: `workflow_dispatch` (can be triggered manually from GitHub Actions UI)

**Job `test`** (runs always):
- Linting (Ruff, Black)
- Unit + functional tests (13 tests total)
- Coverage reports to Codecov and artifact upload

**Job `deploy`** (runs only on push to `main`):
- Deploys to Hugging Face Spaces via git push
- Requires `HF_TOKEN` secret in GitHub
- Deployment URL: https://huggingface.co/spaces/Pedro1321/Api-Technova

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

## Production Architecture (Hugging Face Spaces)

### Docker Container Architecture

The application runs in a **single Docker container** with **two processes**:

```
┌─────────────────────────────────────────────────┐
│   Docker Container (Hugging Face Spaces)       │
│                                                 │
│  ┌──────────────────────────────────────────┐  │
│  │ Process 1: FastAPI (port 8000)          │  │
│  │ → Internal API, not exposed to Internet │  │
│  └──────────────────────────────────────────┘  │
│                    ↑                            │
│                    │ localhost:8000             │
│                    │ (internal communication)   │
│  ┌──────────────────────────────────────────┐  │
│  │ Process 2: Streamlit (port 7860)        │  │
│  │ → Public interface exposed to Internet  │  │
│  └──────────────────────────────────────────┘  │
│                                                 │
│  Port 7860 exposed → Internet                  │
└─────────────────────────────────────────────────┘
```

**Important**: `localhost:8000` is the **CORRECT** URL for production because both Streamlit and FastAPI run in the same container. Streamlit communicates with FastAPI via internal localhost networking.

### Startup Sequence and Retry Logic

The `streamlit_launcher.py` implements intelligent startup management:

1. **API Starts First**: FastAPI launches on port 8000
2. **Health Check with Retry**: Waits up to 30 seconds for API to become ready
   - Polls `/health` endpoint every 1 second
   - Shows progress messages every 5 seconds
   - Continues even if API doesn't respond (with warning)
3. **Streamlit Starts**: Once API is ready (or timeout), Streamlit launches on port 7860

```python
# streamlit_launcher.py uses wait_for_api() function
api_ready = wait_for_api(API_PORT, max_retries=30, retry_interval=1)
```

This prevents the common 503 error caused by Streamlit trying to connect before FastAPI is ready.

## Troubleshooting Production Issues

### Error 503: Service Unavailable

**Symptom**: Streamlit shows "503 Server Error: Service Unavailable for url: http://localhost:8000/..."

**Cause**: FastAPI hasn't finished starting when Streamlit tries to connect.

**Solution**: The app now includes automatic retry logic (up to 30 seconds). If you still see this error:

1. **Wait and Retry**: Click the "🔄 Réessayer la connexion" button in the UI
2. **Check Logs**: In HF Spaces, view the container logs to see if API started successfully
3. **Verify Configuration**: Ensure `ENV API_URL=http://localhost:8000` is in Dockerfile

**Prevention**: CI/CD now validates this configuration automatically.

### Error: API URL Configuration

**Symptom**: Application tries to connect to wrong URL or times out.

**Root Cause**: Incorrect `API_URL` environment variable.

**Correct Configuration**:
- **Local Development**: `http://localhost:8000` (default)
- **HF Spaces**: `http://localhost:8000` (both processes in same container)
- **Separate Deployments**: Use full URL (e.g., `https://api.example.com`)

**Verification**:
```bash
# Run configuration tests
pytest tests/unit/test_config.py -v

# Check Dockerfile
grep "ENV API_URL" Dockerfile
# Should output: ENV API_URL=http://localhost:8000
```

### Health Check Failures

The app.py now handles health check failures gracefully:
- Shows clear warning message
- Displays retry button
- Provides error details in expandable section
- Shows configured API_URL for debugging

## Configuration Validation in CI/CD

The pipeline now includes configuration validation steps:

```yaml
- name: Validate Configuration
  # Checks that Dockerfile has correct ENV variables

- name: Run Configuration Tests
  # Runs tests/unit/test_config.py

- name: Run API Availability Tests
  # Runs tests/functional/test_api_availability.py
```

This catches configuration errors before deployment, preventing 503 errors in production.

## Testing Strategy

### Configuration Tests (`tests/unit/test_config.py`)
- Validates `API_URL` default value
- Tests environment variable overrides
- Checks `DB_TYPE` configuration

### API Availability Tests (`tests/functional/test_api_availability.py`)
- Verifies `/health` endpoint exists and responds quickly
- Tests Streamlit→API connection
- Validates Dockerfile environment variables
- Ensures API responds after startup delay

### Coverage Configuration

Coverage is separated into two phases:
1. **Individual Test Runs**: Use `--no-cov` flag for speed
2. **Final Coverage Report**: Comprehensive coverage of core modules only

Excluded from coverage:
- Streamlit pages (`pages/*`)
- UI entry point (`app.py`)
- Database migration scripts
- Launcher script (`streamlit_launcher.py`)

Current coverage target: **60%** (core modules: `utils.api_client`, `api`, `database`, `main`)

## Debug Checklist

When troubleshooting production issues:

1. ✅ Check HF Spaces container logs
2. ✅ Verify `API_URL=http://localhost:8000` in environment
3. ✅ Confirm both processes are running (API + Streamlit)
4. ✅ Test `/health` endpoint accessibility
5. ✅ Review startup sequence timing (should be < 30s)
6. ✅ Click "Réessayer la connexion" if initial load fails

## Key Files for Production Configuration

- `Dockerfile` - Sets `ENV API_URL` and `ENV DB_TYPE`
- `config.py` - Reads `API_URL` from environment
- `streamlit_launcher.py` - Manages startup and retry logic
- `app.py` - Graceful error handling for health checks
- `.github/workflows/ci-cd.yml` - Validates configuration before deployment
