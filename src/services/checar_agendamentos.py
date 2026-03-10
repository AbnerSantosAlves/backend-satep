from datetime import datetime, timedelta, time
from sqlalchemy.orm import Session
from src.infra import models
from src.services.liberar_vaga import liberar_vaga



def lembrar_confirmacao(db: Session):
    hoje = datetime.now().date()
    amanha = hoje + timedelta(days=1)

    agendamentos = db.query(models.Agendamento).filter(
        models.Agendamento.data_agendamento == amanha,
        models.Agendamento.status_agendamento == "Agendado"
    ).all()

    for ag in agendamentos:
        ag.status_agendamento = "Confirmação Pendente"
        db.add(ag)

        from services.notificacao import enviar_notificacao
        mensagem = f"Olá, {ag.paciente.nome}! Seu agendamento precisa ser confirmado até às 16:30 de hoje."
        enviar_notificacao(ag.paciente.telefone, mensagem)
        print(f"Notificação enviada e status atualizado para paciente {ag.paciente.nome} (Agendamento {ag.id}).")

    db.commit()


def checar_agendamentos(db: Session):
    hoje = datetime.now().date()
    amanha = hoje + timedelta(days=1)

    agendamentos = db.query(models.Agendamento).filter(
        models.Agendamento.data_agendamento == amanha,
        models.Agendamento.status_agendamento == "Confirmação Pendente"
    ).all()

    limite = datetime.combine(hoje, time(16, 30))
    agora = datetime.now()

    if agora > limite:
        for ag in agendamentos:
            # ainda não confirmou → liberar vaga
            from services.liberar_vaga import liberar_vaga
            liberar_vaga(db, ag.id)
            print(f"Agendamento {ag.id} liberado (não confirmou até 16:30).")

        db.commit()

