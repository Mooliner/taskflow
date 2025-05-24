from db.mongo import projects_collection
from models.project import ProjectCreate
from bson import ObjectId

def create_project(project: ProjectCreate):
    project_dict = project.dict()
    project_dict["members"] = [project.owner_email]  # Owner sempre membre
    result = projects_collection.insert_one(project_dict)
    project_in_db = project_dict
    project_in_db["id"] = str(result.inserted_id)
    return project_in_db

def get_projects_for_user(user_email: str):
    cursor = projects_collection.find({"members": user_email})
    projects = []
    for doc in cursor:
        doc["id"] = str(doc["_id"])
        projects.append(doc)
    return projects

def add_member_to_project(project_id: str, user_email: str) -> bool:
    project = projects_collection.find_one({"_id": ObjectId(project_id)})
    if not project:
        return False
    if user_email in project.get("members", []):
        return False
    result = projects_collection.update_one(
        {"_id": ObjectId(project_id)},
        {"$push": {"members": user_email}}
    )
    return result.modified_count > 0
