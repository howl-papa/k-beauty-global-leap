'use client';

import { useState, useEffect } from 'react';
import { useAuthStore } from '@/store/authStore';
import { useRouter } from 'next/navigation';
import {
  getMarketInsights,
  getTrendingHashtags,
  searchPosts,
  analyzePosts,
} from '@/utils/instagramApi';
import type {
  MarketInsights,
  InstagramHashtag,
  InstagramPost,
  PostAnalytics,
  Market,
} from '@/types/instagram';

export default function TrendAnalysisPage() {
  const { isAuthenticated, isLoading: authLoading } = useAuthStore();
  const router = useRouter();

  // State
  const [selectedMarket, setSelectedMarket] = useState<Market>('germany');
  const [insights, setInsights] = useState<MarketInsights | null>(null);
  const [trendingHashtags, setTrendingHashtags] = useState<InstagramHashtag[]>([]);
  const [recentPosts, setRecentPosts] = useState<InstagramPost[]>([]);
  const [analytics, setAnalytics] = useState<PostAnalytics | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Auth check
  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, authLoading, router]);

  // Fetch data when market changes
  useEffect(() => {
    if (isAuthenticated) {
      fetchMarketData();
    }
  }, [selectedMarket, isAuthenticated]);

  const fetchMarketData = async () => {
    setIsLoading(true);
    setError(null);

    try {
      // Fetch market insights
      const insightsData = await getMarketInsights(selectedMarket);
      setInsights(insightsData);

      // Fetch trending hashtags
      const hashtagsData = await getTrendingHashtags({
        market: selectedMarket,
        limit: 20,
        min_trend_score: 50,
      });
      setTrendingHashtags(hashtagsData);

      // Fetch recent posts
      const postsData = await searchPosts({
        market: selectedMarket,
        limit: 12,
      });
      setRecentPosts(postsData);

      // Fetch analytics
      const analyticsData = await analyzePosts({
        market: selectedMarket,
      });
      setAnalytics(analyticsData);
    } catch (err: any) {
      console.error('Error fetching market data:', err);
      setError(err.response?.data?.detail || 'Failed to fetch market data');
    } finally {
      setIsLoading(false);
    }
  };

  if (authLoading || isLoading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-pink-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading market insights...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  const marketLabels: Record<Market, string> = {
    germany: '🇩🇪 Germany',
    france: '🇫🇷 France',
    japan: '🇯🇵 Japan',
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">📈 Trend Analysis</h1>
          <p className="text-gray-600 mt-1">K-Beauty market trends and insights</p>
        </div>

        {/* Market Selector */}
        <div className="flex space-x-2">
          {(['germany', 'france', 'japan'] as Market[]).map((market) => (
            <button
              key={market}
              onClick={() => setSelectedMarket(market)}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                selectedMarket === market
                  ? 'bg-pink-600 text-white'
                  : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50'
              }`}
            >
              {marketLabels[market]}
            </button>
          ))}
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-800">{error}</p>
          <button
            onClick={fetchMarketData}
            className="mt-2 text-red-600 hover:text-red-800 font-medium"
          >
            Retry
          </button>
        </div>
      )}

      {/* Overview Stats */}
      {analytics && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Total Posts</p>
                <p className="text-3xl font-bold text-gray-900 mt-2">
                  {analytics.total_posts.toLocaleString()}
                </p>
              </div>
              <div className="bg-blue-100 rounded-full p-3">
                <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
            </div>
            <p className="text-sm text-gray-500 mt-2">Last 30 days</p>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Avg Engagement</p>
                <p className="text-3xl font-bold text-gray-900 mt-2">
                  {analytics.avg_engagement_rate.toFixed(1)}%
                </p>
              </div>
              <div className="bg-green-100 rounded-full p-3">
                <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                </svg>
              </div>
            </div>
            <p className="text-sm text-gray-500 mt-2">Likes + Comments</p>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Total Likes</p>
                <p className="text-3xl font-bold text-gray-900 mt-2">
                  {(analytics.total_likes / 1000).toFixed(1)}K
                </p>
              </div>
              <div className="bg-pink-100 rounded-full p-3">
                <svg className="w-8 h-8 text-pink-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                </svg>
              </div>
            </div>
            <p className="text-sm text-gray-500 mt-2">
              Avg {analytics.avg_likes_per_post.toFixed(0)} per post
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Total Comments</p>
                <p className="text-3xl font-bold text-gray-900 mt-2">
                  {(analytics.total_comments / 1000).toFixed(1)}K
                </p>
              </div>
              <div className="bg-purple-100 rounded-full p-3">
                <svg className="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
              </div>
            </div>
            <p className="text-sm text-gray-500 mt-2">
              Avg {analytics.avg_comments_per_post.toFixed(0)} per post
            </p>
          </div>
        </div>
      )}

      {/* Trending Hashtags */}
      <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
        <h2 className="text-xl font-bold text-gray-900 mb-4">🔥 Trending Hashtags</h2>
        
        {trendingHashtags.length === 0 ? (
          <p className="text-gray-600">No trending hashtags found.</p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {trendingHashtags.slice(0, 8).map((hashtag) => (
              <div
                key={hashtag.id}
                className="border border-gray-200 rounded-lg p-4 hover:border-pink-300 hover:shadow-md transition-all"
              >
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-bold text-lg text-gray-900">#{hashtag.name}</h3>
                  {hashtag.is_trending && (
                    <span className="bg-red-100 text-red-600 text-xs font-bold px-2 py-1 rounded">
                      HOT
                    </span>
                  )}
                </div>
                
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Trend Score</span>
                    <span className="font-semibold text-pink-600">
                      {hashtag.trend_score.toFixed(1)}
                    </span>
                  </div>
                  
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Growth</span>
                    <span className={`font-semibold ${hashtag.growth_rate > 0 ? 'text-green-600' : 'text-red-600'}`}>
                      {hashtag.growth_rate > 0 ? '+' : ''}{hashtag.growth_rate.toFixed(1)}%
                    </span>
                  </div>
                  
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Posts</span>
                    <span className="font-semibold text-gray-900">
                      {(hashtag.post_count / 1000).toFixed(1)}K
                    </span>
                  </div>
                  
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Competition</span>
                    <span className={`font-semibold ${
                      hashtag.competition_level === 'low' ? 'text-green-600' :
                      hashtag.competition_level === 'medium' ? 'text-yellow-600' :
                      'text-red-600'
                    }`}>
                      {hashtag.competition_level?.toUpperCase()}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Top Hashtags by Frequency */}
      {analytics && analytics.top_hashtags.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
          <h2 className="text-xl font-bold text-gray-900 mb-4">📊 Most Used Hashtags</h2>
          <div className="flex flex-wrap gap-3">
            {analytics.top_hashtags.map((item, index) => (
              <div
                key={index}
                className="inline-flex items-center bg-gradient-to-r from-pink-50 to-purple-50 border border-pink-200 rounded-full px-4 py-2"
              >
                <span className="font-semibold text-pink-600">#{item.hashtag}</span>
                <span className="ml-2 bg-pink-200 text-pink-800 text-xs font-bold rounded-full px-2 py-0.5">
                  {item.count}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Peak Posting Times */}
      {analytics && analytics.peak_posting_times.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
          <h2 className="text-xl font-bold text-gray-900 mb-4">⏰ Peak Posting Times</h2>
          <p className="text-gray-600 mb-4">
            Optimal times to post for maximum engagement in {marketLabels[selectedMarket]}:
          </p>
          <div className="flex space-x-4">
            {analytics.peak_posting_times.map((time, index) => (
              <div
                key={index}
                className="flex-1 bg-gradient-to-br from-blue-50 to-indigo-50 border border-blue-200 rounded-lg p-4 text-center"
              >
                <p className="text-sm text-gray-600">#{index + 1} Best Time</p>
                <p className="text-2xl font-bold text-blue-600 mt-1">{time}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Recent Posts */}
      <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
        <h2 className="text-xl font-bold text-gray-900 mb-4">📸 Recent K-Beauty Posts</h2>
        
        {recentPosts.length === 0 ? (
          <p className="text-gray-600">No recent posts found.</p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {recentPosts.slice(0, 6).map((post) => (
              <div
                key={post.id}
                className="border border-gray-200 rounded-lg overflow-hidden hover:shadow-lg transition-shadow"
              >
                <div className="bg-gradient-to-br from-pink-100 to-purple-100 h-48 flex items-center justify-center">
                  <svg className="w-16 h-16 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                </div>
                
                <div className="p-4">
                  <div className="flex items-center justify-between mb-2">
                    <p className="font-semibold text-gray-900">@{post.username}</p>
                    {post.is_verified_account && (
                      <svg className="w-5 h-5 text-blue-500" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                      </svg>
                    )}
                  </div>
                  
                  <p className="text-sm text-gray-600 line-clamp-2 mb-3">
                    {post.caption || 'No caption'}
                  </p>
                  
                  <div className="flex items-center justify-between text-sm">
                    <div className="flex items-center space-x-3">
                      <span className="flex items-center text-gray-600">
                        <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clipRule="evenodd" />
                        </svg>
                        {post.like_count.toLocaleString()}
                      </span>
                      <span className="flex items-center text-gray-600">
                        <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z" clipRule="evenodd" />
                        </svg>
                        {post.comment_count}
                      </span>
                    </div>
                    <span className="bg-pink-100 text-pink-600 text-xs font-semibold px-2 py-1 rounded">
                      {post.engagement_rate.toFixed(1)}%
                    </span>
                  </div>
                  
                  {post.hashtags.length > 0 && (
                    <div className="mt-3 flex flex-wrap gap-1">
                      {post.hashtags.slice(0, 3).map((tag, idx) => (
                        <span key={idx} className="text-xs text-pink-600">
                          #{tag}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
