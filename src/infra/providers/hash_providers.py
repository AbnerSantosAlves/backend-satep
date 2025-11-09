from pwdlib import PasswordHash

pwd_context = PasswordHash.recommended()

def gerar_hash(texto: str) -> str:
    return pwd_context.hash(texto)

def verificar_hash(texto: str, hash: str) -> bool:
    return pwd_context.verify(texto, hash)
