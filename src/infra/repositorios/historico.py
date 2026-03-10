# --- historico.py (CORRIGIDO) ---
from sqlalchemy.orm import Session
from src.infra.schema import schemas
from src.infra.models import models
from typing import Optional, List
from datetime import date

class RepositorioHistorico:

    def __init__(self, db: Session):
        self.db = db


    def setHistorico(self, historico):
        """
        Registra um novo histórico (log de ação).
        Pode receber tanto um objeto schemas.Logs quanto um dicionário.
        """
        # Permite receber tanto um objeto Pydantic quanto um dict
        if hasattr(historico, "dict"):  # caso seja um schema Pydantic
            historico_data = historico.dict()
        elif isinstance(historico, dict):
            historico_data = historico
        else:
            raise TypeError("O parâmetro 'historico' deve ser um objeto schemas.Logs ou dict.")

        # Cria o registro do log
        novo_registro = models.Logs(
            nm_usuario=historico_data.get("nm_usuario"),
            agendamento_id=historico_data.get("agendamento_id"),
            tipo_acao=historico_data.get("tipo_acao"),
        )

        # Campo opcional
        if "nm_paciente" in historico_data:
            novo_registro.nm_paciente = historico_data["nm_paciente"]

        # Salva no banco
        self.db.add(novo_registro)
        self.db.commit()
        self.db.refresh(novo_registro)

        return novo_registro


    def desfazerAcao(self, log_id, usuario_nome):
        log = self.db.query(models.Logs).filter(models.Logs.id==log_id).first()
        
        if not log:
            raise Exception("Log não encontrado.")

        agendamento = self.db.query(models.Agendamento).filter(models.Agendamento.id==log.agendamento_id).first()
        
        if not agendamento:
            raise Exception("Agendamento associado ao log não encontrado.")
            
        paciente = self.db.query(models.Paciente).filter(models.Paciente.id==agendamento.paciente_id).first()

        if log.tipo_acao == "Aprovado":
            agendamento.status_agendamento = "Em análise"
        
        if log.tipo_acao == "Reprovado":
            agendamento.status_agendamento = "Em análise"

        novo_registro = models.Logs(
            nm_usuario=usuario_nome,
            nm_paciente=paciente.nome,
            agendamento_id=agendamento.id,
            tipo_acao="Desfeita"
        )

        self.db.add(novo_registro)
        self.db.delete(log)
        
        self.db.commit()
        self.db.refresh(novo_registro)
        
        return novo_registro


    def getHistoricos(self, tipo: Optional[List[str]] = None, data: Optional[date] = None):
        query = (
            self.db.query(
                models.Logs,
                models.Agendamento,
                models.Paciente
            )
            .outerjoin(models.Agendamento, models.Agendamento.id == models.Logs.agendamento_id)
            .outerjoin(models.Paciente, models.Paciente.id == models.Agendamento.paciente_id)
            .distinct()
            .order_by(models.Logs.data.desc()) # Note: Aqui você ordena por 'data', assumindo que é a coluna correta.
        )

        if tipo:
            query = query.filter(models.Logs.tipo_acao.in_(tipo))

        if data:
            query = query.filter(models.Agendamento.data_agendamento == data)

        # print(str(query.statement.compile(compile_kwargs={"literal_binds": True}))) # Removido print de debug

        historico = query.all()

        resultado = []
        for hi, agendamento, paciente in historico:
            match hi.tipo_acao:
                case "Aprovado":
                    ds_acao = "aprovou um agendamento"
                case "Reprovado":
                    ds_acao = "reprovou um agendamento"
                case "Impressao":
                    ds_acao = "imprimiu uma ficha de viagem"
                case "Desfeita":
                    ds_acao = "desfez uma ação"
                case _:
                    ds_acao = hi.tipo_acao

            resultado.append({
                "id_historico": hi.id,
                "nm_usuario": hi.nm_usuario,
                "agendamento_id": hi.agendamento_id,
                "nm_paciente": paciente.nome if paciente else None,
                "tipo_acao": hi.tipo_acao,
                "ds_acao": ds_acao,
                # Corrigido para usar hi.data, que é o campo usado no order_by
                "dt_criacao": hi.data.isoformat() if hi.data else None
            })

        # CRÍTICO: Movemos o RETURN para fora do loop FOR!
        return resultado