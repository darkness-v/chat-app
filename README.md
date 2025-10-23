# Lightweight Multi-Turn Chat Application

A production-ready microservice-based chat application with persistent conversation history, streaming support, and **ChatGPT-like conversation management**.

## Architecture

### Services
1. **Chat Service** (Port 8001) - Handles AI chat interactions, streaming, and vision API
2. **Storage Service** (Port 8002) - Manages conversation persistence and image uploads
3. **Frontend Service** (Port 3000) - React/Next.js UI with conversation sidebar

## Features
- ✅ **Multi-conversation management** - Create, switch, and delete conversations
- ✅ **Conversation sidebar** - ChatGPT-like interface with conversation list
- ✅ **Auto-generated titles** - Intelligent conversation naming
- ✅ **Multi-turn conversation history** - Persistent conversation tracking
- ✅ **Streaming responses** - Real-time AI responses with loading states
- ✅ **Image upload and chat** - PNG/JPG/JPEG support with GPT-4 Vision
- ✅ **CSV data analysis** - Upload CSV files for AI-powered analysis with plots
- ✅ **Message feedback** - Like/dislike assistant responses
- ✅ **Clean, modern UI** - Responsive design with Tailwind CSS

## Tech Stack
- **Backend**: FastAPI, SQLAlchemy, SQLite, UV (package manager)
- **Frontend**: Next.js, React, Tailwind CSS
- **AI**: OpenAI API (GPT-4o for vision, GPT-4o-mini for text)

## Quick Start (Recommended)

### Prerequisites
- Python 3.10+
- Node.js 18+
- OpenAI API Key
- UV (will be installed automatically)

### One-Command Setup

```bash
# Navigate to the project
cd chat-app

# Run setup script
./setup.sh

# Update your OpenAI API key
nano chat-service/.env
# or
code chat-service/.env

# Start all services
./start-services.sh

# Open http://localhost:3000 in your browser
```

### Stop Services

```bash
./stop-services.sh
```

## Manual Setup

### Backend Setup with UV

1. **Install UV** (if not already installed):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. **Storage Service**:
```bash
cd storage-service
uv venv
uv pip install -e .
mkdir -p uploads
```

3. **Chat Service**:
```bash
cd chat-service
uv venv
uv pip install -e .
```

4. **Set up environment variables**:

chat-service/.env:
```bash
OPENAI_API_KEY=your_api_key_here
STORAGE_SERVICE_URL=http://localhost:8002
MODEL=gpt-4o-mini
```

5. **Run services**:
```bash
# Terminal 1 - Storage Service
cd storage-service
uv run uvicorn main:app --host 0.0.0.0 --port 8002

# Terminal 2 - Chat Service
cd chat-service
uv run uvicorn main:app --host 0.0.0.0 --port 8001
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## Usage

### Text Chat
1. Open http://localhost:3000
2. Type a message and press Enter or click Send
3. AI responds with streaming responses
4. All conversations are automatically saved

### Image Chat
1. Click the 📷 image icon to upload an image (PNG, JPG, JPEG)
2. Preview appears with × button to remove
3. Add a message or leave blank (defaults to "What is in this image?")
4. Click Send - AI analyzes using GPT-4 Vision
5. Images are included in conversation context for follow-up questions

### CSV Data Analysis
1. Click the 📊 CSV icon to upload a CSV file
2. AI can analyze data, create plots, and answer questions
3. Python code is executed in a sandboxed environment
4. Visualizations are generated automatically using matplotlib/seaborn
5. All plots are displayed inline with the conversation

### Conversation Management
1. Create new conversations with the "New Chat" button
2. Switch between conversations in the sidebar
3. Delete conversations with the trash icon
4. Conversations are auto-titled based on the first message


## Project Structure

```
chat-app/
├── setup.sh                 
├── start-services.sh      
├── stop-services.sh       
├── storage-service/         
│   ├── main.py             
│   ├── models.py           
│   ├── schemas.py          
│   ├── database.py         
│   ├── pyproject.toml     
│   └── uploads/            
├── chat-service/           
│   ├── main.py           
│   ├── code_executor.py    
│   ├── data_analysis_agent.py  
│   └── pyproject.toml      
└── frontend/              
    ├── src/
    │   ├── components/
    │   │   ├── ChatInput.tsx    
    │   │   ├── ChatMessage.tsx  
    │   │   ├── CSVUpload.tsx    
    │   │   └── Sidebar.tsx     
    │   ├── app/
    │   │   └── page.tsx     
    │   └── types/
    │       └── index.ts        
    └── package.json
```
## Demo

Watch a demonstration of the application in action:

🎥 [View Demo Video](https://drive.google.com/file/d/1kSv-o7igU78u1z-6W5eYmOWXkPyNCoqn/view?usp=sharing)

*Note: Click the link to open the video in Google Drive*


