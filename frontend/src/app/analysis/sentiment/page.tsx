/**
 * Sentiment Analysis Dashboard
 * 
 * Analyzes sentiment of Instagram posts and provides market insights
 */

'use client';

import React, { useState } from 'react';
import { aiAnalysisApi, SentimentAnalysisResult } from '@/utils/aiAnalysisApi';
import ScoreCard from '@/components/ai/ScoreCard';
import InsightCard from '@/components/ai/InsightCard';

export default function SentimentAnalysisPage() {
  const [market, setMarket] = useState<string>('germany');
  const [hashtag, setHashtag] = useState<string>('');
  const [limit, setLimit] = useState<number>(50);
  const [loading, setLoading] = useState<boolean>(false);
  const [analysis, setAnalysis] = useState<SentimentAnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async () => {
    setLoading(true);
    setError(null);

    try {
      const result = await aiAnalysisApi.getMarketSentiment(
        market,
        hashtag || undefined,
        limit
      );
      setAnalysis(result);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to analyze sentiment');
      console.error('Sentiment analysis error:', err);
    } finally {
      setLoading(false);
    }
  };

  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case 'positive':
        return 'success';
      case 'negative':
        return 'danger';
      default:
        return 'warning';
    }
  };

  const getSentimentScore = () => {
    if (!analysis) return 0;
    return analysis.sentiment_score * 100;
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Sentiment Analysis</h1>
          <p className="mt-2 text-gray-600">
            Analyze consumer sentiment and emotions from Instagram posts
          </p>
        </div>

        {/* Analysis Form */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">Analysis Parameters</h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Target Market
              </label>
              <select
                value={market}
                onChange={(e) => setMarket(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="germany">🇩🇪 Germany</option>
                <option value="france">🇫🇷 France</option>
                <option value="japan">🇯🇵 Japan</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Hashtag (Optional)
              </label>
              <input
                type="text"
                value={hashtag}
                onChange={(e) => setHashtag(e.target.value)}
                placeholder="e.g., kbeauty"
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Sample Size
              </label>
              <input
                type="number"
                value={limit}
                onChange={(e) => setLimit(Number(e.target.value))}
                min="10"
                max="100"
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>

          <button
            onClick={handleAnalyze}
            disabled={loading}
            className="w-full bg-blue-600 text-white py-3 px-6 rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors font-medium"
          >
            {loading ? (
              <span className="flex items-center justify-center">
                <svg
                  className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                  ></circle>
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  ></path>
                </svg>
                Analyzing...
              </span>
            ) : (
              'Analyze Sentiment'
            )}
          </button>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-8">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg
                  className="h-5 w-5 text-red-400"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    fillRule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                    clipRule="evenodd"
                  />
                </svg>
              </div>
              <div className="ml-3">
                <p className="text-sm text-red-700">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Analysis Results */}
        {analysis && (
          <div className="space-y-6">
            {/* Overall Sentiment Score */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <ScoreCard
                title="Overall Sentiment"
                score={getSentimentScore()}
                subtitle={`${analysis.overall_sentiment.toUpperCase()} - Based on ${analysis.analyzed_posts_count} posts`}
                variant={getSentimentColor(analysis.overall_sentiment) as any}
                size="lg"
              />
              <ScoreCard
                title="Market Opportunity"
                score={analysis.market_insights.opportunity_score * 100}
                subtitle={`${analysis.market_insights.market_maturity} market`}
                size="lg"
              />
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-sm font-medium text-gray-700 mb-3">Competition Level</h3>
                <div className="text-center">
                  <span className="text-4xl font-bold text-gray-800">
                    {analysis.market_insights.competition_level}
                  </span>
                  <p className="text-xs text-gray-500 mt-2">Market Competition</p>
                </div>
              </div>
            </div>

            {/* Key Themes */}
            <InsightCard
              title="Key Themes"
              insights={analysis.key_themes}
              variant="info"
              icon={
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"
                  />
                </svg>
              }
            />

            {/* Trending Topics */}
            <InsightCard
              title="Trending Topics"
              insights={analysis.trending_topics}
              variant="success"
              icon={
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"
                  />
                </svg>
              }
            />

            {/* Consumer Preferences */}
            <InsightCard
              title="Consumer Preferences"
              insights={analysis.consumer_preferences}
              variant="info"
              icon={
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"
                  />
                </svg>
              }
            />

            {/* Content Insights */}
            <InsightCard
              title="Content Insights"
              insights={analysis.content_insights}
              variant="warning"
              collapsible
              icon={
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
                  />
                </svg>
              }
            />

            {/* Actionable Recommendations */}
            <InsightCard
              title="Actionable Recommendations"
              insights={analysis.actionable_recommendations}
              variant="success"
              icon={
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              }
            />

            {/* Market Insights Details */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold text-gray-800 mb-4">Market Insights</h3>
              <div className="space-y-4">
                <div>
                  <h4 className="text-sm font-medium text-gray-700 mb-2">Recommended Focus</h4>
                  <p className="text-gray-600">{analysis.market_insights.recommended_focus}</p>
                </div>
              </div>
            </div>

            {/* Metadata */}
            <div className="text-center text-sm text-gray-500">
              Analysis completed at {new Date(analysis.analysis_timestamp).toLocaleString()}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
