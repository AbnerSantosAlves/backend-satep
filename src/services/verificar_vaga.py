from sqlalchemy.orm import Session
from src.infra.models import models

def verificar_vaga(db: Session, agendamento_id: int):
    agendamento = db.query(models.Agendamento).filter(
        models.Agendamento.id == agendamento_id
    ).first()

    if not agendamento:
        return {"message": "Agendamento não encontrado"}

    data_agendamento = agendamento.data_agendamento

    viagens = db.query(models.Viagem).all()

    for viagem in viagens:

        total_agendamentos_data = db.query(models.Agendamento).filter(
            models.Agendamento.viagem_id == viagem.id,
            models.Agendamento.data_agendamento == data_agendamento,
            models.Agendamento.status_agendamento == "Agendado"
        ).count()

        veiculo = db.query(models.Veiculo).filter(
            models.Veiculo.id_veiculo == viagem.veiculo_id
        ).first()

        capacidade_veiculo = int(veiculo.nr_capacidade_veiculo)

        if total_agendamentos_data < capacidade_veiculo:
            return {
                "message": "Vaga disponível",
                "viagem_id": viagem.id,
                "ocupados": total_agendamentos_data,
                "capacidade": capacidade_veiculo
            }

    return {"message": "Nenhuma vaga disponível, agendamento será movido para o encaixe."}
