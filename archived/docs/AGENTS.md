# Repository Guidelines

## Project Structure & Module Organization
The repository splits into `backend/` and `web/`. The backend hosts the Flask email capture API (`server.py`), SMTP test scripts, deployment helpers, and `requirements.txt`. Vercel/Railway configs and startup scripts live alongside. The static frontend is served from `web/` with `index.html`, `script.js`, translation assets, and the chatbot configuration. Persisted leads land in `user_data/` (JSON + txt) at runtime; keep the directory out of version control. Deployment notes in `DEPLOY*.md` explain production targets.

## Build, Test, and Development Commands
```
python -m venv .venv && source .venv/bin/activate   # create env (use Scripts\\activate on Windows)
pip install -r backend/requirements.txt             # install backend deps
python backend/server.py                            # run Flask API on localhost:5000
(cd web && python -m http.server 8000)              # serve static frontend
python backend/test_email.py                        # interactive SMTP smoke test
```
Use `start.sh` or `start.bat` for combined backend launch during demos. Avoid editing the committed `venv/`; create a fresh virtualenv instead.

## Coding Style & Naming Conventions
Stick to PEP 8: 4-space indentation, snake_case for Python functions, UPPER_CASE for environment keys. The frontend favors camelCase for JS functions and kebab-case for CSS classes. Keep docstrings bilingual-friendly and reuse the emoji-forward tone where present. Run `python -m compileall backend` before committing large changes to catch syntax slips; format JS/CSS manually to match the current spacing.

## Testing Guidelines
There is no automated suite yet; add pytest-based tests under `backend/tests/` when contributing sizable logic. For now, verify SMTP paths with `python backend/test_email.py` or the quick `send_test.py`. When adding tests, name files `test_<feature>.py`, target >80% coverage for new modules, and document any external dependencies in the test docstring.

## Commit & Pull Request Guidelines
Follow the concise, present-tense style already in `git log` (e.g., “Actualizar URL del backend ...”). Scope each commit to a single topic, keep subjects under ~60 chars, and add an optional Spanish summary if context is subtle. Pull requests should link the related issue or brief rationale, list manual verification steps (frontend load, SMTP test), and attach screenshots or terminal output for UI-facing tweaks.
