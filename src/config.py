"""
Configuration Module - Centralized configuration management.

Load and manage environment variables and configuration settings
for the Gmail Reader application.
"""

import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)


class Config:
    """Application configuration class."""
    
    # Gmail Configuration
    GMAIL_USER = os.getenv('GMAIL_USER', '')
    GMAIL_API_CREDENTIALS = os.getenv('GMAIL_API_CREDENTIALS', 'credentials.json')
    
    # Translation Configuration
    TRANSLATION_API_KEY = os.getenv('TRANSLATION_API_KEY', '')
    TRANSLATION_SERVICE = os.getenv('TRANSLATION_SERVICE', 'google')
    
    # Speech Configuration
    SPEECH_LANGUAGE = os.getenv('SPEECH_LANGUAGE', 'en-US')
    SPEECH_ENGINE = os.getenv('SPEECH_ENGINE', 'pyttsx3')
    SPEECH_RATE = float(os.getenv('SPEECH_RATE', '0.9'))
    
    # Azure Configuration (optional)
    AZURE_SPEECH_KEY = os.getenv('AZURE_SPEECH_KEY', '')
    AZURE_SPEECH_REGION = os.getenv('AZURE_SPEECH_REGION', 'eastus')
    
    # Application Settings
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    MAX_EMAILS = int(os.getenv('MAX_EMAILS', '10'))
    CACHE_ENABLED = os.getenv('CACHE_ENABLED', 'True').lower() == 'true'
    CACHE_TTL = int(os.getenv('CACHE_TTL', '3600'))
    
    # File paths
    TOKEN_PATH = 'token.pickle'
    LOG_FILE = 'gmail_reader.log'
    
    @classmethod
    def validate(cls) -> bool:
        """
        Validate required configuration.
        
        Returns:
            bool: True if all required config is present
        """
        required_fields = [
            'GMAIL_USER',
            'GMAIL_API_CREDENTIALS',
            'TRANSLATION_API_KEY',
        ]
        
        missing = []
        for field in required_fields:
            if not getattr(cls, field, ''):
                missing.append(field)
        
        if missing:
            logger.warning(f"Missing configuration: {', '.join(missing)}")
            return False
        
        logger.info("Configuration validated successfully")
        return True
    
    @classmethod
    def to_dict(cls) -> dict:
        """
        Convert configuration to dictionary.
        
        Returns:
            Dictionary of all configuration values
        """
        return {
            key: getattr(cls, key) for key in dir(cls)
            if not key.startswith('_') and key.isupper()
        }
    
    @classmethod
    def log_config(cls, hide_sensitive: bool = True) -> None:
        """
        Log configuration values.
        
        Args:
            hide_sensitive: Whether to hide sensitive values like API keys
        """
        config_dict = cls.to_dict()
        
        for key, value in config_dict.items():
            if hide_sensitive and ('KEY' in key or 'SECRET' in key or 'PASSWORD' in key):
                value = '***HIDDEN***'
            
            logger.info(f"{key}: {value}")


# Configure logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Config.LOG_FILE),
        logging.StreamHandler()
    ]
)

logger.info("Configuration loaded successfully")
Config.log_config()