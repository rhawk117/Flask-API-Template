import os
from dotenv import load_dotenv

# put your configs here and load them here 
load_dotenv()

# base configuration
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallbacksecret')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///todos.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# e.g 
class Development(Config):
    DEBUG = True
