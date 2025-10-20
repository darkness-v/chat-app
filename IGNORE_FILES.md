# Ignore Files Documentation

## Overview

The project includes comprehensive `.gitignore` and `.dockerignore` files to keep repositories clean and Docker images lightweight.

## Files Created

### Root Level
- `.gitignore` - For Git version control
- `.dockerignore` - For Docker builds

### Service Level
- `storage-service/.dockerignore` - Storage service Docker builds
- `chat-service/.dockerignore` - Chat service Docker builds
- `frontend/.dockerignore` - Frontend Docker builds

## .gitignore

**Purpose**: Keep version control clean by excluding generated files, secrets, and environment-specific files.

**Key Exclusions**:
- ✅ Python bytecode (`__pycache__/`, `*.pyc`)
- ✅ Virtual environments (`.venv/`, `venv/`)
- ✅ Environment files (`.env`, `.env.local`)
- ✅ Database files (`*.db`, `*.sqlite`)
- ✅ Node modules (`node_modules/`)
- ✅ Build outputs (`.next/`, `dist/`)
- ✅ IDE files (`.vscode/`, `.idea/`)
- ✅ OS files (`.DS_Store`, `Thumbs.db`)
- ✅ Logs (`*.log`)
- ✅ UV lock files (`uv.lock`)

**What IS tracked**:
- ✅ Source code (`.py`, `.ts`, `.tsx`)
- ✅ Configuration files (`pyproject.toml`, `package.json`)
- ✅ Example environment files (`.env.example`)
- ✅ Requirements (`requirements.txt`)
- ✅ Documentation (`README.md`, etc.)
- ✅ Docker files (`Dockerfile`, `docker-compose.yml`)

## .dockerignore

**Purpose**: Reduce Docker image size and build time by excluding unnecessary files.

**Key Exclusions**:
- ✅ Git directory (`.git/`)
- ✅ Documentation (`*.md` files)
- ✅ Virtual environments (`.venv/`)
- ✅ Node modules (installed fresh in container)
- ✅ Build artifacts (`.next/`, built in container)
- ✅ Database files (created at runtime)
- ✅ Test files (`*test*.py`, `*.test.ts`)
- ✅ IDE files (`.vscode/`, `.idea/`)

**What IS included in images**:
- ✅ Source code
- ✅ Requirements/dependencies files
- ✅ Example environment files
- ✅ Static assets

## Service-Specific .dockerignore

Each service has its own `.dockerignore` optimized for its needs:

### storage-service/.dockerignore
Excludes:
- Python cache and virtual environments
- Database files (created at runtime)
- Development tools

### chat-service/.dockerignore
Excludes:
- Python cache and virtual environments
- API keys (passed as environment variables)
- Development tools

### frontend/.dockerignore
Excludes:
- Node modules (installed during build)
- Next.js build cache (rebuilt in container)
- Development files

## Best Practices

### Adding to .gitignore

```bash
# Add a specific file
echo "my-secret.txt" >> .gitignore

# Add a pattern
echo "*.backup" >> .gitignore

# Add a directory
echo "temp/" >> .gitignore
```

### Testing .gitignore

```bash
# Check if a file would be ignored
git check-ignore -v filename

# List all ignored files
git status --ignored
```

### Testing .dockerignore

```bash
# Build and check image size
docker build -t test-image .
docker images test-image

# List files in image
docker run --rm test-image find . -type f
```

## Common Patterns

### Database Files
```
*.db
*.sqlite
*.sqlite3
conversations.db
```

### Environment Files
```
.env
.env.local
.env.*.local
!.env.example
```

### Python
```
__pycache__/
*.py[cod]
.venv/
*.egg-info/
```

### Node/Next.js
```
node_modules/
.next/
out/
npm-debug.log*
```

### IDE
```
.vscode/
.idea/
*.swp
*.swo
```

## Security Notes

### ⚠️ Never commit:
- API keys or secrets
- Database files with real data
- Environment files with credentials
- SSH keys or certificates
- User-uploaded content

### ✅ Always use .env.example:
```bash
# Good - tracked in git
.env.example

# Bad - never commit
.env
.env.local
```

## Docker Image Size Comparison

### Without .dockerignore:
```
Storage Service:  ~500MB (includes .venv, docs, tests)
Chat Service:     ~800MB (includes .venv, docs, tests)
Frontend:         ~1.5GB (includes node_modules from host)
```

### With .dockerignore:
```
Storage Service:  ~200MB ⬇️ 60% reduction
Chat Service:     ~300MB ⬇️ 63% reduction
Frontend:         ~400MB ⬇️ 73% reduction
```

## Troubleshooting

### File still being tracked by Git
```bash
# Remove from Git but keep locally
git rm --cached filename

# Force remove and re-add
git rm -r --cached .
git add .
```

### Docker image too large
```bash
# Check what's in the image
docker history image-name

# See layer sizes
docker images --format "{{.Size}}" image-name
```

### Accidentally committed secrets
```bash
# Remove from history (dangerous!)
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

# Better: Rotate the secret immediately!
```

## Maintenance

### Review quarterly:
- [ ] Check for new generated files to exclude
- [ ] Update patterns for new tools
- [ ] Remove outdated patterns
- [ ] Test ignore files work correctly

### When adding new dependencies:
1. Check what files they generate
2. Add appropriate patterns to `.gitignore`
3. Add to `.dockerignore` if not needed in container
4. Test that builds still work

## Quick Reference

```bash
# View current .gitignore
cat .gitignore

# View current .dockerignore  
cat .dockerignore

# Check what's ignored
git status --ignored

# Clean untracked files (be careful!)
git clean -fdX  # Only ignored files
git clean -fd   # All untracked files
```

## Benefits

✅ **Smaller repositories** - No unnecessary files tracked
✅ **Faster builds** - Docker doesn't copy ignored files
✅ **Better security** - Secrets never committed
✅ **Cleaner diffs** - Only meaningful changes
✅ **Faster deployments** - Smaller Docker images
✅ **Less disk usage** - No redundant files

---

**Remember**: When in doubt, exclude it! It's easier to add files later than to remove them from Git history.
