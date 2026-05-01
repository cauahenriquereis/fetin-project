from fastapi import APIRouter

doctor_router = APIRouter(prefix="/doctor", tags = ["doctor"])

@doctor_router.get("/")
async def home():
    return{"mensagem": "Você acessou a rota padrão de médicos", "autenticado":False}