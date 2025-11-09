from pydantic import BaseModel, Field # Adicionado o import de Field
from typing import Optional
from datetime import time, date


class Usuario(BaseModel):
    id: Optional[int] = None
    nome: str
    email: str
    senha: str
    tipo: str  #"operador", "administrador"

    class Config:
        from_attributes = True


class LoginData(BaseModel):
    email: str
    senha: str


# Paciente, incluindo os dados de usuário completos
class Paciente(BaseModel):
    id: Optional[int] = None
    nome: str
    email: str
    senha: str
    telefone: str
    cpf: str
    nr_endereco: int
    nm_endereco: str
    nm_bairro: str
    nm_municipio: str

    class Config:
        from_attributes = True

class hospital(BaseModel):
    id: Optional[int] = None
    nome: str
    municipio: str

    class Config:
        from_attributes = True


class AlteracaoStatusAgendamento(BaseModel):
    status_agendamento: str


class viagem(BaseModel):
    id: Optional[int] = None
    nm_motorista: str
    nr_carteira: str
    nr_fone: str
    nr_capacidade: int
    status_viagem: Optional[str] = "Em andamento"

    class Config:
        from_attributes = True


# CORRIGIDO: Adicionado Field(alias="nome") para mapear o campo 'nome' do ORM 
# para 'nm_hospital' no schema de saída.
class HospitalOut(BaseModel):
    nm_hospital: str = Field(alias="nome") # Mapeamento corrigido

    class Config:
        from_attributes = True

class AgendamentoOut(BaseModel):
    id: int
    status_agendamento: Optional[str]
    hospital: HospitalOut # aqui ele vai mostrar só nm_hospital

    class Config:
        from_attributes = True


class UsuarioCriado(BaseModel):
    id: int
    nome: str
    email: str

    class Config:
        from_attributes = True # CORRIGIDO: 'from_atribbuts' alterado para 'from_attributes'

class Logs(BaseModel):
    id: Optional[int] = None
    nm_usuario: str
    agendamento_id: int 
    tipo_acao: str  
    data: str

class LogsRegistroAprovado(BaseModel):
    nm_usuario: str
    nm_paciente: str
    tipo_acao: str
    data: str

class AgendamentoBase(BaseModel):
    hospital_id: int
    data_agendamento: date
    hora_agendamento: time
    nm_endereco: str
    nr_endereco: str
    nm_bairro: str
    nm_cidade: str
    ds_agendamento: str | None = None
    procedimento: str
    status_agendamento: Optional[str] = None

class AgendamentoCreate(AgendamentoBase):
    pass  # Sem paciente_id

class Agendamento(AgendamentoBase):
    id: int
    paciente_id: int

    class Config:
        orm_mode = True


class PacienteUpdate(BaseModel):
    nome: Optional[str]
    email: Optional[str]
    telefone: Optional[str]
    cpf: Optional[str]
    nr_endereco: Optional[str]
    nm_endereco: Optional[str]
    nm_bairro: Optional[str]
    nm_municipio: Optional[str]