/**
 * Trend Analysis Dashboard
 * 
 * Predicts future trends and provides strategic marketing recommendations
 */

'use client';

import React, { useState } from 'react';
import { aiAnalysisApi, TrendAnalysisResult, EmergingTrend, PredictedTrend } from '@/utils/aiAnalysisApi';
import ScoreCard from '@/components/ai/ScoreCard';
import InsightCard from '@/components/ai/InsightCard';

export default function TrendAnalysisPage() {
  const [market, setMarket] = useState<string>('germany');
  const [limit, setLimit] = useState<number>(20);
  const [loading, setLoading] = useState<boolean>(false);
  const [analysis, setAnalysis] = useState<TrendAnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async () => {
    setLoading(true);
    setError(null);

    try {
      const result = await aiAnalysisApi.getMarketTrends(market, limit);
      setAnalysis(result);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to analyze trends');
      console.error('Trend analysis error:', err);
    } finally {
      setLoading(false);
    }
  };

  const getGrowthPotentialColor = (potential: string) => {
    switch (potential) {
      case 'high':
        return 'text-green-600 bg-green-100';
      case 'medium':
        return 'text-yellow-600 bg-yellow-100';
      default:
        return 'text-gray-600 bg-gray-100';
    }
  };

  const getConfidenceBadge = (confidence: number) => {
    const percentage = Math.round(confidence * 100);
    let color = 'bg-gray-100 text-gray-700';
    if (percentage >= 80) color = 'bg-green-100 text-green-700';
    else if (percentage >= 60) color = 'bg-blue-100 text-blue-700';
    else if (percentage >= 40) color = 'bg-yellow-100 text-yellow-700';

    return (
      <span className={`px-2 py-1 rounded-full text-xs font-semibold ${color}`}>
        {percentage}% confident
      </span>
    );
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Trend Analysis & Prediction</h1>
          <p className="mt-2 text-gray-600">
            Discover emerging trends and predict future market movements
          </p>
        </div>

        {/* Analysis Form */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">Analysis Parameters</h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
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
                Number of Hashtags
              </label>
              <input
                type="number"
                value={limit}
                onChange={(e) => setLimit(Number(e.target.value))}
                min="5"
                max="50"
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
                Analyzing Trends...
              </span>
            ) : (
              'Analyze Trends'
            )}
          </button>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-8">
            <p className="text-sm text-red-700">{error}</p>
          </div>
        )}

        {/* Analysis Results */}
        {analysis && (
          <div className="space-y-6">
            {/* Emerging Trends */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
                <svg
                  className="w-6 h-6 mr-2 text-green-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"
                  />
                </svg>
                Emerging Trends
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {analysis.emerging_trends.map((trend: EmergingTrend, index: number) => (
                  <div key={index} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex items-start justify-between mb-2">
                      <h4 className="font-semibold text-gray-800">{trend.trend}</h4>
                      <span
                        className={`px-2 py-1 rounded-full text-xs font-semibold ${getGrowthPotentialColor(
                          trend.growth_potential
                        )}`}
                      >
                        {trend.growth_potential.toUpperCase()}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600 mb-2">{trend.description}</p>
                    <p className="text-xs text-gray-500">
                      ⏱️ Time to peak: {trend.time_to_peak}
                    </p>
                  </div>
                ))}
              </div>
            </div>

            {/* Predicted Trends */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
                <svg
                  className="w-6 h-6 mr-2 text-blue-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
                  />
                </svg>
                Predicted Trends
              </h3>
              <div className="space-y-4">
                {analysis.predicted_trends.map((trend: PredictedTrend, index: number) => (
                  <div key={index} className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                    <div className="flex items-start justify-between mb-2">
                      <h4 className="font-semibold text-gray-800">{trend.trend}</h4>
                      {getConfidenceBadge(trend.confidence)}
                    </div>
                    <p className="text-sm text-gray-700 mb-2">{trend.market_impact}</p>
                    <p className="text-xs text-gray-600">📅 Timeframe: {trend.timeframe}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Declining Trends */}
            {analysis.declining_trends && analysis.declining_trends.length > 0 && (
              <InsightCard
                title="Declining Trends"
                insights={analysis.declining_trends}
                variant="warning"
                icon={
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6"
                    />
                  </svg>
                }
              />
            )}

            {/* Seasonal Patterns */}
            <InsightCard
              title="Seasonal Patterns"
              insights={analysis.seasonal_patterns}
              variant="info"
              collapsible
              icon={
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"
                  />
                </svg>
              }
            />

            {/* Competitive Landscape */}
            <InsightCard
              title="Competitive Landscape"
              insights={analysis.competitive_landscape}
              variant="warning"
              collapsible
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

            {/* Consumer Behavior */}
            <InsightCard
              title="Consumer Behavior Insights"
              insights={analysis.consumer_behavior}
              variant="info"
              collapsible
              icon={
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                  />
                </svg>
              }
            />

            {/* Marketing Recommendations */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
                <svg
                  className="w-6 h-6 mr-2 text-green-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
                Marketing Recommendations
              </h3>
              <div className="space-y-4">
                {analysis.marketing_recommendations.map((rec, index) => (
                  <div key={index} className="bg-green-50 border border-green-200 rounded-lg p-4">
                    <div className="flex items-start justify-between mb-2">
                      <h4 className="font-semibold text-gray-800">{rec.action}</h4>
                      <div className="flex flex-col items-end space-y-1">
                        <span className="px-2 py-1 rounded-full text-xs font-semibold bg-blue-100 text-blue-700">
                          {rec.expected_impact} impact
                        </span>
                        <span className="px-2 py-1 rounded-full text-xs font-semibold bg-gray-100 text-gray-700">
                          {rec.timeline}
                        </span>
                      </div>
                    </div>
                    <p className="text-sm text-gray-700">{rec.rationale}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Metadata */}
            <div className="text-center text-sm text-gray-500">
              Analyzed {analysis.analyzed_hashtags_count} hashtags •{' '}
              {new Date(analysis.analysis_timestamp).toLocaleString()}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
