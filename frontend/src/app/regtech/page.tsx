'use client';

import { useState, useEffect } from 'react';
import { useAuthStore } from '@/store/authStore';
import { useRouter } from 'next/navigation';
import ProductAnalysisForm from '@/components/regtech/ProductAnalysisForm';
import AnalysisResults from '@/components/regtech/AnalysisResults';
import ComplianceStatistics from '@/components/regtech/ComplianceStatistics';
import AnalysisHistory from '@/components/regtech/AnalysisHistory';

export default function RegTechPage() {
  const { isAuthenticated, isLoading: authLoading } = useAuthStore();
  const router = useRouter();
  
  const [activeTab, setActiveTab] = useState<'analyze' | 'history' | 'statistics'>('analyze');
  const [currentAnalysis, setCurrentAnalysis] = useState<any>(null);

  // Auth check
  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, authLoading, router]);

  if (authLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  const handleAnalysisComplete = (analysis: any) => {
    setCurrentAnalysis(analysis);
    setActiveTab('analyze');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-3">
                🔬 RegTech Compliance
              </h1>
              <p className="mt-2 text-gray-600">
                AI-powered cosmetic regulatory compliance analysis
              </p>
            </div>
            <div className="flex items-center gap-2">
              <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium">
                🇺🇸 FDA MoCRA
              </span>
              <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">
                🇪🇺 EU CPNP
              </span>
              <span className="px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-sm font-medium">
                🌏 ASEAN
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex space-x-8" aria-label="Tabs">
            <button
              onClick={() => setActiveTab('analyze')}
              className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                activeTab === 'analyze'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              ⚗️ Analyze Product
            </button>
            <button
              onClick={() => setActiveTab('history')}
              className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                activeTab === 'history'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              📋 Analysis History
            </button>
            <button
              onClick={() => setActiveTab('statistics')}
              className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                activeTab === 'statistics'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              📊 Statistics
            </button>
          </nav>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'analyze' && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div>
              <ProductAnalysisForm onAnalysisComplete={handleAnalysisComplete} />
            </div>
            <div>
              {currentAnalysis ? (
                <AnalysisResults analysis={currentAnalysis} />
              ) : (
                <div className="bg-white rounded-lg shadow-md p-8 text-center text-gray-500">
                  <div className="text-6xl mb-4">🔍</div>
                  <p className="text-lg">
                    Submit a product for analysis to see results here
                  </p>
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === 'history' && (
          <AnalysisHistory onViewAnalysis={setCurrentAnalysis} />
        )}

        {activeTab === 'statistics' && (
          <ComplianceStatistics />
        )}
      </div>
    </div>
  );
}
