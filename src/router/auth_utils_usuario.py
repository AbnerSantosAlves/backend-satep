from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from src.infra.config.database import get_db
from src.infra.providers import token_providers
from jose import JWTError
from src.infra.repositorios.usuario import RepositorioUsuario


oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")

def obter_usuario_logado(token: str = Depends(oauth2_schema), session: Session = Depends(get_db)):

    exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Token inválido')
    try:
        email = token_providers.verificar_access_token(token)
    except JWTError:
        raise exception
    
    if not email:
        raise exception
    
    usuario = RepositorioUsuario(session).obter_por_email(email)
    

    if not usuario:
        raise exception
    
    return usuario 

