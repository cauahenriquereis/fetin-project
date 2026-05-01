from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PatientInput(BaseModel):
   full_name: str
   age: int
   symptoms: str
   pain_level: int

   class Config:
        from_attributes = True

class PatientOutput(BaseModel):
    id: int
    full_name: str
    age: int
    symptoms: str
    pain_level: int
    urgency_level: Optional[str] = None
    priority_number: Optional[int] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
   
