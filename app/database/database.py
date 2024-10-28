import boto3
import json
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

def get_secret():
    secret_name = "dev/posapp/db"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    client = boto3.client('secretsmanager', region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = get_secret_value_response['SecretString']

        return json.loads(secret)
    except Exception as e:
        raise Exception(f"Error retrieving secret: {str(e)}")

secret = get_secret()
DATABASE_URL = f"postgresql://{secret['username']}:{secret['password']}@{secret['host']}/{secret['db_name']}"

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()