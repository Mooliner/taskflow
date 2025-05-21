from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId
import pika
import json

MONGO_URI = "mongodb+srv://taskflow:R3Co0hNU414lomzP@cluster0.an2dj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client.taskFlow
tasks_collection = db.tasks

RABBITMQ_URL = "amqp://guest:guest@localhost:5672/"
QUEUE_NAME = "notifications"

app = FastAPI()

# Pydantic model per la tasca
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "pending"

class TaskUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    status: Optional[str]

def json_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


# Funció per publicar missatges a RabbitMQ
def publish_notification(message: dict):
    params = pika.URLParameters(RABBITMQ_URL)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.basic_publish(
        exchange='',
        routing_key=QUEUE_NAME,
        body=json.dumps(message, default=json_serializer),
        properties=pika.BasicProperties(
            delivery_mode=2,
        )
    )
    connection.close()


@app.post("/tasks")
def create_task(task: TaskCreate):
    task_dict = task.dict()
    task_dict.update({
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    })
    result = tasks_collection.insert_one(task_dict)
    task_dict["_id"] = str(result.inserted_id)
    publish_notification({"type": "new_task", "task": task_dict})
    return task_dict

@app.get("/tasks/{task_id}")
def get_task(task_id: str):
    task = tasks_collection.find_one({"_id": ObjectId(task_id)})
    if not task:
        raise HTTPException(status_code=404, detail="Tasca no trobada")
    task["_id"] = str(task["_id"])
    return task

@app.patch("/tasks/{task_id}")
def update_task(task_id: str, task_update: TaskUpdate):
    update_data = {k: v for k, v in task_update.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No hi ha camps per actualitzar")
    update_data["updated_at"] = datetime.utcnow()
    result = tasks_collection.update_one({"_id": ObjectId(task_id)}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Tasca no trobada")
    updated_task = tasks_collection.find_one({"_id": ObjectId(task_id)})
    updated_task["_id"] = str(updated_task["_id"])
    publish_notification({"type": "update_task", "task": updated_task})
    return updated_task
