# backend/api/users.py
from fastapi import APIRouter, HTTPException
from models.user import UserCreate, LoginRequest, Token, UserInDB
from services.auth import get_user_by_email, create_user, verify_password, create_access_token

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/signup", response_model=UserInDB)
def signup(user: UserCreate):
    if get_user_by_email(user.email):
        raise HTTPException(status_code=400, detail="Email ja registrat")
    return create_user(user)

@router.post("/login", response_model=Token)
def login(login_req: LoginRequest):
    user = get_user_by_email(login_req.email)
    if not user or not verify_password(login_req.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Usuari o contrasenya incorrectes")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
