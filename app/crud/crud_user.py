from sqlalchemy.orm import Session
#import user_profile from the models folder
from app.models.user_profile import UserProfile
from datetime import datetime

# Create a new user
def create_user(db: Session, user_data: dict):
    user = UserProfile(**user_data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Get a user by ID
def get_user(db: Session, user_id: int):
    return db.query(UserProfile).filter(UserProfile.id == user_id).first()

# Get all users
def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(UserProfile).offset(skip).limit(limit).all()

# Update a user by ID
def update_user(db: Session, user_id: int, updated_data: dict):
    user = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if user:
        for key, value in updated_data.items():
            setattr(user, key, value)
        user.modified_at = datetime.utcnow()  # Update the modified timestamp
        db.commit()
        db.refresh(user)
    return user

# Delete a user by ID
def delete_user(db: Session, user_id: int):
    user = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user
