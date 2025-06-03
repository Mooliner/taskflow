# backend/services/websocket_manager.py

from fastapi import WebSocket  # Importem WebSocket per gestionar connexions en temps real
from typing import List  # Tipus per indicar llistes

# Classe que gestiona múltiples connexions WebSocket actives
class ConnectionManager:
    def __init__(self):
        # Llista on guardem totes les connexions WebSocket actives
        self.active_connections: List[WebSocket] = []

    # Funció asíncrona per acceptar una nova connexió i afegir-la a la llista
    async def connect(self, websocket: WebSocket):
        await websocket.accept()  # Acceptem la connexió WebSocket (handshake)
        self.active_connections.append(websocket)  # Afegim la connexió a la llista

    # Funció per eliminar una connexió quan es desconnecta
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)  # Eliminem la connexió de la llista

    # Funció asíncrona per enviar un missatge de text a totes les connexions actives
    async def send_message(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)  # Enviem el missatge a cada connexió

# Instància global de la classe ConnectionManager per ser usada en tota l'aplicació
manager = ConnectionManager()
