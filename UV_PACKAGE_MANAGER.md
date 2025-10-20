# UV Package Manager - Complete Guide

## What is UV?

[UV](https://github.com/astral-sh/uv) is an extremely fast Python package installer and resolver, written in Rust. It's designed to be a drop-in replacement for pip and pip-tools.

### Key Benefits

- ⚡ **10-100x faster** than pip
- 🔒 **Reliable**: Deterministic dependency resolution  
- 🎯 **Simple**: Drop-in replacement for pip/venv
- 💾 **Efficient**: Global package cache
- 🔄 **Compatible**: Works with existing requirements.txt and pyproject.toml

## Installation

```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with Homebrew
brew install uv

# Or with pip
pip install uv
```

## Basic Usage

### Virtual Environments

```bash
# Create a virtual environment
uv venv

# Create with specific Python version
uv venv --python 3.11

# Activate (same as standard venv)
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

### Package Installation

```bash
# Install from requirements.txt
uv pip install -r requirements.txt

# Install from pyproject.toml
uv pip install -e .

# Install a single package
uv pip install fastapi

# Install with specific version
uv pip install "fastapi>=0.115.0"

# Install dev dependencies
uv pip install -e ".[dev]"
```

### Running Commands

```bash
# Run Python with UV (automatically uses venv)
uv run python script.py

# Run uvicorn server
uv run uvicorn main:app --port 8001

# Run any command in the venv
uv run pytest
```

## Project Setup

### Using pyproject.toml (Recommended)

Create a `pyproject.toml`:

```toml
[project]
name = "my-project"
version = "1.0.0"
description = "My awesome project"
requires-python = ">=3.10"
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.30.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

Install:
```bash
uv pip install -e .
```

### Using requirements.txt

```bash
# Generate from current environment
uv pip freeze > requirements.txt

# Install from requirements.txt
uv pip install -r requirements.txt
```

## This Project's Setup

### Storage Service

```bash
cd storage-service
uv venv                    # Create virtual environment
uv pip install -e .        # Install from pyproject.toml
uv run uvicorn main:app --port 8002  # Run service
```

### Chat Service

```bash
cd chat-service
uv venv                    # Create virtual environment
uv pip install -e .        # Install from pyproject.toml
uv run uvicorn main:app --port 8001  # Run service
```

## Common Commands

```bash
# List installed packages
uv pip list

# Show package info
uv pip show fastapi

# Uninstall package
uv pip uninstall fastapi

# Update UV itself
uv self update

# Check for outdated packages
uv pip list --outdated

# Sync environment to match requirements
uv pip sync requirements.txt
```

## Advanced Features

### Lock Files

```bash
# Generate a lock file
uv pip compile pyproject.toml -o requirements.lock

# Install from lock file
uv pip sync requirements.lock
```

### Global Package Cache

UV uses a global cache to avoid re-downloading packages:

```bash
# View cache location
uv cache dir

# Clean cache
uv cache clean
```

### Multiple Python Versions

```bash
# Create venv with specific Python
uv venv --python 3.11

# UV can download Python versions automatically
uv python install 3.11
uv venv --python 3.11
```

## Comparison with pip

| Feature | pip | UV |
|---------|-----|-----|
| Install speed | Baseline | 10-100x faster |
| Resolver | Yes | Much faster |
| Caching | Basic | Global, efficient |
| Parallel downloads | No | Yes |
| Lock files | pip-tools | Built-in |
| Python version management | No | Yes |

## Troubleshooting

### UV command not found
```bash
# Add to PATH (if installer didn't)
export PATH="$HOME/.cargo/bin:$PATH"

# Add to shell config (.zshrc, .bashrc)
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.zshrc
```

### Virtual environment issues
```bash
# Remove and recreate
rm -rf .venv
uv venv
uv pip install -e .
```

### Package conflicts
```bash
# UV's resolver is very good, but if issues persist:
uv pip install --upgrade-package problematic-package
```

## Migration from pip

### From requirements.txt

```bash
# No changes needed!
uv pip install -r requirements.txt
```

### From pip commands

Simply replace `pip` with `uv pip`:

```bash
# Before
pip install fastapi

# After
uv pip install fastapi
```

### From virtualenv

```bash
# Before
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# After
uv venv
uv pip install -r requirements.txt
uv run python script.py  # No need to activate!
```

## Best Practices

1. **Use pyproject.toml**: Modern Python standard
2. **Use `uv run`**: Avoid manual activation
3. **Global cache**: Let UV manage it, don't clear unless needed
4. **Lock files**: For production deployments
5. **Version pinning**: Use `>=` for development, exact versions for production

## This Project's Scripts

All automated scripts use UV:

```bash
# Setup with UV
./setup-uv.sh

# Start services (uses UV internally)
./start-services.sh

# Manual service start
cd storage-service
uv run uvicorn main:app --port 8002
```

## Resources

- [UV Documentation](https://github.com/astral-sh/uv)
- [UV vs pip performance](https://github.com/astral-sh/uv#performance)
- [Python Packaging Guide](https://packaging.python.org/)

## Summary

UV is a modern, fast Python package manager that's fully compatible with existing Python projects. It requires minimal changes to your workflow while providing significant speed improvements.

For this chat application:
- ✅ Faster setup and installation
- ✅ Reliable dependency resolution
- ✅ Simple workflow with `uv run`
- ✅ Compatible with existing tools
