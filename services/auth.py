from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
import os

MEU_USUARIO = os.getenv("MEU_USUARIO") or "pokemon"  # Valor padrão para desenvolvimento
MINHA_SENHA = os.getenv("MINHA_SENHA") or "pokemon123"  # Valor padrão para desenvolvimento

security = HTTPBasic()

def autenticar_meu_usuario(credentials: HTTPBasicCredentials = Depends(security)):
    is_username_correct = secrets.compare_digest(credentials.username, MEU_USUARIO)
    is_password_correct = secrets.compare_digest(credentials.password, MINHA_SENHA)

    if not (is_username_correct and is_password_correct):
        raise HTTPException(
            status_code=401,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Basic"},
        )