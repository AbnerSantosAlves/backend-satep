from fastapi import FastAPI
from src.infra.config.database import get_db, criar_db 
from apscheduler.schedulers.background import BackgroundScheduler
from src.services.checar_agendamentos import checar_agendamentos, lembrar_confirmacao
from fastapi.middleware.cors import CORSMiddleware
from src.router import rotas_usuario, rotas_paciente, rotas_agendamento, rotas_viagem, rotas_hospital, rotas_historico
from src.services.checar_viagem import checar_viagens
from src.infra.repositorios.usuario import RepositorioUsuario
from src.infra.repositorios.hospital import RepositorioHospital

criar_db()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

scheduler = BackgroundScheduler()
scheduler.add_job(lambda: checar_viagens(next(get_db())), 'cron', hour=0, minute=5)
scheduler.add_job(lambda: lembrar_confirmacao(next(get_db())), "cron", hour=8, minute=0)
scheduler.add_job(lambda: checar_agendamentos(next(get_db())), "cron", hour=16, minute=31)
scheduler.start()




@app.api_route("/ping", methods=["GET", "HEAD"])
def ping():
    return {"status": "alive"}


RepositorioUsuario.criar_administrador()
RepositorioHospital.criar_hospitais()

# ROTAS DE USUÁRIO
app.include_router(rotas_usuario.router)


# ROTAS DE PACIENTE
app.include_router(rotas_paciente.router)


# ROTAS DE AGENDAMENTO
app.include_router(rotas_agendamento.router)

# ROTAS DE VIAGEM
app.include_router(rotas_viagem.router)


# ROTAS DE HOSPITAL
app.include_router(rotas_hospital.router)


app.include_router(rotas_historico.router)
