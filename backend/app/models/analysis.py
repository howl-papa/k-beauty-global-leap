from sqlalchemy import Column, Integer, String, ForeignKey, JSON, DateTime, Text
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime


class Analysis(Base):
    """Analysis model for storing market analysis results"""
    
    __tablename__ = "analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False, index=True)  # "trend", "localization", "competitor", "market_entry"
    title = Column(String, nullable=False)
    target_market = Column(String, nullable=True)  # "germany", "france", "japan"
    
    # Input and output data stored as JSON
    input_data = Column(JSON, default=dict)
    output_data = Column(JSON, default=dict)
    
    # AI-generated insights
    insights = Column(Text, nullable=True)
    
    # Status tracking
    status = Column(String, default="pending", index=True)  # "pending", "processing", "completed", "failed"
    error_message = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    completed_at = Column(DateTime, nullable=True)
    
    # Foreign key
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="analyses")
    
    def __repr__(self):
        return f"<Analysis(id={self.id}, type='{self.type}', status='{self.status}')>"
