/**
 * AI Analysis API Client
 * 
 * Handles all AI analysis API calls:
 * - Sentiment Analysis
 * - Trend Prediction
 * - Content Quality Evaluation
 * - Influencer Authenticity
 * - Cultural Fit Assessment
 * - Performance Prediction
 */

import api from './api';

// ========== Types ==========

export interface SentimentAnalysisRequest {
  market: string;
  limit?: number;
  hashtag?: string;
}

export interface SentimentAnalysisResult {
  overall_sentiment: 'positive' | 'neutral' | 'negative';
  sentiment_score: number;
  key_themes: string[];
  trending_topics: string[];
  consumer_preferences: string[];
  content_insights: {
    popular_content_types: string[];
    effective_messaging: string;
    visual_trends: string[];
  };
  market_insights: {
    market_maturity: string;
    competition_level: string;
    opportunity_score: number;
    recommended_focus: string;
  };
  actionable_recommendations: string[];
  analyzed_posts_count: number;
  market: string;
  analysis_timestamp: string;
}

export interface TrendAnalysisRequest {
  market: string;
  limit?: number;
  time_period?: string;
}

export interface EmergingTrend {
  trend: string;
  description: string;
  growth_potential: 'high' | 'medium' | 'low';
  time_to_peak: string;
}

export interface PredictedTrend {
  trend: string;
  confidence: number;
  timeframe: string;
  market_impact: string;
}

export interface TrendAnalysisResult {
  emerging_trends: EmergingTrend[];
  declining_trends: string[];
  seasonal_patterns: {
    current_season_focus: string;
    upcoming_opportunities: string[];
  };
  competitive_landscape: {
    saturation_level: string;
    white_space_opportunities: string[];
    differentiation_strategies: string[];
  };
  consumer_behavior: {
    purchase_drivers: string[];
    content_preferences: string[];
    engagement_triggers: string[];
  };
  marketing_recommendations: Array<{
    action: string;
    rationale: string;
    expected_impact: string;
    timeline: string;
  }>;
  predicted_trends: PredictedTrend[];
  analyzed_hashtags_count: number;
  market: string;
  time_period: string;
  analysis_timestamp: string;
}

export interface ContentQualityRequest {
  post_id: number;
  detailed?: boolean;
}

export interface ContentQualityResult {
  overall_score: number;
  scores: {
    visual_appeal: number;
    caption_quality: number;
    hashtag_relevance: number;
    engagement_potential: number;
    brand_alignment: number;
  };
  strengths: string[];
  weaknesses: string[];
  improvement_suggestions: Array<{
    area: string;
    suggestion: string;
    priority: 'high' | 'medium' | 'low';
    expected_impact: string;
  }>;
  best_practices_followed: string[];
  missed_opportunities: string[];
  competitive_advantage: string;
  post_id: number;
  analysis_timestamp: string;
}

export interface AuthenticityAnalysisRequest {
  influencer_id: number;
  include_recent_posts?: boolean;
}

export interface AuthenticityAnalysisResult {
  authenticity_score: number;
  confidence: number;
  authenticity_factors: {
    engagement_quality: number;
    content_consistency: number;
    audience_alignment: number;
    growth_pattern: number;
    transparency: number;
  };
  red_flags: Array<{
    flag: string;
    severity: 'high' | 'medium' | 'low';
    evidence: string;
  }>;
  green_flags: string[];
  audience_quality: {
    estimated_real_followers_percent: number;
    engagement_authenticity: 'high' | 'medium' | 'low';
    bot_likelihood: number;
  };
  partnership_recommendation: {
    recommended: boolean;
    rationale: string;
    ideal_collaboration_type: string;
    estimated_value: string;
  };
  risk_assessment: {
    overall_risk: 'low' | 'medium' | 'high';
    specific_risks: string[];
    mitigation_strategies: string[];
  };
  influencer_id: number;
  analysis_timestamp: string;
}

export interface CulturalFitRequest {
  content: {
    caption?: string;
    hashtags?: string[];
    visual_description?: string;
    target_audience?: string;
  };
  target_market: 'germany' | 'france' | 'japan';
}

export interface CulturalFitResult {
  cultural_alignment_score: number;
  confidence: number;
  alignment_factors: {
    values_alignment: number;
    communication_style_fit: number;
    visual_appropriateness: number;
    language_suitability: number;
    emotional_resonance: number;
  };
  cultural_strengths: string[];
  cultural_concerns: Array<{
    concern: string;
    severity: 'high' | 'medium' | 'low';
    explanation: string;
    suggestion: string;
  }>;
  taboo_check: {
    detected_taboos: string[];
    risk_level: 'none' | 'low' | 'medium' | 'high';
    alternative_approaches: string[];
  };
  localization_recommendations: Array<{
    aspect: string;
    current: string;
    recommended: string;
    rationale: string;
  }>;
  market_fit_verdict: {
    ready_to_launch: boolean;
    required_changes: string[];
    optional_improvements: string[];
    expected_reception: string;
  };
  target_market: string;
  analysis_timestamp: string;
}

export interface PerformancePredictionRequest {
  draft_content: {
    caption: string;
    hashtags: string[];
    category?: string;
    posting_time?: string;
  };
  market: string;
  include_historical?: boolean;
}

export interface PerformancePredictionResult {
  predicted_performance: {
    engagement_rate: {
      estimate: number;
      confidence_range: [number, number];
      vs_average: 'above' | 'average' | 'below';
    };
    estimated_likes: {
      estimate: number;
      confidence_range: [number, number];
    };
    estimated_comments: {
      estimate: number;
      confidence_range: [number, number];
    };
    viral_potential: {
      score: number;
      factors: string[];
    };
  };
  optimization_suggestions: Array<{
    area: string;
    current: string;
    suggested: string;
    expected_improvement: string;
  }>;
  best_posting_time: {
    day: string;
    time: string;
    timezone: string;
    rationale: string;
  };
  a_b_testing_recommendations: Array<{
    variation: string;
    version_a: string;
    version_b: string;
    expected_winner: 'a' | 'b' | 'uncertain';
  }>;
  overall_assessment: {
    readiness_score: number;
    go_live_recommendation: 'publish' | 'optimize' | 'reconsider';
    key_message: string;
  };
  analysis_timestamp: string;
}

export interface MarketEntryRecommendations {
  market_assessment: {
    opportunity_score: number;
    difficulty_level: string;
    market_maturity: string;
    key_advantages: string[];
    key_challenges: string[];
  };
  entry_strategy: {
    recommended_approach: string;
    initial_focus: string;
    positioning: string;
    differentiation: string;
  };
  go_to_market_plan: {
    phase1_30days: {
      objectives: string[];
      key_actions: string[];
      success_metrics: string[];
    };
    phase2_90days: {
      objectives: string[];
      key_actions: string[];
      success_metrics: string[];
    };
    phase3_180days: {
      objectives: string[];
      key_actions: string[];
      success_metrics: string[];
    };
  };
  content_strategy: {
    key_messages: string[];
    content_pillars: string[];
    hashtag_strategy: string[];
    posting_frequency: string;
  };
  partnership_recommendations: {
    influencer_tier: string;
    ideal_partner_profile: string;
    collaboration_types: string[];
    estimated_budget: string;
  };
  risk_mitigation: Array<{
    risk: string;
    impact: string;
    mitigation: string;
  }>;
  investment_estimate: {
    initial_investment: string;
    monthly_marketing_budget: string;
    expected_roi_timeline: string;
    break_even_estimate: string;
  };
  analysis_timestamp: string;
}

// ========== API Client Class ==========

class AIAnalysisAPI {
  /**
   * Analyze sentiment of Instagram posts
   */
  async analyzeSentiment(request: SentimentAnalysisRequest): Promise<SentimentAnalysisResult> {
    const response = await api.post('/analysis/sentiment', request);
    return response.data.analysis;
  }

  /**
   * Quick sentiment analysis (GET endpoint)
   */
  async getMarketSentiment(
    market: string,
    hashtag?: string,
    limit: number = 50
  ): Promise<SentimentAnalysisResult> {
    const params = { hashtag, limit };
    const response = await api.get(`/analysis/sentiment/${market}`, { params });
    return response.data.analysis;
  }

  /**
   * Analyze trends and predict future movements
   */
  async analyzeTrends(request: TrendAnalysisRequest): Promise<TrendAnalysisResult> {
    const response = await api.post('/analysis/trends', request);
    return response.data.insights;
  }

  /**
   * Quick trend analysis (GET endpoint)
   */
  async getMarketTrends(market: string, limit: number = 20): Promise<TrendAnalysisResult> {
    const response = await api.get(`/analysis/trends/${market}`, { params: { limit } });
    return response.data.insights;
  }

  /**
   * Evaluate content quality
   */
  async evaluateContentQuality(request: ContentQualityRequest): Promise<ContentQualityResult> {
    const response = await api.post('/analysis/quality', request);
    return response.data.evaluation;
  }

  /**
   * Quick quality evaluation (GET endpoint)
   */
  async getPostQuality(postId: number, detailed: boolean = true): Promise<ContentQualityResult> {
    const response = await api.get(`/analysis/quality/${postId}`, { params: { detailed } });
    return response.data.evaluation;
  }

  /**
   * Analyze influencer authenticity
   */
  async analyzeInfluencerAuthenticity(
    request: AuthenticityAnalysisRequest
  ): Promise<AuthenticityAnalysisResult> {
    const response = await api.post('/analysis/authenticity', request);
    return response.data.analysis;
  }

  /**
   * Quick authenticity check (GET endpoint)
   */
  async getInfluencerAuthenticity(influencerId: number): Promise<AuthenticityAnalysisResult> {
    const response = await api.get(`/analysis/authenticity/${influencerId}`);
    return response.data.analysis;
  }

  /**
   * Analyze cultural fit for target market
   */
  async analyzeCulturalFit(request: CulturalFitRequest): Promise<CulturalFitResult> {
    const response = await api.post('/analysis/cultural-fit', request);
    return response.data.analysis;
  }

  /**
   * Predict post performance before publishing
   */
  async predictPerformance(
    request: PerformancePredictionRequest
  ): Promise<PerformancePredictionResult> {
    const response = await api.post('/analysis/predict-performance', request);
    return response.data.prediction;
  }

  /**
   * Get market entry recommendations
   */
  async getMarketEntryRecommendations(
    market: string,
    category: string = 'beauty'
  ): Promise<MarketEntryRecommendations> {
    const response = await api.get(`/analysis/market-entry/${market}`, { params: { category } });
    return response.data.recommendations;
  }

  /**
   * Batch analyze multiple posts
   */
  async batchAnalyze(
    postIds: number[],
    analysisType: 'sentiment' | 'quality' | 'all' = 'all'
  ): Promise<any> {
    const response = await api.post('/analysis/batch-analyze', postIds, {
      params: { analysis_type: analysisType },
    });
    return response.data;
  }
}

// Export singleton instance
export const aiAnalysisApi = new AIAnalysisAPI();

// Export default
export default aiAnalysisApi;
