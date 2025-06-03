# backend/services/auth.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from jose import JWTError, jwt
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from db.mongo import users_collection
from models.user import UserCreate, UserInDB

# Configuració per a la gestió de contrasenyes amb bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuració d'OAuth2 per obtenir el token a través de l'endpoint 'token'
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Funció per verificar si una contrasenya en pla coincideix amb el hash emmagatzemat
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Funció per generar el hash d'una contrasenya nova
def get_password_hash(password):
    return pwd_context.hash(password)

# Funció per crear un token JWT amb un temps d'expiració
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    # Definim la data d'expiració: ara + el temps que es passi (o el valor per defecte)
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})  # Afegim el camp d'expiració al payload
    # Generem el token JWT codificat amb la clau secreta i l'algoritme especificat
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Funció per obtenir un usuari de la base de dades per correu electrònic
def get_user_by_email(email: str) -> Optional[UserInDB]:
    user = users_collection.find_one({"email": email})  # Busquem l'usuari
    if user:
        # Si existeix, retornem un objecte UserInDB construït amb les dades
        return UserInDB(
            id=str(user["_id"]),  # Convertim l'ObjectId a string
            name=user["name"],
            email=user["email"],
            hashed_password=user["password"],  # Password ja hashat
        )
    return None  # Si no existeix, retornem None

# Funció per crear un usuari nou a la base de dades
def create_user(user: UserCreate) -> UserInDB:
    hashed_password = get_password_hash(user.password)  # Hash de la contrasenya
    user_dict = {
        "name": user.name,
        "email": user.email,
        "password": hashed_password,  # Guardem el hash, no la contrasenya en pla
        "date_registered": datetime.utcnow()  # Data actual d'alta
    }
    result = users_collection.insert_one(user_dict)  # Inserim a MongoDB
    # Retornem l'objecte UserInDB amb l'id de Mongo convertit a string
    return UserInDB(
        id=str(result.inserted_id),
        name=user.name,
        email=user.email,
        hashed_password=hashed_password
    )

# Funció asíncrona per obtenir l'usuari actual segons el token d'autenticació
async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserInDB:
    # Excepció que llençarem si no es poden validar les credencials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decodifiquem el token JWT amb la clau secreta
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")  # El subject hauria de ser el correu de l'usuari
        if email is None:
            raise credentials_exception  # Si no hi ha correu, error
    except JWTError:
        raise credentials_exception  # Si el token és invàlid o caducat, error
    # Busquem l'usuari a la base de dades
    user = get_user_by_email(email)
    if user is None:
        raise credentials_exception  # Si no trobem l'usuari, error
    return user  # Retornem l'usuari actual
