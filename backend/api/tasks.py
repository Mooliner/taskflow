from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from datetime import datetime
from services.auth import get_current_user
from models.task import TaskCreate, TaskUpdate
from models.project import ProjectInDB
from db.mongo import tasks_collection, projects_collection
from services.notification import publish_notification

router = APIRouter(prefix="/tasks", tags=["Tasks"])

def check_user_project_access(user_email: str, project_id: str):
    try:
        obj_id = ObjectId(project_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid project_id format")
    
    project_data = projects_collection.find_one({"_id": obj_id})
    if not project_data:
        raise HTTPException(status_code=404, detail="Project not found")

    project = ProjectInDB(
        id=str(project_data["_id"]),
        name=project_data["name"],
        description=project_data.get("description"),
        owner_email=project_data["owner_email"],
        members=project_data.get("members", []),
    )

    if user_email != project.owner_email and user_email not in project.members:
        raise HTTPException(status_code=403, detail="Access denied")

@router.post("/")
def create_task(task: TaskCreate, user=Depends(get_current_user)):
    if not task.project_id:
        raise HTTPException(status_code=400, detail="project_id is required")
    check_user_project_access(user.email, task.project_id)
    task_dict = task.dict()
    task_dict.update({
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    })
    result = tasks_collection.insert_one(task_dict)
    task_dict["_id"] = str(result.inserted_id)
    publish_notification({"type": "new_task", "task": task_dict})
    return task_dict

@router.get("/{task_id}")
def get_task(task_id: str, user=Depends(get_current_user)):
    task = tasks_collection.find_one({"_id": ObjectId(task_id)})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    check_user_project_access(user.email, task["project_id"])
    task["_id"] = str(task["_id"])
    return task

@router.patch("/{task_id}")
def update_task(task_id: str, task_update: TaskUpdate, user=Depends(get_current_user)):
    task = tasks_collection.find_one({"_id": ObjectId(task_id)})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    check_user_project_access(user.email, task["project_id"])
    update_data = {k: v for k, v in task_update.dict().items() if v is not None}
    update_data["updated_at"] = datetime.utcnow()
    result = tasks_collection.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": update_data}
    )
    updated_task = tasks_collection.find_one({"_id": ObjectId(task_id)})
    updated_task["_id"] = str(updated_task["_id"])
    publish_notification({"type": "update_task", "task": updated_task})
    return updated_task

@router.get("/")
def list_tasks(project_id: str, user=Depends(get_current_user)):
    check_user_project_access(user.email, project_id)
    tasks_cursor = tasks_collection.find({"project_id": project_id})
    return [{**task, "_id": str(task["_id"])} for task in tasks_cursor]
