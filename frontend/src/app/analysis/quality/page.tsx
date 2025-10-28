/**
 * Content Quality Analyzer
 * 
 * Evaluates Instagram post quality and provides improvement suggestions
 */

'use client';

import React, { useState } from 'react';
import { aiAnalysisApi, ContentQualityResult } from '@/utils/aiAnalysisApi';
import ScoreCard from '@/components/ai/ScoreCard';
import InsightCard from '@/components/ai/InsightCard';

export default function ContentQualityPage() {
  const [postId, setPostId] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [analysis, setAnalysis] = useState<ContentQualityResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async () => {
    if (!postId) {
      setError('Please enter a post ID');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const result = await aiAnalysisApi.getPostQuality(Number(postId), true);
      setAnalysis(result);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to analyze content quality');
      console.error('Quality analysis error:', err);
    } finally {
      setLoading(false);
    }
  };

  const getPriorityBadge = (priority: string) => {
    const colors = {
      high: 'bg-red-100 text-red-700',
      medium: 'bg-yellow-100 text-yellow-700',
      low: 'bg-blue-100 text-blue-700',
    };
    return colors[priority as keyof typeof colors] || colors.low;
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Content Quality Analyzer</h1>
          <p className="mt-2 text-gray-600">
            Evaluate your content quality and get actionable improvement suggestions
          </p>
        </div>

        {/* Analysis Form */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">Enter Post ID</h2>

          <div className="flex gap-4">
            <input
              type="number"
              value={postId}
              onChange={(e) => setPostId(e.target.value)}
              placeholder="Enter Instagram post ID"
              className="flex-1 px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <button
              onClick={handleAnalyze}
              disabled={loading || !postId}
              className="bg-blue-600 text-white py-2 px-8 rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors font-medium"
            >
              {loading ? 'Analyzing...' : 'Analyze'}
            </button>
          </div>
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
            {/* Overall Score */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <ScoreCard
                title="Overall Quality"
                score={analysis.overall_score}
                subtitle="Composite score across all metrics"
                size="lg"
                type="circular"
              />
              <ScoreCard
                title="Visual Appeal"
                score={analysis.scores.visual_appeal}
                subtitle="Image/video quality"
              />
              <ScoreCard
                title="Caption Quality"
                score={analysis.scores.caption_quality}
                subtitle="Writing effectiveness"
              />
            </div>

            {/* Additional Scores */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <ScoreCard
                title="Hashtag Relevance"
                score={analysis.scores.hashtag_relevance}
                subtitle="Hashtag effectiveness"
              />
              <ScoreCard
                title="Engagement Potential"
                score={analysis.scores.engagement_potential}
                subtitle="Predicted engagement"
              />
              <ScoreCard
                title="Brand Alignment"
                score={analysis.scores.brand_alignment}
                subtitle="Brand consistency"
              />
            </div>

            {/* Strengths */}
            <InsightCard
              title="Strengths"
              insights={analysis.strengths}
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

            {/* Weaknesses */}
            {analysis.weaknesses && analysis.weaknesses.length > 0 && (
              <InsightCard
                title="Areas for Improvement"
                insights={analysis.weaknesses}
                variant="warning"
                icon={
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                    />
                  </svg>
                }
              />
            )}

            {/* Improvement Suggestions */}
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
                    d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
                  />
                </svg>
                Improvement Suggestions
              </h3>
              <div className="space-y-4">
                {analysis.improvement_suggestions.map((suggestion, index) => (
                  <div
                    key={index}
                    className="border border-gray-200 rounded-lg p-4 hover:border-blue-300 transition-colors"
                  >
                    <div className="flex items-start justify-between mb-2">
                      <h4 className="font-semibold text-gray-800 capitalize">{suggestion.area}</h4>
                      <span
                        className={`px-2 py-1 rounded-full text-xs font-semibold ${getPriorityBadge(
                          suggestion.priority
                        )}`}
                      >
                        {suggestion.priority.toUpperCase()} PRIORITY
                      </span>
                    </div>
                    <p className="text-sm text-gray-700 mb-2">{suggestion.suggestion}</p>
                    <p className="text-xs text-green-600">
                      💡 Expected impact: {suggestion.expected_impact}
                    </p>
                  </div>
                ))}
              </div>
            </div>

            {/* Best Practices */}
            <InsightCard
              title="Best Practices Followed"
              insights={analysis.best_practices_followed}
              variant="success"
              collapsible
              icon={
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M5 13l4 4L19 7"
                  />
                </svg>
              }
            />

            {/* Missed Opportunities */}
            {analysis.missed_opportunities && analysis.missed_opportunities.length > 0 && (
              <InsightCard
                title="Missed Opportunities"
                insights={analysis.missed_opportunities}
                variant="info"
                collapsible
                icon={
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                  </svg>
                }
              />
            )}

            {/* Competitive Advantage */}
            <div className="bg-gradient-to-r from-purple-50 to-pink-50 border border-purple-200 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-gray-800 mb-2">Competitive Advantage</h3>
              <p className="text-gray-700">{analysis.competitive_advantage}</p>
            </div>

            {/* Metadata */}
            <div className="text-center text-sm text-gray-500">
              Post ID: {analysis.post_id} •{' '}
              {new Date(analysis.analysis_timestamp).toLocaleString()}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
