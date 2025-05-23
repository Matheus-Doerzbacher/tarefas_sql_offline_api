from pydantic import BaseModel
from typing import Optional


class TarefaCreate(BaseModel):
    titulo: str
    descricao: str


class Tarefa(TarefaCreate):
    id_tarefa: int
    id_usuario: int
    api_status: str
    data_criacao: str
    data_alteracao: str
    is_concluida: bool
    pass

    class Config:
        from_attributes = True
