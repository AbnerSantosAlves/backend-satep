# rotas_agendamento.py
from fastapi import APIRouter, Depends, HTTPException
from src.infra.repositorios.agendamento import RepositorioAgendamento
from src.infra.repositorios.historico import RepositorioHistorico
from src.infra.schema.schemas import Agendamento, Paciente, Usuario
from sqlalchemy.orm import Session
from src.infra.config.database import get_db
from src.router.auth_utils_usuario import obter_usuario_logado
from src.router.auth_utils_paciente import obter_paciente_logado
from datetime import date, datetime
from src.infra.schema.schemas import AgendamentoCreate
from src.services.verificar_vaga import verificar_vaga

from src.infra.schema import schemas

router = APIRouter()

@router.post("/agendamento/novo", response_model=Agendamento, status_code=201)
def createAgendamento(
    agendamento_data: AgendamentoCreate,
    paciente: Paciente = Depends(obter_paciente_logado),
    db: Session = Depends(get_db)
):
    novo_agendamento = RepositorioAgendamento(db).createAgendamento(
        paciente_id=paciente.id, 
        agendamento=agendamento_data
    )

    if not novo_agendamento:
        raise HTTPException(status_code=400, detail="Erro ao criar agendamento.")
        
    return novo_agendamento

@router.get("/agendamento/{id_agendamento}")
def getAgendamento(id_agendamento: int, usuario: Usuario = Depends(obter_usuario_logado), db: Session = Depends(get_db)):
    ag = RepositorioAgendamento(db).getAgendamentoById(id_agendamento)
    if not ag:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado.")
    return ag

@router.get("/agendamentos/paciente")
def getAgendamentos(
    paciente: Paciente = Depends(obter_paciente_logado),
    db: Session = Depends(get_db),
    status: str | None = None,
    data: str | None = None
):
    return RepositorioAgendamento(db).getAgendamentosPaciente(
        paciente.id,
        status=status,
        data=data
    )

@router.post("/agendamento/{id_agendamento}/aprovar")
def aprovarAgendamento(id_agendamento: int, usuario: Usuario = Depends(obter_usuario_logado), db: Session = Depends(get_db)):

    agora = datetime.now().date()
    RepositorioHistorico(db).setHistorico(
    schemas.Logs(
        nm_usuario=usuario.nome,
        agendamento_id=id_agendamento,
        tipo_acao="Aprovado",
        data=f"{agora}"
        )
    )
    return RepositorioAgendamento(db).aprovarAgendamento(id_agendamento)

@router.post("/agendamento/{id_agendamento}/reprovar")
def reprovarAgendamento(id_agendamento: int, usuario: Usuario = Depends(obter_usuario_logado), db: Session = Depends(get_db)):
    agora = datetime.now().date()
    RepositorioHistorico(db).setHistorico(
    schemas.Logs(
        nm_usuario=usuario.nome,
        agendamento_id=id_agendamento,
        tipo_acao="Reprovado",
        data=f"{agora}"
        )
    )
    return RepositorioAgendamento(db).reprovarAgendamento(id_agendamento)

@router.post("/agendamento/{id_agendamento}/confirmar")
def confirmarAgendamento(id_agendamento: int, usuario: Usuario = Depends(obter_usuario_logado), db: Session = Depends(get_db)):
    return RepositorioAgendamento(db).confirmacaoAgendamento(id_agendamento)

@router.get("/agendamentos/pendentes")
def agendamentosPendentes(usuario: Usuario = Depends(obter_usuario_logado), db: Session = Depends(get_db)):
    return RepositorioAgendamento(db).agendamentosPendenteCard()

@router.delete("/agendamento/{id_agendamento}/cancelar")
def cancelarAgendamento(
    id_agendamento: int,
    paciente: Paciente = Depends(obter_paciente_logado),
    db: Session = Depends(get_db)
):
    return RepositorioAgendamento(db).cancelarAgendamento(id_agendamento, paciente.id)


@router.post("/agendamento/disponibilidade/{idd_agendamento}"):
def verificarDisponibilidade(id_agendamento: int, usuario: Usuario = Depends(obter_usuario_logado), db: Session = Depends(get_db)):
    return verificar_vaga(db, id_agendamento)
