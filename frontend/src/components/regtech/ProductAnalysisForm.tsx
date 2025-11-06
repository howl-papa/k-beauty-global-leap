'use client';

import { useState } from 'react';
import { analyzeProductCompliance } from '@/utils/regtechApi';

interface ProductAnalysisFormProps {
  onAnalysisComplete: (analysis: any) => void;
}

export default function ProductAnalysisForm({ onAnalysisComplete }: ProductAnalysisFormProps) {
  const [formData, setFormData] = useState({
    product_name: '',
    product_category: '',
    brand_name: '',
    target_country: 'US',
    ingredients_text: '',
  });
  
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsAnalyzing(true);
    setError(null);

    try {
      // Parse ingredients from text (comma or newline separated)
      const ingredients = formData.ingredients_text
        .split(/[,\n]/)
        .map((ing) => ing.trim())
        .filter((ing) => ing.length > 0);

      if (ingredients.length === 0) {
        throw new Error('Please enter at least one ingredient');
      }

      const payload = {
        product_name: formData.product_name,
        product_category: formData.product_category || undefined,
        brand_name: formData.brand_name || undefined,
        target_country: formData.target_country,
        ingredients_list: ingredients,
        full_ingredient_text: formData.ingredients_text,
      };

      const result = await analyzeProductCompliance(payload);
      onAnalysisComplete(result);
      
      // Reset form
      setFormData({
        product_name: '',
        product_category: '',
        brand_name: '',
        target_country: 'US',
        ingredients_text: '',
      });
    } catch (err: any) {
      setError(err.message || 'Analysis failed. Please try again.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Product Analysis</h2>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Product Name */}
        <div>
          <label htmlFor="product_name" className="block text-sm font-medium text-gray-700">
            Product Name <span className="text-red-500">*</span>
          </label>
          <input
            type="text"
            id="product_name"
            required
            value={formData.product_name}
            onChange={(e) => setFormData({ ...formData, product_name: e.target.value })}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm px-4 py-2 border"
            placeholder="e.g., Hydrating Face Serum"
          />
        </div>

        {/* Brand Name */}
        <div>
          <label htmlFor="brand_name" className="block text-sm font-medium text-gray-700">
            Brand Name
          </label>
          <input
            type="text"
            id="brand_name"
            value={formData.brand_name}
            onChange={(e) => setFormData({ ...formData, brand_name: e.target.value })}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm px-4 py-2 border"
            placeholder="e.g., K-Beauty Labs"
          />
        </div>

        {/* Product Category */}
        <div>
          <label htmlFor="product_category" className="block text-sm font-medium text-gray-700">
            Product Category
          </label>
          <select
            id="product_category"
            value={formData.product_category}
            onChange={(e) => setFormData({ ...formData, product_category: e.target.value })}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm px-4 py-2 border"
          >
            <option value="">Select category...</option>
            <option value="Skincare">Skincare</option>
            <option value="Makeup">Makeup</option>
            <option value="Haircare">Haircare</option>
            <option value="Body Care">Body Care</option>
            <option value="Sun Protection">Sun Protection</option>
            <option value="Other">Other</option>
          </select>
        </div>

        {/* Target Country */}
        <div>
          <label htmlFor="target_country" className="block text-sm font-medium text-gray-700">
            Target Market <span className="text-red-500">*</span>
          </label>
          <select
            id="target_country"
            required
            value={formData.target_country}
            onChange={(e) => setFormData({ ...formData, target_country: e.target.value })}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm px-4 py-2 border"
          >
            <optgroup label="Americas">
              <option value="US">🇺🇸 United States (FDA MoCRA)</option>
            </optgroup>
            <optgroup label="Europe">
              <option value="EU">🇪🇺 European Union (CPNP)</option>
              <option value="DE">🇩🇪 Germany</option>
              <option value="FR">🇫🇷 France</option>
              <option value="IT">🇮🇹 Italy</option>
              <option value="ES">🇪🇸 Spain</option>
              <option value="UK">🇬🇧 United Kingdom</option>
            </optgroup>
            <optgroup label="Asia-Pacific">
              <option value="TH">🇹🇭 Thailand (ASEAN)</option>
              <option value="SG">🇸🇬 Singapore (ASEAN)</option>
              <option value="MY">🇲🇾 Malaysia (ASEAN)</option>
              <option value="ID">🇮🇩 Indonesia (ASEAN)</option>
              <option value="VN">🇻🇳 Vietnam (ASEAN)</option>
            </optgroup>
          </select>
        </div>

        {/* Ingredients */}
        <div>
          <label htmlFor="ingredients_text" className="block text-sm font-medium text-gray-700">
            Ingredients List <span className="text-red-500">*</span>
          </label>
          <p className="text-xs text-gray-500 mt-1">
            Enter ingredients separated by commas or line breaks
          </p>
          <textarea
            id="ingredients_text"
            required
            rows={8}
            value={formData.ingredients_text}
            onChange={(e) => setFormData({ ...formData, ingredients_text: e.target.value })}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm px-4 py-2 border"
            placeholder="Water, Glycerin, Hyaluronic Acid, Niacinamide, Panthenol, Adenosine, Caffeine..."
          />
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded relative">
            <span className="block sm:inline">{error}</span>
          </div>
        )}

        {/* Submit Button */}
        <button
          type="submit"
          disabled={isAnalyzing}
          className="w-full flex justify-center items-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {isAnalyzing ? (
            <>
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
            </>
          ) : (
            <>
              🔍 Analyze Product
            </>
          )}
        </button>
      </form>
    </div>
  );
}
