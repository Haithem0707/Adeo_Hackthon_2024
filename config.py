# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
from decouple import config
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    basedir = os.path.abspath(os.path.dirname(__file__))

    # Set up the App SECRET_KEY
    SECRET_KEY = config('SECRET_KEY', default='S#perS3crEt_007')

    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # API Keys
    SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY')
    HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    FIRECRAWL_API_KEY = os.getenv('FIRECRAWL_API_KEY', None)  # Optional
    FIREBASE_PROJECT_ID = os.getenv('FIREBASE_PROJECT_ID', None)  # Optional

    @staticmethod
    def check_required_keys():
        missing_keys = []
        if not os.getenv('SERPAPI_API_KEY'):
            missing_keys.append('SERPAPI_API_KEY')
        if not os.getenv('HUGGINGFACE_API_KEY'):
            missing_keys.append('HUGGINGFACE_API_KEY')
        if not os.getenv('OPENAI_API_KEY'):
            missing_keys.append('OPENAI_API_KEY')
        if not os.getenv('FIREBASE_PROJECT_ID'):
            missing_keys.append('FIREBASE_PROJECT_ID')
        
        if missing_keys:
            raise ValueError(f"Missing required API keys: {', '.join(missing_keys)}")


class ProductionConfig(Config):
    DEBUG = False

    # Security
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600

    # PostgreSQL database
    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
        config('DB_ENGINE', default='postgresql'),
        config('DB_USERNAME', default='appseed'),
        config('DB_PASS', default='pass'),
        config('DB_HOST', default='localhost'),
        config('DB_PORT', default=5432),
        config('DB_NAME', default='appseed-flask')
    )


class DebugConfig(Config):
    DEBUG = True


# Load all possible configurations
config_dict = {
    'Production': ProductionConfig,
    'Debug': DebugConfig
}
