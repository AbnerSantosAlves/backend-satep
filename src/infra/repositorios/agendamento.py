# agendamento.py
from sqlalchemy.orm import Session, joinedload
from src.infra.schema import schemas
from src.infra.models import models
from datetime import datetime, date, timedelta
from src.services.atribuir_agendamento import atribuir_agendamento
from sqlalchemy import asc

class RepositorioAgendamento:

    def __init__(self, db: Session):
        self.db = db

    def createAgendamento(self, paciente_id: int, agendamento: schemas.AgendamentoCreate):
        novo_agendamento = models.Agendamento(
            paciente_id=paciente_id,
            hospital_id=agendamento.hospital_id,
            data_agendamento=agendamento.data_agendamento,
            hora_agendamento=agendamento.hora_agendamento,
            nm_endereco=agendamento.nm_endereco,
            nr_endereco=agendamento.nr_endereco,
            nm_bairro=agendamento.nm_bairro,
            nm_cidade=agendamento.nm_cidade,
            ds_agendamento=agendamento.ds_agendamento,
            procedimento=agendamento.procedimento,
        )
        self.db.add(novo_agendamento)
        self.db.commit()
        self.db.refresh(novo_agendamento)
        return novo_agendamento

    def getAgendamentosPaciente(self, paciente_id, status=None, data=None):
        query = (
            self.db.query(models.Agendamento)
            .options(joinedload(models.Agendamento.hospital),
                     joinedload(models.Agendamento.paciente))
            .filter(models.Agendamento.paciente_id == paciente_id)
        )

        if status:
            query = query.filter(models.Agendamento.status_agendamento == status)
        if data:
            query = query.filter(models.Agendamento.data_agendamento == data)

        agendamentos = query.order_by(models.Agendamento.data_agendamento.asc()).all()
        return agendamentos or []

    def getAgendamentoById(self, agendamento_id: int):
        """Retorna um payload detalhado para o frontend."""
        ag = (
            self.db.query(models.Agendamento)
            .options(joinedload(models.Agendamento.paciente), joinedload(models.Agendamento.hospital))
            .filter(models.Agendamento.id == agendamento_id)
            .first()
        )
        if not ag:
            return None

        # Normaliza o retorno como dicionário JSON-serializável
        paciente_nome = getattr(ag.paciente, "nome", None) if ag.paciente else None
        hospital_nome = getattr(ag.hospital, "nome", None) if ag.hospital else None

        return {
            "id": ag.id,
            "paciente": {
                "id": ag.paciente_id,
                "nome": paciente_nome
            } if ag.paciente_id else None,
            "nm_paciente": paciente_nome,
            "hospital": {
                "id": ag.hospital_id,
                "nome": hospital_nome
            } if ag.hospital_id else None,
            "status": ag.status_agendamento,
            "status_agendamento": ag.status_agendamento,
            "data_agendamento": ag.data_agendamento.isoformat() if ag.data_agendamento else None,
            "hora_agendamento": ag.hora_agendamento.isoformat() if getattr(ag, "hora_agendamento", None) else None,
            "origem": ag.nm_endereco or None,
            "destino": ag.nm_cidade or None,
            "nm_endereco": ag.nm_endereco,
            "nr_endereco": ag.nr_endereco,
            "nm_bairro": ag.nm_bairro,
            "nm_cidade": ag.nm_cidade,
            "ds_agendamento": ag.ds_agendamento,
            "observacoes": ag.ds_agendamento or "",
            "procedimento": ag.procedimento
        }

    def aprovarAgendamento(self, agendamento_id):
        agendamento = self.db.query(models.Agendamento).filter(models.Agendamento.id==agendamento_id).first()
        if not agendamento:
            return {"message": "Agendamento não encontrado."}
        resultado = atribuir_agendamento(self.db, agendamento_id)
        return {
            "message": "Agendamento aprovado",
            "status_final": resultado.get("status", None),
            "detalhes": resultado
        }

    def reprovarAgendamento(self, agendamento_id):
        agendamento = self.getAgendamentoById(agendamento_id)
        if not agendamento:
            return {"message": "Agendamento não encontrado."}
        # Caso precise alterar o modelo real:
        ag = self.db.query(models.Agendamento).filter(models.Agendamento.id==agendamento_id).first()
        ag.status_agendamento = "Recusado"
        self.db.commit()
        self.db.refresh(ag)
        return {"message": "Agendamento reprovado"}

    def getAgendamentosParaConfirmar(self, id_paciente: int):
        amanha = date.today() + timedelta(days=1)
        return (
            self.db.query(models.Agendamento)
            .filter(models.Agendamento.paciente_id == id_paciente, models.Agendamento.data_agendamento == amanha)
            .all()
        )

    def confirmacaoAgendamento(self, id_agendamento: int):
        agendamento = self.db.query(models.Agendamento).filter(models.Agendamento.id==id_agendamento).first()
        if not agendamento:
            return {"message": "Agendamento não encontrado."}
        agendamento.status_agendamento = "Confirmado"
        self.db.commit()
        self.db.refresh(agendamento)
        return {"message": "Confirmado"}

    def agendamentosPendenteCard(self):
        agendamentos = (
            self.db.query(models.Agendamento)
            .options(joinedload(models.Agendamento.hospital),
                     joinedload(models.Agendamento.paciente))
            .order_by(models.Agendamento.data_agendamento.asc())
            .filter(models.Agendamento.status_agendamento == "Em análise")
            .all()
        )
        return agendamentos or []

    def cancelarAgendamento(self, id_agendamento: int, paciente_id: int):
        ag = self.db.query(models.Agendamento).filter(models.Agendamento.id == id_agendamento,
                                                      models.Agendamento.paciente_id == paciente_id).first()
        if not ag:
            return {"message": "Agendamento não encontrado ou não pertence ao paciente."}
        ag.status_agendamento = "Cancelado"
        self.db.commit()
        self.db.refresh(ag)
        return {"message": "Agendamento cancelado"}
