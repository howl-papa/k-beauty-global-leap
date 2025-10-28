"""
Instagram Hashtag Model

Tracks hashtag trends and performance metrics across different markets.
"""

from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, Index
from datetime import datetime

from app.core.database import Base


class InstagramHashtag(Base):
    """Instagram Hashtag Model
    
    Tracks hashtag performance and trends across different markets.
    Used for identifying trending topics and optimal hashtags for campaigns.
    """
    __tablename__ = "instagram_hashtags"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String, unique=True, index=True, nullable=False)  # Instagram hashtag ID
    
    # Hashtag Information
    name = Column(String, index=True, nullable=False)  # "kbeauty" (without #)
    display_name = Column(String, nullable=True)  # "#KBeauty" (with formatting)
    market = Column(String, index=True, nullable=False)  # "germany", "france", "japan"
    category = Column(String, index=True, nullable=True)  # "beauty", "skincare", "makeup"
    
    # Metrics
    post_count = Column(Integer, default=0)  # Total posts with this hashtag
    avg_likes = Column(Float, default=0.0)  # Average likes per post
    avg_comments = Column(Float, default=0.0)  # Average comments per post
    avg_engagement = Column(Float, default=0.0)  # Average engagement rate
    
    # Trend Analysis
    growth_rate = Column(Float, default=0.0)  # % change week-over-week
    velocity = Column(Float, default=0.0)  # Posts per hour
    is_trending = Column(Boolean, default=False)  # Currently trending flag
    trend_score = Column(Float, default=0.0)  # 0-100 composite score
    peak_trend_date = Column(DateTime, nullable=True)  # When it peaked
    
    # Competition
    competition_level = Column(String, nullable=True)  # "low", "medium", "high"
    difficulty_score = Column(Float, default=0.0)  # 0-100, how hard to rank
    
    # Related Hashtags (JSON array of strings)
    # related_hashtags = Column(JSON, default=list)  # ["koreanbeauty", "skincare"]
    
    # Tracking Metadata
    tracked_at = Column(DateTime, default=datetime.utcnow, index=True)  # When data was collected
    data_source = Column(String, default="mock")  # "instagram_api", "apify", "mock"
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Composite Indexes for efficient queries
    __table_args__ = (
        Index('idx_hashtag_market_trending', 'market', 'is_trending'),
        Index('idx_hashtag_market_score', 'market', 'trend_score'),
        Index('idx_hashtag_tracked_at', 'tracked_at'),
    )
    
    def __repr__(self):
        return f"<InstagramHashtag(id={self.id}, name={self.name}, market={self.market})>"
    
    @property
    def formatted_name(self) -> str:
        """Return hashtag with # prefix"""
        return f"#{self.name}"
    
    def calculate_trend_score(self) -> float:
        """
        Calculate composite trend score (0-100)
        
        Formula:
        - Growth rate: 40%
        - Velocity: 30%
        - Engagement: 20%
        - Post count: 10%
        """
        # Normalize metrics to 0-100 scale
        growth_component = min(abs(self.growth_rate), 100) * 0.4
        velocity_component = min(self.velocity / 10, 100) * 0.3  # Assuming max 1000 posts/hour
        engagement_component = min(self.avg_engagement, 100) * 0.2
        volume_component = min(self.post_count / 1000, 100) * 0.1  # Assuming max 100k posts
        
        return growth_component + velocity_component + engagement_component + volume_component
    
    def update_trend_status(self):
        """Update is_trending flag based on trend_score"""
        self.trend_score = self.calculate_trend_score()
        self.is_trending = self.trend_score >= 60.0  # Threshold for trending
        
        if self.is_trending and not self.peak_trend_date:
            self.peak_trend_date = datetime.utcnow()
