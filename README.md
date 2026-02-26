# Python + Playwright Setup

This repository is set up for browser end-to-end testing with **Playwright** and **pytest**.

## Prerequisites
- Python 3.10+

## Quick start
1. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

3. Install Playwright browser binaries:

```bash
playwright install
```

4. Run tests:

```bash
pytest
```

## Project structure
- `tests/` - pytest test files
- `requirements.txt` - Python dependencies
- `pyproject.toml` - pytest configuration

## Notes
- The `page` fixture comes from `pytest-playwright`.
- To run headed browser mode:

```bash
pytest --headed
```
