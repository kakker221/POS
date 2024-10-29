from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from app.utils.utils import get_secret, get_env_path

env_path = get_env_path()
load_dotenv(dotenv_path=env_path)

secret_name = os.getenv("AWS_DATABASE_SECRET_NAME")
region_name = os.getenv("AWS_DATABASE_SECRETS_REGION_NAME")

secret = get_secret(secret_name, region_name)
DATABASE_URL = f"postgresql://{secret['username']}:{secret['password']}@{secret['host']}/{secret['db_name']}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()