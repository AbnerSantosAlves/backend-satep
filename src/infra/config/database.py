from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# URL com * corretamente encodado como %2A
DATABASE_URL = (
    "postgresql://postgres.aptnrmrdoxxgmmgtuzqu:"
    "binho%2A225544"
    "@aws-0-us-west-2.pooler.supabase.com:6543/postgres"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,   # melhora estabilidade
    pool_size=10,         # (opcional)
    max_overflow=20       # (opcional)
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def criar_db():
    """Cria tabelas no banco"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Sessão de banco para uso no FastAPI"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
