'use client';

interface AnalysisResultsProps {
  analysis: any;
}

export default function AnalysisResults({ analysis }: AnalysisResultsProps) {
  if (!analysis) return null;

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'COMPLIANT':
        return 'bg-green-100 text-green-800 border-green-200';
      case 'WARNING':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'NON_COMPLIANT':
        return 'bg-red-100 text-red-800 border-red-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'LOW':
        return 'bg-green-500';
      case 'MEDIUM':
        return 'bg-yellow-500';
      case 'HIGH':
        return 'bg-orange-500';
      case 'CRITICAL':
        return 'bg-red-500';
      default:
        return 'bg-gray-500';
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 90) return 'text-green-600';
    if (score >= 70) return 'text-yellow-600';
    if (score >= 50) return 'text-orange-600';
    return 'text-red-600';
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Analysis Results</h2>
        <p className="text-sm text-gray-500">
          Product: <span className="font-medium text-gray-900">{analysis.product_name}</span>
        </p>
        {analysis.brand_name && (
          <p className="text-sm text-gray-500">
            Brand: <span className="font-medium text-gray-900">{analysis.brand_name}</span>
          </p>
        )}
      </div>

      {/* Compliance Status */}
      <div className={`border rounded-lg p-4 ${getStatusColor(analysis.compliance_status)}`}>
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm font-medium mb-1">Compliance Status</p>
            <p className="text-2xl font-bold">{analysis.compliance_status.replace('_', ' ')}</p>
          </div>
          <div className="text-right">
            <p className="text-sm font-medium mb-1">Risk Level</p>
            <div className="flex items-center gap-2">
              <div className={`w-3 h-3 rounded-full ${getRiskColor(analysis.risk_level)}`}></div>
              <p className="text-xl font-bold">{analysis.risk_level}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Compliance Score */}
      <div className="bg-gray-50 rounded-lg p-4">
        <div className="flex items-center justify-between mb-2">
          <p className="text-sm font-medium text-gray-700">Compliance Score</p>
          <p className={`text-3xl font-bold ${getScoreColor(analysis.compliance_score)}`}>
            {analysis.compliance_score.toFixed(1)}/100
          </p>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-4">
          <div
            className={`h-4 rounded-full transition-all ${
              analysis.compliance_score >= 90
                ? 'bg-green-500'
                : analysis.compliance_score >= 70
                ? 'bg-yellow-500'
                : analysis.compliance_score >= 50
                ? 'bg-orange-500'
                : 'bg-red-500'
            }`}
            style={{ width: `${analysis.compliance_score}%` }}
          ></div>
        </div>
      </div>

      {/* Prohibited Ingredients */}
      {analysis.prohibited_ingredients_found && analysis.prohibited_ingredients_found.length > 0 && (
        <div>
          <h3 className="text-lg font-semibold text-red-700 mb-3 flex items-center gap-2">
            ⚠️ Prohibited Ingredients ({analysis.prohibited_ingredients_found.length})
          </h3>
          <div className="space-y-2">
            {analysis.prohibited_ingredients_found.map((ingredient: any, index: number) => (
              <div key={index} className="bg-red-50 border border-red-200 rounded-lg p-3">
                <p className="font-medium text-red-900">{ingredient.ingredient_name}</p>
                {ingredient.cas_number && (
                  <p className="text-xs text-red-700 mt-1">CAS: {ingredient.cas_number}</p>
                )}
                {ingredient.restriction_notes && (
                  <p className="text-sm text-red-800 mt-2">{ingredient.restriction_notes}</p>
                )}
                {ingredient.alternatives && ingredient.alternatives.length > 0 && (
                  <div className="mt-2">
                    <p className="text-xs text-red-700 font-medium">Alternatives:</p>
                    <p className="text-sm text-red-800">{ingredient.alternatives.join(', ')}</p>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Restricted Ingredients */}
      {analysis.restricted_ingredients_found && analysis.restricted_ingredients_found.length > 0 && (
        <div>
          <h3 className="text-lg font-semibold text-yellow-700 mb-3 flex items-center gap-2">
            ⚡ Restricted Ingredients ({analysis.restricted_ingredients_found.length})
          </h3>
          <div className="space-y-2">
            {analysis.restricted_ingredients_found.map((ingredient: any, index: number) => (
              <div key={index} className="bg-yellow-50 border border-yellow-200 rounded-lg p-3">
                <p className="font-medium text-yellow-900">{ingredient.ingredient_name}</p>
                {ingredient.max_concentration && (
                  <p className="text-sm text-yellow-800 mt-1">
                    Max concentration: <span className="font-medium">{ingredient.max_concentration}</span>
                  </p>
                )}
                {ingredient.restriction_notes && (
                  <p className="text-sm text-yellow-800 mt-2">{ingredient.restriction_notes}</p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Warnings */}
      {analysis.warnings && analysis.warnings.length > 0 && (
        <div>
          <h3 className="text-lg font-semibold text-gray-900 mb-3">Warnings</h3>
          <div className="space-y-2">
            {analysis.warnings.map((warning: string, index: number) => (
              <div key={index} className="bg-blue-50 border border-blue-200 rounded-lg p-3">
                <p className="text-sm text-blue-900">{warning}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Recommendations */}
      {analysis.recommendations && analysis.recommendations.length > 0 && (
        <div>
          <h3 className="text-lg font-semibold text-gray-900 mb-3">Recommendations</h3>
          <div className="space-y-2">
            {analysis.recommendations.map((recommendation: string, index: number) => (
              <div key={index} className="bg-green-50 border border-green-200 rounded-lg p-3">
                <p className="text-sm text-green-900">✓ {recommendation}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* AI Analysis Summary */}
      {analysis.ai_analysis_summary && (
        <div>
          <h3 className="text-lg font-semibold text-gray-900 mb-3 flex items-center gap-2">
            🤖 AI Analysis
          </h3>
          <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
            <p className="text-sm text-purple-900 whitespace-pre-wrap">
              {analysis.ai_analysis_summary}
            </p>
            {analysis.ai_model_used && (
              <p className="text-xs text-purple-700 mt-3">
                Powered by {analysis.ai_model_used}
              </p>
            )}
          </div>
        </div>
      )}

      {/* Metadata */}
      <div className="border-t pt-4 text-sm text-gray-500">
        <p>Target Market: {analysis.target_country} ({analysis.regulation_type})</p>
        <p>Analyzed: {new Date(analysis.created_at).toLocaleString()}</p>
      </div>
    </div>
  );
}
