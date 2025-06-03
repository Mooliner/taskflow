# backend/api/projects.py

from fastapi import APIRouter, Depends, HTTPException  # Imports per crear rutes, depèndencies i errors HTTP
from typing import List  # Tipus per retornar llistes
from bson import ObjectId  # Per convertir strings a ObjectId (MongoDB)

from models.project import ProjectCreate, ProjectInDB  # Models Pydantic per projecte
from services.auth import get_current_user  # Per obtenir usuari autenticat
from services.project import create_project, get_projects_for_user, add_member_to_project  # Funcions de projecte
from db.mongo import projects_collection  # Accés directe a la col·lecció de projectes MongoDB

# Creem un router amb prefix /projects i etiquetem amb "Projects"
router = APIRouter(prefix="/projects", tags=["Projects"])

# Endpoint per crear un projecte nou
@router.post("/", response_model=ProjectInDB)
def create_new_project(project: ProjectCreate, current_user=Depends(get_current_user)):
    # Comprovem que l'usuari autenticat és realment l'owner que declara el projecte
    if current_user.email != project.owner_email:
        # Si no, retornem error 403 Forbidden
        raise HTTPException(status_code=403, detail="Only owner can create the project")
    # Creem i retornem el projecte
    return create_project(project)

# Endpoint per llistar els projectes on l'usuari és membre
@router.get("/", response_model=List[ProjectInDB])
def list_projects(current_user=Depends(get_current_user)):
    # Obtenim i retornem els projectes de l'usuari autenticat
    return get_projects_for_user(current_user.email)

# Endpoint per afegir un membre a un projecte
@router.post("/{project_id}/members")
def add_member(project_id: str, user_email: str, current_user=Depends(get_current_user)):
    # Busquem el projecte a la base de dades
    project = projects_collection.find_one({"_id": ObjectId(project_id)})
    if not project:
        # Si no existeix, retornem 404 Not Found
        raise HTTPException(status_code=404, detail="Project not found")
    # Comprovem que l'usuari autenticat és el propietari del projecte
    if project["owner_email"] != current_user.email:
        # Si no, retornem error 403 Forbidden
        raise HTTPException(status_code=403, detail="Only owner can add members")

    # Intentem afegir el membre al projecte
    success = add_member_to_project(project_id, user_email)
    if not success:
        # Si no s'ha pogut afegir (ja membre o fallada), retornem error 400 Bad Request
        raise HTTPException(status_code=400, detail="User already a member or operation failed")
    # Retornem missatge d'èxit
    return {"message": f"User {user_email} added to project"}
