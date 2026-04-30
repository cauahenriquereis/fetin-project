from sqlalchemy import create_engine, Column,String,Integer,DateTime, Enum, Text, ForeignKey
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

# create the connection with the PostgreSQL database
db = create_engine(os.getenv("DATABASE_URL"))

#create the base of the database
Base = declarative_base()

#create the classes/tables of the database

class Patient(Base):
    __tablename__ = "patients"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    full_name = Column("full_name", String(100), nullable=False)
    age = Column("age", Integer, nullable=False)
    symptoms = Column("symptoms", Text, nullable=False)
    pain_level = Column("pain_level", Integer, nullable=False)   
    urgency_level = Column("urgency_level", Enum("baixa", "média", "alta", name="urgency_level_enum"))
    priority_number = Column("priority_number", Integer)
    status = Column("status", Enum("aguardando", "em atendimento", "atendido", name="patient_status_enum"), nullable=False)
    created_at = Column("created_at", DateTime, nullable=False)

    def __init__ (self, full_name, age, symptoms, pain_level, status, created_at):
        self.full_name = full_name
        self.age = age
        self.symptoms = symptoms
        self.pain_level = pain_level
        self.status = status
        self.created_at = created_at

class Queue(Base):
    __tablename__ = "queue"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    patient_id = Column("patient_id", Integer, ForeignKey("patients.id"), nullable=False)
    position = Column("position", Integer, nullable=False)
    status = Column("status", Enum("ativo", "removido", name="queue_status_enum"), nullable=False)
    created_at = Column("created_at", DateTime, nullable=False)

    def __init__ (self, patient_id, position, status, created_at):
        self.patient_id = patient_id
        self.position = position
        self.status = status
        self.created_at = created_at

#executa a criaçaõ dos metadados do seu banco (cria efetivamente o banco de dados)