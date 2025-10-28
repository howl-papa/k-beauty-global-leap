"""
Extended AI Analyzer Service

Additional AI analysis capabilities:
- Content quality evaluation
- Influencer authenticity analysis  
- Cultural fit assessment
- Performance prediction
"""

import json
from typing import List, Dict, Optional, Any
from datetime import datetime
from openai import OpenAI
from sqlalchemy.orm import Session
from sqlalchemy import func
import redis

from app.core.config import get_settings
from app.models.instagram_post import InstagramPost
from app.models.instagram_influencer import InstagramInfluencer


class AIAnalyzerExtended:
    """Extended AI analysis capabilities"""
    
    def __init__(self, db: Session):
        self.db = db
        self.settings = get_settings()
        
        # Initialize OpenAI client
        if self.settings.OPENAI_API_KEY:
            self.openai_client = OpenAI(api_key=self.settings.OPENAI_API_KEY)
        else:
            self.openai_client = None
            print("⚠️  Warning: OPENAI_API_KEY not set. AI features will use mock data.")
        
        # Initialize Redis cache
        try:
            self.cache = redis.from_url(self.settings.REDIS_URL)
        except:
            self.cache = None
            print("⚠️  Warning: Redis not available. Caching disabled.")
    
    async def evaluate_content_quality(
        self,
        post: InstagramPost,
        detailed: bool = True
    ) -> Dict[str, Any]:
        """
        Evaluate content quality using GPT-4
        
        Args:
            post: Instagram post to evaluate
            detailed: Include detailed breakdown
            
        Returns:
            Dict with quality scores and recommendations
        """
        # Check cache first
        cache_key = f"quality:{post.id}"
        if self.cache:
            cached = self.cache.get(cache_key)
            if cached:
                return json.loads(cached)
        
        if not self.openai_client:
            return self._get_mock_quality_evaluation()
        
        try:
            post_data = {
                "caption": post.caption[:500] if post.caption else "",
                "hashtags": post.hashtags[:10] if post.hashtags else [],
                "like_count": post.like_count,
                "comment_count": post.comment_count,
                "engagement_rate": post.engagement_rate,
                "category": post.category
            }
            
            prompt = f"""
Evaluate the marketing effectiveness of this Instagram post:

{json.dumps(post_data, indent=2)}

Provide quality assessment in JSON format:
{{
    "overall_score": 0-100,
    "scores": {{
        "visual_appeal": 0-100,
        "caption_quality": 0-100,
        "hashtag_relevance": 0-100,
        "engagement_potential": 0-100,
        "brand_alignment": 0-100
    }},
    "strengths": ["strength1", "strength2", "strength3"],
    "weaknesses": ["weakness1", "weakness2"],
    "improvement_suggestions": [
        {{
            "area": "specific area",
            "suggestion": "actionable suggestion",
            "priority": "high/medium/low",
            "expected_impact": "description"
        }}
    ],
    "best_practices_followed": ["practice1", "practice2"],
    "missed_opportunities": ["opportunity1", "opportunity2"],
    "competitive_advantage": "what makes this stand out or generic"
}}
"""
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert social media marketing analyst specializing in Instagram content optimization."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.5,
                max_tokens=1200,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            result["post_id"] = post.id
            result["analysis_timestamp"] = datetime.utcnow().isoformat()
            
            # Cache for 24 hours
            if self.cache:
                self.cache.setex(cache_key, 86400, json.dumps(result))
            
            return result
            
        except Exception as e:
            print(f"❌ Error evaluating content quality: {e}")
            return self._get_mock_quality_evaluation()
    
    async def analyze_influencer_authenticity(
        self,
        influencer: InstagramInfluencer,
        recent_posts: List[InstagramPost] = None
    ) -> Dict[str, Any]:
        """
        Analyze influencer authenticity and audience quality
        
        Args:
            influencer: Influencer to analyze
            recent_posts: Recent posts for pattern analysis
            
        Returns:
            Dict with authenticity scores and insights
        """
        # Check cache
        cache_key = f"authenticity:{influencer.id}"
        if self.cache:
            cached = self.cache.get(cache_key)
            if cached:
                return json.loads(cached)
        
        if not self.openai_client:
            return self._get_mock_authenticity_analysis()
        
        try:
            influencer_data = {
                "username": influencer.username,
                "followers_count": influencer.followers_count,
                "avg_likes": influencer.avg_likes,
                "avg_comments": influencer.avg_comments,
                "engagement_rate": influencer.engagement_rate,
                "post_frequency": influencer.post_frequency,
                "bio": influencer.bio[:200] if influencer.bio else ""
            }
            
            # Add recent post data if available
            if recent_posts:
                influencer_data["recent_posts_sample"] = [
                    {
                        "likes": p.like_count,
                        "comments": p.comment_count,
                        "engagement": p.engagement_rate
                    }
                    for p in recent_posts[:10]
                ]
            
            prompt = f"""
Analyze this influencer's authenticity and audience quality:

{json.dumps(influencer_data, indent=2)}

Provide authenticity assessment in JSON format:
{{
    "authenticity_score": 0-100,
    "confidence": 0.0-1.0,
    "authenticity_factors": {{
        "engagement_quality": 0-100,
        "content_consistency": 0-100,
        "audience_alignment": 0-100,
        "growth_pattern": 0-100,
        "transparency": 0-100
    }},
    "red_flags": [
        {{
            "flag": "specific issue",
            "severity": "high/medium/low",
            "evidence": "description"
        }}
    ],
    "green_flags": ["positive indicator1", "positive indicator2"],
    "audience_quality": {{
        "estimated_real_followers_percent": 0-100,
        "engagement_authenticity": "high/medium/low",
        "bot_likelihood": 0-100
    }},
    "partnership_recommendation": {{
        "recommended": true/false,
        "rationale": "explanation",
        "ideal_collaboration_type": "type",
        "estimated_value": "value range"
    }},
    "risk_assessment": {{
        "overall_risk": "low/medium/high",
        "specific_risks": ["risk1", "risk2"],
        "mitigation_strategies": ["strategy1", "strategy2"]
    }}
}}
"""
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert influencer marketing analyst with deep experience in detecting fake engagement and assessing influencer quality."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,  # Lower temperature for more consistent analysis
                max_tokens=1500,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            result["influencer_id"] = influencer.id
            result["analysis_timestamp"] = datetime.utcnow().isoformat()
            
            # Cache for 7 days (influencer quality doesn't change frequently)
            if self.cache:
                self.cache.setex(cache_key, 604800, json.dumps(result))
            
            return result
            
        except Exception as e:
            print(f"❌ Error analyzing influencer authenticity: {e}")
            return self._get_mock_authenticity_analysis()
    
    async def analyze_cultural_fit(
        self,
        content: Dict[str, Any],
        target_market: str
    ) -> Dict[str, Any]:
        """
        Analyze cultural appropriateness for target market
        
        Args:
            content: Content to analyze (post, caption, visual description)
            target_market: Target market (germany, france, japan)
            
        Returns:
            Dict with cultural fit scores and recommendations
        """
        # Market-specific cultural contexts
        cultural_contexts = {
            "germany": {
                "values": ["efficiency", "quality", "sustainability", "directness"],
                "taboos": ["overpromising", "aggressive marketing", "false claims"],
                "preferences": ["natural ingredients", "clinical proof", "minimalism"],
                "communication_style": "Direct, factual, evidence-based"
            },
            "france": {
                "values": ["elegance", "sophistication", "tradition", "artistry"],
                "taboos": ["loud advertising", "too much text", "oversimplification"],
                "preferences": ["luxury", "artisanal", "sensory experience", "heritage"],
                "communication_style": "Refined, artistic, emphasizing experience"
            },
            "japan": {
                "values": ["harmony", "precision", "respect", "quality"],
                "taboos": ["direct confrontation", "boastfulness", "disorder"],
                "preferences": ["cute packaging", "detailed info", "cleanliness", "technology"],
                "communication_style": "Polite, detailed, emphasizing care and attention"
            }
        }
        
        market_context = cultural_contexts.get(target_market, cultural_contexts["germany"])
        
        if not self.openai_client:
            return self._get_mock_cultural_fit()
        
        try:
            prompt = f"""
Analyze the cultural appropriateness of this content for the {target_market} market:

Content:
{json.dumps(content, indent=2)}

Market Cultural Context:
{json.dumps(market_context, indent=2)}

Provide cultural fit assessment in JSON format:
{{
    "cultural_alignment_score": 0-100,
    "confidence": 0.0-1.0,
    "alignment_factors": {{
        "values_alignment": 0-100,
        "communication_style_fit": 0-100,
        "visual_appropriateness": 0-100,
        "language_suitability": 0-100,
        "emotional_resonance": 0-100
    }},
    "cultural_strengths": ["strength1", "strength2"],
    "cultural_concerns": [
        {{
            "concern": "specific issue",
            "severity": "high/medium/low",
            "explanation": "why this matters",
            "suggestion": "how to fix"
        }}
    ],
    "taboo_check": {{
        "detected_taboos": ["taboo1 if any"],
        "risk_level": "none/low/medium/high",
        "alternative_approaches": ["approach1", "approach2"]
    }},
    "localization_recommendations": [
        {{
            "aspect": "what to change",
            "current": "current approach",
            "recommended": "better approach",
            "rationale": "why this works better"
        }}
    ],
    "market_fit_verdict": {{
        "ready_to_launch": true/false,
        "required_changes": ["change1", "change2"],
        "optional_improvements": ["improvement1", "improvement2"],
        "expected_reception": "description"
    }}
}}
"""
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {
                        "role": "system",
                        "content": f"You are an expert cross-cultural marketing consultant specializing in {target_market} market. You have deep knowledge of local cultural nuances, taboos, and preferences."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.4,
                max_tokens=1500,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            result["target_market"] = target_market
            result["analysis_timestamp"] = datetime.utcnow().isoformat()
            
            return result
            
        except Exception as e:
            print(f"❌ Error analyzing cultural fit: {e}")
            return self._get_mock_cultural_fit()
    
    async def predict_post_performance(
        self,
        post_draft: Dict[str, Any],
        market: str,
        historical_data: Optional[List[InstagramPost]] = None
    ) -> Dict[str, Any]:
        """
        Predict performance of a post before publishing
        
        Args:
            post_draft: Draft post content
            market: Target market
            historical_data: Similar historical posts for comparison
            
        Returns:
            Dict with performance predictions and optimization suggestions
        """
        if not self.openai_client:
            return self._get_mock_performance_prediction()
        
        try:
            # Calculate historical benchmarks
            if historical_data:
                avg_engagement = sum(p.engagement_rate for p in historical_data) / len(historical_data)
                avg_likes = sum(p.like_count for p in historical_data) / len(historical_data)
            else:
                # Use market averages
                avg_engagement = self.db.query(func.avg(InstagramPost.engagement_rate)).filter(
                    InstagramPost.market == market
                ).scalar() or 5.0
                avg_likes = self.db.query(func.avg(InstagramPost.like_count)).filter(
                    InstagramPost.market == market
                ).scalar() or 100
            
            context = {
                "draft": post_draft,
                "market": market,
                "benchmarks": {
                    "avg_engagement_rate": float(avg_engagement),
                    "avg_likes": float(avg_likes)
                }
            }
            
            prompt = f"""
Predict the performance of this draft Instagram post:

{json.dumps(context, indent=2)}

Provide performance prediction in JSON format:
{{
    "predicted_performance": {{
        "engagement_rate": {{
            "estimate": 0.0-20.0,
            "confidence_range": [min, max],
            "vs_average": "above/average/below"
        }},
        "estimated_likes": {{
            "estimate": number,
            "confidence_range": [min, max]
        }},
        "estimated_comments": {{
            "estimate": number,
            "confidence_range": [min, max]
        }},
        "viral_potential": {{
            "score": 0-100,
            "factors": ["factor1", "factor2"]
        }}
    }},
    "optimization_suggestions": [
        {{
            "area": "caption/hashtags/timing/visual",
            "current": "current approach",
            "suggested": "optimization",
            "expected_improvement": "percentage or description"
        }}
    ],
    "best_posting_time": {{
        "day": "day of week",
        "time": "HH:MM",
        "timezone": "timezone",
        "rationale": "why this time"
    }},
    "a_b_testing_recommendations": [
        {{
            "variation": "what to test",
            "version_a": "option 1",
            "version_b": "option 2",
            "expected_winner": "a/b/uncertain"
        }}
    ],
    "overall_assessment": {{
        "readiness_score": 0-100,
        "go_live_recommendation": "publish/optimize/reconsider",
        "key_message": "brief summary"
    }}
}}
"""
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert social media performance analyst with proven track record in predicting post engagement and viral potential."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.6,
                max_tokens=1500,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            result["analysis_timestamp"] = datetime.utcnow().isoformat()
            
            return result
            
        except Exception as e:
            print(f"❌ Error predicting performance: {e}")
            return self._get_mock_performance_prediction()
    
    # ========== MOCK DATA METHODS ==========
    
    def _get_mock_quality_evaluation(self) -> Dict[str, Any]:
        """Mock quality evaluation"""
        return {
            "overall_score": 78,
            "scores": {
                "visual_appeal": 82,
                "caption_quality": 75,
                "hashtag_relevance": 80,
                "engagement_potential": 76,
                "brand_alignment": 77
            },
            "strengths": [
                "Clear product focus",
                "Relevant hashtags",
                "Engaging caption hook"
            ],
            "weaknesses": [
                "Could use more call-to-action",
                "Hashtag variety could be improved"
            ],
            "improvement_suggestions": [
                {
                    "area": "caption",
                    "suggestion": "Add a question to encourage comments",
                    "priority": "medium",
                    "expected_impact": "10-15% more comments"
                }
            ],
            "best_practices_followed": [
                "Natural lighting",
                "Product clearly visible"
            ],
            "missed_opportunities": [
                "No user-generated content mention",
                "Missing trending audio reference"
            ],
            "competitive_advantage": "Strong visual aesthetic aligns with K-Beauty brand values",
            "analysis_timestamp": datetime.utcnow().isoformat(),
            "note": "Mock data. Set OPENAI_API_KEY for real analysis."
        }
    
    def _get_mock_authenticity_analysis(self) -> Dict[str, Any]:
        """Mock authenticity analysis"""
        return {
            "authenticity_score": 85,
            "confidence": 0.82,
            "authenticity_factors": {
                "engagement_quality": 88,
                "content_consistency": 82,
                "audience_alignment": 85,
                "growth_pattern": 83,
                "transparency": 87
            },
            "red_flags": [],
            "green_flags": [
                "Consistent engagement rate",
                "Genuine audience interactions",
                "Transparent about partnerships"
            ],
            "audience_quality": {
                "estimated_real_followers_percent": 92,
                "engagement_authenticity": "high",
                "bot_likelihood": 8
            },
            "partnership_recommendation": {
                "recommended": True,
                "rationale": "High authenticity score and engaged audience",
                "ideal_collaboration_type": "Long-term partnership",
                "estimated_value": "€500-1000 per post"
            },
            "risk_assessment": {
                "overall_risk": "low",
                "specific_risks": ["Moderate follower count may limit reach"],
                "mitigation_strategies": ["Combine with other micro-influencers"]
            },
            "analysis_timestamp": datetime.utcnow().isoformat(),
            "note": "Mock data. Set OPENAI_API_KEY for real analysis."
        }
    
    def _get_mock_cultural_fit(self) -> Dict[str, Any]:
        """Mock cultural fit analysis"""
        return {
            "cultural_alignment_score": 82,
            "confidence": 0.85,
            "alignment_factors": {
                "values_alignment": 85,
                "communication_style_fit": 80,
                "visual_appropriateness": 82,
                "language_suitability": 78,
                "emotional_resonance": 84
            },
            "cultural_strengths": [
                "Emphasizes quality and effectiveness",
                "Clean, minimalist visual style"
            ],
            "cultural_concerns": [
                {
                    "concern": "Slightly too enthusiastic tone",
                    "severity": "low",
                    "explanation": "Target market prefers understated messaging",
                    "suggestion": "Tone down superlatives, add factual evidence"
                }
            ],
            "taboo_check": {
                "detected_taboos": [],
                "risk_level": "none",
                "alternative_approaches": []
            },
            "localization_recommendations": [
                {
                    "aspect": "language",
                    "current": "English with emojis",
                    "recommended": "Local language with moderate emoji use",
                    "rationale": "Builds trust and shows commitment to market"
                }
            ],
            "market_fit_verdict": {
                "ready_to_launch": True,
                "required_changes": [],
                "optional_improvements": [
                    "Add local testimonials",
                    "Include sustainability certifications"
                ],
                "expected_reception": "Positive - aligns well with market values"
            },
            "target_market": "germany",
            "analysis_timestamp": datetime.utcnow().isoformat(),
            "note": "Mock data. Set OPENAI_API_KEY for real analysis."
        }
    
    def _get_mock_performance_prediction(self) -> Dict[str, Any]:
        """Mock performance prediction"""
        return {
            "predicted_performance": {
                "engagement_rate": {
                    "estimate": 6.5,
                    "confidence_range": [5.2, 7.8],
                    "vs_average": "above"
                },
                "estimated_likes": {
                    "estimate": 850,
                    "confidence_range": [700, 1000]
                },
                "estimated_comments": {
                    "estimate": 42,
                    "confidence_range": [30, 55]
                },
                "viral_potential": {
                    "score": 68,
                    "factors": [
                        "Trending topic",
                        "Strong visual appeal"
                    ]
                }
            },
            "optimization_suggestions": [
                {
                    "area": "hashtags",
                    "current": "10 hashtags",
                    "suggested": "Add 3 trending niche hashtags",
                    "expected_improvement": "12% more reach"
                }
            ],
            "best_posting_time": {
                "day": "Wednesday",
                "time": "18:30",
                "timezone": "CET",
                "rationale": "Peak engagement time for target audience"
            },
            "a_b_testing_recommendations": [
                {
                    "variation": "caption style",
                    "version_a": "Question-based",
                    "version_b": "Statement with CTA",
                    "expected_winner": "b"
                }
            ],
            "overall_assessment": {
                "readiness_score": 82,
                "go_live_recommendation": "publish",
                "key_message": "Strong content, minor optimizations recommended but not required"
            },
            "analysis_timestamp": datetime.utcnow().isoformat(),
            "note": "Mock data. Set OPENAI_API_KEY for real analysis."
        }
