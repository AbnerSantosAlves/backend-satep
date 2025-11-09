from fastapi import APIRouter, Depends, HTTPException, status
from src.infra.repositorios.pacientes import RepositorioPaciente
from src.infra.providers import hash_providers, token_providers
from src.infra.schema.schemas import Paciente, LoginData, Usuario
from sqlalchemy.orm import Session
from src.router.auth_utils_paciente import obter_paciente_logado
from src.router.auth_utils_usuario import obter_usuario_logado
from src.infra.config.database import get_db
from src.infra.schema import schemas
from src.infra.models import models

router = APIRouter()

# Criar paciente
@router.post("/pacientes", response_model=Paciente)
def create_paciente(paciente: Paciente, db: Session = Depends(get_db)):
    paciente.senha = hash_providers.gerar_hash(paciente.senha)
    novo_paciente = RepositorioPaciente(db).createPaciente(paciente)
    if not novo_paciente:
        raise HTTPException(status_code=400, detail="Erro ao criar paciente")
    return novo_paciente

# Buscar paciente por ID
@router.get("/pacientes/{id_paciente}", response_model=Paciente)
def get_paciente_by_id(id_paciente: int, usuario: Usuario = Depends(obter_usuario_logado), db: Session = Depends(get_db)):
    return RepositorioPaciente(db).getPacienteById(id_paciente)

# Listar todos os pacientes
@router.get("/pacientes", response_model=list[Paciente])
def get_pacientes(usuario: Usuario = Depends(obter_usuario_logado), db: Session = Depends(get_db)):
    return RepositorioPaciente(db).getPacientes()

# Editar paciente
@router.put("/paciente/editar")
def editar_paciente(
    paciente_dados: schemas.PacienteUpdate,
    db: Session = Depends(get_db),
    paciente: models.Paciente = Depends(obter_paciente_logado)
):
    repo = RepositorioPaciente(db)
    paciente_db = repo.editarPaciente(paciente.id, paciente_dados)
    if not paciente_db:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return paciente_db




@router.post("/paciente/token")
def login(login_data: LoginData, session: Session = Depends(get_db)): 
   email = login_data.email
   senha = login_data.senha

   usuario = RepositorioPaciente(session).obter_por_email(email)

   if not usuario:
       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email ou senha inválidos")
   
   senha_valida = hash_providers.verificar_hash(senha, usuario.senha)

   if not senha_valida:
       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email ou senha inválidos")
   

   token = token_providers.criar_access_token({'sub': usuario.email})
   return {'usuario': usuario, 'acess_token': token}


@router.get('/paciente/me')
def me(paciente: Paciente = Depends(obter_paciente_logado)):
    return paciente

