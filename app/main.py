from fastapi import FastAPI, HTTPException, Depends
import logging
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.crud.crud_user import create_user, get_user, get_users, update_user, delete_user


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Data Analytics Platform"}
       
# Create a new user
@app.post("/users/")
def add_user(user_data: dict, db: Session = Depends(get_db)):
    return create_user(db, user_data)

# Get a user by ID
@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Get all users
@app.get("/users/")
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_users(db, skip, limit)

# Update a user by ID
@app.put("/users/{user_id}")
def modify_user(user_id: int, updated_data: dict, db: Session = Depends(get_db)):
    user = update_user(db, user_id, updated_data)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Delete a user by ID
@app.delete("/users/{user_id}")
def remove_user(user_id: int, db: Session = Depends(get_db)):
    user = delete_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}