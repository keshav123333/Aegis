from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from db.db import get_db
from fastapi import (Response , Cookie)
 
# cd backend
# pip install fastapi uvicorn passlib[bcrypt] python-jose[cryptography] python-multipart pydantic
# Data required to create a new user
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

# Data required to log in
class UserLogin(BaseModel):
    email: str
    password: str

# The shape of the JWT token we send back to the frontend
class Token(BaseModel):
    access_token: str
    token_type: str

# The shape of the user data we send back to the frontend
class UserResponse(BaseModel):
    id: int
    username: str
    email: str


SECRET_KEY="9447b2037106646fce9b050fd12f80b4b741d0adf00fbf1917543680e8e5da6b"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=100000


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(username:str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return {
            "id": user[0],
            "username": user[1],
            "email": user[2],
            "community_saver": user[3],
            "password": user[4]
        }
    return None

def authenticate_user(username: str, password: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    if not user:
        return False
    if not verify_password(password, user[4]):
        return False
    return {
        "id": user[0],
        "username": user[1],
        "email": user[2],
        "community_saver": user[3],
        "password": user[4]
    }

def create_access_token(data:dict,expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(access_token:str=Cookie(None)):
    if access_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user=get_user(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


