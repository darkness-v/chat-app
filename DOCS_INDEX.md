# 📚 Chat App Documentation Index

Welcome to the Chat Application with Image Support! This index will help you find the right documentation for your needs.

## 🚀 Getting Started

**New to the project? Start here:**
1. [README.md](./README.md) - Overview and main documentation
2. [QUICK_REFERENCE.md](./QUICK_REFERENCE.md) - Essential commands
3. Run `./setup-uv.sh` to set everything up

## 📖 Documentation Structure

### Essential Guides

| Document | Purpose | When to Use |
|----------|---------|-------------|
| [README.md](./README.md) | Complete project documentation | Understanding the full system |
| [QUICK_REFERENCE.md](./QUICK_REFERENCE.md) | Quick command reference | Need a command fast |
| [VISUAL_GUIDE.md](./VISUAL_GUIDE.md) | Visual architecture & flows | Understanding how it works |

### Feature Documentation

| Document | Purpose | When to Use |
|----------|---------|-------------|
| [IMAGE_CHAT_GUIDE.md](./IMAGE_CHAT_GUIDE.md) | Image chat feature details | Using image functionality |
| [IMPLEMENTATION_SUMMARY.md](./IMPLEMENTATION_SUMMARY.md) | What was built & how | Understanding changes made |

### Technical Guides

| Document | Purpose | When to Use |
|----------|---------|-------------|
| [UV_PACKAGE_MANAGER.md](./UV_PACKAGE_MANAGER.md) | UV package manager guide | Managing Python dependencies |
| [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) | Common issues & solutions | Something's not working |

### Setup & Operations

| Document | Purpose | When to Use |
|----------|---------|-------------|
| [START.md](./START.md) | Original start guide | Alternative setup method |
| [RUNNING.md](./RUNNING.md) | Running instructions | Operating the services |

## 🎯 Find What You Need

### "I want to..."

#### Setup & Installation
- **Set up the project for the first time**
  → Run `./setup-uv.sh` or see [README.md](./README.md#quick-start-recommended)

- **Understand what UV is**
  → [UV_PACKAGE_MANAGER.md](./UV_PACKAGE_MANAGER.md)

- **Set up without the script**
  → [README.md](./README.md#manual-setup)

#### Running & Operating
- **Start all services quickly**
  → Run `./start-services.sh` or see [QUICK_REFERENCE.md](./QUICK_REFERENCE.md#-quick-start)

- **Stop all services**
  → Run `./stop-services.sh`

- **See all available commands**
  → [QUICK_REFERENCE.md](./QUICK_REFERENCE.md)

- **View service logs**
  → `tail -f logs/[service-name].log` or see [QUICK_REFERENCE.md](./QUICK_REFERENCE.md#-troubleshooting)

#### Using Features
- **Send a text message**
  → Open http://localhost:3000 and type

- **Upload and chat about images**
  → [IMAGE_CHAT_GUIDE.md](./IMAGE_CHAT_GUIDE.md#usage)

- **Understand the image flow**
  → [VISUAL_GUIDE.md](./VISUAL_GUIDE.md#-image-chat-flow)

#### Understanding the System
- **See the architecture**
  → [VISUAL_GUIDE.md](./VISUAL_GUIDE.md#%EF%B8%8F-system-architecture)

- **Understand how messages flow**
  → [VISUAL_GUIDE.md](./VISUAL_GUIDE.md#-image-chat-flow)

- **See what files do what**
  → [VISUAL_GUIDE.md](./VISUAL_GUIDE.md#-file-structure)

- **Know what changed in this version**
  → [IMPLEMENTATION_SUMMARY.md](./IMPLEMENTATION_SUMMARY.md)

#### Troubleshooting
- **Service won't start**
  → [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) or [QUICK_REFERENCE.md](./QUICK_REFERENCE.md#-troubleshooting)

- **Image upload fails**
  → [IMAGE_CHAT_GUIDE.md](./IMAGE_CHAT_GUIDE.md#troubleshooting)

- **UV not working**
  → [UV_PACKAGE_MANAGER.md](./UV_PACKAGE_MANAGER.md#troubleshooting)

- **Database issues**
  → [QUICK_REFERENCE.md](./QUICK_REFERENCE.md#reset-database)

#### Development
- **Add a new Python dependency**
  → Edit `pyproject.toml`, then run `uv pip install -e .`

- **Migrate the database**
  → Run `cd storage-service && uv run python migrate_db.py`

- **Understand the API**
  → [README.md](./README.md#api-endpoints)

## 📋 Quick Command Reference

```bash
# Setup (once)
./setup-uv.sh

# Start all services
./start-services.sh

# Stop all services
./stop-services.sh

# View logs
tail -f logs/storage-service.log
tail -f logs/chat-service.log
tail -f logs/frontend.log
```

## 🌐 Service URLs

- **Frontend**: http://localhost:3000
- **Chat API**: http://localhost:8001 ([docs](http://localhost:8001/docs))
- **Storage API**: http://localhost:8002 ([docs](http://localhost:8002/docs))

## 🔑 Key Files

### Configuration
- `chat-service/.env` - OpenAI API key & settings
- `frontend/.env.local` - Frontend configuration
- `storage-service/uploads/` - Uploaded images
- `storage-service/chat.db` - SQLite database

### Scripts
- `setup-uv.sh` - Complete setup automation
- `start-services.sh` - Start all services
- `stop-services.sh` - Stop all services

### Code
- `storage-service/main.py` - Storage API
- `chat-service/main.py` - Chat API with vision
- `frontend/src/app/page.tsx` - Main chat page
- `frontend/src/components/ChatInput.tsx` - Input with image upload
- `frontend/src/components/ChatMessage.tsx` - Message display

## 🎓 Learning Path

### Beginner
1. Read [README.md](./README.md)
2. Run `./setup-uv.sh`
3. Try [QUICK_REFERENCE.md](./QUICK_REFERENCE.md) commands
4. Test image upload feature

### Intermediate
1. Review [VISUAL_GUIDE.md](./VISUAL_GUIDE.md)
2. Read [IMAGE_CHAT_GUIDE.md](./IMAGE_CHAT_GUIDE.md)
3. Explore API docs (http://localhost:8001/docs)
4. Learn [UV_PACKAGE_MANAGER.md](./UV_PACKAGE_MANAGER.md)

### Advanced
1. Study [IMPLEMENTATION_SUMMARY.md](./IMPLEMENTATION_SUMMARY.md)
2. Examine source code
3. Modify and extend features
4. Deploy to production

## 💡 Tips

- 📌 **Bookmark this page** for quick access to all docs
- 🔖 Use [QUICK_REFERENCE.md](./QUICK_REFERENCE.md) for daily commands
- 🎨 Reference [VISUAL_GUIDE.md](./VISUAL_GUIDE.md) for architecture
- 🐛 Check [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) first when stuck
- 📚 Read [IMAGE_CHAT_GUIDE.md](./IMAGE_CHAT_GUIDE.md) for image features

## 🆘 Getting Help

1. Check [QUICK_REFERENCE.md](./QUICK_REFERENCE.md) for commands
2. Read [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) for solutions
3. Review logs in `logs/` directory
4. Check API docs at http://localhost:8001/docs

## ✨ Key Features

- ✅ Multi-turn text conversations
- ✅ Image upload and analysis
- ✅ GPT-4 Vision integration
- ✅ Streaming responses
- ✅ Persistent conversations
- ✅ Fast setup with UV
- ✅ Easy service management

## 🎉 Ready to Start?

```bash
# Clone/navigate to project
cd chat-app

# Run setup
./setup-uv.sh

# Add your OpenAI API key
nano chat-service/.env

# Start services
./start-services.sh

# Open browser
open http://localhost:3000
```

Happy coding! 🚀
