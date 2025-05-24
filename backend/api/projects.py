from fastapi import APIRouter, Depends, HTTPException
from typing import List
from bson import ObjectId

from models.project import ProjectCreate, ProjectInDB
from services.auth import get_current_user
from services.project import create_project, get_projects_for_user, add_member_to_project
from db.mongo import projects_collection

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("/", response_model=ProjectInDB)
def create_new_project(project: ProjectCreate, current_user=Depends(get_current_user)):
    if current_user.email != project.owner_email:
        raise HTTPException(status_code=403, detail="Only owner can create the project")
    return create_project(project)

@router.get("/", response_model=List[ProjectInDB])
def list_projects(current_user=Depends(get_current_user)):
    return get_projects_for_user(current_user.email)

@router.post("/{project_id}/members")
def add_member(project_id: str, user_email: str, current_user=Depends(get_current_user)):
    project = projects_collection.find_one({"_id": ObjectId(project_id)})
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project["owner_email"] != current_user.email:
        raise HTTPException(status_code=403, detail="Only owner can add members")

    success = add_member_to_project(project_id, user_email)
    if not success:
        raise HTTPException(status_code=400, detail="User already a member or operation failed")
    return {"message": f"User {user_email} added to project"}
