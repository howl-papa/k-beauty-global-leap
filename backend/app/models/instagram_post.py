"""
Instagram Post Model

Stores Instagram post data for market trend analysis.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Float, JSON, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class InstagramPost(Base):
    """Instagram Post Model
    
    Stores individual Instagram posts collected for market analysis.
    Includes content, metadata, metrics, and analysis results.
    """
    __tablename__ = "instagram_posts"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String, unique=True, index=True, nullable=False)  # Instagram post ID
    
    # Content
    caption = Column(Text, nullable=True)  # Post caption text
    media_type = Column(String, nullable=False)  # IMAGE, VIDEO, CAROUSEL_ALBUM
    media_url = Column(String, nullable=True)  # Primary media URL
    thumbnail_url = Column(String, nullable=True)  # Thumbnail for videos
    permalink = Column(String, nullable=True)  # Link to Instagram post
    
    # Author Information
    username = Column(String, index=True, nullable=False)  # Instagram username
    user_id = Column(String, nullable=True)  # Instagram user ID
    
    # Metadata
    timestamp = Column(DateTime, index=True, nullable=False)  # Post creation time
    location = Column(String, nullable=True)  # Location name (if tagged)
    location_id = Column(String, nullable=True)  # Location ID
    
    # Metrics (Engagement)
    like_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    save_count = Column(Integer, nullable=True)  # Only available via Instagram Insights API
    share_count = Column(Integer, nullable=True)
    reach = Column(Integer, nullable=True)  # Unique accounts reached
    impressions = Column(Integer, nullable=True)  # Total views
    
    # Calculated Metrics
    engagement_rate = Column(Float, default=0.0)  # (likes + comments) / followers * 100
    
    # Analysis Fields
    hashtags = Column(JSON, default=list)  # ["kbeauty", "skincare", "koreanbeauty"]
    mentions = Column(JSON, default=list)  # ["@brand", "@influencer"]
    market = Column(String, index=True, nullable=False)  # "germany", "france", "japan"
    category = Column(String, index=True, nullable=True)  # "skincare", "makeup", "haircare"
    
    # AI Analysis Results (populated later)
    sentiment_score = Column(Float, nullable=True)  # -1.0 to 1.0
    sentiment_label = Column(String, nullable=True)  # "positive", "negative", "neutral"
    detected_products = Column(JSON, default=list)  # AI-detected products
    detected_brands = Column(JSON, default=list)  # AI-detected brands
    
    # Quality Flags
    is_sponsored = Column(Boolean, default=False)  # Ad detection
    is_verified_account = Column(Boolean, default=False)  # Blue checkmark
    
    # Relationships
    analysis_id = Column(Integer, ForeignKey("analyses.id"), nullable=True)
    analysis = relationship("Analysis", back_populates="instagram_posts")
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<InstagramPost(id={self.id}, external_id={self.external_id}, username={self.username})>"
    
    @property
    def total_engagement(self) -> int:
        """Total engagement (likes + comments)"""
        return (self.like_count or 0) + (self.comment_count or 0)
    
    def calculate_engagement_rate(self, follower_count: int) -> float:
        """Calculate engagement rate based on follower count"""
        if follower_count == 0:
            return 0.0
        return (self.total_engagement / follower_count) * 100
