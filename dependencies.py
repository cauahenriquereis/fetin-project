from sqlalchemy.orm import sessionmaker
from models import db
from jose import jwt, JWTError
from config import DOCTOR_PASSWORD, ALGORITHM, oauth2_schema
from fastapi import HTTPException, Depends

# Create session factory once at startup
SessionLocal = sessionmaker(bind=db)

def pegar_sessao():
    # Yields a database session and ensures it is closed after use
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def verify_token(token: str = Depends(oauth2_schema)):
    # Decodes and validates the JWT token
    # Raises 401 if the token is invalid or expired
    try:
        info_dictionary = jwt.decode(token, DOCTOR_PASSWORD, algorithms=[ALGORITHM])
        return info_dictionary
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido, verifique a validade do token")