from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# Criar engine usando apenas o arquivo local "meubd.db"
engine = create_engine(
    "sqlite:///meubd.db",
    connect_args={"check_same_thread": False}
)

# Criar sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base
Base = declarative_base()

# Criar tabelas
def criar_db():
    Base.metadata.create_all(bind=engine)

# Dependência (FastAPI ou uso manual)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
