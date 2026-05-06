from fastapi import APIRouter, Depends, HTTPException
from models import Patient
from dependencies import pegar_sessao
from schemas import PatientInput, PatientOutput, PatientQueueInfo
from sqlalchemy.orm import Session
from datetime import datetime
from gemini_service import symptoms_analyze

patient_router = APIRouter(prefix="/patients", tags = ["patients"])

@patient_router.get("/")
async def home():
    return{"mensagem": "Você acessou a rota padrão de pacientes", "autenticado":False}

@patient_router.post("/register", response_model = PatientOutput)
async def register_patient(patient_input: PatientInput, session: Session = Depends(pegar_sessao)):

    analyze = symptoms_analyze(patient_input.symptoms, patient_input.pain_level, patient_input.age)
    urgency_level = analyze["urgency_level"]
    urgency_order = {"alta": 1, "média": 2, "baixa": 3}
    urgency_weight = urgency_order.get(urgency_level, 2)

    patients_same_urgency = session.query(Patient).filter(
    Patient.status == "aguardando",
    Patient.urgency_level == urgency_level
    ).count()

    priority_number = (urgency_weight * 100) + patients_same_urgency

    print(f"AI analyzed: {analyze['ai_analyzed']}")

    new_patient = Patient(
        full_name=patient_input.full_name,
        age=patient_input.age,
        symptoms=patient_input.symptoms,
        pain_level=patient_input.pain_level,
        urgency_level = urgency_level,
        priority_number = priority_number,
        status="aguardando",
        created_at=datetime.now()
    )

    session.add(new_patient)
    session.commit()
    session.refresh(new_patient) 
    return new_patient

@patient_router.get("/{patient_id}", response_model = PatientQueueInfo)
async def get_patient(patient_id: int, session: Session = Depends(pegar_sessao)):
    patient = session.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    
    patients_ahead_high = session.query(Patient).filter(
    Patient.status == "aguardando",
    Patient.urgency_level == "alta",
    Patient.priority_number < patient.priority_number
    ).count()

    patients_ahead_medium = session.query(Patient).filter(
    Patient.status == "aguardando",
    Patient.urgency_level == "média",
    Patient.priority_number < patient.priority_number
    ).count()
    patients_ahead_medium += patients_ahead_high

    patients_ahead_low = session.query(Patient).filter(
    Patient.status == "aguardando",
    Patient.urgency_level == "baixa",
    Patient.priority_number < patient.priority_number
    ).count()
    patients_ahead_low += patients_ahead_medium

    if(patient.priority_number < 199):
        waiting_time = patients_ahead_high * 15
    elif(200 <= patient.priority_number < 299):
        waiting_time = (patients_ahead_high * 15) + (patients_ahead_medium * 10)
    else:
        waiting_time = (patients_ahead_high * 15) + (patients_ahead_medium * 10) + (patients_ahead_low * 5)  

    if (patient.priority_number < 199):
        queue_position = patients_ahead_high
    elif (200 <= patient.priority_number < 299):
        queue_position = patients_ahead_medium
    else:
        queue_position = patients_ahead_low    

    return PatientQueueInfo(
        patient=patient,
        queue_position=queue_position,
        waiting_time_minutes=waiting_time
    )      