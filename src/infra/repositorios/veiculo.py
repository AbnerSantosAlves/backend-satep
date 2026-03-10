from sqlalchemy.orm import Session
from src.infra.schema import schemas
from src.infra.models import models


class RepositorioVeiculo:

    def __init__(self, db: Session):
        self.db = db


    def criarVeiculo(self, veiculo: schemas.veiculo):
        veiculo = models.Veiculo(
            modelo_veiculo=veiculo.modelo_veiculo,
            nr_placa_veiculo=veiculo.nr_placa_veiculo,
            nr_capacidade_veiculo=veiculo.nr_capacidade_veiculo
        )

        self.db.add(veiculo)
        self.db.commit()
        self.db.refresh(veiculo)

        return veiculo

    def editarVeiculo(self, veiculo_id: int, alteracao: schemas.veiculo):
        veiculo = self.db.query(models.Veiculo).filter(models.Veiculo.id_veiculo == veiculo_id).first()

        veiculo.modelo_veiculo = alteracao.modelo_veiculo
        veiculo.nr_placa_veiculo = alteracao.nr_placa_veiculo
        veiculo.nr_capacidade_veiculo = alteracao.nr_capacidade_veiculo

        self.db.commit()
        self.db.refresh(veiculo)

        return {"message": "Registro editado"}

    def excluirVeiculo(self, veiculo_id: int):
        veiculo = self.db.query(models.Veiculo).filter(models.Veiculo.id_veiculo == veiculo_id).first()

        self.db.delete(veiculo)
        self.db.commit()

        return {"message": "Registro excluído"}

    def getVeiculos(self):
        return self.db.query(models.Veiculo).all()

    def getVeiculoById(self, veiculo_id: int):
        return self.db.query(models.Veiculo).filter(models.Veiculo.id_veiculo==veiculo_id).first()
    
