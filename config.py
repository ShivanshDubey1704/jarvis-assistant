import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Bhindi API
    BHINDI_API_KEY = os.getenv('BHINDI_API_KEY', '')
    BHINDI_BASE_URL = os.getenv('BHINDI_BASE_URL', 'https://api.bhindi.io')
    
    # Assistant Settings
    ASSISTANT_NAME = os.getenv('ASSISTANT_NAME', 'JARVIS')
    VOICE_ENABLED = os.getenv('VOICE_ENABLED', 'true').lower() == 'true'
    VOICE_RATE = int(os.getenv('VOICE_RATE', '180'))
    VOICE_VOLUME = float(os.getenv('VOICE_VOLUME', '0.9'))
    
    # Memory Settings
    SESSION_MEMORY = os.getenv('SESSION_MEMORY', 'true').lower() == 'true'
    CONTEXT_WINDOW = int(os.getenv('CONTEXT_WINDOW', '10'))
    
    # UI Settings
    THEME = 'dark'
    PRIMARY_COLOR = '#00D9FF'
    SECONDARY_COLOR = '#FFD700'
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.BHINDI_API_KEY:
            raise ValueError("BHINDI_API_KEY is required. Please set it in .env file")
        return True