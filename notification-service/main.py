from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
import pika
import json
from threading import Thread

RABBITMQ_URL = "amqp://guest:guest@localhost:5672/"
QUEUE_NAME = "notifications"

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/notifications")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # Manté obert el WebSocket
    except WebSocketDisconnect:
        manager.disconnect(websocket)

def rabbitmq_consumer():
    params = pika.URLParameters(RABBITMQ_URL)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    def callback(ch, method, properties, body):
        message = body.decode()
        asyncio.run(send_to_all(message))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    async def send_to_all(message):
        await manager.send_message(message)

    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)
    channel.start_consuming()

@app.on_event("startup")
def startup_event():
    thread = Thread(target=rabbitmq_consumer, daemon=True)
    thread.start()
