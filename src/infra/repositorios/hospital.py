from sqlalchemy.orm import Session
from src.infra.schema import schemas
from src.infra.models import models


class RepositorioHospital:

    def __init__(self, db: Session):
        self.db = db


    
    def criar_hospitais(self):
        hospital1 = models.Hospital(
            nome = "Hospital das clínicas",
            municipio = "São paulo"
        )

        hospital2 = models.Hospital(
            nome = "Hospital São paulo",
            municipio = "São paulo"
        )

        hospital3 = models.Hospital(
            nome = "Hospital Menino Jesus",
            municipio = "São paulo"
        )


        self.db.add(hospital1)
        self.db.add(hospital2)
        self.db.add(hospital3)
        self.db.commit()
        self.db.refresh(hospital1)
        self.db.refresg(hospital2)
        self.db.refresh(hospital3)
        


    # CORREÇÃO: Mapeamento de 'nome' do Schema (hospital.nome) para o Model (nome = ...)
    def createHospital(self, hospital: schemas.hospital):
        # O schema Pydantic 'hospital' usa o campo 'nome', não 'nm_hospital'.
        novo_hospital = models.Hospital(
            nome = hospital.nome, # Corrigido: usando hospital.nome
            municipio = hospital.municipio
        )

        self.db.add(novo_hospital)
        self.db.commit()
        self.db.refresh(novo_hospital) # Garante que o objeto retornado tenha o ID
        
        return novo_hospital

    def getHospitais(self):
        hospitais = self.db.query(models.Hospital).all()
        return hospitais
    
    # CORREÇÃO: Adicionando .first() para retornar a instância do objeto (ou None)
    def getHospitalById(self, id_hospital: int):
        return self.db.query(models.Hospital).filter(models.Hospital.id == id_hospital).first() # Corrigido: adicionado .first()

    # CORREÇÃO: Buscando a instância do objeto antes de deletar
    def removerHospital(self, id_hospital: int):
        hospital = self.db.query(models.Hospital).filter(models.Hospital.id == id_hospital).first()
        
        if hospital:
            self.db.delete(hospital) # Deleta a instância, não o objeto Query
            self.db.commit()
            return True # Indica sucesso na remoção
        
        return False # Indica que o hospital não foi encontrado
