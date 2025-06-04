from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import bcrypt
import logging
from config.config import MONGO_URI, DB_NAME, USERS_COLLECTION, MONGO_OPTIONS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

_mongo_client = None

def get_database():
    """
    Get MongoDB database connection with connection pooling.
    Returns a database instance.
    """
    global _mongo_client
    
    try:
        if _mongo_client is None:
            logger.info("Establishing new MongoDB connection...")
            _mongo_client = MongoClient(MONGO_URI, **MONGO_OPTIONS)
            # Verify connection
            _mongo_client.admin.command('ping')
            logger.info("Successfully connected to MongoDB")
        
        return _mongo_client[DB_NAME]
    
    except ConnectionFailure as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise
    except ServerSelectionTimeoutError as e:
        logger.error(f"Could not connect to MongoDB server: {e}")
        raise

def close_connection():
    """
    Close the MongoDB connection.
    Should be called when the application shuts down.
    """
    global _mongo_client
    if _mongo_client:
        _mongo_client.close()
        _mongo_client = None
        logger.info("MongoDB connection closed")

def register_user(email, password):
    """
    Register a new user with email and password.
    Returns (success: bool, message: str)
    """
    try:
        db = get_database()
        users = db[USERS_COLLECTION]
        
        # Check if user already exists
        if users.find_one({"email": email}):
            return False, "User already exists"
        
        # Hash the password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        
        # Insert new user
        user_doc = {
            "email": email,
            "password": hashed_password
        }
        users.insert_one(user_doc)
        logger.info(f"Successfully registered user: {email}")
        return True, "Registration successful"
    
    except Exception as e:
        logger.error(f"Error during user registration: {e}")
        return False, "Registration failed due to server error"

def verify_user(email, password):
    """
    Verify user credentials.
    Returns (success: bool, message: str)
    """
    try:
        db = get_database()
        users = db[USERS_COLLECTION]
        
        user = users.find_one({"email": email})
        if not user:
            return False, "User not found"
        
        if bcrypt.checkpw(password.encode('utf-8'), user['password']):
            logger.info(f"Successful login for user: {email}")
            return True, "Login successful"
        
        logger.warning(f"Failed login attempt for user: {email}")
        return False, "Invalid password"
    
    except Exception as e:
        logger.error(f"Error during user verification: {e}")
        return False, "Login failed due to server error" 