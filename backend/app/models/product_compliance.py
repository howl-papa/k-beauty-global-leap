from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, Float, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime
import enum


class ComplianceStatus(str, enum.Enum):
    """Compliance status levels"""
    COMPLIANT = "COMPLIANT"
    WARNING = "WARNING"
    NON_COMPLIANT = "NON_COMPLIANT"
    PENDING = "PENDING"


class RiskLevel(str, enum.Enum):
    """Risk level categories"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ProductAnalysis(Base):
    """Model for storing product compliance analysis results"""
    
    __tablename__ = "product_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    
    # Product information
    product_name = Column(String(500), nullable=False)
    product_category = Column(String(200), nullable=True)  # e.g., "Skincare", "Makeup", "Haircare"
    brand_name = Column(String(200), nullable=True)
    
    # Target market
    target_country = Column(String(10), nullable=False, index=True)  # US, EU, etc.
    regulation_type = Column(String(50), nullable=False)
    
    # Ingredient list
    ingredients_list = Column(JSON, nullable=False)  # Array of ingredient names
    full_ingredient_text = Column(Text, nullable=True)  # Raw ingredient list text
    
    # Compliance results
    compliance_status = Column(SQLEnum(ComplianceStatus), nullable=False, index=True)
    compliance_score = Column(Float, nullable=False)  # 0-100
    risk_level = Column(SQLEnum(RiskLevel), nullable=False)
    
    # Detailed findings
    prohibited_ingredients_found = Column(JSON, nullable=True)  # Array of prohibited ingredients
    restricted_ingredients_found = Column(JSON, nullable=True)  # Array of restricted ingredients
    warnings = Column(JSON, nullable=True)  # Array of warning messages
    recommendations = Column(JSON, nullable=True)  # Array of recommendations
    
    # AI analysis
    ai_analysis_summary = Column(Text, nullable=True)
    ai_model_used = Column(String(100), nullable=True)  # e.g., "gpt-4", "claude-3"
    
    # Report
    report_pdf_url = Column(String(1000), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="product_analyses")
    
    def __repr__(self):
        return f"<ProductAnalysis(id={self.id}, product='{self.product_name}', status={self.compliance_status})>"


class ComplianceAlert(Base):
    """Model for tracking regulation changes and alerts"""
    
    __tablename__ = "compliance_alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Alert details
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=False)
    regulation_type = Column(String(50), nullable=False, index=True)
    country_code = Column(String(10), nullable=False, index=True)
    
    # Severity
    severity = Column(SQLEnum(RiskLevel), nullable=False)
    
    # Affected products/ingredients
    affected_ingredients = Column(JSON, nullable=True)  # Array of ingredient names
    affected_categories = Column(JSON, nullable=True)  # Array of product categories
    
    # Dates
    effective_date = Column(DateTime, nullable=True)
    published_date = Column(DateTime, default=datetime.utcnow)
    
    # Source
    source_url = Column(String(1000), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f"<ComplianceAlert(id={self.id}, title='{self.title}', severity={self.severity})>"
