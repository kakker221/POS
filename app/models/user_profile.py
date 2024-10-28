from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy.orm import relationship
from app.database.database import Base

class UserProfile(Base):
    __tablename__ = 'user_profiles'

    id = Column(Integer, primary_key=True, index=True)
    cognito_user_id = Column(String, unique=True, index=True, nullable=False)
    username = Column(String)
    email = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    modified_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    addresses = relationship("UserAddress", back_populates="user")
    roles = relationship("UserRoleAssignment", back_populates="user")
    preferences = relationship("UserPreference", back_populates="user")
    sessions = relationship("UserSession", back_populates="user")
    activity_logs = relationship("UserActivityLog", back_populates="user")
    contacts = relationship("UserContact", back_populates="user")
