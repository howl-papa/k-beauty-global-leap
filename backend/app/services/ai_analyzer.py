"""
AI Analyzer Service

Integrates OpenAI GPT-4 for:
- Sentiment analysis of Instagram posts
- Trend insight generation
- Market opportunity identification
- Content recommendations
"""

import json
from typing import List, Dict, Optional, Any
from datetime import datetime
import openai
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.instagram_post import InstagramPost
from app.models.instagram_hashtag import InstagramHashtag


class AIAnalyzer:
    """AI-powered analysis service using OpenAI GPT-4"""
    
    def __init__(self, db: Session):
        self.db = db
        if settings.OPENAI_API_KEY:
            openai.api_key = settings.OPENAI_API_KEY
        else:
            print("⚠️  Warning: OPENAI_API_KEY not set. AI features will be disabled.")
    
    async def analyze_post_sentiment(
        self,
        posts: List[InstagramPost],
        market: str
    ) -> Dict[str, Any]:
        """
        Analyze sentiment and themes from Instagram posts
        
        Args:
            posts: List of Instagram posts to analyze
            market: Target market (germany, france, japan)
            
        Returns:
            Dict with sentiment analysis, key themes, and insights
        """
        if not settings.OPENAI_API_KEY or not posts:
            return self._get_mock_sentiment_analysis(market)
        
        try:
            # Prepare post summaries for GPT-4
            post_summaries = []
            for post in posts[:30]:  # Limit to 30 posts to avoid token limits
                post_summaries.append({
                    "caption": post.caption[:200] if post.caption else "",
                    "hashtags": post.hashtags[:5] if post.hashtags else [],
                    "like_count": post.like_count,
                    "comment_count": post.comment_count,
                    "engagement_rate": post.engagement_rate
                })
            
            # Create GPT-4 prompt
            prompt = f"""
Analyze these Instagram posts from the {market} K-Beauty market and provide insights:

Posts data:
{json.dumps(post_summaries, indent=2)}

Provide analysis in the following JSON format:
{{
    "overall_sentiment": "positive/neutral/negative",
    "sentiment_score": 0.0-1.0,
    "key_themes": ["theme1", "theme2", "theme3"],
    "trending_topics": ["topic1", "topic2", "topic3"],
    "consumer_preferences": ["preference1", "preference2"],
    "content_insights": {{
        "popular_content_types": ["type1", "type2"],
        "effective_messaging": "description",
        "visual_trends": ["trend1", "trend2"]
    }},
    "market_insights": {{
        "market_maturity": "emerging/growing/mature",
        "competition_level": "low/medium/high",
        "opportunity_score": 0.0-1.0,
        "recommended_focus": "specific recommendation"
    }},
    "actionable_recommendations": [
        "recommendation1",
        "recommendation2",
        "recommendation3"
    ]
}}

Focus on actionable insights for K-Beauty brands entering the {market} market.
"""
            
            # Call GPT-4
            response = openai.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert K-Beauty market analyst specializing in social media trends and consumer insights. Provide data-driven, actionable recommendations."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=1500,
                response_format={"type": "json_object"}
            )
            
            # Parse response
            analysis = json.loads(response.choices[0].message.content)
            
            # Add metadata
            analysis["analyzed_posts_count"] = len(posts)
            analysis["market"] = market
            analysis["analysis_timestamp"] = datetime.utcnow().isoformat()
            
            return analysis
            
        except Exception as e:
            print(f"❌ Error in sentiment analysis: {e}")
            return self._get_mock_sentiment_analysis(market)
    
    async def generate_trend_insights(
        self,
        hashtags: List[InstagramHashtag],
        market: str,
        time_period: str = "recent"
    ) -> Dict[str, Any]:
        """
        Generate trend insights from hashtag data using GPT-4
        
        Args:
            hashtags: List of trending hashtags
            market: Target market
            time_period: Time period for analysis
            
        Returns:
            Dict with trend insights and predictions
        """
        if not settings.OPENAI_API_KEY or not hashtags:
            return self._get_mock_trend_insights(market)
        
        try:
            # Prepare hashtag data
            hashtag_data = []
            for tag in hashtags[:20]:  # Limit to top 20
                hashtag_data.append({
                    "hashtag": tag.hashtag,
                    "post_count": tag.post_count,
                    "total_engagement": tag.total_engagement,
                    "avg_engagement": tag.avg_engagement_rate,
                    "growth_rate": tag.growth_rate
                })
            
            prompt = f"""
Analyze these trending K-Beauty hashtags from {market} and provide strategic insights:

Hashtag data:
{json.dumps(hashtag_data, indent=2)}

Provide analysis in JSON format:
{{
    "emerging_trends": [
        {{
            "trend": "trend name",
            "description": "brief description",
            "growth_potential": "high/medium/low",
            "time_to_peak": "weeks/months"
        }}
    ],
    "declining_trends": ["trend1", "trend2"],
    "seasonal_patterns": {{
        "current_season_focus": "description",
        "upcoming_opportunities": ["opp1", "opp2"]
    }},
    "competitive_landscape": {{
        "saturation_level": "low/medium/high",
        "white_space_opportunities": ["opp1", "opp2"],
        "differentiation_strategies": ["strategy1", "strategy2"]
    }},
    "consumer_behavior": {{
        "purchase_drivers": ["driver1", "driver2"],
        "content_preferences": ["pref1", "pref2"],
        "engagement_triggers": ["trigger1", "trigger2"]
    }},
    "marketing_recommendations": [
        {{
            "action": "specific action",
            "rationale": "why this matters",
            "expected_impact": "high/medium/low",
            "timeline": "short-term/medium-term/long-term"
        }}
    ],
    "predicted_trends": [
        {{
            "trend": "predicted trend",
            "confidence": 0.0-1.0,
            "timeframe": "1-3 months / 3-6 months",
            "market_impact": "description"
        }}
    ]
}}
"""
            
            response = openai.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert trend forecaster specializing in K-Beauty and social media marketing. Provide strategic, data-driven insights."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=2000,
                response_format={"type": "json_object"}
            )
            
            insights = json.loads(response.choices[0].message.content)
            
            # Add metadata
            insights["analyzed_hashtags_count"] = len(hashtags)
            insights["market"] = market
            insights["time_period"] = time_period
            insights["analysis_timestamp"] = datetime.utcnow().isoformat()
            
            return insights
            
        except Exception as e:
            print(f"❌ Error in trend insights: {e}")
            return self._get_mock_trend_insights(market)
    
    async def generate_market_entry_recommendations(
        self,
        market: str,
        product_category: str,
        brand_profile: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Generate market entry recommendations using GPT-4
        
        Args:
            market: Target market
            product_category: Product category (skincare, makeup, etc.)
            brand_profile: Optional brand information
            
        Returns:
            Dict with market entry strategy and recommendations
        """
        if not settings.OPENAI_API_KEY:
            return self._get_mock_market_entry(market, product_category)
        
        try:
            # Get market data from database
            total_posts = self.db.query(InstagramPost).filter(
                InstagramPost.market == market,
                InstagramPost.category == product_category
            ).count()
            
            avg_engagement = self.db.query(
                func.avg(InstagramPost.engagement_rate)
            ).filter(
                InstagramPost.market == market,
                InstagramPost.category == product_category
            ).scalar() or 0.0
            
            top_hashtags = self.db.query(InstagramHashtag).filter(
                InstagramHashtag.market == market,
                InstagramHashtag.category == product_category
            ).order_by(InstagramHashtag.post_count.desc()).limit(10).all()
            
            market_data = {
                "market": market,
                "category": product_category,
                "total_posts": total_posts,
                "avg_engagement_rate": float(avg_engagement),
                "top_hashtags": [tag.hashtag for tag in top_hashtags]
            }
            
            brand_info = brand_profile or {"type": "small_kbeauty_brand"}
            
            prompt = f"""
As a K-Beauty market entry consultant, analyze this data and provide strategic recommendations:

Market Data:
{json.dumps(market_data, indent=2)}

Brand Profile:
{json.dumps(brand_info, indent=2)}

Provide recommendations in JSON format:
{{
    "market_assessment": {{
        "opportunity_score": 0.0-10.0,
        "difficulty_level": "easy/moderate/challenging",
        "market_maturity": "emerging/growing/mature",
        "key_advantages": ["advantage1", "advantage2"],
        "key_challenges": ["challenge1", "challenge2"]
    }},
    "entry_strategy": {{
        "recommended_approach": "description",
        "initial_focus": "specific focus area",
        "positioning": "recommended positioning",
        "differentiation": "how to stand out"
    }},
    "go_to_market_plan": {{
        "phase1_30days": {{
            "objectives": ["obj1", "obj2"],
            "key_actions": ["action1", "action2"],
            "success_metrics": ["metric1", "metric2"]
        }},
        "phase2_90days": {{
            "objectives": ["obj1", "obj2"],
            "key_actions": ["action1", "action2"],
            "success_metrics": ["metric1", "metric2"]
        }},
        "phase3_180days": {{
            "objectives": ["obj1", "obj2"],
            "key_actions": ["action1", "action2"],
            "success_metrics": ["metric1", "metric2"]
        }}
    }},
    "content_strategy": {{
        "key_messages": ["message1", "message2"],
        "content_pillars": ["pillar1", "pillar2", "pillar3"],
        "hashtag_strategy": ["strategy1", "strategy2"],
        "posting_frequency": "recommendation"
    }},
    "partnership_recommendations": {{
        "influencer_tier": "micro/mid/macro",
        "ideal_partner_profile": "description",
        "collaboration_types": ["type1", "type2"],
        "estimated_budget": "range"
    }},
    "risk_mitigation": [
        {{
            "risk": "risk description",
            "impact": "high/medium/low",
            "mitigation": "mitigation strategy"
        }}
    ],
    "investment_estimate": {{
        "initial_investment": "range",
        "monthly_marketing_budget": "range",
        "expected_roi_timeline": "months",
        "break_even_estimate": "months"
    }}
}}
"""
            
            response = openai.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert K-Beauty market entry consultant with deep knowledge of European and Asian markets."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=2500,
                response_format={"type": "json_object"}
            )
            
            recommendations = json.loads(response.choices[0].message.content)
            recommendations["analysis_timestamp"] = datetime.utcnow().isoformat()
            
            return recommendations
            
        except Exception as e:
            print(f"❌ Error in market entry recommendations: {e}")
            return self._get_mock_market_entry(market, product_category)
    
    # ========== MOCK DATA METHODS (Fallback when OpenAI is not configured) ==========
    
    def _get_mock_sentiment_analysis(self, market: str) -> Dict[str, Any]:
        """Mock sentiment analysis for demo purposes"""
        return {
            "overall_sentiment": "positive",
            "sentiment_score": 0.78,
            "key_themes": [
                "natural ingredients",
                "glowing skin",
                "vegan beauty",
                "sustainable packaging"
            ],
            "trending_topics": [
                "glass skin trend",
                "minimalist skincare",
                "Korean skincare routine"
            ],
            "consumer_preferences": [
                "clean beauty products",
                "multi-functional products",
                "affordable luxury"
            ],
            "content_insights": {
                "popular_content_types": [
                    "before-after transformations",
                    "product reviews",
                    "skincare routines"
                ],
                "effective_messaging": "Authenticity and transparency in ingredient sourcing",
                "visual_trends": [
                    "minimalist aesthetics",
                    "natural lighting",
                    "close-up product shots"
                ]
            },
            "market_insights": {
                "market_maturity": "growing",
                "competition_level": "medium",
                "opportunity_score": 0.82,
                "recommended_focus": "Focus on vegan, cruelty-free products with transparent ingredient lists"
            },
            "actionable_recommendations": [
                "Emphasize natural and vegan ingredients in marketing",
                "Create content around sustainable beauty practices",
                "Partner with micro-influencers focusing on clean beauty",
                "Develop educational content about Korean skincare philosophy"
            ],
            "analyzed_posts_count": 0,
            "market": market,
            "analysis_timestamp": datetime.utcnow().isoformat(),
            "note": "This is mock data. Set OPENAI_API_KEY for real AI analysis."
        }
    
    def _get_mock_trend_insights(self, market: str) -> Dict[str, Any]:
        """Mock trend insights for demo purposes"""
        return {
            "emerging_trends": [
                {
                    "trend": "Probiotic skincare",
                    "description": "Growing interest in microbiome-friendly products",
                    "growth_potential": "high",
                    "time_to_peak": "3-6 months"
                },
                {
                    "trend": "Blue light protection",
                    "description": "Screen-time skincare gaining traction",
                    "growth_potential": "medium",
                    "time_to_peak": "6-12 months"
                }
            ],
            "declining_trends": [
                "Heavy layering routines",
                "Complicated multi-step processes"
            ],
            "seasonal_patterns": {
                "current_season_focus": "Hydration and barrier repair for winter",
                "upcoming_opportunities": [
                    "Spring renewal and brightening",
                    "Sun protection for summer"
                ]
            },
            "competitive_landscape": {
                "saturation_level": "medium",
                "white_space_opportunities": [
                    "Men's K-beauty products",
                    "Teen skincare lines",
                    "Sensitive skin solutions"
                ],
                "differentiation_strategies": [
                    "Focus on specific skin concerns",
                    "Sustainable and eco-friendly approach",
                    "Technology-driven formulations"
                ]
            },
            "consumer_behavior": {
                "purchase_drivers": [
                    "Ingredient transparency",
                    "Proven effectiveness",
                    "Value for money"
                ],
                "content_preferences": [
                    "Educational content",
                    "User testimonials",
                    "Expert recommendations"
                ],
                "engagement_triggers": [
                    "Limited edition releases",
                    "Seasonal promotions",
                    "Interactive content"
                ]
            },
            "marketing_recommendations": [
                {
                    "action": "Develop probiotic skincare line",
                    "rationale": "Emerging trend with high growth potential",
                    "expected_impact": "high",
                    "timeline": "medium-term"
                },
                {
                    "action": "Create educational content series",
                    "rationale": "Consumers value learning about ingredients and benefits",
                    "expected_impact": "medium",
                    "timeline": "short-term"
                }
            ],
            "predicted_trends": [
                {
                    "trend": "Personalized skincare",
                    "confidence": 0.85,
                    "timeframe": "3-6 months",
                    "market_impact": "AI-driven product recommendations will become standard"
                }
            ],
            "analyzed_hashtags_count": 0,
            "market": market,
            "time_period": "recent",
            "analysis_timestamp": datetime.utcnow().isoformat(),
            "note": "This is mock data. Set OPENAI_API_KEY for real AI analysis."
        }
    
    def _get_mock_market_entry(self, market: str, product_category: str) -> Dict[str, Any]:
        """Mock market entry recommendations for demo purposes"""
        return {
            "market_assessment": {
                "opportunity_score": 7.5,
                "difficulty_level": "moderate",
                "market_maturity": "growing",
                "key_advantages": [
                    "Strong consumer interest in K-Beauty",
                    "Growing digital-first purchasing behavior",
                    "Influencer marketing effectiveness"
                ],
                "key_challenges": [
                    "Established competition",
                    "Regulatory compliance requirements",
                    "Localization needs"
                ]
            },
            "entry_strategy": {
                "recommended_approach": "Digital-first with influencer partnerships",
                "initial_focus": "Instagram and TikTok for brand awareness",
                "positioning": "Premium yet accessible K-Beauty expertise",
                "differentiation": "Focus on ingredient transparency and education"
            },
            "go_to_market_plan": {
                "phase1_30days": {
                    "objectives": [
                        "Build social media presence",
                        "Identify and contact 10 micro-influencers"
                    ],
                    "key_actions": [
                        "Create 20 pieces of educational content",
                        "Launch Instagram account with consistent posting",
                        "Set up local e-commerce presence"
                    ],
                    "success_metrics": [
                        "1,000 followers",
                        "5% engagement rate",
                        "3 influencer partnerships confirmed"
                    ]
                },
                "phase2_90days": {
                    "objectives": [
                        "Generate first sales",
                        "Build brand awareness"
                    ],
                    "key_actions": [
                        "Launch influencer campaigns",
                        "Run targeted social ads",
                        "Collect customer testimonials"
                    ],
                    "success_metrics": [
                        "50 orders",
                        "5,000 followers",
                        "10 customer reviews"
                    ]
                },
                "phase3_180days": {
                    "objectives": [
                        "Establish market presence",
                        "Achieve profitability"
                    ],
                    "key_actions": [
                        "Expand product line",
                        "Scale successful marketing channels",
                        "Build retail partnerships"
                    ],
                    "success_metrics": [
                        "500 monthly orders",
                        "20,000 followers",
                        "Positive ROI"
                    ]
                }
            },
            "content_strategy": {
                "key_messages": [
                    "Authentic Korean beauty expertise",
                    "Science-backed formulations",
                    "Sustainable and ethical beauty"
                ],
                "content_pillars": [
                    "Education (ingredients, routines)",
                    "Transformation stories",
                    "Behind-the-scenes content"
                ],
                "hashtag_strategy": [
                    "Use mix of popular and niche hashtags",
                    "Create branded hashtag",
                    "Monitor trending beauty hashtags"
                ],
                "posting_frequency": "Daily on Instagram, 3-4x weekly on TikTok"
            },
            "partnership_recommendations": {
                "influencer_tier": "micro",
                "ideal_partner_profile": "10k-50k followers, genuine engagement, beauty focus",
                "collaboration_types": [
                    "Product reviews",
                    "Sponsored posts",
                    "Affiliate partnerships"
                ],
                "estimated_budget": "€2,000-5,000 per month"
            },
            "risk_mitigation": [
                {
                    "risk": "Low initial brand awareness",
                    "impact": "high",
                    "mitigation": "Invest in micro-influencer partnerships for credibility"
                },
                {
                    "risk": "Regulatory compliance issues",
                    "impact": "high",
                    "mitigation": "Consult with local regulatory expert before launch"
                }
            ],
            "investment_estimate": {
                "initial_investment": "€10,000-15,000",
                "monthly_marketing_budget": "€3,000-5,000",
                "expected_roi_timeline": "6-9 months",
                "break_even_estimate": "12-18 months"
            },
            "analysis_timestamp": datetime.utcnow().isoformat(),
            "note": "This is mock data. Set OPENAI_API_KEY for real AI analysis."
        }
