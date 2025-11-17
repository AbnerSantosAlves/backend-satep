from fastapi import APIRouter, Depends, HTTPException, status
from src.infra.repositorios.usuario import RepositorioUsuario
from src.infra.providers import hash_providers, token_providers
from src.infra.schema.schemas import Usuario, LoginData, UsuarioCriado
from src.infra.models import models
from sqlalchemy.orm import Session
from src.infra.config.database import get_db
from src.router.auth_utils_usuario import obter_usuario_logado


router = APIRouter()


@router.post("/usuarios/criaradministrador", response_model=UsuarioCriado)
def create_administrador(db: Session = Depends(get_db)):
    return RepositorioUsuario.criar_administrador()


# SIGN UP DE ADMINISTRADOR
@router.post("/usuarios/administrador", response_model=UsuarioCriado)
def create_administrador(administrador: Usuario, db: Session = Depends(get_db)):
    administrador.senha = hash_providers.gerar_hash(administrador.senha)
    novo_administrador = RepositorioUsuario(db).createAdministrador(administrador)
    if not novo_administrador:
        raise HTTPException(status_code=400, detail="Erro ao criar administrador")
    return UsuarioCriado(id = novo_administrador.id, nome=novo_administrador.nome, email=novo_administrador.email)

# SIGN UP DE FUNCIONÁRIO
@router.post("/usuarios/funcionario")
def create_funcionario(funcionario: Usuario, db: Session = Depends(get_db)):
    funcionario.senha = hash_providers.gerar_hash(funcionario.senha)
    novo_funcionario = RepositorioUsuario(db).createFuncionario(funcionario)
    if not novo_funcionario:
        raise HTTPException(status_code=400, detail="Erro ao criar funcionário")
    return UsuarioCriado(id = novo_funcionario.id, nome=novo_funcionario.nome, email=novo_funcionario.email)





# CRUD DE USUÁRIOS
@router.put("/usuarios/editar")
def atualizar_perfil(
    usuario_update: Usuario,
    usuario_logado: Usuario = Depends(obter_usuario_logado),
    db: Session = Depends(get_db)
):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_logado.id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # Atualiza apenas os campos enviados
    usuario.nome = usuario_update.nome or usuario.nome
    usuario.email = usuario_update.email or usuario.email

    if usuario_update.senha:
        usuario.senha = hash_providers.gerar_hash(usuario_update.senha)

    db.commit()
    db.refresh(usuario)
    return {"msg": "Perfil atualizado com sucesso", "usuario": usuario}


@router.delete("/usuarios/{id_usuario}")
def deletar_usuario(id_usuario: int, db: Session = Depends(get_db)):
    return RepositorioUsuario(db).deletarUsuario(id_usuario)





#PESQUISA DE TODOS OS ADMINISTRADORES 
@router.get("/administradores")
def get_administradores(db: Session = Depends(get_db)):
    return RepositorioUsuario(db).getAdministradores()


#PESQUISA DE TODOS OS FUNCIONÁRIOS
@router.get("/funcionarios")
def get_funcionarios(db: Session = Depends(get_db)):
    return RepositorioUsuario(db).getFuncionarios()


@router.post("/token")
def login(login_data: LoginData, session: Session = Depends(get_db)): 
   email = login_data.email
   senha = login_data.senha

   usuario = RepositorioUsuario(session).obter_por_email(email)

   if not usuario:
       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email ou senha inválidos")
   
   senha_valida = hash_providers.verificar_hash(senha, usuario.senha)

   if not senha_valida:
       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email ou senha inválidos")
   

   token = token_providers.criar_access_token({'sub': usuario.email})
   return {'usuario': usuario, 'acess_token': token}


@router.get('/me')
def me(usuario: Usuario = Depends(obter_usuario_logado)):
    return usuario





