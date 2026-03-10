# services/notificacao.py

def enviar_notificacao(destinatario: str, mensagem: str):
    """
    Envia uma notificação para o paciente.
    - destinatario: pode ser telefone, e-mail ou identificador do paciente
    - mensagem: texto da notificação
    """
    # Por enquanto apenas simulação (log/print)
    print(f"[NOTIFICAÇÃO] Para: {destinatario} | Mensagem: {mensagem}")

    # Caso queira integrar no futuro:
    # - Email (smtplib, FastAPI-Mail)
    # - WhatsApp/SMS (Twilio, Zenvia, etc.)
    # - Push notifications (Firebase, OneSignal)
