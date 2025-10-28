"""
AI Analysis API Endpoints

Endpoints for AI-powered analysis features:
- Sentiment analysis
- Trend prediction
- Content quality evaluation
- Influencer authenticity
- Cultural fit assessment
- Performance prediction
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Dict, Optional
from pydantic import BaseModel

from app.core.database import get_db
from app.api.endpoints.auth import get_current_user
from app.models.user import User
from app.models.instagram_post import InstagramPost
from app.models.instagram_hashtag import InstagramHashtag
from app.models.instagram_influencer import InstagramInfluencer
from app.services.ai_analyzer import AIAnalyzer
from app.services.ai_analyzer_extended import AIAnalyzerExtended


router = APIRouter()


# ========== Request/Response Models ==========

class SentimentAnalysisRequest(BaseModel):
    market: str
    limit: int = 50
    hashtag: Optional[str] = None


class TrendAnalysisRequest(BaseModel):
    market: str
    limit: int = 20
    time_period: str = "recent"


class ContentQualityRequest(BaseModel):
    post_id: int
    detailed: bool = True


class AuthenticityAnalysisRequest(BaseModel):
    influencer_id: int
    include_recent_posts: bool = True


class CulturalFitRequest(BaseModel):
    content: Dict
    target_market: str


class PerformancePredictionRequest(BaseModel):
    draft_content: Dict
    market: str
    include_historical: bool = True


# ========== Sentiment Analysis Endpoints ==========

@router.post("/sentiment")
async def analyze_sentiment(
    request: SentimentAnalysisRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Analyze sentiment of Instagram posts
    
    Returns overall sentiment, key themes, and consumer insights
    """
    try:
        analyzer = AIAnalyzer(db)
        
        # Get posts
        query = db.query(InstagramPost).filter(InstagramPost.market == request.market)
        
        if request.hashtag:
            query = query.filter(InstagramPost.hashtags.contains([request.hashtag]))
        
        posts = query.limit(request.limit).all()
        
        if not posts:
            raise HTTPException(
                status_code=404,
                detail=f"No posts found for market '{request.market}'"
            )
        
        # Perform analysis
        analysis = await analyzer.analyze_post_sentiment(posts, request.market)
        
        return {
            "success": True,
            "analysis": analysis
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sentiment/{market}")
async def get_market_sentiment(
    market: str,
    hashtag: Optional[str] = None,
    limit: int = Query(50, ge=10, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Quick sentiment analysis endpoint (GET)"""
    try:
        analyzer = AIAnalyzer(db)
        
        query = db.query(InstagramPost).filter(InstagramPost.market == market)
        if hashtag:
            query = query.filter(InstagramPost.hashtags.contains([hashtag]))
        
        posts = query.limit(limit).all()
        
        if not posts:
            return {
                "success": True,
                "message": f"No posts found for market '{market}'",
                "analysis": None
            }
        
        analysis = await analyzer.analyze_post_sentiment(posts, market)
        
        return {
            "success": True,
            "analysis": analysis
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ========== Trend Analysis Endpoints ==========

@router.post("/trends")
async def analyze_trends(
    request: TrendAnalysisRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Analyze trends and predict future movements
    
    Returns emerging trends, predictions, and marketing recommendations
    """
    try:
        analyzer = AIAnalyzer(db)
        
        # Get trending hashtags
        hashtags = db.query(InstagramHashtag).filter(
            InstagramHashtag.market == request.market,
            InstagramHashtag.is_trending == True
        ).order_by(InstagramHashtag.trend_score.desc()).limit(request.limit).all()
        
        if not hashtags:
            raise HTTPException(
                status_code=404,
                detail=f"No trending hashtags found for market '{request.market}'"
            )
        
        # Perform trend analysis
        insights = await analyzer.generate_trend_insights(
            hashtags,
            request.market,
            request.time_period
        )
        
        return {
            "success": True,
            "insights": insights
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trends/{market}")
async def get_market_trends(
    market: str,
    limit: int = Query(20, ge=5, le=50),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Quick trend analysis endpoint (GET)"""
    try:
        analyzer = AIAnalyzer(db)
        
        hashtags = db.query(InstagramHashtag).filter(
            InstagramHashtag.market == market,
            InstagramHashtag.is_trending == True
        ).order_by(InstagramHashtag.trend_score.desc()).limit(limit).all()
        
        if not hashtags:
            return {
                "success": True,
                "message": f"No trending hashtags for market '{market}'",
                "insights": None
            }
        
        insights = await analyzer.generate_trend_insights(hashtags, market, "recent")
        
        return {
            "success": True,
            "insights": insights
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ========== Content Quality Endpoints ==========

@router.post("/quality")
async def evaluate_content_quality(
    request: ContentQualityRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Evaluate content quality of a post
    
    Returns quality scores and improvement suggestions
    """
    try:
        analyzer = AIAnalyzerExtended(db)
        
        # Get post
        post = db.query(InstagramPost).filter(InstagramPost.id == request.post_id).first()
        
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        
        # Perform quality evaluation
        evaluation = await analyzer.evaluate_content_quality(post, request.detailed)
        
        return {
            "success": True,
            "evaluation": evaluation
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/quality/{post_id}")
async def get_post_quality(
    post_id: int,
    detailed: bool = True,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Quick quality evaluation endpoint (GET)"""
    try:
        analyzer = AIAnalyzerExtended(db)
        
        post = db.query(InstagramPost).filter(InstagramPost.id == post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        
        evaluation = await analyzer.evaluate_content_quality(post, detailed)
        
        return {
            "success": True,
            "evaluation": evaluation
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ========== Influencer Authenticity Endpoints ==========

@router.post("/authenticity")
async def analyze_influencer_authenticity(
    request: AuthenticityAnalysisRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Analyze influencer authenticity
    
    Returns authenticity scores and partnership recommendations
    """
    try:
        analyzer = AIAnalyzerExtended(db)
        
        # Get influencer
        influencer = db.query(InstagramInfluencer).filter(
            InstagramInfluencer.id == request.influencer_id
        ).first()
        
        if not influencer:
            raise HTTPException(status_code=404, detail="Influencer not found")
        
        # Get recent posts if requested
        recent_posts = None
        if request.include_recent_posts:
            recent_posts = db.query(InstagramPost).filter(
                InstagramPost.username == influencer.username
            ).order_by(InstagramPost.timestamp.desc()).limit(10).all()
        
        # Perform authenticity analysis
        analysis = await analyzer.analyze_influencer_authenticity(influencer, recent_posts)
        
        return {
            "success": True,
            "analysis": analysis
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/authenticity/{influencer_id}")
async def get_influencer_authenticity(
    influencer_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Quick authenticity check endpoint (GET)"""
    try:
        analyzer = AIAnalyzerExtended(db)
        
        influencer = db.query(InstagramInfluencer).filter(
            InstagramInfluencer.id == influencer_id
        ).first()
        
        if not influencer:
            raise HTTPException(status_code=404, detail="Influencer not found")
        
        recent_posts = db.query(InstagramPost).filter(
            InstagramPost.username == influencer.username
        ).order_by(InstagramPost.timestamp.desc()).limit(10).all()
        
        analysis = await analyzer.analyze_influencer_authenticity(influencer, recent_posts)
        
        return {
            "success": True,
            "analysis": analysis
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ========== Cultural Fit Endpoints ==========

@router.post("/cultural-fit")
async def analyze_cultural_fit(
    request: CulturalFitRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Analyze cultural appropriateness for target market
    
    Returns cultural fit scores and localization recommendations
    """
    try:
        analyzer = AIAnalyzerExtended(db)
        
        # Validate market
        valid_markets = ["germany", "france", "japan"]
        if request.target_market not in valid_markets:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid market. Choose from: {', '.join(valid_markets)}"
            )
        
        # Perform cultural fit analysis
        analysis = await analyzer.analyze_cultural_fit(
            request.content,
            request.target_market
        )
        
        return {
            "success": True,
            "analysis": analysis
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ========== Performance Prediction Endpoints ==========

@router.post("/predict-performance")
async def predict_post_performance(
    request: PerformancePredictionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Predict performance of draft post before publishing
    
    Returns predicted metrics and optimization suggestions
    """
    try:
        analyzer = AIAnalyzerExtended(db)
        
        # Get historical data if requested
        historical_data = None
        if request.include_historical:
            historical_data = db.query(InstagramPost).filter(
                InstagramPost.market == request.market
            ).order_by(InstagramPost.timestamp.desc()).limit(30).all()
        
        # Perform prediction
        prediction = await analyzer.predict_post_performance(
            request.draft_content,
            request.market,
            historical_data
        )
        
        return {
            "success": True,
            "prediction": prediction
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ========== Market Entry Recommendations ==========

@router.get("/market-entry/{market}")
async def get_market_entry_recommendations(
    market: str,
    category: str = "beauty",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get comprehensive market entry recommendations
    
    Returns market assessment, strategy, and go-to-market plan
    """
    try:
        analyzer = AIAnalyzer(db)
        
        # Get brand profile from user data
        brand_profile = {
            "company_name": current_user.company_name,
            "type": "small_kbeauty_brand"
        }
        
        # Generate recommendations
        recommendations = await analyzer.generate_market_entry_recommendations(
            market,
            category,
            brand_profile
        )
        
        return {
            "success": True,
            "recommendations": recommendations
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ========== Batch Analysis Endpoints ==========

@router.post("/batch-analyze")
async def batch_analyze_posts(
    post_ids: list[int],
    analysis_type: str = Query(..., regex="^(sentiment|quality|all)$"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Analyze multiple posts at once
    
    Analysis types: sentiment, quality, all
    """
    if len(post_ids) > 20:
        raise HTTPException(
            status_code=400,
            detail="Maximum 20 posts per batch analysis"
        )
    
    try:
        analyzer = AIAnalyzer(db)
        analyzer_ext = AIAnalyzerExtended(db)
        
        results = []
        
        for post_id in post_ids:
            post = db.query(InstagramPost).filter(InstagramPost.id == post_id).first()
            
            if not post:
                results.append({
                    "post_id": post_id,
                    "error": "Post not found"
                })
                continue
            
            post_result = {"post_id": post_id}
            
            if analysis_type in ["sentiment", "all"]:
                sentiment = await analyzer.analyze_post_sentiment([post], post.market)
                post_result["sentiment"] = sentiment
            
            if analysis_type in ["quality", "all"]:
                quality = await analyzer_ext.evaluate_content_quality(post, detailed=False)
                post_result["quality"] = quality
            
            results.append(post_result)
        
        return {
            "success": True,
            "analyzed_count": len(results),
            "results": results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
