# Repository Guidelines

## Project Structure & Module Organization
- Source: `meraki_mcp/`
  - Entry: `meraki_mcp/main.py` (FastMCP server)
  - Services: `meraki_mcp/services/` (API wrappers, e.g., `MerakiClient`)
  - Tools: `meraki_mcp/tools/` (MCP tools registered with FastMCP)
  - Config/Models: `meraki_mcp/settings.py`, `meraki_mcp/schemas.py`
- Tests: top-level files like `test_meraki_api.py` (pytest). Prefer `tests/` folder with `test_*.py`.
- Ops: `Dockerfile`, `docker-compose.yml`, `.pre-commit-config.yaml`, `pyproject.toml`.

## Build, Test, and Development Commands
- Create venv and install (editable):
  - `python3.12 -m venv .venv && source .venv/bin/activate`
  - `pip install -U pip && pip install -e .`
- Run server locally (FastMCP):
  - `export MERAKI_API_KEY=...`
  - `fastmcp run meraki_mcp/main.py:mcp`
- Docker (build/run):
  - `docker-compose up -d` or `docker build -t meraki-mcp:latest .`
- Tests:
  - `pytest -q` (run all) or `pytest -q test_meraki_api.py`
- Lint/format/type-check:
  - `ruff check .` • `ruff format .` • `mypy .`
- Pre-commit (install hooks): `pre-commit install` then `pre-commit run -a`.

Tip: A `Makefile` is provided. Common targets:
- `make init` • `make test` • `make lint` • `make format` • `make type` • `make run` • `make test-integration`

## Coding Style & Naming Conventions
- Python 3.12, 4-space indent, max line length 88, double quotes by default (Ruff/Black-style).
- Use type hints; Pydantic for settings/models where applicable.
- Names: modules/functions `snake_case`, classes `CapWords`, constants `UPPER_SNAKE_CASE`.
- Keep tools cohesive under `meraki_mcp/tools/`; non-MCP helpers belong in `services/`.

## Testing Guidelines
- Framework: `pytest`. Place tests under `tests/` mirroring package paths; name `test_*.py`.
- Integration tests: marked `@pytest.mark.integration` and skipped by default via `pytest.ini`. Run explicitly with: `MERAKI_API_KEY=... pytest -m integration -q`.
- Unit tests: mock Meraki SDK for deterministic behavior; avoid live network.
- Aim for meaningful coverage on tool registration and service logic.

## Commit & Pull Request Guidelines
- Conventional Commits observed: `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`.
- Commits: small, focused, imperative mood (e.g., `feat: add XDR tools`).
- PRs: clear description, motivation, before/after if applicable; link issues; note env or README changes; include test updates. CI must pass (ruff, mypy, pytest unit).

## Security & Configuration Tips
- Secrets via env vars; never commit keys. Primary var: `MERAKI_API_KEY` (supported via `.env`).
- Prefer read-only interactions by default; be explicit with mutating operations.
- Avoid logging sensitive fields; see `REDACT_KEYS` in `settings.py`.
