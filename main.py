from fastapi import FastAPI
from doctor_routes import doctor_router
from patients_routes import patient_router
from queue_routes import queue_router

# Main application instance
app = FastAPI(
    title="FETIN - Hospital Triage API",
    description="Automated hospital triage system powered by AI",
    version="1.0.0"
)

# Register routers
app.include_router(doctor_router)
app.include_router(patient_router)
app.include_router(queue_router)

