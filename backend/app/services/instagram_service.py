"""
Instagram Service

Handles Instagram data collection, analysis, and insights generation.
Supports both Mock data (MVP) and Real Instagram Graph API.
"""

import json
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from datetime import datetime, timedelta

from app.models.instagram_post import InstagramPost
from app.models.instagram_hashtag import InstagramHashtag
from app.models.instagram_influencer import InstagramInfluencer
from app.core.config import get_settings
from app.integrations.instagram_api import InstagramGraphAPI, InstagramAPIError


class InstagramService:
    """
    Service for Instagram data operations
    
    Supports two modes:
    1. Mock Data Mode (USE_REAL_INSTAGRAM_API=False): Uses database mock data
    2. Real API Mode (USE_REAL_INSTAGRAM_API=True): Fetches from Instagram Graph API
    """
    
    def __init__(self, db: Session, access_token: Optional[str] = None):
        """
        Initialize Instagram Service
        
        Args:
            db: Database session
            access_token: Instagram access token (optional, for real API mode)
        """
        self.db = db
        self.settings = get_settings()
        self.use_real_api = self.settings.USE_REAL_INSTAGRAM_API
        
        # Initialize API client if using real API
        if self.use_real_api and access_token:
            self.api_client = InstagramGraphAPI(access_token)
        else:
            self.api_client = None
    
    # ========== POST OPERATIONS ==========
    
    async def search_posts(
        self,
        market: str,
        hashtag: Optional[str] = None,
        category: Optional[str] = None,
        limit: int = 50,
        min_engagement: Optional[float] = None
    ) -> List[InstagramPost]:
        """
        Search Instagram posts by market, hashtag, and filters
        
        Supports both mock data and real API fetching based on configuration.
        
        Args:
            market: Target market (germany, france, japan)
            hashtag: Filter by hashtag (optional)
            category: Filter by category (optional)
            limit: Maximum number of results
            min_engagement: Minimum engagement rate filter
            
        Returns:
            List of InstagramPost objects
        """
        # Always query from database first (caching layer)
        query = self.db.query(InstagramPost).filter(InstagramPost.market == market)
        
        if hashtag:
            # Search for hashtag in JSON array
            query = query.filter(InstagramPost.hashtags.contains([hashtag]))
        
        if category:
            query = query.filter(InstagramPost.category == category)
        
        if min_engagement:
            query = query.filter(InstagramPost.engagement_rate >= min_engagement)
        
        # Order by engagement rate (most engaging first)
        query = query.order_by(InstagramPost.engagement_rate.desc())
        
        db_posts = query.limit(limit).all()
        
        # If using real API and no recent cached data, fetch from API
        if self.use_real_api and self.api_client and len(db_posts) < limit:
            try:
                # Note: Real implementation would fetch from API here
                # For now, return cached data
                pass
            except InstagramAPIError as e:
                # Fallback to cached data on API error
                pass
        
        return db_posts
    
    async def get_post_by_id(self, post_id: int) -> Optional[InstagramPost]:
        """Get single post by ID"""
        return self.db.query(InstagramPost).filter(InstagramPost.id == post_id).first()
    
    async def create_post(self, post_data: dict) -> InstagramPost:
        """Create new Instagram post record"""
        post = InstagramPost(**post_data)
        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)
        return post
    
    async def bulk_create_posts(self, posts_data: List[dict]) -> List[InstagramPost]:
        """Bulk create Instagram posts (for mock data import)"""
        posts = [InstagramPost(**data) for data in posts_data]
        self.db.add_all(posts)
        self.db.commit()
        return posts
    
    async def analyze_post_engagement(self, posts: List[InstagramPost]) -> Dict:
        """
        Analyze engagement patterns across posts
        
        Returns aggregated metrics and insights
        """
        if not posts:
            return {
                "total_posts": 0,
                "avg_engagement_rate": 0.0,
                "total_likes": 0,
                "total_comments": 0,
                "top_hashtags": [],
                "peak_posting_times": []
            }
        
        total_likes = sum(post.like_count or 0 for post in posts)
        total_comments = sum(post.comment_count or 0 for post in posts)
        avg_engagement = sum(post.engagement_rate or 0 for post in posts) / len(posts)
        
        # Extract all hashtags
        all_hashtags = []
        for post in posts:
            all_hashtags.extend(post.hashtags or [])
        
        # Count hashtag frequency
        hashtag_counts = {}
        for tag in all_hashtags:
            hashtag_counts[tag] = hashtag_counts.get(tag, 0) + 1
        
        # Sort by frequency
        top_hashtags = sorted(hashtag_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Analyze posting times
        posting_hours = [post.timestamp.hour for post in posts if post.timestamp]
        hour_counts = {}
        for hour in posting_hours:
            hour_counts[hour] = hour_counts.get(hour, 0) + 1
        peak_hours = sorted(hour_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        peak_times = [f"{hour:02d}:00" for hour, _ in peak_hours]
        
        return {
            "total_posts": len(posts),
            "avg_engagement_rate": round(avg_engagement, 2),
            "total_likes": total_likes,
            "total_comments": total_comments,
            "top_hashtags": [{"hashtag": tag, "count": count} for tag, count in top_hashtags],
            "peak_posting_times": peak_times,
            "avg_likes_per_post": round(total_likes / len(posts), 2),
            "avg_comments_per_post": round(total_comments / len(posts), 2)
        }
    
    # ========== HASHTAG OPERATIONS ==========
    
    async def get_trending_hashtags(
        self,
        market: str,
        limit: int = 20,
        min_trend_score: float = 60.0
    ) -> List[InstagramHashtag]:
        """
        Get trending hashtags for a market
        
        Args:
            market: Target market
            limit: Maximum number of results
            min_trend_score: Minimum trend score threshold
            
        Returns:
            List of trending InstagramHashtag objects
        """
        query = self.db.query(InstagramHashtag).filter(
            and_(
                InstagramHashtag.market == market,
                InstagramHashtag.is_trending == True,
                InstagramHashtag.trend_score >= min_trend_score
            )
        ).order_by(InstagramHashtag.trend_score.desc())
        
        return query.limit(limit).all()
    
    async def get_hashtag_by_name(
        self,
        name: str,
        market: str
    ) -> Optional[InstagramHashtag]:
        """Get hashtag by name and market"""
        return self.db.query(InstagramHashtag).filter(
            and_(
                InstagramHashtag.name == name,
                InstagramHashtag.market == market
            )
        ).first()
    
    async def create_hashtag(self, hashtag_data: dict) -> InstagramHashtag:
        """Create new hashtag record"""
        hashtag = InstagramHashtag(**hashtag_data)
        hashtag.update_trend_status()  # Calculate trend score
        self.db.add(hashtag)
        self.db.commit()
        self.db.refresh(hashtag)
        return hashtag
    
    async def bulk_create_hashtags(self, hashtags_data: List[dict]) -> List[InstagramHashtag]:
        """Bulk create hashtags (for mock data import)"""
        hashtags = []
        for data in hashtags_data:
            hashtag = InstagramHashtag(**data)
            hashtag.update_trend_status()
            hashtags.append(hashtag)
        
        self.db.add_all(hashtags)
        self.db.commit()
        return hashtags
    
    async def get_hashtag_suggestions(
        self,
        market: str,
        category: str = "beauty",
        difficulty: str = "low"
    ) -> List[InstagramHashtag]:
        """
        Get hashtag suggestions based on difficulty and category
        
        Useful for recommending hashtags for campaigns
        """
        query = self.db.query(InstagramHashtag).filter(
            and_(
                InstagramHashtag.market == market,
                InstagramHashtag.category == category,
                InstagramHashtag.competition_level == difficulty
            )
        ).order_by(InstagramHashtag.avg_engagement.desc())
        
        return query.limit(15).all()
    
    # ========== INFLUENCER OPERATIONS ==========
    
    async def find_influencers(
        self,
        market: str,
        min_followers: int = 10000,
        max_followers: int = 500000,
        min_engagement: float = 3.0,
        min_authenticity: float = 70.0,
        category: Optional[str] = None,
        limit: int = 20
    ) -> List[InstagramInfluencer]:
        """
        Find influencers matching criteria
        
        Args:
            market: Target market
            min_followers: Minimum follower count
            max_followers: Maximum follower count
            min_engagement: Minimum engagement rate
            min_authenticity: Minimum authenticity score
            category: Filter by category
            limit: Maximum results
            
        Returns:
            List of InstagramInfluencer objects
        """
        query = self.db.query(InstagramInfluencer).filter(
            and_(
                InstagramInfluencer.market == market,
                InstagramInfluencer.followers_count >= min_followers,
                InstagramInfluencer.followers_count <= max_followers,
                InstagramInfluencer.engagement_rate >= min_engagement,
                InstagramInfluencer.authenticity_score >= min_authenticity
            )
        )
        
        if category:
            query = query.filter(InstagramInfluencer.category == category)
        
        # Order by collaboration score (best prospects first)
        query = query.order_by(InstagramInfluencer.collaboration_score.desc())
        
        return query.limit(limit).all()
    
    async def get_influencer_by_username(
        self,
        username: str
    ) -> Optional[InstagramInfluencer]:
        """Get influencer by username"""
        return self.db.query(InstagramInfluencer).filter(
            InstagramInfluencer.username == username
        ).first()
    
    async def create_influencer(self, influencer_data: dict) -> InstagramInfluencer:
        """Create new influencer record"""
        influencer = InstagramInfluencer(**influencer_data)
        influencer.calculate_quality_scores()  # Calculate AI scores
        self.db.add(influencer)
        self.db.commit()
        self.db.refresh(influencer)
        return influencer
    
    async def bulk_create_influencers(
        self,
        influencers_data: List[dict]
    ) -> List[InstagramInfluencer]:
        """Bulk create influencers (for mock data import)"""
        influencers = []
        for data in influencers_data:
            influencer = InstagramInfluencer(**data)
            influencer.calculate_quality_scores()
            influencers.append(influencer)
        
        self.db.add_all(influencers)
        self.db.commit()
        return influencers
    
    async def update_influencer_status(
        self,
        influencer_id: int,
        status: str,
        notes: Optional[str] = None
    ) -> InstagramInfluencer:
        """
        Update influencer partnership status
        
        Status options: discovered, contacted, negotiating, partnered, rejected
        """
        influencer = self.db.query(InstagramInfluencer).filter(
            InstagramInfluencer.id == influencer_id
        ).first()
        
        if influencer:
            influencer.status = status
            if notes:
                influencer.contact_notes = notes
            self.db.commit()
            self.db.refresh(influencer)
        
        return influencer
    
    # ========== DATA IMPORT ==========
    
    async def import_mock_data(self, json_file_path: str) -> Dict:
        """
        Import mock data from JSON file
        
        Used for initial MVP data population
        """
        with open(json_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Convert ISO datetime strings to datetime objects
        for post in data["posts"]:
            if isinstance(post["timestamp"], str):
                post["timestamp"] = datetime.fromisoformat(post["timestamp"].replace("Z", "+00:00"))
        
        for hashtag in data["hashtags"]:
            if isinstance(hashtag["tracked_at"], str):
                hashtag["tracked_at"] = datetime.fromisoformat(hashtag["tracked_at"].replace("Z", "+00:00"))
        
        for influencer in data["influencers"]:
            if isinstance(influencer["last_scraped_at"], str):
                influencer["last_scraped_at"] = datetime.fromisoformat(influencer["last_scraped_at"].replace("Z", "+00:00"))
        
        # Bulk import
        posts = await self.bulk_create_posts(data["posts"])
        hashtags = await self.bulk_create_hashtags(data["hashtags"])
        influencers = await self.bulk_create_influencers(data["influencers"])
        
        return {
            "success": True,
            "imported": {
                "posts": len(posts),
                "hashtags": len(hashtags),
                "influencers": len(influencers)
            }
        }
    
    # ========== ANALYTICS ==========
    
    async def get_market_insights(self, market: str) -> Dict:
        """
        Generate comprehensive market insights
        
        Returns aggregated analytics for a specific market
        """
        # Get recent posts (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_posts = self.db.query(InstagramPost).filter(
            and_(
                InstagramPost.market == market,
                InstagramPost.timestamp >= thirty_days_ago
            )
        ).all()
        
        # Get trending hashtags
        trending_hashtags = await self.get_trending_hashtags(market, limit=10)
        
        # Get top influencers
        top_influencers = await self.find_influencers(market, limit=10)
        
        # Analyze posts
        post_analytics = await self.analyze_post_engagement(recent_posts)
        
        return {
            "market": market,
            "period": "last_30_days",
            "post_analytics": post_analytics,
            "trending_hashtags": [
                {
                    "name": h.name,
                    "trend_score": h.trend_score,
                    "growth_rate": h.growth_rate,
                    "post_count": h.post_count
                }
                for h in trending_hashtags
            ],
            "top_influencers": [
                {
                    "username": inf.username,
                    "followers": inf.followers_count,
                    "engagement_rate": inf.engagement_rate,
                    "estimated_cost": inf.estimated_post_cost,
                    "authenticity_score": inf.authenticity_score
                }
                for inf in top_influencers
            ]
        }
