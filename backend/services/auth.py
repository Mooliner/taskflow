from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from jose import JWTError, jwt
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from db.mongo import users_collection
from models.user import UserCreate, UserInDB

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_user_by_email(email: str) -> Optional[UserInDB]:
    user = users_collection.find_one({"email": email})
    if user:
        return UserInDB(
            id=str(user["_id"]),
            name=user["name"],
            email=user["email"],
            hashed_password=user["password"],  # no hi ha project_id aquí
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
    return UserInDB(
        id=str(result.inserted_id),
        name=user.name,
        email=user.email,
        hashed_password=hashed_password
    )


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserInDB:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(email)
    if user is None:
        raise credentials_exception
    return user
