from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime


class User(Base):
    """User model for authentication and profile management"""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    company_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Instagram Integration
    instagram_access_token = Column(String, nullable=True)
    instagram_user_id = Column(String, nullable=True)
    instagram_token_expires_at = Column(DateTime, nullable=True)
    
    # Relationships
    company = relationship("Company", back_populates="user", uselist=False)
    analyses = relationship("Analysis", back_populates="user")
    product_analyses = relationship("ProductAnalysis", back_populates="user")
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', company='{self.company_name}')>"
