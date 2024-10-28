from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy.orm import relationship
from app.database.database import Base

class UserContact(Base):
    __tablename__ = 'user_contacts'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user_profiles.id', ondelete="CASCADE"))
    contact_name = Column(String, nullable=False)
    contact_relationship = Column(String)
    contact_phone = Column(String)
    contact_email = Column(String)
    
    user = relationship("UserProfile", back_populates="contacts")