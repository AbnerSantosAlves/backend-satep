from sqlalchemy.orm import Session
from src.infra.schema import schemas
from src.infra.models import models


class RepositorioMotorista:

    def __init__(self, db: Session):
        self.db = db

    def criarMotorista(self, motorista: schemas.motorista):
        motorista = models.Motorista(
            nm_motorista=motorista.nm_motorista,
            nr_fone_motorista=motorista.nr_fone_motorista
        )

        self.db.add(motorista)
        self.db.commit()
        self.db.refresh(motorista)

    def editarMotorista(self, motorista_id: int, alteracao: schemas.motorista):
        motorista = self.db.query(models.Motorista).filter(models.Motorista.id_motorista == motorista_id).first()

        motorista.nm_motorista = alteracao.nm_motorista
        motorista.nr_fone_motorista = alteracao.nr_fone_motorista

        self.db.add(motorista)
        self.db.commit()
        self.db.refresh(motorista)

    def excluirMotorista(self, motorista_id: int):
        motorista = self.db.query(models.Motorista).filter(models.Motorista.id_motorista == motorista_id).first()

        self.db.delete(motorista)
        self.db.commit()

    def getMotorista(self):
        return self.db.query(models.Motorista).all()

    def getMotoristaById(self, motorista_id: int):
        return self.db.query(models.Motorista).filter(models.Motorista.id_motorista==motorista_id).first()
    