# backend/api/websocket.py

from fastapi import APIRouter, WebSocket, WebSocketDisconnect  # Imports per websocket i gestió de desconexions
from threading import Thread  # Per executar consumidor RabbitMQ en un fil separat
import pika, asyncio, json  # pika per RabbitMQ, asyncio per crides async, json per serialització
from jose import jwt, JWTError  # Per verificar i decodificar JWT
from services.websocket_manager import manager  # Gestor de connexions WebSocket
from services.history import save_notification  # Funció per guardar notificacions a BD
from config import SECRET_KEY, ALGORITHM, RABBITMQ_URL, QUEUE_NAME  # Configuració general

router = APIRouter()

# Endpoint websocket per rebre notificacions en temps real
@router.websocket("/ws/notifications")
async def websocket_endpoint(websocket: WebSocket):
    token = websocket.query_params.get("token")  # Agafem el token JWT de la query
    try:
        # Decodifiquem el token per validar-lo i extreure l'usuari (email)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = payload.get("sub")
        if user_email is None:
            raise Exception("Invalid token")  # Token sense subjecte
    except JWTError:
        # Tancament websocket si el token no és vàlid
        await websocket.close(code=1008)
        return

    await manager.connect(websocket)  # Acceptem la connexió i l'afegim al manager

    try:
        # Bucle infinit per mantenir la connexió oberta; espera missatges (aquí no s’espera cap)
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        # Si el client es desconnecta, el retirem del manager
        manager.disconnect(websocket)

# Consumidor RabbitMQ que rep missatges i els envia als websockets
def rabbitmq_consumer(loop):
    params = pika.URLParameters(RABBITMQ_URL)
    connection = pika.BlockingConnection(params)  # Connexió a RabbitMQ
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)  # Declarem la cua (durable)

    # Callback que s'executa quan arriba un missatge a RabbitMQ
    def callback(ch, method, properties, body):
        message = body.decode()  # Decodifiquem el missatge rebut (bytes -> str)
        parsed = json.loads(message)  # Parsejem JSON
        save_notification(parsed)  # Guardem notificació a base de dades

        # Enviem el missatge a tots els websockets de manera asincrona
        asyncio.run_coroutine_threadsafe(manager.send_message(message), loop)

        ch.basic_ack(delivery_tag=method.delivery_tag)  # Confirmem recepció del missatge

    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)
    channel.start_consuming()  # Iniciem el consum de missatges (bloquejant)

# Esdeveniment de startup que llença el consumidor RabbitMQ en un fil separat
@router.on_event("startup")
async def startup_event():
    loop = asyncio.get_running_loop()  # Agafem el loop asyncio corrent
    # Creem un fil daemon per executar el consumidor i no bloquejar l'app principal
    Thread(target=rabbitmq_consumer, args=(loop,), daemon=True).start()
