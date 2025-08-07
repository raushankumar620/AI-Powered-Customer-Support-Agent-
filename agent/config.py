import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

# Vector database settings
VECTOR_DB_PATH = "agent/db"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# AI model settings
DEFAULT_MODEL = "gpt-3.5-turbo"
TEMPERATURE = 0.7