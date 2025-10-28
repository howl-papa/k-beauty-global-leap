'use client';

import { useState, useEffect } from 'react';
import { useAuthStore } from '@/store/authStore';
import { useRouter } from 'next/navigation';
import { findInfluencers } from '@/utils/instagramApi';
import type { InstagramInfluencer, Market, Category } from '@/types/instagram';

export default function InfluencersPage() {
  const { isAuthenticated, isLoading: authLoading } = useAuthStore();
  const router = useRouter();

  // State
  const [selectedMarket, setSelectedMarket] = useState<Market>('germany');
  const [selectedCategory, setSelectedCategory] = useState<Category>('skincare');
  const [minFollowers, setMinFollowers] = useState(10000);
  const [maxFollowers, setMaxFollowers] = useState(100000);
  const [minEngagement, setMinEngagement] = useState(3.0);
  const [minAuthenticity, setMinAuthenticity] = useState(70.0);
  
  const [influencers, setInfluencers] = useState<InstagramInfluencer[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Auth check
  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, authLoading, router]);

  // Initial fetch
  useEffect(() => {
    if (isAuthenticated) {
      handleSearch();
    }
  }, [selectedMarket, isAuthenticated]);

  const handleSearch = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const data = await findInfluencers({
        market: selectedMarket,
        min_followers: minFollowers,
        max_followers: maxFollowers,
        min_engagement: minEngagement,
        min_authenticity: minAuthenticity,
        category: selectedCategory,
        limit: 20,
      });
      setInfluencers(data);
    } catch (err: any) {
      console.error('Error fetching influencers:', err);
      setError(err.response?.data?.detail || 'Failed to fetch influencers');
    } finally {
      setIsLoading(false);
    }
  };

  if (authLoading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-pink-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
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

  const getTierBadgeColor = (tier: string | null) => {
    switch (tier) {
      case 'nano':
        return 'bg-gray-100 text-gray-700';
      case 'micro':
        return 'bg-green-100 text-green-700';
      case 'mid':
        return 'bg-blue-100 text-blue-700';
      default:
        return 'bg-gray-100 text-gray-700';
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">👥 Influencer Discovery</h1>
        <p className="text-gray-600 mt-1">Find K-Beauty micro-influencers for partnerships</p>
      </div>

      {/* Search Filters */}
      <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
        <h2 className="text-lg font-bold text-gray-900 mb-4">🔍 Search Filters</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {/* Market */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Market
            </label>
            <select
              value={selectedMarket}
              onChange={(e) => setSelectedMarket(e.target.value as Market)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-pink-500 focus:border-pink-500"
            >
              <option value="germany">🇩🇪 Germany</option>
              <option value="france">🇫🇷 France</option>
              <option value="japan">🇯🇵 Japan</option>
            </select>
          </div>

          {/* Category */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Category
            </label>
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value as Category)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-pink-500 focus:border-pink-500"
            >
              <option value="skincare">Skincare</option>
              <option value="makeup">Makeup</option>
              <option value="haircare">Haircare</option>
            </select>
          </div>

          {/* Min Engagement */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Min Engagement Rate: {minEngagement}%
            </label>
            <input
              type="range"
              min="1"
              max="10"
              step="0.5"
              value={minEngagement}
              onChange={(e) => setMinEngagement(parseFloat(e.target.value))}
              className="w-full"
            />
          </div>

          {/* Min Followers */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Min Followers: {(minFollowers / 1000).toFixed(0)}K
            </label>
            <input
              type="range"
              min="5000"
              max="100000"
              step="5000"
              value={minFollowers}
              onChange={(e) => setMinFollowers(parseInt(e.target.value))}
              className="w-full"
            />
          </div>

          {/* Max Followers */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Max Followers: {(maxFollowers / 1000).toFixed(0)}K
            </label>
            <input
              type="range"
              min="50000"
              max="500000"
              step="50000"
              value={maxFollowers}
              onChange={(e) => setMaxFollowers(parseInt(e.target.value))}
              className="w-full"
            />
          </div>

          {/* Min Authenticity */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Min Authenticity: {minAuthenticity.toFixed(0)}
            </label>
            <input
              type="range"
              min="50"
              max="95"
              step="5"
              value={minAuthenticity}
              onChange={(e) => setMinAuthenticity(parseFloat(e.target.value))}
              className="w-full"
            />
          </div>
        </div>

        <button
          onClick={handleSearch}
          disabled={isLoading}
          className="mt-4 w-full bg-pink-600 text-white px-6 py-3 rounded-lg hover:bg-pink-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors font-medium"
        >
          {isLoading ? 'Searching...' : '🔍 Search Influencers'}
        </button>
      </div>

      {/* Error Display */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-800">{error}</p>
        </div>
      )}

      {/* Results */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-bold text-gray-900">
            Results: {influencers.length} influencers found
          </h2>
          {influencers.length > 0 && (
            <p className="text-sm text-gray-600">
              Sorted by collaboration score
            </p>
          )}
        </div>

        {isLoading ? (
          <div className="flex items-center justify-center py-12">
            <div className="text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-pink-600 mx-auto"></div>
              <p className="mt-4 text-gray-600">Searching for influencers...</p>
            </div>
          </div>
        ) : influencers.length === 0 ? (
          <div className="bg-white rounded-lg shadow-md p-12 border border-gray-200 text-center">
            <svg className="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
            <p className="text-gray-600 text-lg">No influencers found matching your criteria</p>
            <p className="text-gray-500 text-sm mt-2">Try adjusting your filters</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {influencers.map((influencer) => (
              <div
                key={influencer.id}
                className="bg-white rounded-lg shadow-md border border-gray-200 overflow-hidden hover:shadow-xl transition-shadow"
              >
                {/* Header */}
                <div className="bg-gradient-to-br from-pink-50 to-purple-50 p-6">
                  <div className="flex items-center space-x-4">
                    <div className="w-16 h-16 bg-gradient-to-br from-pink-400 to-purple-400 rounded-full flex items-center justify-center text-white text-2xl font-bold">
                      {influencer.username.charAt(0).toUpperCase()}
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center space-x-2">
                        <h3 className="font-bold text-gray-900">@{influencer.username}</h3>
                        {influencer.is_verified && (
                          <svg className="w-5 h-5 text-blue-500" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                          </svg>
                        )}
                      </div>
                      <p className="text-sm text-gray-600">
                        {(influencer.followers_count / 1000).toFixed(1)}K followers
                      </p>
                    </div>
                  </div>
                  
                  <div className="mt-3">
                    <span className={`inline-block px-3 py-1 rounded-full text-xs font-semibold ${getTierBadgeColor(influencer.partnership_tier)}`}>
                      {influencer.partnership_tier?.toUpperCase() || 'NANO'}
                    </span>
                  </div>
                </div>

                {/* Bio */}
                {influencer.biography && (
                  <div className="px-6 py-3 border-b border-gray-100">
                    <p className="text-sm text-gray-600 line-clamp-2">
                      {influencer.biography}
                    </p>
                  </div>
                )}

                {/* Metrics */}
                <div className="px-6 py-4 space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Engagement Rate</span>
                    <span className="font-semibold text-pink-600">
                      {influencer.engagement_rate.toFixed(1)}%
                    </span>
                  </div>

                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Authenticity</span>
                    <span className={`font-semibold ${getScoreColor(influencer.authenticity_score)}`}>
                      {influencer.authenticity_score.toFixed(0)}
                    </span>
                  </div>

                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Brand Affinity</span>
                    <span className={`font-semibold ${getScoreColor(influencer.brand_affinity_score)}`}>
                      {influencer.brand_affinity_score.toFixed(0)}
                    </span>
                  </div>

                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-600">Content Quality</span>
                    <span className={`font-semibold ${getScoreColor(influencer.content_quality_score)}`}>
                      {influencer.content_quality_score.toFixed(0)}
                    </span>
                  </div>

                  <div className="flex justify-between items-center pt-2 border-t border-gray-200">
                    <span className="text-sm font-medium text-gray-700">Collaboration Score</span>
                    <span className={`font-bold text-lg ${getScoreColor(influencer.collaboration_score)}`}>
                      {influencer.collaboration_score.toFixed(0)}
                    </span>
                  </div>
                </div>

                {/* Pricing */}
                {influencer.estimated_post_cost && (
                  <div className="px-6 py-4 bg-gray-50 border-t border-gray-200">
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-sm text-gray-600">Est. Post Cost</span>
                      <span className="font-bold text-gray-900">
                        ${influencer.estimated_post_cost.toFixed(0)}
                      </span>
                    </div>
                    {influencer.estimated_story_cost && (
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600">Est. Story Cost</span>
                        <span className="font-bold text-gray-900">
                          ${influencer.estimated_story_cost.toFixed(0)}
                        </span>
                      </div>
                    )}
                  </div>
                )}

                {/* Actions */}
                <div className="px-6 py-4 bg-white border-t border-gray-200">
                  <button className="w-full bg-pink-600 text-white px-4 py-2 rounded-lg hover:bg-pink-700 transition-colors font-medium">
                    💌 Contact
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
