# viagem.py
from sqlalchemy.orm import Session, joinedload
from src.infra.schema import schemas
from src.infra.models import models
from typing import Optional, List
from datetime import datetime, date
from src.services.checar_viagem import checar_viagens

class RepositorioViagem:

    def __init__(self, db: Session):
        self.db = db    

    def createViagem(self, viagem: schemas.viagem):
        viagem_obj = models.Viagem(
            nm_motorista = viagem.nm_motorista,
            nr_carteira = viagem.nr_carteira,
            nr_fone = viagem.nr_fone,
            nr_capacidade= viagem.nr_capacidade,
            status_viagem="Em andamento"
        )
        self.db.add(viagem_obj)
        self.db.commit()
        self.db.refresh(viagem_obj) 
        return viagem_obj

    def editarViagem(self, viagem_id: int, alteracao: schemas.viagem):
        viagem = self.db.query(models.Viagem).filter(models.Viagem.id == viagem_id).first()
        if not viagem:
            return None

        viagem.nm_motorista = alteracao.nm_motorista
        viagem.nr_carteira = alteracao.nr_carteira
        viagem.nr_fone = alteracao.nr_fone

        self.db.commit()
        self.db.refresh(viagem)

        return viagem
    
    def getViagens(self, status: Optional[List[str]] = None, data: Optional[date] = None):
        """
        Retorna lista de viagens com agendamentos embutidos.
        Se 'data' for None -> não filtra por data (retorna todas as viagens).
        Se 'status' for informado -> filtra pelo status_viagem.
        """
        query = (
            self.db.query(models.Viagem)
            .outerjoin(models.Agendamento, models.Agendamento.viagem_id == models.Viagem.id)
            .options(
                joinedload(models.Viagem.agendamentos).joinedload(models.Agendamento.paciente)
            )
        )

        if status:
            query = query.filter(models.Viagem.status_viagem.in_(status))

        # Se data for informada, aplicamos filtro; caso contrário, deixamos todas as viagens
        if data:
            query = query.filter(
                (models.Agendamento.data_agendamento == data) |
                (models.Agendamento.id == None)
            )

        viagens = query.distinct(models.Viagem.id).all()

        resultado = []
        for vi in viagens:
            # filtra agendamentos caso data tenha sido informada
            agendamentos_filtrados = [
                ag for ag in vi.agendamentos
                if (not data) or (ag.data_agendamento == data)
            ]

            ags = []
            for ag in agendamentos_filtrados:
                paciente_nome = getattr(ag.paciente, "nome", None) if ag.paciente else None
                ags.append({
                    "id": ag.id,
                    "data_agendamento": ag.data_agendamento.isoformat() if ag.data_agendamento else None,
                    "nm_paciente": paciente_nome,
                    "origem": ag.nm_endereco,
                    "destino": ag.nm_cidade,
                    "observacoes": ag.ds_agendamento,
                    "status": ag.status_agendamento
                })

            resultado.append({
                "id": vi.id,
                "nm_motorista": vi.nm_motorista,
                "nr_fone": vi.nr_fone,
                "nr_capacidade": vi.nr_capacidade,
                "veiculo": getattr(vi, "veiculo", None),
                "status": vi.status_viagem,
                "observacoes": getattr(vi, "observacoes", None) or getattr(vi, "ds_viagem", None) or "",
                "agendamentos": ags
            })

        return resultado

    def getViagemById(self, id_viagem):
        vi = (
            self.db.query(models.Viagem)
            .options(joinedload(models.Viagem.agendamentos).joinedload(models.Agendamento.paciente))
            .filter(models.Viagem.id == id_viagem)
            .first()
        )
        if not vi:
            return None

        ags = []
        for ag in vi.agendamentos:
            paciente_nome = getattr(ag.paciente, "nome", None) if ag.paciente else None
            ags.append({
                "id": ag.id,
                "data_agendamento": ag.data_agendamento.isoformat() if ag.data_agendamento else None,
                "nm_paciente": paciente_nome,
                "origem": ag.nm_endereco,
                "destino": ag.nm_cidade,
                "observacoes": ag.ds_agendamento,
                "status": ag.status_agendamento
            })

        return {
            "id": vi.id,
            "nm_motorista": vi.nm_motorista,
            "nr_carteira": vi.nr_carteira,
            "nr_fone": vi.nr_fone,
            "nr_capacidade": vi.nr_capacidade,
            "veiculo": getattr(vi, "veiculo", None),
            "status": vi.status_viagem,
            "observacoes": getattr(vi, "observacoes", None) or getattr(vi, "ds_viagem", None) or "",
            "agendamentos": ags
        }
