from fastapi import FastAPI
from doctor_routes import doctor_router
from patients_routes import patient_router
from queue_routes import queue_router

app = FastAPI()

app.include_router(doctor_router)
app.include_router(patient_router)
app.include_router(queue_router)

