#!/bin/bash

# K-Beauty Global Leap - Database Initialization Script
# This script sets up the database and imports mock data

set -e  # Exit on error

echo "=========================================="
echo "K-Beauty Global Leap - Database Setup"
echo "=========================================="
echo ""

# Check if we're in the correct directory
if [ ! -f "alembic.ini" ]; then
    echo "❌ Error: Please run this script from the backend directory"
    echo "   cd backend && bash scripts/init_database.sh"
    exit 1
fi

echo "✅ Running from correct directory"
echo ""

# Step 1: Check database connection
echo "📍 Step 1: Checking database connection..."
python -c "
from app.core.database import engine
try:
    with engine.connect() as conn:
        conn.execute('SELECT 1')
    print('✅ Database connection successful')
except Exception as e:
    print(f'❌ Database connection failed: {e}')
    print('')
    print('Please ensure:')
    print('1. PostgreSQL is running')
    print('2. Database credentials in .env are correct')
    print('3. Database exists (or create it: createdb kbeauty)')
    exit(1)
"
echo ""

# Step 2: Run migrations
echo "📍 Step 2: Running database migrations..."
alembic upgrade head
echo "✅ Migrations completed"
echo ""

# Step 3: Generate mock data (if not exists)
if [ ! -f "scripts/mock_instagram_data.json" ]; then
    echo "📍 Step 3: Generating mock Instagram data..."
    python scripts/generate_mock_instagram_data.py
    echo "✅ Mock data generated"
else
    echo "📍 Step 3: Mock data already exists"
fi
echo ""

# Step 4: Import mock data
echo "📍 Step 4: Importing mock data into database..."
python -c "
import asyncio
from app.core.database import SessionLocal
from app.services.instagram_service import InstagramService
from app.models.instagram_post import InstagramPost

db = SessionLocal()
service = InstagramService(db)

# Check if data already exists
existing_count = db.query(InstagramPost).count()
if existing_count > 0:
    print(f'⚠️  Data already exists ({existing_count} posts)')
    print('   Skipping import to avoid duplicates')
else:
    print('📥 Importing mock data...')
    result = asyncio.run(service.import_mock_data('scripts/mock_instagram_data.json'))
    if result['success']:
        print('✅ Mock data imported successfully!')
        print(f\"   - Posts: {result['imported']['posts']}\")
        print(f\"   - Hashtags: {result['imported']['hashtags']}\")
        print(f\"   - Influencers: {result['imported']['influencers']}\")
    else:
        print('❌ Import failed')

db.close()
"
echo ""

# Step 5: Create test user
echo "📍 Step 5: Creating test user..."
python -c "
from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

db = SessionLocal()

# Check if test user exists
existing = db.query(User).filter(User.email == 'test@example.com').first()
if existing:
    print('⚠️  Test user already exists')
else:
    user = User(
        email='test@example.com',
        hashed_password=get_password_hash('testpassword123'),
        full_name='Test User',
        company_name='Test K-Beauty Company',
        is_active=True,
        is_verified=True
    )
    db.add(user)
    db.commit()
    print('✅ Test user created')

print('')
print('Login credentials:')
print('   Email: test@example.com')
print('   Password: testpassword123')

db.close()
"
echo ""

echo "=========================================="
echo "✨ Database setup complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Start backend:  uvicorn main:app --reload"
echo "2. Start frontend: cd ../frontend && npm run dev"
echo "3. Open browser:   http://localhost:3000"
echo "4. Login with:     test@example.com / testpassword123"
echo ""
echo "API Documentation: http://localhost:8000/docs"
echo "=========================================="
