# rotas_viagem.py
from fastapi import APIRouter, Depends, HTTPException
from src.infra.repositorios.viagem import RepositorioViagem
from src.infra.schema.schemas import viagem, Usuario
from sqlalchemy.orm import Session, Query
from src.router.auth_utils_usuario import obter_usuario_logado
from src.infra.config.database import get_db
from typing import Optional, List
from datetime import datetime, date

router = APIRouter()

@router.post("/viagem")
def createViagem(viagem: viagem, db: Session = Depends(get_db)):
    nova_viagem = RepositorioViagem(db).criarViagem(viagem)
    return nova_viagem

@router.post("/viagem/{id_viagem}/editar")
def editarViagem(viagem: viagem, id_viagem, usuario: Usuario = Depends(obter_usuario_logado), db: Session = Depends(get_db)):
    viagem = RepositorioViagem(db).editarViagem(id_viagem, viagem)
    return viagem   

@router.get("/viagens")
def listViagens(status: Optional[str] = None, data: Optional[date] = None, usuario: Usuario = Depends(obter_usuario_logado), db: Session = Depends(get_db)): 
    # 1. TRATAMENTO DO STATUS: Converte a string separada por vírgula em uma lista
    status_list: Optional[List[str]] = None
    if status:
        status_list = [s.strip() for s in status.split(',')] 

    # 2. NÃO FORÇAR data para hoje — se data = None, passamos None ao repositório
    data_consulta = data

    # 3. CHAMA O REPOSITÓRIO
    return RepositorioViagem(db).getViagens(status=status_list, data=data_consulta)
  

@router.get("/viagem/{id_viagem}")
def getViagemDetail(id_viagem: int, usuario: Usuario = Depends(obter_usuario_logado), db: Session = Depends(get_db)):
    vi = RepositorioViagem(db).getViagemById(id_viagem)
    if not vi:
        raise HTTPException(status_code=404, detail="Viagem não encontrada.")
    return vi
