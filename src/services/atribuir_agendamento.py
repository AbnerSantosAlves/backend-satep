from sqlalchemy.orm import Session
from src.infra.models import models
from datetime import date  # Importar o tipo date para trabalhar com datas

# ----------------------------------------------------------------------------------
# É crucial que sua tabela Agendamento (models.Agendamento) tenha um campo:
# - data_agendamento: Mapped[date] (ou equivalente, tipo DATE no SQL)
# - viagem_modelo_id: Mapped[int] (ForeignKey para models.ViagemModelo)
# ----------------------------------------------------------------------------------

def atribuir_agendamento(db: Session, agendamento_id: int):
    agendamento = db.query(models.Agendamento).filter(models.Agendamento.id == agendamento_id).first()

    if not agendamento: 
        return {"message": "Agendamento não encontrado"}
    
    data_agendamento = agendamento.data_agendamento


    viagens = db.query(models.Viagem).all()

    # Contabiliza quantos agendamentos possui uma determinada viagem na data específica.
    for viagem in viagens:
        total_agendamentos_data = db.query(models.Agendamento).filter(
            models.Agendamento.viagem_id == viagem.id,
            models.Agendamento.data_agendamento == data_agendamento,  # FILTRO ESSENCIAL
            models.Agendamento.status_agendamento == "Agendado"
        ).count()

        veiculo = db.query(models.Veiculo).filter(models.Veiculo.id_veiculo == viagem.veiculo_id).first()
        if total_agendamentos_data < veiculo.nr_capacidade_veiculo:
            agendamento.viagem_id = viagem.id
            agendamento.status_agendamento = "Agendado"

            db.commit()
            db.refresh(agendamento)
            
            return {
                "message": f"Agendamento atribuído ao modelo {viagem.id} para a data {data_agendamento}",
                "status": "Agendado"
            }
    

    agendamento.viagem_id = None
    agendamento.status_agendamento = "Encaixe"
    db.commit()
    db.refresh(agendamento)

    return {
        "message": f"Agendamento marcado como Encaixe (todas viagens lotadas para o dia {data_agendamento})",
        "status": "Encaixe"
    }



