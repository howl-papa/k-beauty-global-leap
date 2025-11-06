from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime
import enum


class RegulationType(str, enum.Enum):
    """Types of cosmetic regulations"""
    FDA_MOCRA = "FDA_MOCRA"  # US FDA Modernization of Cosmetics Regulation Act
    EU_CPNP = "EU_CPNP"      # EU Cosmetic Products Notification Portal
    ASEAN = "ASEAN"          # ASEAN Cosmetic Directive
    OTHER = "OTHER"


class RegulationDocument(Base):
    """Model for storing regulation documents and guidelines"""
    
    __tablename__ = "regulation_documents"
    
    id = Column(Integer, primary_key=True, index=True)
    regulation_type = Column(SQLEnum(RegulationType), nullable=False, index=True)
    country_code = Column(String(10), nullable=False, index=True)  # US, EU, TH, SG, etc.
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    source_url = Column(String(1000), nullable=True)
    document_content = Column(Text, nullable=True)  # Full text content
    last_updated = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Metadata
    version = Column(String(50), nullable=True)
    effective_date = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<RegulationDocument(id={self.id}, type={self.regulation_type}, country={self.country_code})>"


class ProhibitedIngredient(Base):
    """Model for prohibited or restricted cosmetic ingredients"""
    
    __tablename__ = "prohibited_ingredients"
    
    id = Column(Integer, primary_key=True, index=True)
    ingredient_name = Column(String(500), nullable=False, index=True)
    cas_number = Column(String(50), nullable=True, index=True)  # Chemical Abstracts Service number
    inci_name = Column(String(500), nullable=True, index=True)  # International Nomenclature Cosmetic Ingredient
    
    # Regulation details
    regulation_type = Column(SQLEnum(RegulationType), nullable=False, index=True)
    country_code = Column(String(10), nullable=False, index=True)
    status = Column(String(50), nullable=False)  # PROHIBITED, RESTRICTED, ALLOWED_WITH_LIMITS
    
    # Restriction details
    max_concentration = Column(String(100), nullable=True)  # e.g., "0.1%", "2mg/kg"
    restriction_notes = Column(Text, nullable=True)
    prohibited_use_cases = Column(JSON, nullable=True)  # e.g., ["rinse-off products", "leave-on products"]
    
    # Additional info
    hazard_category = Column(String(200), nullable=True)  # e.g., "Carcinogen", "Skin Irritant"
    alternative_ingredients = Column(JSON, nullable=True)  # Suggested alternatives
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<ProhibitedIngredient(id={self.id}, name='{self.ingredient_name}', status={self.status})>"
