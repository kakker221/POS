import boto3
import json
import os

def get_secret(secret_name, region_name):
    client = boto3.client('secretsmanager', region_name=region_name)
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = get_secret_value_response['SecretString']

        return json.loads(secret)
    except Exception as e:
        raise Exception(f"Error retrieving secret: {str(e)}")
    
def get_env_path():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '../../.env'))