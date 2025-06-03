# backend/services/history.py

from db.mongo import db  # Importem la connexió a la base de dades MongoDB
from datetime import datetime  # Per treballar amb dates i hores

# Referència a la col·lecció de notificacions dins la base de dades
notifications_collection = db.notifications

# Funció per guardar una notificació a la base de dades
def save_notification(message: dict):
    # Si el missatge no té un timestamp, li assignem la data/hora actual en format ISO
    message["timestamp"] = message.get("timestamp", datetime.utcnow().isoformat())
    # Inserim el missatge (amb el timestamp) a la col·lecció de notificacions
    notifications_collection.insert_one(message)

# Funció per obtenir l'historial de notificacions d'un projecte concret
def get_project_history(project_id: str, limit=20):
    # Busquem totes les notificacions on el camp 'task.project_id' coincideixi amb project_id
    # Ordenem per timestamp de més recent a més antic (descendent)
    # Limitem el nombre de documents retornats al valor de 'limit' (per defecte 20)
    cursor = notifications_collection.find({"task.project_id": project_id}).sort("timestamp", -1).limit(limit)
    # Retornem la llista completa de notificacions trobades
    return list(cursor)
