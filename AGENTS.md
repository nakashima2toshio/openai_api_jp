# Repository Guidelines

## Project Structure & Module Organization
- Source demos live at the repo root: `a00_responses_api.py` (main), `a01`–`a06` feature demos, utilities like `a10_get_vsid.py`, `helper_api.py`, `helper_st.py`.
- Resources: `assets/` (screenshots), `images/` (samples), `data/` (sample data), `doc/` (docs), `config.yml` (settings).
- Tests: `tests/` (pytest; see `pytest.ini` for markers). Create it if missing.

## Build, Test, and Development Commands
- Environment: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`.
- Run demos (Streamlit): `streamlit run a00_responses_api.py` (use `--server.port=8501` as needed). Other demos can be run similarly (e.g., `a03_images_and_vision.py`).
- Quality checks: `black *.py`, `flake8 *.py --max-line-length=120`, `mypy *.py --ignore-missing-imports`.
- Tests: `pytest` (all), `pytest --cov=. --cov-report=html` (coverage), `pytest -m unit|integration|ui|functional|performance|slow|api` (markers).

## Coding Style & Naming Conventions
- Python 3.11+, 4-space indent, soft 120-char line length.
- Prefer type hints throughout; use Pydantic models where appropriate.
- Naming: modules/files `snake_case`; demo scripts follow `aNN_description.py`; classes `CamelCase`; functions/vars `snake_case`; constants `UPPER_SNAKE_CASE`.
- Avoid side effects at import time; put runnable code under `if __name__ == "__main__":`.

## Testing Guidelines
- Framework: pytest. Structure tests under `tests/` as `test_*.py`; classes `Test*`; functions `test_*`.
- Use markers from `pytest.ini` (e.g., `@pytest.mark.unit`, `@pytest.mark.integration`).
- Unit tests must not call external APIs; mock I/O (`responses`, `requests-mock`) and use sample files under `data/`.
- For real API checks, mark as `integration` and optionally `slow`; keep them opt-in.

## Commit & Pull Request Guidelines
- Commits: imperative, present tense (e.g., "Add vision demo"), scoped and logical. Include rationale when non-trivial.
- PRs must: describe what/why/how, link issues, list affected files, and include screenshots or console output for Streamlit/UI changes.
- Requirements: all checks pass (lint, type, tests), docs updated (`README.md`, `doc/`) when behavior or UX changes.

## Security & Configuration Tips
- Set secrets via environment variables: `OPENAI_API_KEY` (required); optional `OPENWEATHER_API_KEY`, `EXCHANGERATE_API_KEY`. Use a local `.env` if desired; do not commit it.
- Do not commit credentials, large binaries, or generated artifacts. Keep sample inputs small and under `data/`.
- Prefer `config.yml` for configuration with environment overrides; document defaults in PRs when adding new settings.

## Agent-Specific Instructions
- Preserve public demo entry points (`a00`–`a06`); don’t rename without updating README examples.
- When changing `helper_api.py` or `helper_st.py`, ensure all demos still run and adjust imports consistently.
