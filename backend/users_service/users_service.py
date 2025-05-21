from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from pymongo import MongoClient
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import os

app = FastAPI()

# Configura la URI de MongoDB Atlas amb base de dades taskflow
MONGODB_URI = os.environ.get("MONGODB_URI", "mongodb://taskflow:R3Co0hNU414lomzP@mongodb:27017/taskFlow?authSource=admin")

client = MongoClient(MONGODB_URI)
db = client["taskFlow"]
auth_collection = db["users"]

SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/auth/signup")
def signup(user: UserCreate):
    if auth_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Usuari ja registrat")

    user_dict = user.dict()
    user_dict["password"] = get_password_hash(user.password)
    user_dict["data_registre"] = datetime.utcnow()
    auth_collection.insert_one(user_dict)
    return {"msg": "Usuari creat correctament"}

@app.post("/auth/login", response_model=Token)
def login(user: UserLogin):
    db_user = auth_collection.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Credencials incorrectes")

    token_data = {"sub": str(db_user["_id"])}
    access_token = create_access_token(data=token_data, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}
