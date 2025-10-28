from sqlalchemy import Column, Integer, String, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime


class Company(Base):
    """Company model for K-Beauty brands"""
    
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    industry = Column(String, nullable=True)  # "skincare", "makeup", "haircare"
    target_markets = Column(JSON, default=list)  # ["germany", "france", "japan"]
    website = Column(String, nullable=True)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign key
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="company")
    
    def __repr__(self):
        return f"<Company(id={self.id}, name='{self.name}', industry='{self.industry}')>"
