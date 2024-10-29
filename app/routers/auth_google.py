from fastapi import APIRouter, HTTPException, Request
from starlette.responses import RedirectResponse
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from google.auth.transport import requests as google_requests
import os
import boto3
import json
from dotenv import load_dotenv

env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../.env'))
load_dotenv(dotenv_path=env_path)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
secret_name = os.getenv("AWS_AUTH_SECRET_NAME")
region_name = os.getenv("AWS_AUTH_SECRETS_REGION_NAME")

def get_secret():
    client = boto3.client('secretsmanager', region_name=region_name)
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = get_secret_value_response['SecretString']
        return json.loads(secret)
    except Exception as e:
        raise Exception(f"Error retrieving secret: {str(e)}")

router = APIRouter()

secrets = get_secret()
CLIENT_ID = secrets.get('client_id')
CLIENT_SECRET = secrets.get('client_secret')
AUTH_URI = secrets.get('auth_uri')
TOKEN_URI = secrets.get('token_uri')
REDIRECT_URIS = secrets.get('redirect_uris')
SCOPES = ['openid', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile']

@router.get("/google-login/")
def login_with_google():
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "auth_uri": AUTH_URI,
                "token_uri": TOKEN_URI
            }
        },
        scopes=SCOPES
    )
    flow.redirect_uri = "http://127.0.0.1:8000/auth/callback"

    auth_url, state = flow.authorization_url(prompt='consent')
    return RedirectResponse(url=auth_url)

@router.get("/callback")
def callback(request: Request):
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "auth_uri": AUTH_URI,
                "token_uri": TOKEN_URI,
                "auth_provider_x509_cert_url": secrets.get('auth_provider_x509_cert_url'),
                "redirect_uris": REDIRECT_URIS
            }
        },
        scopes=SCOPES
    )
    flow.redirect_uri = REDIRECT_URIS  # Use the first redirect URI
    try:
        # Exchange the authorization code for a token
        flow.fetch_token(authorization_response=str(request.url))
    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to fetch token")

    # Get the user's credentials
    credentials = flow.credentials

    try:
        user_info = id_token.verify_oauth2_token(
            credentials.id_token,
            google_requests.Request(), 
            CLIENT_ID,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to verify token")

    # Return user info
    return {"email": user_info['email'], "name": user_info['name']}