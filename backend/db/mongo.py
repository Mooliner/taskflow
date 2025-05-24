# backend/db/mongo.py
from pymongo import MongoClient
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client.taskFlow
users_collection = db.users
tasks_collection = db.tasks
projects_collection = db.projects
