from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, timedelta
from jose import jwt, JWTError
from pymongo import MongoClient
from bson import ObjectId
import os

# --- Configuració MongoDB ---
MONGODB_URI = os.environ.get("MONGODB_URI", "mongodb://localhost:27017")
client = MongoClient(MONGODB_URI)
db = client["taskFlow"]
tasks_collection = db["tasks"]

# --- Configuració JWT ---
SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# --- Models ---
class Task(BaseModel):
    id: Optional[str]
    title: str
    description: Optional[str] = None
    assigned_to: Optional[str] = None
    status: str = "pendent"  # pendent, en procés, completat
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    assigned_to: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    assigned_to: Optional[str]
    status: Optional[str]

# --- Funcions auxiliars ---

def verify_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No s'ha pogut validar l'usuari",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return user_id

def task_helper(task) -> dict:
    return {
        "id": str(task["_id"]),
        "title": task["title"],
        "description": task.get("description"),
        "assigned_to": task.get("assigned_to"),
        "status": task.get("status", "pendent"),
        "created_at": task.get("created_at"),
        "updated_at": task.get("updated_at"),
    }

# --- FastAPI app ---
app = FastAPI()

@app.post("/tasks/", response_model=Task)
def create_task(task: TaskCreate, user_id: str = Depends(verify_token)):
    task_dict = task.dict()
    task_dict["status"] = "pendent"
    task_dict["created_at"] = datetime.utcnow()
    task_dict["updated_at"] = datetime.utcnow()
    inserted = tasks_collection.insert_one(task_dict)
    new_task = tasks_collection.find_one({"_id": inserted.inserted_id})
    return task_helper(new_task)

@app.get("/tasks/", response_model=List[Task])
def get_tasks(user_id: str = Depends(verify_token)):
    # Retornem totes les tasques (podes afegir filtre per usuari si vols)
    tasks = tasks_collection.find()
    return [task_helper(task) for task in tasks]

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: str, user_id: str = Depends(verify_token)):
    task = tasks_collection.find_one({"_id": ObjectId(task_id)})
    if not task:
        raise HTTPException(status_code=404, detail="Tasca no trobada")
    return task_helper(task)

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: str, task_update: TaskUpdate, user_id: str = Depends(verify_token)):
    existing_task = tasks_collection.find_one({"_id": ObjectId(task_id)})
    if not existing_task:
        raise HTTPException(status_code=404, detail="Tasca no trobada")

    updated_data = {k: v for k, v in task_update.dict().items() if v is not None}
    if updated_data:
        updated_data["updated_at"] = datetime.utcnow()
        tasks_collection.update_one({"_id": ObjectId(task_id)}, {"$set": updated_data})

    task = tasks_collection.find_one({"_id": ObjectId(task_id)})
    return task_helper(task)

@app.delete("/tasks/{task_id}")
def delete_task(task_id: str, user_id: str = Depends(verify_token)):
    result = tasks_collection.delete_one({"_id": ObjectId(task_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Tasca no trobada")
    return {"msg": "Tasca eliminada correctament"}
