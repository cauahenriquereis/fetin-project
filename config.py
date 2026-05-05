import os 
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
DOCTOR_PASSWORD = os.getenv("DOCTOR_PASSWORD")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
oauth2_schema = OAuth2PasswordBearer(tokenUrl="doctor/login-form")