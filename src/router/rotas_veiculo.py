# rotas_viagem.py
from fastapi import APIRouter, Depends, HTTPException
from src.infra.repositorios.veiculo import RepositorioVeiculo
from src.infra.schema.schemas import viagem, Usuario, veiculo
from sqlalchemy.orm import Session, Query
from src.router.auth_utils_usuario import obter_usuario_logado
from src.infra.config.database import get_db
from typing import Optional, List
from datetime import datetime, date

router = APIRouter()


@router.post("/veiculo")
def createVeiculo(veiculo: veiculo, usuario: Usuario = Depends(obter_usuario_logado),db: Session = Depends(get_db)):
    veiculo = RepositorioVeiculo(db).criarVeiculo(veiculo)
    return veiculo  

@router.post("/veiculo/{id_veiculo}/editar")
def editarVeiculo(id_veiculo: int, veiculo: veiculo, usuario: Usuario = Depends(obter_usuario_logado), db: Session = Depends(get_db)):
    veiculo = RepositorioVeiculo(db).editarVeiculo(id_veiculo, veiculo)
    return veiculo


@router.post("/veiculo/{id_veiculo}/excluir")
def excluirVeiculo(id_veiculo: int, usuario: Usuario = Depends(obter_usuario_logado), db: Session = Depends(get_db)):
    return RepositorioVeiculo(db).excluirVeiculo(id_veiculo)

@router.get("/veiculo")
def listarVeiculos(db: Session = Depends(get_db)):
    return RepositorioVeiculo(db).getVeiculos()

@router.get("/veiculo/{id_veiculo}")
def getVeiculoID(id_veiculo: int, db: Session = Depends(get_db)):
    return RepositorioVeiculo(db).getVeiculoById(id_veiculo)

