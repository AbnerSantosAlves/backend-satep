from sqlalchemy.orm import Session
from src.infra.models import models
from datetime import date  # Importar o tipo date para trabalhar com datas

# ----------------------------------------------------------------------------------
# É crucial que sua tabela Agendamento (models.Agendamento) tenha um campo:
# - data_agendamento: Mapped[date] (ou equivalente, tipo DATE no SQL)
# - viagem_modelo_id: Mapped[int] (ForeignKey para models.ViagemModelo)
# ----------------------------------------------------------------------------------

def atribuir_agendamento(db: Session, agendamento_id: int):
    """
    Atribui um Agendamento a um Modelo de Viagem (ocorrência) no mesmo dia, 
    respeitando a capacidade.
    """
    
    # 1. Busca o agendamento a ser atribuído
    agendamento = db.query(models.Agendamento).filter(
        models.Agendamento.id == agendamento_id
    ).first()

    if not agendamento:
        return {"message": "Agendamento não encontrado"}
    
    # PEÇA CHAVE: Captura a data do agendamento
    data_do_agendamento: date = agendamento.data_agendamento
    
    # 2. Busca todos os MODELOS de Viagem disponíveis
    # NOTA: O 'models.Viagem' do seu código anterior foi renomeado para 'models.ViagemModelo'
    viagens_modelos = db.query(models.Viagem).all()

    # 3. Itera sobre os Modelos de Viagem para encontrar onde encaixar o agendamento
    for modelo in viagens_modelos:
        
        # PEÇA CHAVE: Conta quantos agendamentos JÁ ESTÃO atribuídos a ESTE MODELO
        # E NESTA DATA ESPECÍFICA!
        total_agendamentos_no_dia = db.query(models.Agendamento).filter(
            models.Agendamento.viagem_id == modelo.id,
            models.Agendamento.data_agendamento == data_do_agendamento,  # FILTRO ESSENCIAL
            models.Agendamento.status_agendamento == "Agendado"
        ).count()

        # 4. Verifica a capacidade
        # NOTA: Assumindo que 'nr_capacidade' está no modelo de Viagem (ViagemModelo)
        if total_agendamentos_no_dia < modelo.nr_capacidade:
            
            # 5. Atribui e salva
            agendamento.viagem_id = modelo.id
            agendamento.status_agendamento = "Agendado"
            
            # Garantimos que a data já está definida em agendamento.data_agendamento 
            # (ela deveria ter sido definida na criação do agendamento)
            
            db.commit()
            db.refresh(agendamento)
            
            return {
                "message": f"Agendamento atribuído ao modelo {modelo.id} para a data {data_do_agendamento}",
                "status": "Agendado"
            }

    # 6. Se todas as viagens/ocorrências do dia estiverem lotadas
    # NOTA: Se você quiser que o status "Encaixe" se aplique apenas se 
    # não houver mais capacidade em *nenhum* modelo de viagem naquele dia.
    agendamento.viagem_modelo_id = None # Remove a atribuição, já que não encaixou
    agendamento.status_agendamento = "Encaixe"
    db.commit()
    db.refresh(agendamento)
    
    return {
        "message": f"Agendamento marcado como Encaixe (todas viagens lotadas para o dia {data_do_agendamento})",
        "status": "Encaixe"
    }