# backend/api/notifications.py

from fastapi import APIRouter, Depends  # APIRouter per modularitzar rutes, Depends per dependències
from services.history import get_project_history  # Funció per obtenir l'historial de notificacions
from services.auth import get_current_user  # Funció per obtenir l'usuari autenticat

router = APIRouter()  # Creem un router per definir les rutes relacionades amb notificacions

# Ruta GET per obtenir les notificacions d'un projecte concret
@router.get("/projects/{project_id}/notifications")
def get_notifications(project_id: str, limit: int = 20, current_user=Depends(get_current_user)):
    # Obtenim les últimes 'limit' notificacions del projecte (per defecte 20)
    results = get_project_history(project_id, limit)
    # Convertim l'_id de MongoDB de ObjectId a string per poder enviar-ho en la resposta JSON
    for doc in results:
        doc["_id"] = str(doc["_id"])
    # Retornem la llista de notificacions al client
    return results
