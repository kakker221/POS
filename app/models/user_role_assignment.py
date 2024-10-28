from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy.orm import relationship
from app.database.database import Base

class UserRoleAssignment(Base):
    __tablename__ = 'user_role_assignments'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user_profiles.id', ondelete="CASCADE"))
    role_id = Column(Integer, ForeignKey('user_roles.id', ondelete="CASCADE"))
    
    user = relationship("UserProfile", back_populates="roles")
    role = relationship("UserRole")