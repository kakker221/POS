from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy.orm import relationship
from app.database.database import Base

class UserActivityLog(Base):
    __tablename__ = 'user_activity_logs'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user_profiles.id', ondelete="CASCADE"))
    activity_type = Column(String, nullable=False)
    activity_timestamp = Column(DateTime, default=datetime.utcnow)
    details = Column(String)
    
    user = relationship("UserProfile", back_populates="activity_logs")

    