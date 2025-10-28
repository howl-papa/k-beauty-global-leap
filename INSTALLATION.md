# 🚀 K-Beauty Global Leap - Installation Guide

Complete installation and setup guide for local development.

## 📋 Prerequisites

### Required
- **Python 3.9+** - Backend runtime
- **Node.js 18+** - Frontend runtime
- **PostgreSQL 13+** - Database
- **Git** - Version control

### Optional
- **Redis** - Caching (not required for MVP)
- **Docker & Docker Compose** - Containerized deployment

---

## 🛠️ Installation Methods

### Method 1: Local Development (Recommended)

This method gives you full control and is best for active development.

#### Step 1: Clone Repository

```bash
git clone https://github.com/howl-papa/k-beauty-global-leap.git
cd k-beauty-global-leap
```

#### Step 2: Backend Setup

**2.1 Create Python Virtual Environment**

```bash
cd backend
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

**2.2 Install Python Dependencies**

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**2.3 Configure Environment Variables**

Create `.env` file in `backend/` directory:

```bash
cat > .env << 'EOF'
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/kbeauty

# JWT Settings
JWT_SECRET_KEY=your-super-secret-key-change-this-in-production-use-openssl-rand-hex-32
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# Redis (Optional)
REDIS_URL=redis://localhost:6379

# API Settings
API_V1_STR=/api/v1
PROJECT_NAME=K-Beauty Global Leap
EOF
```

**Generate a secure JWT secret:**
```bash
openssl rand -hex 32
# Copy the output and replace JWT_SECRET_KEY in .env
```

**2.4 Setup PostgreSQL Database**

**Option A: Using local PostgreSQL**
```bash
# Create database
createdb kbeauty

# Or using psql
psql -U postgres
CREATE DATABASE kbeauty;
\q
```

**Option B: Using Docker for PostgreSQL only**
```bash
docker run -d \
  --name kbeauty-postgres \
  -e POSTGRES_DB=kbeauty \
  -e POSTGRES_USER=user \
  -e POSTGRES_PASSWORD=password \
  -p 5432:5432 \
  postgres:15

# Update DATABASE_URL in .env to match these credentials
```

**2.5 Run Database Setup Script**

```bash
# This will:
# - Run migrations
# - Generate mock data
# - Import data to database
# - Create test user

bash scripts/init_database.sh
```

**Or manually:**

```bash
# Run migrations
alembic upgrade head

# Generate mock data
python scripts/generate_mock_instagram_data.py

# Import mock data and create test user
python scripts/test_system.py
```

**2.6 Start Backend Server**

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

✅ Backend is now running at:
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

#### Step 3: Frontend Setup

Open a **new terminal window**.

**3.1 Navigate to Frontend Directory**

```bash
cd frontend  # From project root
```

**3.2 Install Node.js Dependencies**

```bash
npm install
```

**3.3 Configure Environment Variables**

Create `.env.local` file in `frontend/` directory:

```bash
cat > .env.local << 'EOF'
NEXT_PUBLIC_API_URL=http://localhost:8000
EOF
```

**3.4 Start Frontend Development Server**

```bash
npm run dev
```

✅ Frontend is now running at:
- **Website**: http://localhost:3000

---

### Method 2: Docker Compose

Quick setup for testing and demos.

#### Step 1: Clone and Setup

```bash
git clone https://github.com/howl-papa/k-beauty-global-leap.git
cd k-beauty-global-leap
```

#### Step 2: Configure Environment

```bash
cp .env.example .env
# Edit .env with your settings
```

#### Step 3: Start All Services

```bash
docker-compose up -d
```

#### Step 4: Initialize Database

```bash
# Run migrations
docker-compose exec backend alembic upgrade head

# Import mock data (via API after signup)
# Or manually:
docker-compose exec backend python scripts/test_system.py
```

✅ All services are now running:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs
- PostgreSQL: localhost:5432
- Redis: localhost:6379

---

## ✅ Verify Installation

### 1. Test Backend API

Visit http://localhost:8000/docs and try:

- `GET /api/v1/auth/login` - Auth endpoint exists
- Check API documentation is loading correctly

### 2. Test Frontend

Visit http://localhost:3000 and verify:

- Landing page loads
- Can navigate to `/signup`
- Can navigate to `/login`

### 3. Create Test Account

1. Go to http://localhost:3000/signup
2. Fill in the form:
   - Email: `your@email.com`
   - Password: `yourpassword`
   - Full Name: `Your Name`
   - Company: `Your Company` (optional)
3. Click "Sign Up"
4. You should be redirected to `/dashboard`

### 4. Import Mock Data

**Option A: Via API (if not done during setup)**

1. Login to http://localhost:3000
2. Open http://localhost:8000/docs
3. Click "Authorize" button
4. Enter your access token (from browser dev tools → Application → Local Storage → `access_token`)
5. Find `POST /api/v1/instagram/import-mock-data`
6. Click "Try it out" → "Execute"
7. Should return success with counts

**Option B: Via Script (already done if you ran init_database.sh)**

```bash
cd backend
python scripts/test_system.py
```

### 5. Test Main Features

**Trend Analysis Dashboard:**
- Visit http://localhost:3000/dashboard/trend-analysis
- Switch between markets (Germany, France, Japan)
- Should see:
  - 4 overview stat cards
  - 8 trending hashtags
  - Top hashtags by frequency
  - Peak posting times
  - Recent posts grid

**Influencer Discovery:**
- Visit http://localhost:3000/dashboard/influencers
- Adjust filters (market, followers, engagement)
- Click "Search Influencers"
- Should see influencer cards with metrics

---

## 🧪 Running Tests

### Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run specific test file
pytest tests/test_auth.py

# Run with coverage
pytest --cov=app tests/
```

### Frontend Tests

```bash
cd frontend

# Run tests
npm test

# Run with coverage
npm test -- --coverage
```

### System Integration Test

```bash
cd backend
python scripts/test_system.py
```

This will test:
- ✅ Database connection
- ✅ All tables exist
- ✅ Mock data import
- ✅ Instagram service methods
- ✅ Test user creation

---

## 🐛 Troubleshooting

### Backend Issues

**Issue: Database connection fails**
```
Solution:
1. Check PostgreSQL is running: pg_isready
2. Verify credentials in backend/.env
3. Ensure database exists: psql -l
4. Create database: createdb kbeauty
```

**Issue: Alembic migrations fail**
```
Solution:
1. Check database connection
2. Delete alembic/versions/ folder
3. Run: alembic revision --autogenerate -m "Initial"
4. Run: alembic upgrade head
```

**Issue: Import error: No module named 'app'**
```
Solution:
1. Ensure virtual environment is activated
2. cd to backend directory
3. pip install -r requirements.txt
```

### Frontend Issues

**Issue: Cannot connect to API**
```
Solution:
1. Check backend is running: curl http://localhost:8000
2. Verify NEXT_PUBLIC_API_URL in .env.local
3. Check CORS settings in backend
```

**Issue: npm install fails**
```
Solution:
1. Clear npm cache: npm cache clean --force
2. Delete node_modules and package-lock.json
3. Run: npm install
```

**Issue: Page shows 401 Unauthorized**
```
Solution:
1. Clear browser localStorage
2. Logout and login again
3. Check token in dev tools → Application → Local Storage
```

### Common Issues

**Issue: Port already in use**
```
Solution:
# Find process using port
lsof -i :8000  # or :3000

# Kill process
kill -9 <PID>

# Or use different port
uvicorn main:app --port 8001
npm run dev -- -p 3001
```

**Issue: Mock data import fails**
```
Solution:
1. Ensure mock data file exists:
   ls backend/scripts/mock_instagram_data.json
2. Generate if missing:
   python backend/scripts/generate_mock_instagram_data.py
3. Check file path in import script
```

---

## 📚 Additional Resources

### Documentation
- [Development Roadmap](docs/DEVELOPMENT_ROADMAP.md)
- [Week 1 Tasks](docs/WEEK1_TASKS.md)
- [Instagram Integration](docs/INSTAGRAM_INTEGRATION.md)
- [API Documentation](http://localhost:8000/docs) (when running)

### Project Structure
```
k-beauty-global-leap/
├── backend/
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Core utilities
│   │   ├── models/       # Database models
│   │   ├── schemas/      # Pydantic schemas
│   │   └── services/     # Business logic
│   ├── alembic/          # Migrations
│   ├── scripts/          # Utility scripts
│   └── main.py           # Entry point
├── frontend/
│   ├── src/
│   │   ├── app/          # Pages (App Router)
│   │   ├── components/   # React components
│   │   ├── store/        # State management
│   │   ├── types/        # TypeScript types
│   │   └── utils/        # Utilities
│   └── public/           # Static files
└── docs/                 # Documentation
```

### Default Credentials
- **Test User Email**: test@example.com
- **Test User Password**: testpassword123

### Default Ports
- **Frontend**: 3000
- **Backend**: 8000
- **PostgreSQL**: 5432
- **Redis**: 6379

---

## 🎉 Success!

If you've made it here, your K-Beauty Global Leap platform should be fully operational!

### Next Steps:
1. **Explore the dashboard**: Try different markets and filters
2. **Test API endpoints**: Use http://localhost:8000/docs
3. **Review the code**: Understand the architecture
4. **Start developing**: Add new features!

### Need Help?
- Check [Troubleshooting](#-troubleshooting) section
- Review logs: `backend/app.log`, browser console
- Open an issue on GitHub

---

**Created**: 2025-10-28  
**Version**: 1.0 (Week 1 MVP)  
**Company**: (주)뷰티인사이드랩 (Beauty Insight Lab Inc.)
