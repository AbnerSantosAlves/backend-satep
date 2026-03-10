from sqlalchemy.orm import Session, joinedload
from src.infra.schema import schemas
from src.infra.models import models

class RepositorioPaciente:
    
    def __init__(self, db: Session):
        self.db = db  

    def createPaciente(self, paciente: schemas.Paciente):
        db_paciente = models.Paciente(
            nome=paciente.nome,
            email=paciente.email,
            senha=paciente.senha,
            telefone=paciente.telefone,
            cpf=paciente.cpf,
            nr_endereco=paciente.nr_endereco,
            nm_endereco=paciente.nm_endereco,
            nm_bairro=paciente.nm_bairro,
            nm_municipio=paciente.nm_municipio

        )

        self.db.add(db_paciente)
        self.db.commit()
        self.db.refresh(db_paciente)

        return db_paciente

        
        sucess = f"{db_paciente.nome} com o ID {db_paciente.id}, foi cadastrado com sucesso."
        return sucess

    def getPacienteById(self, id_paciente: int):
        # Usa joinedload para carregar o relacionamento "usuario"
        return (
            self.db.query(models.Paciente).filter(models.Paciente.id == id_paciente).first()
        )


    def getPacientes(self):
        # Usa joinedload para carregar o relacionamento "usuario"
        return (
            self.db.query(models.Paciente).all()
        )

    def editarPaciente(self, paciente_id: int, paciente: schemas.PacienteUpdate):
        db_paciente = self.db.query(models.Paciente).filter(models.Paciente.id == paciente_id).first()
        if not db_paciente:
            return None  

        for campo, valor in paciente.dict(exclude_unset=True).items():
            setattr(db_paciente, campo, valor)

        self.db.commit()
        self.db.refresh(db_paciente)
        return db_paciente
    
    def obter_por_email(self, email: str):
        paciente = self.db.query(models.Paciente).filter(models.Paciente.email==email).first()
        return paciente
    

    def cancelarAgendamento(self, agendamento_id, paciente_id):
        agendamento = (
            self.db.query(models.Agendamento)
            .filter(
                models.Agendamento.id == agendamento_id,
                models.Agendamento.paciente_id == paciente_id
            )
            .first()
        )
        if not agendamento:
            return {"message": "Agendamento não encontrado."}

        agendamento.status_agendamento = "Cancelado"
        self.db.commit()
        self.db.refresh(agendamento)
        return {"message": "Agendamento cancelado com sucesso."}