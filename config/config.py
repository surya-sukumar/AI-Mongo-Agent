import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Environment
ENV = os.getenv('ENV', 'development')

# MongoDB Configuration
if ENV == 'production':
    # Production MongoDB Atlas URI
    MONGO_URI = os.getenv('MONGO_ATLAS_URI')
    if not MONGO_URI:
        raise ValueError("Production MongoDB URI not found in environment variables")
else:
    # Development local MongoDB URI
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')

# Database Configuration
DB_NAME = os.getenv('DB_NAME', 'ai_mongo_agent')
USERS_COLLECTION = 'users'

# MongoDB Connection Options
MONGO_OPTIONS = {
    'connectTimeoutMS': 5000,
    'socketTimeoutMS': 30000,
    'serverSelectionTimeoutMS': 5000,
    'retryWrites': True,
    'w': 'majority'
} 