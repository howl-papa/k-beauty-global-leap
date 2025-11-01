'use client';

import { useState, useEffect } from 'react';
import { getUserAnalyses, deleteAnalysis, getAnalysisById } from '@/utils/regtechApi';
import type { ProductAnalysisSummary } from '@/utils/regtechApi';

interface AnalysisHistoryProps {
  onViewAnalysis: (analysis: any) => void;
}

export default function AnalysisHistory({ onViewAnalysis }: AnalysisHistoryProps) {
  const [analyses, setAnalyses] = useState<ProductAnalysisSummary[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchAnalyses();
  }, []);

  const fetchAnalyses = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await getUserAnalyses(0, 50);
      setAnalyses(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleView = async (analysisId: number) => {
    try {
      const analysis = await getAnalysisById(analysisId);
      onViewAnalysis(analysis);
    } catch (err: any) {
      alert(`Failed to load analysis: ${err.message}`);
    }
  };

  const handleDelete = async (analysisId: number, productName: string) => {
    if (!confirm(`Are you sure you want to delete the analysis for "${productName}"?`)) {
      return;
    }

    try {
      await deleteAnalysis(analysisId);
      setAnalyses(analyses.filter((a) => a.id !== analysisId));
    } catch (err: any) {
      alert(`Failed to delete analysis: ${err.message}`);
    }
  };

  const getStatusBadge = (status: string) => {
    const styles = {
      COMPLIANT: 'bg-green-100 text-green-800',
      WARNING: 'bg-yellow-100 text-yellow-800',
      NON_COMPLIANT: 'bg-red-100 text-red-800',
      PENDING: 'bg-gray-100 text-gray-800',
    };
    return styles[status as keyof typeof styles] || styles.PENDING;
  };

  const getRiskBadge = (risk: string) => {
    const styles = {
      LOW: 'bg-green-500',
      MEDIUM: 'bg-yellow-500',
      HIGH: 'bg-orange-500',
      CRITICAL: 'bg-red-500',
    };
    return styles[risk as keyof typeof styles] || 'bg-gray-500';
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
        <p>Error loading analyses: {error}</p>
      </div>
    );
  }

  if (analyses.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="text-6xl mb-4">📋</div>
        <h3 className="text-xl font-semibold text-gray-900 mb-2">No analyses yet</h3>
        <p className="text-gray-600">
          Start by analyzing your first product in the "Analyze Product" tab
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-gray-900">
          Analysis History ({analyses.length})
        </h2>
        <button
          onClick={fetchAnalyses}
          className="px-4 py-2 text-sm font-medium text-blue-600 hover:text-blue-700 transition-colors"
        >
          🔄 Refresh
        </button>
      </div>

      <div className="grid gap-4">
        {analyses.map((analysis) => (
          <div
            key={analysis.id}
            className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"
          >
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-2">
                  <h3 className="text-lg font-semibold text-gray-900">
                    {analysis.product_name}
                  </h3>
                  <span className={`px-2 py-1 rounded text-xs font-medium ${getStatusBadge(analysis.compliance_status)}`}>
                    {analysis.compliance_status}
                  </span>
                </div>

                <div className="flex items-center gap-4 text-sm text-gray-600 mb-3">
                  <span className="flex items-center gap-1">
                    🌍 {analysis.target_country}
                  </span>
                  <span className="flex items-center gap-2">
                    <div className={`w-2 h-2 rounded-full ${getRiskBadge(analysis.risk_level)}`}></div>
                    {analysis.risk_level} Risk
                  </span>
                  <span>
                    Score: {analysis.compliance_score.toFixed(1)}/100
                  </span>
                  <span>
                    {new Date(analysis.created_at).toLocaleDateString()}
                  </span>
                </div>

                <div className="flex items-center gap-2">
                  <button
                    onClick={() => handleView(analysis.id)}
                    className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors text-sm font-medium"
                  >
                    View Details
                  </button>
                  <button
                    onClick={() => handleDelete(analysis.id, analysis.product_name)}
                    className="px-4 py-2 bg-red-100 text-red-600 rounded-md hover:bg-red-200 transition-colors text-sm font-medium"
                  >
                    Delete
                  </button>
                </div>
              </div>

              <div className="text-right">
                <div className="text-3xl font-bold text-gray-900 mb-1">
                  {analysis.compliance_score.toFixed(0)}
                </div>
                <div className="text-xs text-gray-500">Compliance</div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
