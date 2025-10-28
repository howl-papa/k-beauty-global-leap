/**
 * Instagram API Types
 * 
 * TypeScript type definitions for Instagram API responses
 */

export interface InstagramPost {
  id: number;
  external_id: string;
  caption: string | null;
  media_type: 'IMAGE' | 'VIDEO' | 'CAROUSEL_ALBUM';
  media_url: string | null;
  permalink: string | null;
  username: string;
  timestamp: string;
  market: string;
  like_count: number;
  comment_count: number;
  engagement_rate: number;
  hashtags: string[];
  mentions: string[];
  category: string | null;
  sentiment_score: number | null;
  sentiment_label: string | null;
  detected_products: string[];
  detected_brands: string[];
  is_sponsored: boolean;
  is_verified_account: boolean;
  created_at: string;
}

export interface InstagramHashtag {
  id: number;
  external_id: string;
  name: string;
  display_name: string | null;
  market: string;
  category: string | null;
  post_count: number;
  avg_likes: number;
  avg_comments: number;
  avg_engagement: number;
  growth_rate: number;
  velocity: number;
  is_trending: boolean;
  trend_score: number;
  competition_level: string | null;
  difficulty_score: number;
  tracked_at: string;
}

export interface InstagramInfluencer {
  id: number;
  external_id: string;
  username: string;
  full_name: string | null;
  biography: string | null;
  profile_picture_url: string | null;
  website: string | null;
  is_verified: boolean;
  is_business_account: boolean;
  followers_count: number;
  following_count: number;
  media_count: number;
  avg_likes: number;
  avg_comments: number;
  engagement_rate: number;
  posts_per_week: number;
  category: string | null;
  sub_categories: string[];
  market: string;
  languages: string[];
  authenticity_score: number;
  brand_affinity_score: number;
  content_quality_score: number;
  collaboration_score: number;
  estimated_post_cost: number | null;
  estimated_story_cost: number | null;
  partnership_tier: string | null;
  has_branded_content: boolean;
  status: string;
}

export interface PostAnalytics {
  total_posts: number;
  avg_engagement_rate: number;
  total_likes: number;
  total_comments: number;
  top_hashtags: Array<{ hashtag: string; count: number }>;
  peak_posting_times: string[];
  avg_likes_per_post: number;
  avg_comments_per_post: number;
}

export interface TrendingHashtagSummary {
  name: string;
  trend_score: number;
  growth_rate: number;
  post_count: number;
}

export interface TopInfluencerSummary {
  username: string;
  followers: number;
  engagement_rate: number;
  estimated_cost: number | null;
  authenticity_score: number;
}

export interface MarketInsights {
  market: string;
  period: string;
  post_analytics: PostAnalytics;
  trending_hashtags: TrendingHashtagSummary[];
  top_influencers: TopInfluencerSummary[];
}

export type Market = 'germany' | 'france' | 'japan';
export type Category = 'skincare' | 'makeup' | 'haircare';
export type CompetitionLevel = 'low' | 'medium' | 'high';
export type PartnershipStatus = 'discovered' | 'contacted' | 'negotiating' | 'partnered' | 'rejected';
