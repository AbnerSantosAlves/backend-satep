from sqlalchemy.orm import Session
from src.infra.models import models
from datetime import datetime

def checar_viagens(db: Session):
    viagens = db.query(models.Viagem).all()
    agora = datetime.now().date()
    mensagens = []

    for vi in viagens:
        agendamentos = (
            db.query(models.Agendamento)
            .filter(
                models.Agendamento.viagem_id == vi.id,
                models.Agendamento.data_agendamento == vi.data_viagem
            )
            .count()
        )

        if vi.data_viagem < agora:
            vi.status_viagem = "Finalizado"
            mensagens.append(f"Viagem {vi.id}: Finalizada")

        elif agendamentos < vi.nr_capacidade:
            vi.status_viagem = "Em andamento"
            mensagens.append(f"Viagem {vi.id}: Em andamento")

        elif agendamentos == vi.nr_capacidade:
            vi.status_viagem = "Agendado"
            mensagens.append(f"Viagem {vi.id}: Agendada")

    db.commit()
    return mensagens
