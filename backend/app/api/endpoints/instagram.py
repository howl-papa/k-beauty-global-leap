"""
Instagram API Endpoints

Provides access to Instagram data, insights, and analytics.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.api.dependencies.auth import get_current_active_user
from app.models.user import User
from app.services.instagram_service import InstagramService
from app.schemas.instagram import (
    InstagramPostResponse,
    InstagramHashtagResponse,
    InstagramInfluencerResponse,
    MarketInsightsResponse,
    PostAnalyticsResponse
)

router = APIRouter()


@router.get("/posts", response_model=List[InstagramPostResponse])
async def get_instagram_posts(
    market: str = Query(..., description="Target market (germany, france, japan)"),
    hashtag: Optional[str] = Query(None, description="Filter by hashtag"),
    category: Optional[str] = Query(None, description="Filter by category (skincare, makeup, haircare)"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of results"),
    min_engagement: Optional[float] = Query(None, ge=0, description="Minimum engagement rate"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Search Instagram posts by market and filters
    
    Returns posts matching the specified criteria, ordered by engagement rate.
    """
    service = InstagramService(db)
    posts = await service.search_posts(
        market=market,
        hashtag=hashtag,
        category=category,
        limit=limit,
        min_engagement=min_engagement
    )
    
    return posts


@router.get("/posts/{post_id}", response_model=InstagramPostResponse)
async def get_instagram_post(
    post_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get single Instagram post by ID"""
    service = InstagramService(db)
    post = await service.get_post_by_id(post_id)
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Instagram post not found"
        )
    
    return post


@router.get("/posts/analyze", response_model=PostAnalyticsResponse)
async def analyze_posts(
    market: str = Query(..., description="Target market"),
    hashtag: Optional[str] = Query(None, description="Filter by hashtag"),
    category: Optional[str] = Query(None, description="Filter by category"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Analyze engagement patterns for posts matching criteria
    
    Returns aggregated metrics including:
    - Average engagement rate
    - Top hashtags
    - Peak posting times
    - Total likes/comments
    """
    service = InstagramService(db)
    posts = await service.search_posts(
        market=market,
        hashtag=hashtag,
        category=category,
        limit=100
    )
    
    analytics = await service.analyze_post_engagement(posts)
    
    return analytics


@router.get("/hashtags/trending", response_model=List[InstagramHashtagResponse])
async def get_trending_hashtags(
    market: str = Query(..., description="Target market"),
    limit: int = Query(20, ge=1, le=50, description="Maximum number of results"),
    min_trend_score: float = Query(60.0, ge=0, le=100, description="Minimum trend score"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get trending hashtags for a specific market
    
    Returns hashtags with trend_score >= min_trend_score, ordered by trend score.
    """
    service = InstagramService(db)
    hashtags = await service.get_trending_hashtags(
        market=market,
        limit=limit,
        min_trend_score=min_trend_score
    )
    
    return hashtags


@router.get("/hashtags/suggestions", response_model=List[InstagramHashtagResponse])
async def get_hashtag_suggestions(
    market: str = Query(..., description="Target market"),
    category: str = Query("beauty", description="Category filter"),
    difficulty: str = Query("low", description="Competition level (low, medium, high)"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get hashtag suggestions based on competition level
    
    Useful for campaign planning - suggests hashtags with good engagement
    but lower competition.
    """
    service = InstagramService(db)
    suggestions = await service.get_hashtag_suggestions(
        market=market,
        category=category,
        difficulty=difficulty
    )
    
    return suggestions


@router.get("/hashtags/{name}", response_model=InstagramHashtagResponse)
async def get_hashtag_details(
    name: str,
    market: str = Query(..., description="Target market"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get detailed information about a specific hashtag"""
    service = InstagramService(db)
    hashtag = await service.get_hashtag_by_name(name=name, market=market)
    
    if not hashtag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hashtag '{name}' not found in {market} market"
        )
    
    return hashtag


@router.get("/influencers", response_model=List[InstagramInfluencerResponse])
async def find_influencers(
    market: str = Query(..., description="Target market"),
    min_followers: int = Query(10000, ge=1000, description="Minimum follower count"),
    max_followers: int = Query(500000, le=10000000, description="Maximum follower count"),
    min_engagement: float = Query(3.0, ge=0, description="Minimum engagement rate"),
    min_authenticity: float = Query(70.0, ge=0, le=100, description="Minimum authenticity score"),
    category: Optional[str] = Query(None, description="Filter by category"),
    limit: int = Query(20, ge=1, le=50, description="Maximum number of results"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Find influencers matching criteria
    
    Returns influencers within specified follower range and quality thresholds,
    ordered by collaboration score.
    
    Perfect for finding micro-influencers for partnerships.
    """
    service = InstagramService(db)
    influencers = await service.find_influencers(
        market=market,
        min_followers=min_followers,
        max_followers=max_followers,
        min_engagement=min_engagement,
        min_authenticity=min_authenticity,
        category=category,
        limit=limit
    )
    
    return influencers


@router.get("/influencers/{username}", response_model=InstagramInfluencerResponse)
async def get_influencer_details(
    username: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get detailed information about a specific influencer"""
    service = InstagramService(db)
    influencer = await service.get_influencer_by_username(username=username)
    
    if not influencer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Influencer '@{username}' not found"
        )
    
    return influencer


@router.patch("/influencers/{influencer_id}/status")
async def update_influencer_status(
    influencer_id: int,
    status: str = Query(..., description="New status (discovered, contacted, negotiating, partnered, rejected)"),
    notes: Optional[str] = Query(None, description="Contact notes"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update influencer partnership status
    
    Use this to track outreach progress and partnership negotiations.
    """
    valid_statuses = ["discovered", "contacted", "negotiating", "partnered", "rejected"]
    if status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
        )
    
    service = InstagramService(db)
    influencer = await service.update_influencer_status(
        influencer_id=influencer_id,
        status=status,
        notes=notes
    )
    
    if not influencer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Influencer not found"
        )
    
    return {
        "success": True,
        "influencer_id": influencer_id,
        "status": status,
        "message": f"Status updated to '{status}'"
    }


@router.get("/insights/{market}", response_model=MarketInsightsResponse)
async def get_market_insights(
    market: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get comprehensive market insights
    
    Returns aggregated analytics including:
    - Post engagement trends
    - Trending hashtags
    - Top influencers
    - Optimal posting times
    
    This is the main endpoint for market analysis dashboard.
    """
    valid_markets = ["germany", "france", "japan"]
    if market not in valid_markets:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid market. Must be one of: {', '.join(valid_markets)}"
        )
    
    service = InstagramService(db)
    insights = await service.get_market_insights(market=market)
    
    return insights


@router.post("/import-mock-data")
async def import_mock_data(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Import mock Instagram data from JSON file
    
    This endpoint is used for development/testing to populate the database
    with realistic mock data.
    
    **Note**: Only use this in development environment!
    """
    service = InstagramService(db)
    
    # Check if data already exists
    existing_posts = db.query(InstagramPost).count()
    if existing_posts > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Database already contains {existing_posts} posts. Clear database first."
        )
    
    # Import from JSON file
    json_file_path = "backend/scripts/mock_instagram_data.json"
    
    try:
        result = await service.import_mock_data(json_file_path)
        return result
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mock data file not found. Run generate_mock_instagram_data.py first."
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to import mock data: {str(e)}"
        )
