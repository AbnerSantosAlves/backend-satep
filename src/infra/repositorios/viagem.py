from sqlalchemy.orm import Session, joinedload
from src.infra.schema import schemas
from src.infra.models import models
from typing import Optional, List
from datetime import date


class RepositorioViagem:

    def __init__(self, db: Session):
        self.db = db

    def criarViagem(self, viagem: schemas.viagem):
        viagem = models.Viagem(
            veiculo_id=viagem.veiculo_id,
            motorista_id=viagem.motorista_id,
        )

        self.db.add(viagem)
        self.db.commit()
        self.db.refresh(viagem)

        return viagem

    def editarViagem(self, viagem_id: int, alteracao: schemas.viagem):
        viagem = (
            self.db.query(models.Viagem)
            .filter(models.Viagem.id == viagem_id)
            .first()
        )

        if not viagem:
            return {"message": "Essa viagem não foi encontrada"}

        viagem.veiculo_id = alteracao.veiculo_id
        viagem.motorista_id = alteracao.motorista_id

        self.db.commit()
        self.db.refresh(viagem)

        return viagem

    def getViagens(self, status: Optional[List[str]] = None, data: Optional[date] = None):

        query = (
            self.db.query(models.Viagem)
            .outerjoin(models.Agendamento, models.Agendamento.viagem_id == models.Viagem.id)
            .outerjoin(models.Veiculo, models.Veiculo.id_veiculo == models.Viagem.veiculo_id)
            .outerjoin(models.Motorista, models.Motorista.id_motorista == models.Viagem.motorista_id)
            .options(
                joinedload(models.Viagem.agendamentos),
                joinedload(models.Viagem.veiculo),
                joinedload(models.Viagem.motorista)
            )
        )

        if status:
            query = query.filter(models.Agendamento.status_agendamento.in_(status))

        if data:
            query = query.filter(
                (models.Agendamento.data_agendamento == data) |
                (models.Agendamento.id.is_(None))
            )

        viagens = query.distinct(models.Viagem.id).all()
        resultado = []

        for vi in viagens:

            agendamentos_filtrados = [
                ag for ag in vi.agendamentos
                if (not data) or (ag.data_agendamento == data)
            ]

            ags = []
            for ag in agendamentos_filtrados:
                paciente_nome = ag.paciente.nome if ag.paciente else None

                ags.append({
                    "id": ag.id,
                    "data_agendamento": ag.data_agendamento.isoformat() if ag.data_agendamento else None,
                    "nm_paciente": paciente_nome,
                    "origem": ag.nm_endereco,
                    "destino": ag.nm_cidade,
                    "observacoes": ag.ds_agendamento,
                    "status": ag.status_agendamento
                })

            motorista = vi.motorista
            veiculo = vi.veiculo

            resultado.append({
                "id": vi.id,
                "nm_motorista": motorista.nm_motorista if motorista else None,
                "nr_fone": motorista.nr_fone_motorista if motorista else None,
                "veiculo": {
                    "id": veiculo.id_veiculo,
                    "modelo": veiculo.modelo_veiculo,
                    "placa": veiculo.nr_placa_veiculo,
                    "capacidade": veiculo.nr_capacidade_veiculo,
                } if veiculo else None,
                "agendamentos": ags
            })

        return resultado

    def getViagemById(self, viagem_id: int):
        viagem = (
            self.db.query(models.Viagem)
            .outerjoin(models.Agendamento, models.Agendamento.viagem_id == models.Viagem.id)
            .outerjoin(models.Veiculo, models.Veiculo.id_veiculo == models.Viagem.veiculo_id)
            .outerjoin(models.Motorista, models.Motorista.id_motorista == models.Viagem.motorista_id)
            .options(
                joinedload(models.Viagem.agendamentos),
                joinedload(models.Viagem.veiculo),
                joinedload(models.Viagem.motorista)
            )
            .filter(models.Viagem.id == viagem_id)
            .first()
        )

        if not viagem:
            return {"message": "Viagem não encontrada"}

        ags = []
        for ag in viagem.agendamentos:
            paciente_nome = ag.paciente.nome if ag.paciente else None

            ags.append({
                "id": ag.id,
                "data_agendamento": ag.data_agendamento.isoformat() if ag.data_agendamento else None,
                "nm_paciente": paciente_nome,
                "origem": ag.nm_endereco,
                "destino": ag.nm_cidade,
                "observacoes": ag.ds_agendamento,
                "status": ag.status_agendamento
            })

        motorista = viagem.motorista
        veiculo = viagem.veiculo

        return {
            "id": viagem.id,
            "nm_motorista": motorista.nm_motorista if motorista else None,
            "nr_fone": motorista.nr_fone_motorista if motorista else None,
            "veiculo": {
                "id": veiculo.id_veiculo,
                "modelo": veiculo.modelo_veiculo,
                "placa": veiculo.nr_placa_veiculo,
                "capacidade": veiculo.nr_capacidade_veiculo,
            } if veiculo else None,
            "agendamentos": ags
        }
