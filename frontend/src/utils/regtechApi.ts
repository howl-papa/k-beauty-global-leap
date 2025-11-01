/**
 * RegTech API Utilities
 * 
 * API client functions for RegTech compliance analysis endpoints
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Get authentication token from localStorage
 */
function getAuthToken(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('token');
}

/**
 * Make authenticated API request
 */
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = getAuthToken();
  
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Request failed' }));
    throw new Error(error.detail || `HTTP ${response.status}: ${response.statusText}`);
  }

  return response.json();
}

// ============= Types =============

export interface ProductAnalysisRequest {
  product_name: string;
  product_category?: string;
  brand_name?: string;
  target_country: string;
  ingredients_list: string[];
  full_ingredient_text?: string;
}

export interface IngredientFinding {
  ingredient_name: string;
  cas_number?: string;
  inci_name?: string;
  status: string;
  regulation_type: string;
  max_concentration?: string;
  restriction_notes?: string;
  hazard_category?: string;
  alternatives?: string[];
}

export interface ProductAnalysisResponse {
  id: number;
  product_name: string;
  product_category?: string;
  brand_name?: string;
  target_country: string;
  regulation_type: string;
  compliance_status: 'COMPLIANT' | 'WARNING' | 'NON_COMPLIANT' | 'PENDING';
  compliance_score: number;
  risk_level: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  prohibited_ingredients_found: IngredientFinding[];
  restricted_ingredients_found: IngredientFinding[];
  warnings: string[];
  recommendations: string[];
  ai_analysis_summary?: string;
  ai_model_used?: string;
  created_at: string;
  updated_at: string;
}

export interface ProductAnalysisSummary {
  id: number;
  product_name: string;
  target_country: string;
  compliance_status: 'COMPLIANT' | 'WARNING' | 'NON_COMPLIANT' | 'PENDING';
  compliance_score: number;
  risk_level: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  created_at: string;
}

export interface ComplianceStatistics {
  total_analyses: number;
  compliant_count: number;
  warning_count: number;
  non_compliant_count: number;
  average_compliance_score: number;
  recent_analyses: ProductAnalysisSummary[];
}

// ============= API Functions =============

/**
 * Analyze product compliance
 */
export async function analyzeProductCompliance(
  data: ProductAnalysisRequest
): Promise<ProductAnalysisResponse> {
  return apiRequest<ProductAnalysisResponse>('/api/v1/regtech/analyze', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

/**
 * Get all analyses for current user
 */
export async function getUserAnalyses(
  skip: number = 0,
  limit: number = 20
): Promise<ProductAnalysisSummary[]> {
  return apiRequest<ProductAnalysisSummary[]>(
    `/api/v1/regtech/analyses?skip=${skip}&limit=${limit}`
  );
}

/**
 * Get analysis by ID
 */
export async function getAnalysisById(
  analysisId: number
): Promise<ProductAnalysisResponse> {
  return apiRequest<ProductAnalysisResponse>(
    `/api/v1/regtech/analyses/${analysisId}`
  );
}

/**
 * Get compliance statistics
 */
export async function getComplianceStatistics(): Promise<ComplianceStatistics> {
  return apiRequest<ComplianceStatistics>('/api/v1/regtech/statistics');
}

/**
 * Delete analysis
 */
export async function deleteAnalysis(analysisId: number): Promise<void> {
  return apiRequest<void>(`/api/v1/regtech/analyses/${analysisId}`, {
    method: 'DELETE',
  });
}
