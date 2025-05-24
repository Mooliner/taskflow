from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import users, tasks, websocket, projects   # <-- afegit projects

app = FastAPI()

origins = ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(websocket.router)
app.include_router(projects.router)   # <-- afegit
