import jwt
import os, dotenv
from datetime import datetime, timedelta, timezone

dotenv.load_dotenv()

SECRET_KEY = os.getenv("SECREY_KEY") or ""
ALGORITHM = os.getenv("ALGORITHM") or ""
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES") or "")

def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt