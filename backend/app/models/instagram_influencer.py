"""
Instagram Influencer Model

Tracks influencers/content creators for partnership opportunities.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, JSON
from datetime import datetime

from app.core.database import Base


class InstagramInfluencer(Base):
    """Instagram Influencer Model
    
    Stores influencer profile data and metrics for partnership evaluation.
    Focuses on micro-influencers (10k-500k followers) for cost-effective partnerships.
    """
    __tablename__ = "instagram_influencers"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String, unique=True, index=True, nullable=False)  # Instagram user ID
    
    # Profile Information
    username = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    biography = Column(Text, nullable=True)
    profile_picture_url = Column(String, nullable=True)
    website = Column(String, nullable=True)
    
    # Account Type
    is_verified = Column(Boolean, default=False)  # Blue checkmark
    is_business_account = Column(Boolean, default=False)
    is_private = Column(Boolean, default=False)
    
    # Follower Metrics
    followers_count = Column(Integer, default=0, index=True)
    following_count = Column(Integer, default=0)
    media_count = Column(Integer, default=0)  # Total posts
    
    # Engagement Metrics
    avg_likes = Column(Float, default=0.0)
    avg_comments = Column(Float, default=0.0)
    avg_views = Column(Float, nullable=True)  # For video content
    engagement_rate = Column(Float, default=0.0, index=True)  # (likes + comments) / followers * 100
    
    # Posting Behavior
    posts_per_week = Column(Float, default=0.0)
    best_posting_times = Column(JSON, default=list)  # ["18:00", "20:00"]
    content_types = Column(JSON, default=dict)  # {"IMAGE": 0.6, "VIDEO": 0.3, "CAROUSEL": 0.1}
    
    # Category & Market
    category = Column(String, index=True, nullable=True)  # "beauty", "skincare", "makeup"
    sub_categories = Column(JSON, default=list)  # ["kbeauty", "skincare", "antiaging"]
    market = Column(String, index=True, nullable=False)  # "germany", "france", "japan"
    languages = Column(JSON, default=list)  # ["de", "en"]
    
    # Audience Demographics (if available)
    audience_country_top = Column(String, nullable=True)  # Top audience country
    audience_gender_split = Column(JSON, nullable=True)  # {"male": 0.3, "female": 0.7}
    audience_age_range = Column(String, nullable=True)  # "25-34"
    
    # Quality Scores (AI-generated)
    authenticity_score = Column(Float, default=0.0, index=True)  # 0-100, fake follower detection
    brand_affinity_score = Column(Float, default=0.0)  # 0-100, K-Beauty relevance
    content_quality_score = Column(Float, default=0.0)  # 0-100, visual quality
    collaboration_score = Column(Float, default=0.0)  # 0-100, likelihood of partnership
    
    # Partnership Potential
    estimated_post_cost = Column(Float, nullable=True)  # USD per post
    estimated_story_cost = Column(Float, nullable=True)  # USD per story
    partnership_tier = Column(String, nullable=True)  # "nano", "micro", "mid", "macro"
    has_branded_content = Column(Boolean, default=False)  # Has sponsored posts
    
    # Contact Information
    email = Column(String, nullable=True)
    contact_notes = Column(Text, nullable=True)  # Internal notes
    
    # Status
    status = Column(String, default="discovered")  # "discovered", "contacted", "negotiating", "partnered", "rejected"
    
    # Tracking Metadata
    last_scraped_at = Column(DateTime, nullable=True)
    data_source = Column(String, default="mock")  # "instagram_api", "apify", "mock"
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<InstagramInfluencer(id={self.id}, username={self.username}, followers={self.followers_count})>"
    
    @property
    def follower_tier(self) -> str:
        """Categorize influencer by follower count"""
        if self.followers_count < 10000:
            return "nano"
        elif self.followers_count < 100000:
            return "micro"
        elif self.followers_count < 500000:
            return "mid"
        elif self.followers_count < 1000000:
            return "macro"
        else:
            return "mega"
    
    def calculate_engagement_rate(self) -> float:
        """Calculate engagement rate"""
        if self.followers_count == 0:
            return 0.0
        total_engagement = (self.avg_likes or 0) + (self.avg_comments or 0)
        return (total_engagement / self.followers_count) * 100
    
    def estimate_partnership_cost(self) -> dict:
        """
        Estimate partnership costs based on followers and engagement
        
        Formula:
        - Post: $10-20 per 1000 followers for micro-influencers
        - Story: 50% of post cost
        - Adjusted by engagement rate
        """
        base_cost_per_1k = 15  # USD
        follower_thousands = self.followers_count / 1000
        
        # Adjust by engagement rate
        engagement_multiplier = 1.0
        if self.engagement_rate > 5.0:
            engagement_multiplier = 1.5  # High engagement = premium
        elif self.engagement_rate < 2.0:
            engagement_multiplier = 0.7  # Low engagement = discount
        
        post_cost = follower_thousands * base_cost_per_1k * engagement_multiplier
        story_cost = post_cost * 0.5
        
        return {
            "post_cost": round(post_cost, 2),
            "story_cost": round(story_cost, 2),
            "currency": "USD"
        }
    
    def calculate_quality_scores(self):
        """Calculate AI-based quality scores"""
        # Authenticity Score (fake follower detection)
        # Higher engagement rate = more authentic
        if self.engagement_rate > 5.0:
            self.authenticity_score = 90.0
        elif self.engagement_rate > 3.0:
            self.authenticity_score = 75.0
        elif self.engagement_rate > 1.0:
            self.authenticity_score = 60.0
        else:
            self.authenticity_score = 40.0  # Suspicious
        
        # Update costs
        costs = self.estimate_partnership_cost()
        self.estimated_post_cost = costs["post_cost"]
        self.estimated_story_cost = costs["story_cost"]
        self.partnership_tier = self.follower_tier
