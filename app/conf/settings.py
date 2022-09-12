from pathlib import Path

from decouple import config
import boto3

BASE_DIR = Path(__file__).resolve().parent.parent

n = 200

ADMIN_EMAILS = ['andres64372@hotmail.com','hoyos_j@hotmail.com','upb.camilo@gmail.com']
DOMAIN = 'https://aeroptimal.com'
EMAIL_USER = 'aeroptimal@hotmail.com'

SECRET_KEY = config('SECRET_KEY', cast=str)
EMAIL_PASSWORD = config('EMAIL_PASSWORD', cast=str)
AWS_ID = config('AWS_ID', cast=str)
AWS_ACCESS_KEY = config('AWS_ACCESS_KEY', cast=str)
POSTGRES_HOST = config('POSTGRES_HOST', cast=str)
POSTGRES_DB = config('POSTGRES_DB', cast=str)
POSTGRES_USER = config('POSTGRES_USER', cast=str)
POSTGRES_PASSWORD = config('POSTGRES_PASSWORD', cast=str)

OPENFOAM_QUEUE = 'openfoam'
DATABASE_URI=f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}"
AWS_CLIENT = boto3.resource('sqs', region_name='us-east-1',
                    aws_access_key_id=AWS_ID, 
                    aws_secret_access_key=AWS_ACCESS_KEY)