# backend/services/project.py

from db.mongo import projects_collection  # Col·lecció de projectes a la base de dades
from models.project import ProjectCreate  # Model Pydantic per la creació de projectes
from bson import ObjectId  # Per convertir strings a ObjectId de MongoDB

# Funció per crear un projecte nou a la base de dades
def create_project(project: ProjectCreate):
    project_dict = project.dict()  # Convertim l'objecte Pydantic a diccionari
    project_dict["members"] = [project.owner_email]  # Afegim l'owner com a primer membre del projecte
    result = projects_collection.insert_one(project_dict)  # Inserim el projecte a MongoDB
    project_in_db = project_dict
    # Afegim el camp "id" amb l'_id retornat per MongoDB convertit a string (per facilitar el seu ús)
    project_in_db["id"] = str(result.inserted_id)
    return project_in_db  # Retornem el projecte amb id inclòs

# Funció per obtenir tots els projectes en què un usuari és membre
def get_projects_for_user(user_email: str):
    # Cerquem projectes on el camp 'members' contingui el correu de l'usuari
    cursor = projects_collection.find({"members": user_email})
    projects = []
    for doc in cursor:
        # Convertim l'_id de Mongo a string i l'afegim amb la clau 'id'
        doc["id"] = str(doc["_id"])
        projects.append(doc)
    return projects  # Retornem la llista de projectes

# Funció per afegir un nou membre a un projecte existent
def add_member_to_project(project_id: str, user_email: str) -> bool:
    # Busquem el projecte pel seu _id convertit a ObjectId
    project = projects_collection.find_one({"_id": ObjectId(project_id)})
    if not project:
        return False  # Retornem False si el projecte no existeix
    if user_email in project.get("members", []):
        return False  # Retornem False si l'usuari ja és membre
    # Afegim el correu a la llista de membres del projecte (sense duplicats, per això el check anterior)
    result = projects_collection.update_one(
        {"_id": ObjectId(project_id)},
        {"$push": {"members": user_email}}
    )
    # Retornem True si la modificació ha afectat algun document (membre afegit)
    return result.modified_count > 0
