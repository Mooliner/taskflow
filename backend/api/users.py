# backend/api/users.py

from fastapi import APIRouter, HTTPException  # Imports per rutes i gestió d'errors
from models.user import UserCreate, LoginRequest, Token, UserInDB  # Models Pydantic
from services.auth import get_user_by_email, create_user, verify_password, create_access_token  # Funcions d'autenticació

router = APIRouter(prefix="/users", tags=["Users"])  # Router per la ruta /users

# Endpoint per registrar un nou usuari (signup)
@router.post("/signup", response_model=UserInDB)
def signup(user: UserCreate):
    # Comprovem si ja existeix un usuari amb aquest email
    if get_user_by_email(user.email):
        raise HTTPException(status_code=400, detail="Email ja registrat")
    # Creem i retornem l'usuari amb contrasenya hashejada
    return create_user(user)

# Endpoint per fer login i obtenir token JWT
@router.post("/login", response_model=Token)
def login(login_req: LoginRequest):
    # Busquem l'usuari per email
    user = get_user_by_email(login_req.email)
    # Verifiquem que l'usuari existeixi i la contrasenya sigui correcta
    if not user or not verify_password(login_req.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Usuari o contrasenya incorrectes")
    # Creem un token d'accés JWT amb l'email com a subjecte
    access_token = create_access_token(data={"sub": user.email})
    # Retornem el token i el tipus
    return {"access_token": access_token, "token_type": "bearer"}
