# Contributing to DeepuLang

Thanks for your interest!

## Quick Start
1. Fork & clone
2. Create virtualenv & install editable with dev deps:
   ```
   pip install -e .[dev]
   ```
3. Run tests:
   ```
   pytest
   ```

## Code Style
- Keep modules small and focused.
- Favor readability over cleverness.

## Tests
- Add tests for new grammar features or bug fixes.
- Keep test programs minimal.

## Releasing
1. Update `CHANGELOG.md`
2. Bump version in `pyproject.toml` and `deepulang/__init__.py`
3. Build & upload (example):
   ```
   python -m build
   twine check dist/*
   twine upload dist/*
   ```
