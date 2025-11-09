from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time
from sqlalchemy.orm import relationship, declarative_base
from src.infra.config.database import Base

class Usuario(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    email = Column(String)
    senha = Column(String)
    tipo = Column(Integer)


class Paciente(Base):
    __tablename__ = 'paciente'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    email = Column(String)
    senha = Column(String)
    telefone = Column(String)
    cpf = Column(String)
    nr_endereco = Column(Integer)
    nm_endereco = Column(String)
    nm_bairro = Column(String)
    nm_municipio = Column(String)

    agendamentos = relationship("Agendamento", back_populates="paciente")

class Hospital(Base):
    __tablename__ = "hospital"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    municipio = Column(String)

    agendamentos = relationship("Agendamento", back_populates="hospital")

class Agendamento(Base):
    __tablename__ = "agendamento"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("paciente.id"))
    viagem_id = Column(Integer, ForeignKey("viagem.id"), nullable=True) 
    hospital_id = Column(Integer, ForeignKey("hospital.id"))

    data_agendamento = Column(Date, nullable=False)
    hora_agendamento = Column(Time, nullable=False)
    nm_endereco = Column(String, nullable=False)
    nr_endereco = Column(String, nullable=False)
    nm_bairro = Column(String, nullable=False)
    nm_cidade = Column(String, nullable=False)
    ds_agendamento = Column(String, nullable=True)
    procedimento = Column(String, nullable=False)
    status_agendamento = Column(String, nullable=True, default="Em análise")

    logs = relationship("Logs", back_populates="agendamento")
    paciente = relationship("Paciente", back_populates="agendamentos")
    hospital = relationship("Hospital", back_populates="agendamentos")
    viagem = relationship("Viagem", back_populates="agendamentos", foreign_keys=[viagem_id])




class Viagem(Base):
    __tablename__ = "viagem"
    id = Column(Integer, primary_key=True, index=True)
    nm_motorista = Column(String)
    nr_carteira = Column(String)
    nr_fone = Column(String)
    nr_capacidade = Column(Integer)
    status_viagem = Column(String)


    agendamentos = relationship("Agendamento", back_populates="viagem")


class Logs(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    nm_usuario = Column(String)
    agendamento_id = Column(Integer, ForeignKey("agendamento.id"))
    tipo_acao = Column(String)
    data = Column(Date)

    # RELACIONAMENTO
    agendamento = relationship("Agendamento", back_populates="logs")






