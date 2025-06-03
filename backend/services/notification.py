# backend/services/notification.py

import pika, json  # pika per a RabbitMQ, json per serialitzar missatges
from datetime import datetime  # Per gestionar dates i hores
from config import RABBITMQ_URL, QUEUE_NAME  # Configuració de connexió i cua

# Funció que serialitza objectes datetime a string en format ISO per JSON
def json_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()  # Converteix datetime a string ISO 8601
    # Si és un tipus no serialitzable, llença error
    raise TypeError(f"Type {type(obj)} not serializable")

# Funció per publicar un missatge a la cua RabbitMQ
def publish_notification(message: dict):
    # Paràmetres de connexió a RabbitMQ a partir de l'URL configurat
    params = pika.URLParameters(RABBITMQ_URL)
    
    # Creem la connexió bloquejant (síncrona)
    connection = pika.BlockingConnection(params)
    
    # Obrim un canal a través del qual enviar els missatges
    channel = connection.channel()
    
    # Declarem la cua on enviarem el missatge, assegurant-nos que sigui durable (no es perd si RabbitMQ es reinicia)
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    
    # Enviem el missatge JSON a la cua
    channel.basic_publish(
        exchange='',                 # Exchange per defecte (direct)
        routing_key=QUEUE_NAME,      # La cua on s'enviarà el missatge
        body=json.dumps(message, default=json_serializer),  # Convertim el dict a string JSON, serialitzant dates
        properties=pika.BasicProperties(delivery_mode=2)    # Missatge persistent (no es perd si RabbitMQ es reinicia)
    )
    
    # Tanquem la connexió després d'enviar el missatge
    connection.close()
