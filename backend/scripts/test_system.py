"""
System Integration Test Script

Tests the complete K-Beauty Global Leap system:
1. Database connection
2. Mock data import
3. API endpoints
4. Data retrieval
"""

import sys
import asyncio
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.database import SessionLocal, engine
from app.models import User, Company, Analysis, InstagramPost, InstagramHashtag, InstagramInfluencer
from app.services.instagram_service import InstagramService
from app.core.security import get_password_hash


def test_database_connection():
    """Test database connection"""
    print("\n" + "="*60)
    print("TEST 1: Database Connection")
    print("="*60)
    
    try:
        db = SessionLocal()
        # Test query
        result = db.execute("SELECT 1").fetchone()
        print("✅ Database connection successful!")
        print(f"   Test query result: {result}")
        db.close()
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


def test_tables_exist():
    """Test if all tables exist"""
    print("\n" + "="*60)
    print("TEST 2: Database Tables")
    print("="*60)
    
    try:
        db = SessionLocal()
        
        # Check each table
        tables = [
            ("users", User),
            ("companies", Company),
            ("analyses", Analysis),
            ("instagram_posts", InstagramPost),
            ("instagram_hashtags", InstagramHashtag),
            ("instagram_influencers", InstagramInfluencer),
        ]
        
        all_exist = True
        for table_name, model in tables:
            try:
                count = db.query(model).count()
                print(f"✅ Table '{table_name}' exists with {count} rows")
            except Exception as e:
                print(f"❌ Table '{table_name}' check failed: {e}")
                all_exist = False
        
        db.close()
        return all_exist
    except Exception as e:
        print(f"❌ Table check failed: {e}")
        return False


async def test_mock_data_import():
    """Test mock data import"""
    print("\n" + "="*60)
    print("TEST 3: Mock Data Import")
    print("="*60)
    
    try:
        db = SessionLocal()
        service = InstagramService(db)
        
        # Check if data already exists
        existing_posts = db.query(InstagramPost).count()
        if existing_posts > 0:
            print(f"⚠️  Mock data already imported ({existing_posts} posts exist)")
            print("   Skipping import to avoid duplicates")
            db.close()
            return True
        
        # Import mock data
        print("📥 Importing mock data...")
        json_path = "backend/scripts/mock_instagram_data.json"
        result = await service.import_mock_data(json_path)
        
        if result["success"]:
            print("✅ Mock data imported successfully!")
            print(f"   Posts: {result['imported']['posts']}")
            print(f"   Hashtags: {result['imported']['hashtags']}")
            print(f"   Influencers: {result['imported']['influencers']}")
            db.close()
            return True
        else:
            print("❌ Mock data import failed")
            db.close()
            return False
            
    except FileNotFoundError:
        print("❌ Mock data file not found")
        print("   Please run: python backend/scripts/generate_mock_instagram_data.py")
        return False
    except Exception as e:
        print(f"❌ Mock data import failed: {e}")
        return False


async def test_instagram_service():
    """Test Instagram service methods"""
    print("\n" + "="*60)
    print("TEST 4: Instagram Service")
    print("="*60)
    
    try:
        db = SessionLocal()
        service = InstagramService(db)
        
        # Test 1: Search posts
        print("\n📍 Test 4.1: Search posts (Germany market)")
        posts = await service.search_posts(market="germany", limit=5)
        print(f"✅ Found {len(posts)} posts")
        if posts:
            print(f"   Sample: @{posts[0].username} - {posts[0].like_count} likes")
        
        # Test 2: Get trending hashtags
        print("\n📍 Test 4.2: Get trending hashtags (France market)")
        hashtags = await service.get_trending_hashtags(market="france", limit=5)
        print(f"✅ Found {len(hashtags)} trending hashtags")
        if hashtags:
            print(f"   Top: #{hashtags[0].name} (score: {hashtags[0].trend_score})")
        
        # Test 3: Find influencers
        print("\n📍 Test 4.3: Find influencers (Japan market)")
        influencers = await service.find_influencers(
            market="japan",
            min_followers=10000,
            max_followers=100000,
            limit=5
        )
        print(f"✅ Found {len(influencers)} influencers")
        if influencers:
            print(f"   Top: @{influencers[0].username} ({influencers[0].followers_count} followers)")
        
        # Test 4: Get market insights
        print("\n📍 Test 4.4: Get market insights (Germany)")
        insights = await service.get_market_insights(market="germany")
        print(f"✅ Market insights retrieved")
        print(f"   Total posts: {insights['post_analytics']['total_posts']}")
        print(f"   Avg engagement: {insights['post_analytics']['avg_engagement_rate']}%")
        print(f"   Trending hashtags: {len(insights['trending_hashtags'])}")
        print(f"   Top influencers: {len(insights['top_influencers'])}")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Instagram service test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_create_test_user():
    """Create a test user for API testing"""
    print("\n" + "="*60)
    print("TEST 5: Create Test User")
    print("="*60)
    
    try:
        db = SessionLocal()
        
        # Check if test user exists
        existing_user = db.query(User).filter(User.email == "test@example.com").first()
        if existing_user:
            print("⚠️  Test user already exists")
            print(f"   Email: test@example.com")
            print(f"   Password: testpassword123")
            db.close()
            return True
        
        # Create test user
        test_user = User(
            email="test@example.com",
            hashed_password=get_password_hash("testpassword123"),
            full_name="Test User",
            company_name="Test K-Beauty Company",
            is_active=True,
            is_verified=True
        )
        
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        
        print("✅ Test user created successfully!")
        print(f"   Email: test@example.com")
        print(f"   Password: testpassword123")
        print(f"   ID: {test_user.id}")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Test user creation failed: {e}")
        return False


def print_summary(results):
    """Print test summary"""
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    total = len(results)
    passed = sum(results.values())
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print("\n" + "-"*60)
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("\nNext steps:")
        print("1. Start the backend: cd backend && uvicorn main:app --reload")
        print("2. Start the frontend: cd frontend && npm run dev")
        print("3. Open http://localhost:3000")
        print("4. Login with: test@example.com / testpassword123")
    else:
        print("\n⚠️  SOME TESTS FAILED")
        print("\nPlease check the errors above and fix them before proceeding.")
    
    print("="*60)


async def run_all_tests():
    """Run all system tests"""
    print("\n" + "🧪 K-Beauty Global Leap - System Integration Test")
    print("="*60)
    
    results = {}
    
    # Test 1: Database connection
    results["Database Connection"] = test_database_connection()
    if not results["Database Connection"]:
        print("\n❌ Cannot proceed without database connection")
        print_summary(results)
        return
    
    # Test 2: Tables exist
    results["Database Tables"] = test_tables_exist()
    if not results["Database Tables"]:
        print("\n⚠️  Some tables are missing. Run migrations:")
        print("   alembic upgrade head")
    
    # Test 3: Mock data import
    results["Mock Data Import"] = await test_mock_data_import()
    
    # Test 4: Instagram service
    results["Instagram Service"] = await test_instagram_service()
    
    # Test 5: Create test user
    results["Test User Creation"] = test_create_test_user()
    
    # Print summary
    print_summary(results)


if __name__ == "__main__":
    asyncio.run(run_all_tests())
