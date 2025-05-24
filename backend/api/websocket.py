# backend/api/websocket.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from threading import Thread
import pika, asyncio, json
from jose import jwt, JWTError
from services.websocket_manager import manager
from config import SECRET_KEY, ALGORITHM, RABBITMQ_URL, QUEUE_NAME

router = APIRouter()

@router.websocket("/ws/notifications")
async def websocket_endpoint(websocket: WebSocket):
    token = websocket.query_params.get("token")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = payload.get("sub")
        if user_email is None:
            raise Exception("Invalid token")
    except JWTError:
        await websocket.close(code=1008)
        return
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

def rabbitmq_consumer(loop):
    params = pika.URLParameters(RABBITMQ_URL)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    def callback(ch, method, properties, body):
        message = body.decode()
        asyncio.run_coroutine_threadsafe(manager.send_message(message), loop)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)
    channel.start_consuming()

@router.on_event("startup")
async def startup_event():
    loop = asyncio.get_running_loop()
    Thread(target=rabbitmq_consumer, args=(loop,), daemon=True).start()
