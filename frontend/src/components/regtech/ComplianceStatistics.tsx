'use client';

import { useState, useEffect } from 'react';
import { getComplianceStatistics } from '@/utils/regtechApi';
import type { ComplianceStatistics as Stats } from '@/utils/regtechApi';

export default function ComplianceStatistics() {
  const [statistics, setStatistics] = useState<Stats | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchStatistics();
  }, []);

  const fetchStatistics = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await getComplianceStatistics();
      setStatistics(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
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
        <p>Error loading statistics: {error}</p>
      </div>
    );
  }

  if (!statistics || statistics.total_analyses === 0) {
    return (
      <div className="text-center py-12">
        <div className="text-6xl mb-4">📊</div>
        <h3 className="text-xl font-semibold text-gray-900 mb-2">No statistics yet</h3>
        <p className="text-gray-600">
          Analyze some products to see your compliance statistics
        </p>
      </div>
    );
  }

  const complianceRate = statistics.total_analyses > 0
    ? (statistics.compliant_count / statistics.total_analyses) * 100
    : 0;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-gray-900">Compliance Statistics</h2>
        <button
          onClick={fetchStatistics}
          className="px-4 py-2 text-sm font-medium text-blue-600 hover:text-blue-700 transition-colors"
        >
          🔄 Refresh
        </button>
      </div>

      {/* Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 mb-1">Total Analyses</p>
              <p className="text-3xl font-bold text-gray-900">{statistics.total_analyses}</p>
            </div>
            <div className="text-4xl">📋</div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 mb-1">Compliant</p>
              <p className="text-3xl font-bold text-green-600">{statistics.compliant_count}</p>
            </div>
            <div className="text-4xl">✅</div>
          </div>
          <p className="text-xs text-gray-500 mt-2">
            {complianceRate.toFixed(1)}% compliance rate
          </p>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 mb-1">Warnings</p>
              <p className="text-3xl font-bold text-yellow-600">{statistics.warning_count}</p>
            </div>
            <div className="text-4xl">⚠️</div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 mb-1">Non-Compliant</p>
              <p className="text-3xl font-bold text-red-600">{statistics.non_compliant_count}</p>
            </div>
            <div className="text-4xl">❌</div>
          </div>
        </div>
      </div>

      {/* Average Score */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Average Compliance Score</h3>
        <div className="flex items-center gap-4">
          <div className="flex-1">
            <div className="w-full bg-gray-200 rounded-full h-8">
              <div
                className={`h-8 rounded-full transition-all flex items-center justify-end pr-3 ${
                  statistics.average_compliance_score >= 90
                    ? 'bg-green-500'
                    : statistics.average_compliance_score >= 70
                    ? 'bg-yellow-500'
                    : statistics.average_compliance_score >= 50
                    ? 'bg-orange-500'
                    : 'bg-red-500'
                }`}
                style={{ width: `${statistics.average_compliance_score}%` }}
              >
                <span className="text-white font-bold text-sm">
                  {statistics.average_compliance_score.toFixed(1)}
                </span>
              </div>
            </div>
          </div>
          <div className="text-4xl font-bold text-gray-900">
            {statistics.average_compliance_score.toFixed(0)}<span className="text-2xl text-gray-500">/100</span>
          </div>
        </div>
      </div>

      {/* Compliance Distribution Chart */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Compliance Distribution</h3>
        <div className="space-y-3">
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-green-700">Compliant</span>
              <span className="text-sm text-gray-600">
                {statistics.compliant_count} ({((statistics.compliant_count / statistics.total_analyses) * 100).toFixed(0)}%)
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-3">
              <div
                className="h-3 bg-green-500 rounded-full"
                style={{ width: `${(statistics.compliant_count / statistics.total_analyses) * 100}%` }}
              ></div>
            </div>
          </div>

          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-yellow-700">Warning</span>
              <span className="text-sm text-gray-600">
                {statistics.warning_count} ({((statistics.warning_count / statistics.total_analyses) * 100).toFixed(0)}%)
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-3">
              <div
                className="h-3 bg-yellow-500 rounded-full"
                style={{ width: `${(statistics.warning_count / statistics.total_analyses) * 100}%` }}
              ></div>
            </div>
          </div>

          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-red-700">Non-Compliant</span>
              <span className="text-sm text-gray-600">
                {statistics.non_compliant_count} ({((statistics.non_compliant_count / statistics.total_analyses) * 100).toFixed(0)}%)
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-3">
              <div
                className="h-3 bg-red-500 rounded-full"
                style={{ width: `${(statistics.non_compliant_count / statistics.total_analyses) * 100}%` }}
              ></div>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Analyses */}
      {statistics.recent_analyses && statistics.recent_analyses.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Analyses</h3>
          <div className="space-y-3">
            {statistics.recent_analyses.map((analysis) => (
              <div
                key={analysis.id}
                className="flex items-center justify-between border-b border-gray-200 pb-3 last:border-0"
              >
                <div className="flex-1">
                  <p className="font-medium text-gray-900">{analysis.product_name}</p>
                  <p className="text-xs text-gray-500">
                    {new Date(analysis.created_at).toLocaleDateString()} • {analysis.target_country}
                  </p>
                </div>
                <div className="flex items-center gap-3">
                  <span className={`px-2 py-1 rounded text-xs font-medium ${
                    analysis.compliance_status === 'COMPLIANT'
                      ? 'bg-green-100 text-green-800'
                      : analysis.compliance_status === 'WARNING'
                      ? 'bg-yellow-100 text-yellow-800'
                      : 'bg-red-100 text-red-800'
                  }`}>
                    {analysis.compliance_status}
                  </span>
                  <span className="text-lg font-bold text-gray-900">
                    {analysis.compliance_score.toFixed(0)}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
