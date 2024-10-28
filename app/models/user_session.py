from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy.orm import relationship
from app.database.database import Base

class UserSession(Base):
    __tablename__ = 'user_sessions'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user_profiles.id', ondelete="CASCADE"))
    login_timestamp = Column(DateTime, default=datetime.utcnow)
    logout_timestamp = Column(DateTime)
    ip_address = Column(String)
    
    user = relationship("UserProfile", back_populates="sessions")