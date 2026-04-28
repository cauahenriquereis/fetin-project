from fastapi import FastAPI
app = FastAPI()

from auth_routes import auth_router
from triage_routes import triage_router
from queue_routes import queue_router

app.include_router(auth_router)
app.include_router(triage_router)
app.include_router(queue_router)

