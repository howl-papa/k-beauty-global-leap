from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class RegulationType(str, Enum):
    """Types of cosmetic regulations"""
    FDA_MOCRA = "FDA_MOCRA"
    EU_CPNP = "EU_CPNP"
    ASEAN = "ASEAN"
    OTHER = "OTHER"


class ComplianceStatus(str, Enum):
    """Compliance status levels"""
    COMPLIANT = "COMPLIANT"
    WARNING = "WARNING"
    NON_COMPLIANT = "NON_COMPLIANT"
    PENDING = "PENDING"


class RiskLevel(str, Enum):
    """Risk level categories"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


# ============= Product Analysis Schemas =============

class ProductAnalysisRequest(BaseModel):
    """Request schema for analyzing product compliance"""
    product_name: str = Field(..., min_length=1, max_length=500, description="Name of the cosmetic product")
    product_category: Optional[str] = Field(None, max_length=200, description="Product category (e.g., Skincare, Makeup)")
    brand_name: Optional[str] = Field(None, max_length=200, description="Brand name")
    target_country: str = Field(..., description="Target market country code (e.g., US, EU, TH)")
    ingredients_list: List[str] = Field(..., min_items=1, description="List of ingredient names")
    full_ingredient_text: Optional[str] = Field(None, description="Raw ingredient list text")
    
    class Config:
        json_schema_extra = {
            "example": {
                "product_name": "Hydrating Face Serum",
                "product_category": "Skincare",
                "brand_name": "K-Beauty Labs",
                "target_country": "US",
                "ingredients_list": [
                    "Water",
                    "Glycerin",
                    "Hyaluronic Acid",
                    "Niacinamide",
                    "Panthenol"
                ],
                "full_ingredient_text": "Water, Glycerin, Hyaluronic Acid, Niacinamide, Panthenol"
            }
        }


class IngredientFinding(BaseModel):
    """Schema for ingredient compliance finding"""
    ingredient_name: str
    cas_number: Optional[str] = None
    inci_name: Optional[str] = None
    status: str  # PROHIBITED, RESTRICTED, ALLOWED_WITH_LIMITS
    regulation_type: str
    max_concentration: Optional[str] = None
    restriction_notes: Optional[str] = None
    hazard_category: Optional[str] = None
    alternatives: Optional[List[str]] = None


class ProductAnalysisResponse(BaseModel):
    """Response schema for product compliance analysis"""
    id: int
    product_name: str
    product_category: Optional[str]
    brand_name: Optional[str]
    target_country: str
    regulation_type: str
    
    # Compliance results
    compliance_status: ComplianceStatus
    compliance_score: float = Field(..., ge=0, le=100)
    risk_level: RiskLevel
    
    # Findings
    prohibited_ingredients_found: List[IngredientFinding] = []
    restricted_ingredients_found: List[IngredientFinding] = []
    warnings: List[str] = []
    recommendations: List[str] = []
    
    # AI analysis
    ai_analysis_summary: Optional[str] = None
    ai_model_used: Optional[str] = None
    
    # Timestamps
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ProductAnalysisSummary(BaseModel):
    """Summary schema for listing product analyses"""
    id: int
    product_name: str
    target_country: str
    compliance_status: ComplianceStatus
    compliance_score: float
    risk_level: RiskLevel
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============= Regulation Document Schemas =============

class RegulationDocumentBase(BaseModel):
    """Base schema for regulation documents"""
    regulation_type: RegulationType
    country_code: str = Field(..., max_length=10)
    title: str = Field(..., max_length=500)
    description: Optional[str] = None
    source_url: Optional[str] = None
    version: Optional[str] = None
    effective_date: Optional[datetime] = None


class RegulationDocumentResponse(RegulationDocumentBase):
    """Response schema for regulation documents"""
    id: int
    last_updated: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============= Prohibited Ingredient Schemas =============

class ProhibitedIngredientBase(BaseModel):
    """Base schema for prohibited ingredients"""
    ingredient_name: str
    cas_number: Optional[str] = None
    inci_name: Optional[str] = None
    regulation_type: RegulationType
    country_code: str
    status: str
    max_concentration: Optional[str] = None
    restriction_notes: Optional[str] = None
    hazard_category: Optional[str] = None


class ProhibitedIngredientResponse(ProhibitedIngredientBase):
    """Response schema for prohibited ingredients"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class IngredientSearchRequest(BaseModel):
    """Request schema for searching ingredients"""
    ingredient_name: Optional[str] = None
    country_code: Optional[str] = None
    regulation_type: Optional[RegulationType] = None
    status: Optional[str] = None


# ============= Compliance Alert Schemas =============

class ComplianceAlertBase(BaseModel):
    """Base schema for compliance alerts"""
    title: str
    description: str
    regulation_type: str
    country_code: str
    severity: RiskLevel
    affected_ingredients: Optional[List[str]] = None
    affected_categories: Optional[List[str]] = None
    effective_date: Optional[datetime] = None
    source_url: Optional[str] = None


class ComplianceAlertResponse(ComplianceAlertBase):
    """Response schema for compliance alerts"""
    id: int
    published_date: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============= Statistics and Dashboard Schemas =============

class ComplianceStatistics(BaseModel):
    """Statistics for compliance dashboard"""
    total_analyses: int
    compliant_count: int
    warning_count: int
    non_compliant_count: int
    average_compliance_score: float
    recent_analyses: List[ProductAnalysisSummary]


class RegulationCoverage(BaseModel):
    """Regulation coverage statistics"""
    regulation_type: str
    country_code: str
    document_count: int
    ingredient_count: int
    last_updated: datetime
