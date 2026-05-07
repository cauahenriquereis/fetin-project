from fastapi import APIRouter, Depends, HTTPException
from dependencies import verify_token
from dependencies import pegar_sessao
from sqlalchemy.orm import Session
from models import Patient
from schemas import PatientOutput, StatusUpdate
from typing import List

# All routes require a valid JWT token — doctor access only
queue_router = APIRouter(prefix="/queue", tags = ["queue"], dependencies=[Depends(verify_token)])

@queue_router.get("/")
async def home():
    return{"mensagem": "Você acessou a rota padrão de filas", "autenticado":True}

@queue_router.get("/status", response_model = List[PatientOutput])
async def get_ordered_queue(session :Session = Depends(pegar_sessao)):
     # Returns all waiting patients ordered by priority number (lowest = highest priority)
    patients = session.query(Patient).filter(Patient.status == "aguardando").order_by(Patient.priority_number).all()   
    return patients

@queue_router.get("/next/", response_model = PatientOutput)
async def get_next_patient(session :Session = Depends(pegar_sessao)):
    # Returns the next patient to be called based on priority number
    patient = session.query(Patient).filter(Patient.status == "aguardando").order_by(Patient.priority_number).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Não há pacientes aguardando atendimento")
    return patient

@queue_router.get("/status/{patient_id}", response_model = PatientOutput)
async def get_patient_status(patient_id: int, session :Session = Depends(pegar_sessao)):
    # Returns full details of a specific patient
    patient = session.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return patient

@queue_router.patch("/{patient_id}/status", response_model = PatientOutput)
async def update_patient_status(patient_id: int, dados: StatusUpdate, session :Session = Depends(pegar_sessao)):
    # Updates patient status — flow: aguardando → em atendimento → atendido
    patient = session.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    if dados.new_status not in ["aguardando", "em atendimento", "atendido"]:
        raise HTTPException(status_code=400, detail="Status inválido, aceito apenas 'aguardando', 'em atendimento' ou 'atendido'")
    patient.status = dados.new_status
    session.commit()
    session.refresh(patient)
    return patient

@queue_router.delete("/{patient_id}")
async def remove_patient_from_queue(patient_id: int, session :Session = Depends(pegar_sessao)):
    # Permanently removes a patient from the queue
    patient = session.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    session.delete(patient)
    session.commit()
    return {"mensagem": f"Paciente {patient.full_name} removido da fila"}