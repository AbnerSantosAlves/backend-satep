from fastapi import APIRouter, Depends, HTTPException
from src.infra.repositorios.historico import RepositorioHistorico
from src.infra.schema.schemas import Logs, Usuario
from sqlalchemy.orm import Session
from src.infra.config.database import get_db
from src.router.auth_utils_usuario import obter_usuario_logado
from typing import Optional, List
from datetime import date, datetime


router = APIRouter()

# CORREÇÃO: REMOVIDO 'self'
@router.post('/historico')
def setHistorico(log: Logs, usuario: Usuario = Depends(obter_usuario_logado), db: Session = Depends(get_db)):
    return RepositorioHistorico(db).setHistorico(log)


# CORREÇÃO: REMOVIDO 'self'
@router.get('/historicos')
def getHistoricos(status: Optional[str] = None, data: Optional[date] = None, usuario: Usuario = Depends(obter_usuario_logado), db: Session = Depends(get_db)):

    # 1. TRATAMENTO DO STATUS: Converte a string separada por vírgula em uma lista
    status_list: Optional[List[str]] = None
    if status:
        status_list = [s.strip() for s in status.split(',')] 

    # 2. TRATAMENTO DA DATA
    data_consulta = data 
    if data_consulta is None:
        data_consulta = None
        
    # 3. CHAMA O REPOSITÓRIO
    return RepositorioHistorico(db).getHistoricos(tipo=status_list, data=data_consulta)


# CORREÇÃO: REMOVIDO 'self'
@router.post('/historico/{id_historico}/desfazer')
def desfazerHistoricos(id_historico, usuario: Usuario = Depends(obter_usuario_logado), db: Session = Depends(get_db)):
    return RepositorioHistorico(db).desfazerAcao(id_historico, usuario.id)