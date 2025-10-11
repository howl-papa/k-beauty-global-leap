# 🚀 K-Beauty Global Leap - GitHub 프로젝트 설정 가이드

## 즉시 실행할 수 있는 명령어들

### 1. GitHub Repository 생성 및 초기 설정

```bash
# 프로젝트 디렉토리 생성
mkdir k-beauty-global-leap
cd k-beauty-global-leap

# Git 초기화
git init
git branch -M main

# 기본 디렉토리 구조 생성
mkdir -p backend/{app/{api/{endpoints,dependencies},core,models,schemas,services,utils},alembic,scripts,tests}
mkdir -p frontend/{src/{components,pages,hooks,store,utils,types},public,styles}
mkdir -p data/{seeds,migrations}
mkdir -p docs
mkdir -p docker
mkdir -p scripts

# 필수 파일들 생성
touch README.md
touch .gitignore
touch .env.example
touch docker-compose.yml
touch backend/requirements.txt
touch frontend/package.json
```

### 2. .gitignore 파일 생성

```bash
cat > .gitignore << 'EOF'
# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environment
venv/
ENV/
env/
.venv/

# Database
*.db
*.sqlite3
postgresql_data/

# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Next.js
.next/
out/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
logs
*.log

# Docker
docker-compose.override.yml

# AI/ML
*.pkl
*.joblib
model_cache/

# Temporary files
tmp/
temp/
EOF
```

### 3. README.md 생성 (앞서 작성한 내용)

```bash
# README.md 파일 생성 (위에서 작성한 내용을 복사)
# 파일이 이미 생성되어 있으므로 내용만 복사해서 붙여넣기
```

### 4. docker-compose.yml 설정

```bash
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: k_beauty_leap
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./data/init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 30s
      timeout: 10s
      retries: 3

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://postgres:password@postgres:5432/k_beauty_leap
      REDIS_URL: redis://redis:6379
      OPENAI_API_KEY: ${OPENAI_API_KEY}
      PINECONE_API_KEY: ${PINECONE_API_KEY}
      ANTHROPIC_API_KEY: ${ANTHROPIC_API_KEY}
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - ./backend:/app
      - /app/__pycache__
    command: uvicorn main:app --host 0.0.0.0 --reload
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      NEXT_PUBLIC_API_URL: http://localhost:8000
      NEXT_PUBLIC_ENVIRONMENT: development
    volumes:
      - ./frontend:/app
      - /app/node_modules
      - /app/.next
    command: npm run dev
    depends_on:
      backend:
        condition: service_healthy

volumes:
  postgres_data:
EOF
```

### 5. 환경 변수 템플릿 생성

```bash
cat > .env.example << 'EOF'
# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/k_beauty_leap
REDIS_URL=redis://localhost:6379

# AI API Keys
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_ENVIRONMENT=your_pinecone_environment_here

# JWT Secret
JWT_SECRET_KEY=your_jwt_secret_key_here

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_ENVIRONMENT=development

# Analytics
GOOGLE_ANALYTICS_ID=your_ga_id_here

# Email (Optional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password

# Social Media APIs (for data collection)
INSTAGRAM_ACCESS_TOKEN=your_instagram_token
TIKTOK_ACCESS_TOKEN=your_tiktok_token
YOUTUBE_API_KEY=your_youtube_api_key
EOF
```

### 6. Backend 기본 구조 생성

```bash
# Backend Dockerfile
cat > backend/Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

# Backend requirements.txt
cat > backend/requirements.txt << 'EOF'
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
alembic==1.12.1
psycopg2-binary==2.9.9
redis==5.0.1
python-jose[cryptography]==3.3.0
python-multipart==0.0.6
bcrypt==4.1.1
pydantic[email]==2.5.0
python-dotenv==1.0.0

# AI/ML libraries
openai==1.3.7
anthropic==0.7.7
langchain==0.0.350
llama-index==0.9.13
pinecone-client==2.2.4
sentence-transformers==2.2.2

# Data processing
pandas==2.1.4
numpy==1.25.2
aiohttp==3.9.1
beautifulsoup4==4.12.2
requests==2.31.0

# Monitoring and logging
structlog==23.2.0
sentry-sdk[fastapi]==1.38.0

# Development
pytest==7.4.3
pytest-asyncio==0.21.1
black==23.11.0
isort==5.12.0
mypy==1.7.1
EOF

# Backend main.py
cat > backend/main.py << 'EOF'
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="K-Beauty Global Leap API",
    description="AI-Powered Localization Platform for K-Beauty SMEs",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "k-beauty-global-leap-api"}

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to K-Beauty Global Leap API",
        "version": "0.1.0",
        "docs": "/docs"
    }

# API routes will be added here
@app.get("/api/v1/status")
async def api_status():
    return {
        "api_version": "v1",
        "status": "operational",
        "features": [
            "market_analysis",
            "cultural_adaptation", 
            "partner_verification",
            "roi_optimization"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
EOF
```

### 7. Frontend 기본 구조 생성

```bash
# Frontend Dockerfile
cat > frontend/Dockerfile << 'EOF'
FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Expose port
EXPOSE 3000

# Start the application
CMD ["npm", "start"]
EOF

# Frontend package.json
cat > frontend/package.json << 'EOF'
{
  "name": "k-beauty-global-leap-frontend",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "type-check": "tsc --noEmit"
  },
  "dependencies": {
    "next": "14.0.3",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "@types/node": "^20.9.0",
    "@types/react": "^18.2.37",
    "@types/react-dom": "^18.2.15",
    "typescript": "^5.2.2",
    "tailwindcss": "^3.3.5",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.31",
    "@headlessui/react": "^1.7.17",
    "@heroicons/react": "^2.0.18",
    "framer-motion": "^10.16.5",
    "recharts": "^2.8.0",
    "axios": "^1.6.2",
    "swr": "^2.2.4",
    "zustand": "^4.4.6",
    "react-hook-form": "^7.47.0",
    "@hookform/resolvers": "^3.3.2",
    "zod": "^3.22.4"
  },
  "devDependencies": {
    "eslint": "^8.54.0",
    "eslint-config-next": "14.0.3",
    "@tailwindcss/forms": "^0.5.7",
    "@tailwindcss/typography": "^0.5.10"
  }
}
EOF

# Next.js configuration
cat > frontend/next.config.js << 'EOF'
/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    appDir: true,
  },
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
  },
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: `${process.env.NEXT_PUBLIC_API_URL}/api/:path*`,
      },
    ]
  },
}

module.exports = nextConfig
EOF

# Tailwind CSS configuration
cat > frontend/tailwind.config.js << 'EOF'
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#fef2f2',
          500: '#ef4444',
          600: '#dc2626',
          700: '#b91c1c',
        },
        secondary: {
          50: '#f0fdfa',
          500: '#14b8a6',
          600: '#0d9488',
          700: '#0f766e',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
}
EOF
```

### 8. GitHub Actions CI/CD 설정

```bash
mkdir -p .github/workflows

cat > .github/workflows/ci.yml << 'EOF'
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test-backend:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Cache pip packages
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('backend/requirements.txt') }}
    
    - name: Install dependencies
      run: |
        cd backend
        pip install -r requirements.txt
    
    - name: Run tests
      env:
        DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
      run: |
        cd backend
        pytest -v
    
    - name: Lint with black
      run: |
        cd backend
        black --check .
    
    - name: Type check with mypy
      run: |
        cd backend
        mypy .

  test-frontend:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '18'
        cache: 'npm'
        cache-dependency-path: frontend/package-lock.json
    
    - name: Install dependencies
      run: |
        cd frontend
        npm ci
    
    - name: Run type check
      run: |
        cd frontend
        npm run type-check
    
    - name: Run linter
      run: |
        cd frontend
        npm run lint
    
    - name: Build
      run: |
        cd frontend
        npm run build

  security-scan:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        scan-type: 'fs'
        scan-ref: '.'
        format: 'sarif'
        output: 'trivy-results.sarif'
    
    - name: Upload Trivy scan results to GitHub Security tab
      uses: github/codeql-action/upload-sarif@v2
      if: always()
      with:
        sarif_file: 'trivy-results.sarif'
EOF
```

### 9. 프로젝트 커밋 및 푸시

```bash
# 환경 변수 파일 생성 (실제 키 값은 별도 설정)
cp .env.example .env

# Git에 파일 추가
git add .

# 초기 커밋
git commit -m "🎉 Initial project setup: K-Beauty Global Leap

- Set up FastAPI backend with PostgreSQL
- Configure Next.js frontend with Tailwind CSS
- Add Docker Compose for development environment
- Implement CI/CD pipeline with GitHub Actions
- Create comprehensive project documentation

Tech Stack:
- Backend: FastAPI + PostgreSQL + Redis
- Frontend: Next.js + TypeScript + Tailwind CSS
- AI: OpenAI GPT-4 + LangChain + LlamaIndex + Pinecone
- DevOps: Docker + GitHub Actions

Features to implement:
- Market Intelligence Hub
- Cultural Adaptation Engine  
- Partner Verification Network
- ROI Optimization Dashboard"

# GitHub repository 생성 (GitHub CLI 사용)
gh repo create k-beauty-global-leap --public --description "AI-Powered Localization Platform for K-Beauty SMEs - Empowering small businesses to compete globally through intelligent market analysis and cultural adaptation"

# 리모트 저장소 연결 및 푸시
git remote add origin https://github.com/howl-papa/k-beauty-global-leap.git
git push -u origin main
```

### 10. 개발 환경 실행

```bash
# 개발 환경 시작
docker-compose up -d

# 백엔드 로그 확인
docker-compose logs -f backend

# 프론트엔드 로그 확인
docker-compose logs -f frontend

# 서비스 상태 확인
docker-compose ps

# 애플리케이션 접속
echo "Backend API: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo "Frontend: http://localhost:3000"
echo "PostgreSQL: localhost:5432"
echo "Redis: localhost:6379"
```

### 11. Jekyll 블로그 설정 (별도 repository)

```bash
# 새로운 디렉토리에서 블로그 설정
cd ..
mkdir k-beauty-tech-blog
cd k-beauty-tech-blog

# Jekyll 사이트 생성
gem install jekyll bundler
jekyll new . --force

# 블로그 설정 파일들 복사 (위에서 작성한 파일들)
# - _config.yml
# - index.html  
# - about.md
# - 첫 번째 개발 일지 포스트

# GitHub repository 생성 및 GitHub Pages 설정
gh repo create k-beauty-tech-blog --public --description "Development blog for K-Beauty Global Leap project - Technical insights and progress updates"

git init
git add .
git commit -m "🚀 Initialize K-Beauty Tech Blog with Jekyll

- Set up Jekyll blog with custom theme
- Configure GitHub Pages deployment
- Add about page and first development log
- Implement SEO optimization and responsive design"

git branch -M main
git remote add origin https://github.com/howl-papa/k-beauty-tech-blog.git
git push -u origin main

# GitHub Pages 활성화 (GitHub 웹사이트에서 Settings > Pages에서 설정)
echo "GitHub Pages will be available at: https://howl-papa.github.io/k-beauty-tech-blog"
```

이제 모든 설정이 완료되었습니다! 🎉

**다음 단계:**
1. `.env` 파일에 실제 API 키들 설정
2. `docker-compose up -d`로 개발 환경 시작  
3. 첫 번째 기능 개발 시작
4. 정기적인 블로그 포스팅으로 진행상황 공유

프로젝트 진행하시면서 궁금한 점이 있으시면 언제든지 문의해 주세요! 🚀