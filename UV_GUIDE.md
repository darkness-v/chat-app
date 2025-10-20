# Quick Start with UV

## Prerequisites

- Node.js 18+ installed
- uv installed (will auto-install if not present)
- OpenAI API key

## One-Time Setup

```bash
# Clone or navigate to the project
cd chat-app

# Run setup script (installs all dependencies)
chmod +x setup.sh
./setup.sh
```

The setup script will:
1. Check for `uv` and install it if needed
2. Create Python virtual environments for both services
3. Install Python dependencies with `uv pip install`
4. Install Node.js dependencies
5. Create environment files

## Running the Application

### Option 1: Three Terminals (Recommended for Development)

**Terminal 1 - Storage Service:**
```bash
cd storage-service
uv run uvicorn main:app --host 0.0.0.0 --port 8002
```

**Terminal 2 - Chat Service:**
```bash
cd chat-service
uv run uvicorn main:app --host 0.0.0.0 --port 8001
```

**Terminal 3 - Frontend:**
```bash
cd frontend
npm run dev
```

### Option 2: Docker Compose (Production-like)

```bash
docker-compose up
```

## Using UV Commands

### Install dependencies
```bash
cd storage-service
uv pip install -r requirements.txt

cd ../chat-service
uv pip install -r requirements.txt
```

### Run a Python script
```bash
cd storage-service
uv run python main.py
```

### Run uvicorn directly
```bash
cd storage-service
uv run uvicorn main:app --reload --port 8002
```

### Activate virtual environment manually
```bash
cd storage-service
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate  # On Windows
```

## Why UV?

- **Fast**: 10-100x faster than pip
- **Reliable**: Consistent dependency resolution
- **Simple**: No need to manage virtualenvs manually
- **Modern**: Built in Rust for performance
- **Compatible**: Works with existing pip requirements.txt

## Project Structure with UV

```
chat-app/
├── storage-service/
│   ├── .venv/              # Virtual environment (auto-created)
│   ├── pyproject.toml      # Project metadata
│   ├── requirements.txt    # Dependencies
│   └── main.py            # Application code
│
├── chat-service/
│   ├── .venv/              # Virtual environment (auto-created)
│   ├── pyproject.toml      # Project metadata
│   ├── requirements.txt    # Dependencies
│   └── main.py            # Application code
│
└── frontend/
    ├── node_modules/       # NPM dependencies
    ├── package.json        # NPM metadata
    └── ...
```

## Troubleshooting

### UV not found
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add to PATH
export PATH="$HOME/.cargo/bin:$PATH"
```

### Port already in use
```bash
# Find and kill process on port 8002
lsof -ti:8002 | xargs kill -9

# Or use different ports
uv run uvicorn main:app --port 8003
```

### Dependencies not installing
```bash
# Clear cache and reinstall
rm -rf .venv
uv venv
uv pip install -r requirements.txt
```

## Development Workflow

1. Make changes to code
2. Services auto-reload (with --reload flag)
3. Test in browser
4. Commit changes

## Production Deployment

For production, use Docker:

```bash
docker-compose up -d
```

Or build individual images:

```bash
cd storage-service
docker build -t storage-service .
docker run -p 8002:8002 storage-service
```

Happy coding! 🚀
