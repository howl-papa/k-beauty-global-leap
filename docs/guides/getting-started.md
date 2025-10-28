# Getting Started with K-Beauty Global Leap

## Quick Start Guide

This guide will help you set up the K-Beauty Global Leap development environment on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.9+** - [Download Python](https://www.python.org/downloads/)
- **Node.js 18+** - [Download Node.js](https://nodejs.org/)
- **PostgreSQL 13+** - [Download PostgreSQL](https://www.postgresql.org/download/)
- **Redis** - [Download Redis](https://redis.io/download)
- **Docker & Docker Compose** (Optional but recommended) - [Download Docker](https://www.docker.com/products/docker-desktop/)

## Installation Methods

### Method 1: Docker Compose (Recommended)

This is the easiest way to get started with full environment setup.

```bash
# Clone the repository
git clone https://github.com/howl-papa/k-beauty-global-leap.git
cd k-beauty-global-leap

# Copy environment variables
cp .env.example .env

# Edit .env with your API keys
nano .env  # or use your preferred editor

# Start all services
docker-compose up -d

# Initialize database
docker-compose exec backend alembic upgrade head

# Access the applications
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Method 2: Manual Setup

#### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp ../.env.example ../.env
# Edit .env with your configuration

# Run database migrations
alembic upgrade head

# Start the server
uvicorn main:app --reload --port 8000
```

#### Frontend Setup

```bash
# Open a new terminal and navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

## Environment Variables

### Required API Keys

You'll need to obtain API keys for the following services:

1. **OpenAI** - [Get API Key](https://platform.openai.com/api-keys)
   ```
   OPENAI_API_KEY=sk-...
   ```

2. **Anthropic Claude** (Optional) - [Get API Key](https://console.anthropic.com/)
   ```
   ANTHROPIC_API_KEY=sk-ant-...
   ```

3. **Pinecone** (Optional for RAG features) - [Get API Key](https://www.pinecone.io/)
   ```
   PINECONE_API_KEY=...
   PINECONE_ENVIRONMENT=...
   ```

### Database Configuration

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/k_beauty_leap
REDIS_URL=redis://localhost:6379
```

### JWT Configuration

```env
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Verify Installation

### Check Backend

```bash
# Health check
curl http://localhost:8000/health

# API status
curl http://localhost:8000/api/v1/status

# View API documentation
open http://localhost:8000/docs
```

### Check Frontend

```bash
# Open in browser
open http://localhost:3000
```

## Development Workflow

### Running Tests

#### Backend Tests
```bash
cd backend
pytest -v --cov=app
```

#### Frontend Tests
```bash
cd frontend
npm test
```

### Code Formatting

#### Backend
```bash
cd backend
black .
isort .
mypy .
```

#### Frontend
```bash
cd frontend
npm run format
npm run lint
```

### Database Migrations

#### Create a new migration
```bash
cd backend
alembic revision --autogenerate -m "Description of changes"
```

#### Apply migrations
```bash
alembic upgrade head
```

#### Rollback migration
```bash
alembic downgrade -1
```

## Common Issues

### Port Already in Use

If you get an error about ports already in use:

```bash
# Find process using the port
lsof -i :8000  # or :3000 for frontend

# Kill the process
kill -9 <PID>
```

### Database Connection Error

Make sure PostgreSQL is running:

```bash
# macOS
brew services start postgresql

# Linux
sudo systemctl start postgresql

# Docker
docker-compose up postgres
```

### Redis Connection Error

Make sure Redis is running:

```bash
# macOS
brew services start redis

# Linux
sudo systemctl start redis

# Docker
docker-compose up redis
```

## Next Steps

- [Architecture Overview](../architecture/system-overview.md)
- [API Documentation](../api/)
- [Contributing Guidelines](../../CONTRIBUTING.md)

## Need Help?

- 📧 Email: contact@yongrak.pro
- 🐛 Issues: [GitHub Issues](https://github.com/howl-papa/k-beauty-global-leap/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/howl-papa/k-beauty-global-leap/discussions)
