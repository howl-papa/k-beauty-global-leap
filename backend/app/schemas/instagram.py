"""
Instagram Pydantic Schemas

Defines request/response models for Instagram endpoints.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime


# ========== INSTAGRAM POST SCHEMAS ==========

class InstagramPostBase(BaseModel):
    """Base Instagram Post schema"""
    caption: Optional[str] = None
    media_type: str
    media_url: Optional[str] = None
    username: str
    timestamp: datetime
    market: str
    
    class Config:
        from_attributes = True


class InstagramPostResponse(InstagramPostBase):
    """Instagram Post response schema"""
    id: int
    external_id: str
    permalink: Optional[str] = None
    like_count: int = 0
    comment_count: int = 0
    engagement_rate: float = 0.0
    hashtags: List[str] = []
    mentions: List[str] = []
    category: Optional[str] = None
    sentiment_score: Optional[float] = None
    sentiment_label: Optional[str] = None
    detected_products: List[str] = []
    detected_brands: List[str] = []
    is_sponsored: bool = False
    is_verified_account: bool = False
    created_at: datetime
    
    class Config:
        from_attributes = True


class PostAnalyticsResponse(BaseModel):
    """Post analytics response schema"""
    total_posts: int
    avg_engagement_rate: float
    total_likes: int
    total_comments: int
    top_hashtags: List[Dict[str, int]]
    peak_posting_times: List[str]
    avg_likes_per_post: float
    avg_comments_per_post: float


# ========== INSTAGRAM HASHTAG SCHEMAS ==========

class InstagramHashtagBase(BaseModel):
    """Base Instagram Hashtag schema"""
    name: str
    market: str
    
    class Config:
        from_attributes = True


class InstagramHashtagResponse(InstagramHashtagBase):
    """Instagram Hashtag response schema"""
    id: int
    external_id: str
    display_name: Optional[str] = None
    category: Optional[str] = None
    post_count: int = 0
    avg_likes: float = 0.0
    avg_comments: float = 0.0
    avg_engagement: float = 0.0
    growth_rate: float = 0.0
    velocity: float = 0.0
    is_trending: bool = False
    trend_score: float = 0.0
    competition_level: Optional[str] = None
    difficulty_score: float = 0.0
    tracked_at: datetime
    
    class Config:
        from_attributes = True


# ========== INSTAGRAM INFLUENCER SCHEMAS ==========

class InstagramInfluencerBase(BaseModel):
    """Base Instagram Influencer schema"""
    username: str
    market: str
    
    class Config:
        from_attributes = True


class InstagramInfluencerResponse(InstagramInfluencerBase):
    """Instagram Influencer response schema"""
    id: int
    external_id: str
    full_name: Optional[str] = None
    biography: Optional[str] = None
    profile_picture_url: Optional[str] = None
    website: Optional[str] = None
    is_verified: bool = False
    is_business_account: bool = False
    followers_count: int = 0
    following_count: int = 0
    media_count: int = 0
    avg_likes: float = 0.0
    avg_comments: float = 0.0
    engagement_rate: float = 0.0
    posts_per_week: float = 0.0
    category: Optional[str] = None
    sub_categories: List[str] = []
    languages: List[str] = []
    authenticity_score: float = 0.0
    brand_affinity_score: float = 0.0
    content_quality_score: float = 0.0
    collaboration_score: float = 0.0
    estimated_post_cost: Optional[float] = None
    estimated_story_cost: Optional[float] = None
    partnership_tier: Optional[str] = None
    has_branded_content: bool = False
    status: str = "discovered"
    
    class Config:
        from_attributes = True


# ========== MARKET INSIGHTS SCHEMAS ==========

class TrendingHashtagSummary(BaseModel):
    """Trending hashtag summary"""
    name: str
    trend_score: float
    growth_rate: float
    post_count: int


class TopInfluencerSummary(BaseModel):
    """Top influencer summary"""
    username: str
    followers: int
    engagement_rate: float
    estimated_cost: Optional[float]
    authenticity_score: float


class MarketInsightsResponse(BaseModel):
    """Market insights response schema"""
    market: str
    period: str
    post_analytics: PostAnalyticsResponse
    trending_hashtags: List[TrendingHashtagSummary]
    top_influencers: List[TopInfluencerSummary]
