from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///meubd.db")

# 1. Criar o engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

# 2. Criar fábrica de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Declarative base
Base = declarative_base()

# 4. Função para criar o banco
def criar_db():
    Base.metadata.create_all(bind=engine)

# 5. Dependência para FastAPI (ou outros frameworks)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
