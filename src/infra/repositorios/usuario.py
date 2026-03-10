from sqlalchemy.orm import Session
from src.infra.models import models
from src.infra.schema import schemas


class RepositorioUsuario():
    def __init__(self, db: Session):
        self.db = db

    
    def criar_administrador(self):
        administrador = models.Usuario(
            nome = "Abner Santos Alves",
            email = "abneralves562@gmail.com",
            senha = "abner1234",
            tipo = 0
        )

        self.db.add(administrador)
        self.db.commit(administrador)
        self.db.refresh(administrador)

    def createAdministrador(self, administrador: schemas.Usuario):
        administrador = models.Usuario(
            nome = administrador.nome,
            email = administrador.email,
            senha = administrador.senha,
            tipo = 0
        )

        self.db.add(administrador)
        self.db.commit()
        self.db.refresh(administrador)

        return administrador
    
    def createFuncionario(self, funcionario: schemas.Usuario):
        funcionario = models.Usuario(
            nome = funcionario.nome,
            email = funcionario.email,
            senha = funcionario.senha,
            tipo = 1
        )

        self.db.add(funcionario)
        self.db.commit()

        return funcionario

    def getFuncionarios(self):
        funcionarios = self.db.query(models.Usuario).filter(models.Usuario.tipo == 1).all()
        return funcionarios
    
    
    def getAdministradores(self):
        administradores = self.db.query(models.Usuario).filter(models.Usuario.tipo == 0).all()
        return administradores
    

    def getFuncionarioById(self, id_funcionario: int):
        funcionario = self.db.query(models.Usuario).filter(models.Usuario.id == id_funcionario, models.Usuario.tipo == 1).first()
        return funcionario
    
    def getAdministradorById(self, id_administrador: int):
        administrador = self.db.query(models.Usuario).filter(models.Usuario.id == id_administrador, models.Usuario.tipo == 0).first()
        return administrador

    
    def editarUsuario(self, usuario_id: int, alteracao: schemas.Usuario):
        usuario = self.db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
        if not usuario:
            return None

        usuario.nome = alteracao.nome or usuario.nome
        usuario.email = alteracao.email or usuario.email
        if alteracao.senha:
            from infra.providers import hash_providers
            usuario.senha = hash_providers.gerar_hash(alteracao.senha)

        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def deletarUsuario(self, usuario_id: int):
        usuario = self.db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()

        self.db.delete(usuario)
        self.db.commit()

        return "Deletado com sucesso"
    

    def obter_por_email(self, email: str):
        usuario = self.db.query(models.Usuario).filter(models.Usuario.email==email).first()
        return usuario
