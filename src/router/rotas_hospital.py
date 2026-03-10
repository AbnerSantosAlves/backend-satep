from fastapi import APIRouter, Depends, HTTPException
from src.infra.repositorios.hospital import RepositorioHospital
from src.infra.schema.schemas import hospital, Usuario, Paciente
from sqlalchemy.orm import Session
from src.infra.config.database import get_db
from src.router.auth_utils_usuario import obter_usuario_logado
from src.router.auth_utils_paciente import obter_paciente_logado

router = APIRouter()

# Criar hospital
@router.api_route("/criarhospitais")
def criar_hospitais(db: Session = Depends(get_db)):
    return RepositorioHospital(db).criar_hospitais()


# Criar hospital
@router.post("/hospitais", response_model=hospital)
def create_hospital(hospital: hospital, db: Session = Depends(get_db)):
    # Com a correção em hospital.py, createHospital agora retorna o objeto criado ou None/exceção, 
    # mantendo a lógica de checagem.
    novo_hospital = RepositorioHospital(db).createHospital(hospital)
    if not novo_hospital:
        raise HTTPException(status_code=400, detail="Erro ao criar hospital")
    return novo_hospital

# Buscar hospital por ID
@router.get("/hospitais/{id_hospital}", response_model=hospital)
def get_hospital(id_hospital: int, usuario: Usuario = Depends(obter_usuario_logado), db: Session = Depends(get_db)):
    # CORREÇÃO: Com RepositorioHospital.getHospitalById retornando a instância ou None, 
    # a checagem é fundamental.
    hospital = RepositorioHospital(db).getHospitalById(id_hospital)
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital não encontrado")
    return hospital

# Deletar hospital
@router.delete("/hospitais/{id_hospital}")
def delete_hospital(id_hospital: int, usuario: Usuario = Depends(obter_usuario_logado), db: Session = Depends(get_db)):
    # CORREÇÃO: O repositório agora retorna True ou False.
    removido = RepositorioHospital(db).removerHospital(id_hospital)
    
    if not removido:
        # Se retornar False, o hospital não foi encontrado
        raise HTTPException(status_code=404, detail="Hospital não encontrado ou erro ao remover")
        
    return {"mensagem": f"Hospital com ID {id_hospital} removido com sucesso"}

# Listar todos os hospitais
@router.get("/hospitais")
def list_hospitais(paciente: Paciente = Depends(obter_paciente_logado), db: Session = Depends(get_db)):
    return RepositorioHospital(db).getHospitais()
