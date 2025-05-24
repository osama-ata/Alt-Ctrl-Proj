Use Uv for package management and building.
Use Ruff for linting and formatting.
Use type hints, annotation and type checking.
All the dependsencies should be in the pyproject.toml file.

Install dependencies with:

```bash

# Install uv
pip install uv

# Create venv
uv venv

# Install build tool
uv pip install build

# Build package
.venv/bin/python -m build

# Test dependencies
uv pip install .[test]

# Run tests
.venv/bin/python -m pytest

# Docs dependencies
uv pip install .[docs]

```
