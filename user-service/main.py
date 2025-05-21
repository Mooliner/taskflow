from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from typing import Optional
from pymongo import MongoClient

# Constants per JWT
SECRET_KEY = "YxQvGtmwzG_bvRwMTYOa8T3OxVvC4vQyqfEj5W5_KgU"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Connecta a MongoDB online
MONGO_URI = "mongodb+srv://taskflow:R3Co0hNU414lomzP@cluster0.an2dj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client.taskFlow
users_collection = db.users

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserInDB(BaseModel):
    id: str
    name: str
    email: EmailStr
    hashed_password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_user_by_email(email: str) -> Optional[UserInDB]:
    user = users_collection.find_one({"email": email})
    if user:
        return UserInDB(
            id=str(user["_id"]),
            name=user["name"],
            email=user["email"],
            hashed_password=user["password"]
        )
    return None

def create_user(user: UserCreate) -> UserInDB:
    hashed_password = get_password_hash(user.password)
    user_dict = {
        "name": user.name,
        "email": user.email,
        "password": hashed_password,
        "date_registered": datetime.utcnow()
    }
    result = users_collection.insert_one(user_dict)
    return UserInDB(id=str(result.inserted_id), name=user.name, email=user.email, hashed_password=hashed_password)

@app.post("/users/signup", response_model=UserInDB)
def signup(user: UserCreate):
    if get_user_by_email(user.email):
        raise HTTPException(status_code=400, detail="Email ja registrat")
    return create_user(user)

@app.post("/users/login", response_model=Token)
def login(login_req: LoginRequest):
    user = get_user_by_email(login_req.email)
    if not user or not verify_password(login_req.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Usuari o contrasenya incorrectes")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
