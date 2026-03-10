# rotas_viagem.py
from fastapi import APIRouter, Depends, HTTPException
from src.infra.repositorios.motorista import RepositorioMotorista
from src.infra.schema.schemas import motorista, Usuario
from sqlalchemy.orm import Session, Query
from src.router.auth_utils_usuario import obter_usuario_logado
from src.infra.config.database import get_db
from typing import Optional, List
from datetime import datetime, date

router = APIRouter()


@router.post("/motorista")
def createMotorista(motorista: motorista, usuario: Usuario = Depends(obter_usuario_logado),db: Session = Depends(get_db)):
    veiculo = RepositorioMotorista(db).criarMotorista(motorista)
    return veiculo  

@router.post("/motorista/{id_motorista}/editar")
def editarMotorista(id_motorista: int, motorista: motorista, usuario: Usuario = Depends(obter_usuario_logado), db: Session = Depends(get_db)):
    motorista = RepositorioMotorista(db).editarMotorista(id_motorista, motorista)
    return motorista


@router.post("/motorista/{id_motorista}/excluir")
def excluirVeiculo(id_motorista: int, usuario: Usuario = Depends(obter_usuario_logado), db: Session = Depends(get_db)):
    return RepositorioMotorista(db).excluirMotorista(id_motorista)

@router.get("/motorista")
def listarMotorista(db: Session = Depends(get_db)):
    return RepositorioMotorista(db).getMotorista()

@router.get("/motorista/{id_motorista}")
def getMotoristaID(id_motorista: int, db: Session = Depends(get_db)):
    return RepositorioMotorista(db).getMotoristaById(id_motorista)

