# backend/services/notification.py
import pika, json
from datetime import datetime
from config import RABBITMQ_URL, QUEUE_NAME

def json_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def publish_notification(message: dict):
    params = pika.URLParameters(RABBITMQ_URL)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.basic_publish(
        exchange='',
        routing_key=QUEUE_NAME,
        body=json.dumps(message, default=json_serializer),
        properties=pika.BasicProperties(delivery_mode=2)
    )
    connection.close()
