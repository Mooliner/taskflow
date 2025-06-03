# backend/api/tasks.py

from fastapi import APIRouter, HTTPException, Depends  # Imports per crear rutes, gestió d'errors i dependències
from bson import ObjectId  # Per convertir strings a ObjectId (MongoDB)
from datetime import datetime  # Per gestionar dates i hores
from services.auth import get_current_user  # Per obtenir l'usuari autenticat
from models.task import TaskCreate, TaskUpdate  # Models Pydantic per tasques
from models.project import ProjectInDB  # Model Pydantic per projecte
from db.mongo import tasks_collection, projects_collection  # Col·leccions MongoDB
from services.notification import publish_notification  # Funció per enviar notificacions
from models.comment import CommentCreate, CommentOut  # Models per comentaris
from typing import List  # Tipus llista

router = APIRouter(prefix="/tasks", tags=["Tasks"])  # Router per tasques

# Funció per comprovar si un usuari té accés a un projecte
def check_user_project_access(user_email: str, project_id: str):
    try:
        obj_id = ObjectId(project_id)  # Intentem convertir project_id a ObjectId
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid project_id format")

    project_data = projects_collection.find_one({"_id": obj_id})  # Busquem el projecte
    if not project_data:
        raise HTTPException(status_code=404, detail="Project not found")

    # Creem un objecte ProjectInDB per facilitar la gestió
    project = ProjectInDB(
        id=str(project_data["_id"]),
        name=project_data["name"],
        description=project_data.get("description"),
        owner_email=project_data["owner_email"],
        members=project_data.get("members", []),
    )

    # Comprovem que l'usuari és propietari o membre del projecte
    if user_email != project.owner_email and user_email not in project.members:
        raise HTTPException(status_code=403, detail="Access denied")

# Endpoint per crear una tasca nova
@router.post("/")
def create_task(task: TaskCreate, user=Depends(get_current_user)):
    if not task.project_id:
        raise HTTPException(status_code=400, detail="project_id is required")
    check_user_project_access(user.email, task.project_id)  # Comprovem accés al projecte

    task_dict = task.dict()  # Convertim a diccionari
    task_dict.update({
        "created_at": datetime.utcnow(),  # Afegim timestamps
        "updated_at": datetime.utcnow(),
    })

    result = tasks_collection.insert_one(task_dict)  # Inserim la tasca
    task_dict["_id"] = str(result.inserted_id)  # Convertim _id a string per la resposta

    # Publiquem notificació que s'ha creat una nova tasca
    publish_notification({"type": "new_task", "task": task_dict})
    return task_dict

# Endpoint per obtenir una tasca per ID
@router.get("/{task_id}")
def get_task(task_id: str, user=Depends(get_current_user)):
    task = tasks_collection.find_one({"_id": ObjectId(task_id)})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    check_user_project_access(user.email, task["project_id"])  # Comprovem accés
    task["_id"] = str(task["_id"])
    return task

# Endpoint per actualitzar una tasca parcialment
@router.patch("/{task_id}")
def update_task(task_id: str, task_update: TaskUpdate, user=Depends(get_current_user)):
    task = tasks_collection.find_one({"_id": ObjectId(task_id)})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    check_user_project_access(user.email, task["project_id"])

    # Només actualitzem els camps no None del model de dades
    update_data = {k: v for k, v in task_update.dict().items() if v is not None}
    update_data["updated_at"] = datetime.utcnow()

    result = tasks_collection.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": update_data}
    )

    updated_task = tasks_collection.find_one({"_id": ObjectId(task_id)})
    updated_task["_id"] = str(updated_task["_id"])

    # Publiquem notificació de l'actualització
    publish_notification({"type": "update_task", "task": updated_task})
    return updated_task

# Endpoint per llistar les tasques d'un projecte
@router.get("/")
def list_tasks(project_id: str, user=Depends(get_current_user)):
    check_user_project_access(user.email, project_id)  # Comprovem accés
    tasks_cursor = tasks_collection.find({"project_id": project_id})
    # Convertim _id de cada tasca a string
    return [{**task, "_id": str(task["_id"])} for task in tasks_cursor]

# Endpoint per afegir un comentari a una tasca
@router.post("/{task_id}/comments", response_model=List[CommentOut])
def add_comment(task_id: str, comment: CommentCreate, user=Depends(get_current_user)):
    task = tasks_collection.find_one({"_id": ObjectId(task_id)})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    check_user_project_access(user.email, task["project_id"])

    comment_data = {
        "author": user.email,
        "content": comment.content,
        "created_at": datetime.utcnow()
    }

    # Afegim el comentari a l'array comments de la tasca
    tasks_collection.update_one(
        {"_id": ObjectId(task_id)},
        {"$push": {"comments": comment_data}}
    )

    updated_task = tasks_collection.find_one({"_id": ObjectId(task_id)})
    return updated_task.get("comments", [])

# Endpoint per obtenir els comentaris d'una tasca
@router.get("/{task_id}/comments", response_model=List[CommentOut])
def get_comments(task_id: str, user=Depends(get_current_user)):
    task = tasks_collection.find_one({"_id": ObjectId(task_id)})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    check_user_project_access(user.email, task["project_id"])
    return task.get("comments", [])
