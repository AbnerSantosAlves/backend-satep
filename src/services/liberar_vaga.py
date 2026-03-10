from sqlalchemy.orm import Session
from src.infra import models


def liberar_vaga(db: Session, agendamento_id: int):
    agendamento = db.query(models.Agendamento).filter(
        models.Agendamento.id == agendamento_id
    ).first()

    if not agendamento:
        return {"message": "Agendamento não encontrado"}

    # Cancelar o agendamento
    agendamento.status = "Cancelado"
    viagem_id = agendamento.viagem_id
    db.commit()
    db.refresh(agendamento)

    if not viagem_id:
        return {"message": "Agendamento cancelado (não tinha viagem vinculada)"}

    # Buscar primeiro encaixe disponível para o mesmo dia
    encaixe = db.query(models.Agendamento).filter(
        models.Agendamento.data_agendamento == agendamento.data_agendamento,
        models.Agendamento.status == "Encaixe"
    ).first()

    if encaixe:
        encaixe.viagem_id = viagem_id
        encaixe.status = "Agendado"
        db.commit()
        db.refresh(encaixe)
        return {"message": f"Encaixe {encaixe.id} movido para viagem {viagem_id}"}

    return {"message": "Agendamento cancelado e nenhuma pessoa em encaixe foi encontrada"}
