/**
 * Instagram API Client
 * 
 * Wrapper functions for Instagram API endpoints
 */

import api from './api';
import type {
  InstagramPost,
  InstagramHashtag,
  InstagramInfluencer,
  PostAnalytics,
  MarketInsights,
  Market,
  Category,
  CompetitionLevel,
} from '@/types/instagram';

// ========== POSTS ==========

export interface SearchPostsParams {
  market: Market;
  hashtag?: string;
  category?: Category;
  limit?: number;
  min_engagement?: number;
}

export const searchPosts = async (params: SearchPostsParams): Promise<InstagramPost[]> => {
  const response = await api.get<InstagramPost[]>('/api/v1/instagram/posts', { params });
  return response.data;
};

export const getPostById = async (postId: number): Promise<InstagramPost> => {
  const response = await api.get<InstagramPost>(`/api/v1/instagram/posts/${postId}`);
  return response.data;
};

export interface AnalyzePostsParams {
  market: Market;
  hashtag?: string;
  category?: Category;
}

export const analyzePosts = async (params: AnalyzePostsParams): Promise<PostAnalytics> => {
  const response = await api.get<PostAnalytics>('/api/v1/instagram/posts/analyze', { params });
  return response.data;
};

// ========== HASHTAGS ==========

export interface GetTrendingHashtagsParams {
  market: Market;
  limit?: number;
  min_trend_score?: number;
}

export const getTrendingHashtags = async (params: GetTrendingHashtagsParams): Promise<InstagramHashtag[]> => {
  const response = await api.get<InstagramHashtag[]>('/api/v1/instagram/hashtags/trending', { params });
  return response.data;
};

export interface GetHashtagSuggestionsParams {
  market: Market;
  category?: string;
  difficulty?: CompetitionLevel;
}

export const getHashtagSuggestions = async (params: GetHashtagSuggestionsParams): Promise<InstagramHashtag[]> => {
  const response = await api.get<InstagramHashtag[]>('/api/v1/instagram/hashtags/suggestions', { params });
  return response.data;
};

export interface GetHashtagDetailsParams {
  name: string;
  market: Market;
}

export const getHashtagDetails = async (params: GetHashtagDetailsParams): Promise<InstagramHashtag> => {
  const response = await api.get<InstagramHashtag>(`/api/v1/instagram/hashtags/${params.name}`, {
    params: { market: params.market }
  });
  return response.data;
};

// ========== INFLUENCERS ==========

export interface FindInfluencersParams {
  market: Market;
  min_followers?: number;
  max_followers?: number;
  min_engagement?: number;
  min_authenticity?: number;
  category?: Category;
  limit?: number;
}

export const findInfluencers = async (params: FindInfluencersParams): Promise<InstagramInfluencer[]> => {
  const response = await api.get<InstagramInfluencer[]>('/api/v1/instagram/influencers', { params });
  return response.data;
};

export const getInfluencerByUsername = async (username: string): Promise<InstagramInfluencer> => {
  const response = await api.get<InstagramInfluencer>(`/api/v1/instagram/influencers/${username}`);
  return response.data;
};

export interface UpdateInfluencerStatusParams {
  influencerId: number;
  status: string;
  notes?: string;
}

export const updateInfluencerStatus = async (params: UpdateInfluencerStatusParams): Promise<{ success: boolean }> => {
  const response = await api.patch(`/api/v1/instagram/influencers/${params.influencerId}/status`, null, {
    params: { status: params.status, notes: params.notes }
  });
  return response.data;
};

// ========== INSIGHTS ==========

export const getMarketInsights = async (market: Market): Promise<MarketInsights> => {
  const response = await api.get<MarketInsights>(`/api/v1/instagram/insights/${market}`);
  return response.data;
};

// ========== ADMIN ==========

export const importMockData = async (): Promise<{ success: boolean; imported: any }> => {
  const response = await api.post('/api/v1/instagram/import-mock-data');
  return response.data;
};
