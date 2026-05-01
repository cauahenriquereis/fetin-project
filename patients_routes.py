from fastapi import APIRouter, Depends
from models import Patient
from dependencies import pegar_sessao
from schemas import PatientInput, PatientOutput
from sqlalchemy.orm import Session
from datetime import datetime

patient_router = APIRouter(prefix="/patients", tags = ["patients"])

@patient_router.get("/")
async def home():
    return{"mensagem": "Você acessou a rota padrão de pacientes", "autenticado":False}

@patient_router.post("/register", response_model = PatientOutput)
async def register_patient(patient_input: PatientInput, session: Session = Depends(pegar_sessao)):
    new_patient = Patient(
        full_name=patient_input.full_name,
        age=patient_input.age,
        symptoms=patient_input.symptoms,
        pain_level=patient_input.pain_level,
        status="aguardando",
        created_at=datetime.now()
    )
    session.add(new_patient)
    session.commit()
    session.refresh(new_patient) 
    return new_patient