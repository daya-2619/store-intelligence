import jwt
from datetime import datetime, timedelta, timezone
import os
from fastapi import HTTPException, status

SECRET_KEY = os.getenv("JWT_SECRET", "super-secret-challenge-key-2026")
ALGORITHM = "HS256"

# Lightweight mock users for challenge submission
MOCK_USERS = {
    "admin": {"password": "password123", "role": "Admin", "stores": ["*"]},
    "manager_1008": {"password": "password123", "role": "Store Manager", "stores": ["ST1008"]},
    "manager_1009": {"password": "password123", "role": "Store Manager", "stores": ["ST1009"]},
    "analyst": {"password": "password123", "role": "Analyst", "stores": ["ST1008", "ST1009"]}
}

def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=8)):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
def authenticate_user(username: str, password: str):
    user = MOCK_USERS.get(username)
    if not user:
        return None
    
    if user["password"] == password:
        return {"username": username, "role": user["role"], "stores": user["stores"]}
    return None
