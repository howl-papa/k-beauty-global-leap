"""
Instagram Data Collection Background Tasks

Celery tasks for periodic Instagram data collection
"""

from celery import Celery
from celery.schedules import crontab
from sqlalchemy.orm import Session
from typing import List, Dict
from datetime import datetime, timedelta
import asyncio

from app.core.database import SessionLocal
from app.core.config import get_settings
from app.services.instagram_service import InstagramService
from app.integrations.instagram_api import InstagramGraphAPI, InstagramAPIError
from app.models.user import User
from app.models.instagram_post import InstagramPost
from app.models.instagram_hashtag import InstagramHashtag
from app.models.instagram_influencer import InstagramInfluencer


# Initialize Celery app
settings = get_settings()
celery_app = Celery(
    'k_beauty_tasks',
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

# Celery configuration
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 1 hour max per task
)


def get_active_instagram_users() -> List[User]:
    """Get all users with active Instagram connections"""
    db = SessionLocal()
    try:
        # Get users with valid Instagram tokens
        now = datetime.utcnow()
        users = db.query(User).filter(
            User.instagram_access_token.isnot(None),
            User.instagram_token_expires_at > now,
            User.is_active == True
        ).all()
        return users
    finally:
        db.close()


async def collect_user_instagram_data(user: User, db: Session):
    """
    Collect Instagram data for a specific user
    
    Args:
        user: User object with Instagram connection
        db: Database session
    """
    try:
        # Initialize Instagram service with user's token
        service = InstagramService(db, access_token=user.instagram_access_token)
        
        if not service.api_client:
            print(f"⚠️  User {user.id} - No API client available")
            return
        
        api_client = service.api_client
        
        # Step 1: Get user's Instagram profile
        instagram_user = await api_client.get_user_profile(user.instagram_user_id)
        print(f"✅ User {user.id} - Profile: @{instagram_user.username}")
        
        # Step 2: Collect user's recent posts
        media_list = await api_client.get_user_media(
            user.instagram_user_id,
            limit=50
        )
        print(f"✅ User {user.id} - Collected {len(media_list)} posts")
        
        # Step 3: Save posts to database
        for media in media_list:
            # Check if post already exists
            existing_post = db.query(InstagramPost).filter(
                InstagramPost.instagram_id == media.id
            ).first()
            
            if not existing_post:
                # Create new post
                post = InstagramPost(
                    instagram_id=media.id,
                    username=instagram_user.username,
                    caption=media.caption or "",
                    like_count=media.like_count or 0,
                    comment_count=media.comments_count or 0,
                    media_url=media.media_url,
                    timestamp=media.timestamp,
                    hashtags=extract_hashtags(media.caption or ""),
                    market="unknown",  # Would be determined by user's target market
                    category="beauty",  # Default category
                    engagement_rate=calculate_engagement_rate(
                        media.like_count or 0,
                        media.comments_count or 0,
                        instagram_user.media_count or 1
                    )
                )
                db.add(post)
            else:
                # Update existing post metrics
                existing_post.like_count = media.like_count or 0
                existing_post.comment_count = media.comments_count or 0
                existing_post.engagement_rate = calculate_engagement_rate(
                    media.like_count or 0,
                    media.comments_count or 0,
                    instagram_user.media_count or 1
                )
        
        db.commit()
        print(f"✅ User {user.id} - Data saved to database")
        
        # Close API client
        await api_client.close()
        
    except InstagramAPIError as e:
        print(f"❌ User {user.id} - Instagram API Error: {e.message}")
        # Handle specific errors
        if e.code == 190:  # Token expired
            user.instagram_access_token = None
            db.commit()
            print(f"⚠️  User {user.id} - Token expired and removed")
    
    except Exception as e:
        print(f"❌ User {user.id} - Unexpected error: {str(e)}")


def extract_hashtags(caption: str) -> List[str]:
    """Extract hashtags from caption text"""
    words = caption.split()
    hashtags = [word[1:] for word in words if word.startswith('#')]
    return hashtags[:10]  # Limit to 10 hashtags


def calculate_engagement_rate(likes: int, comments: int, followers: int) -> float:
    """Calculate engagement rate"""
    if followers == 0:
        return 0.0
    engagement = ((likes + comments) / followers) * 100
    return round(engagement, 2)


# ========== Celery Tasks ==========

@celery_app.task(name="collect_instagram_posts")
def collect_instagram_posts():
    """
    Collect Instagram posts for all active users
    
    Runs every 6 hours
    """
    print("🚀 Starting Instagram post collection...")
    
    users = get_active_instagram_users()
    print(f"📊 Found {len(users)} active Instagram users")
    
    db = SessionLocal()
    try:
        for user in users:
            try:
                # Run async function in sync context
                asyncio.run(collect_user_instagram_data(user, db))
            except Exception as e:
                print(f"❌ Failed to collect data for user {user.id}: {str(e)}")
                continue
        
        print("✅ Instagram post collection completed")
        
    finally:
        db.close()
    
    return {
        "success": True,
        "users_processed": len(users),
        "timestamp": datetime.utcnow().isoformat()
    }


@celery_app.task(name="update_hashtag_trends")
def update_hashtag_trends():
    """
    Update hashtag trend scores
    
    Runs every 12 hours
    """
    print("🚀 Starting hashtag trend update...")
    
    db = SessionLocal()
    try:
        # Get all tracked hashtags
        hashtags = db.query(InstagramHashtag).all()
        print(f"📊 Updating {len(hashtags)} hashtags")
        
        for hashtag in hashtags:
            # Recalculate trend scores
            hashtag.update_trend_status()
        
        db.commit()
        print("✅ Hashtag trends updated")
        
        return {
            "success": True,
            "hashtags_updated": len(hashtags),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    finally:
        db.close()


@celery_app.task(name="refresh_expiring_tokens")
def refresh_expiring_tokens():
    """
    Refresh Instagram tokens that are expiring soon (within 7 days)
    
    Runs daily
    """
    print("🚀 Starting token refresh check...")
    
    db = SessionLocal()
    try:
        # Get users with tokens expiring in next 7 days
        expire_threshold = datetime.utcnow() + timedelta(days=7)
        users = db.query(User).filter(
            User.instagram_access_token.isnot(None),
            User.instagram_token_expires_at < expire_threshold,
            User.instagram_token_expires_at > datetime.utcnow()
        ).all()
        
        print(f"📊 Found {len(users)} users with expiring tokens")
        
        refreshed_count = 0
        for user in users:
            try:
                # Create API client
                client = InstagramGraphAPI(user.instagram_access_token)
                
                # Refresh token
                async def refresh():
                    result = await client.refresh_long_lived_token(user.instagram_access_token)
                    await client.close()
                    return result
                
                new_token_data = asyncio.run(refresh())
                
                # Update user record
                user.instagram_access_token = new_token_data["access_token"]
                expires_in = new_token_data.get("expires_in", 5184000)
                user.instagram_token_expires_at = datetime.utcnow() + timedelta(seconds=expires_in)
                
                db.commit()
                refreshed_count += 1
                print(f"✅ User {user.id} - Token refreshed")
                
            except Exception as e:
                print(f"❌ User {user.id} - Failed to refresh token: {str(e)}")
                continue
        
        print(f"✅ Token refresh completed: {refreshed_count}/{len(users)} successful")
        
        return {
            "success": True,
            "total_users": len(users),
            "refreshed": refreshed_count,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    finally:
        db.close()


@celery_app.task(name="cleanup_old_data")
def cleanup_old_data():
    """
    Clean up old Instagram data (older than 90 days)
    
    Runs weekly
    """
    print("🚀 Starting data cleanup...")
    
    db = SessionLocal()
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=90)
        
        # Delete old posts
        deleted_posts = db.query(InstagramPost).filter(
            InstagramPost.timestamp < cutoff_date
        ).delete()
        
        db.commit()
        print(f"✅ Deleted {deleted_posts} old posts")
        
        return {
            "success": True,
            "deleted_posts": deleted_posts,
            "cutoff_date": cutoff_date.isoformat(),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    finally:
        db.close()


# ========== Celery Beat Schedule ==========

celery_app.conf.beat_schedule = {
    # Collect Instagram posts every 6 hours
    'collect-posts-every-6-hours': {
        'task': 'collect_instagram_posts',
        'schedule': crontab(hour='*/6'),
    },
    
    # Update hashtag trends every 12 hours
    'update-hashtags-every-12-hours': {
        'task': 'update_hashtag_trends',
        'schedule': crontab(hour='*/12'),
    },
    
    # Refresh expiring tokens daily at 2 AM
    'refresh-tokens-daily': {
        'task': 'refresh_expiring_tokens',
        'schedule': crontab(hour=2, minute=0),
    },
    
    # Clean up old data weekly on Sunday at 3 AM
    'cleanup-old-data-weekly': {
        'task': 'cleanup_old_data',
        'schedule': crontab(hour=3, minute=0, day_of_week=0),
    },
}


if __name__ == "__main__":
    # Test task execution
    print("Testing Instagram collector tasks...")
    
    # Run collection task
    result = collect_instagram_posts()
    print(f"Collection result: {result}")
    
    # Run hashtag update task
    result = update_hashtag_trends()
    print(f"Hashtag update result: {result}")
