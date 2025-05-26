from pydantic import BaseModel, Field
from typing import Optional


class TarefaCreate(BaseModel):
    titulo: str = Field(..., min_length=1, max_length=256)
    descricao: str = Field(..., min_length=1, max_length=256)

    class Config:
        json_schema_extra = {
            "example": {
                "titulo": "Minha Tarefa! @#$%",
                "descricao": "Descrição com caracteres especiais: áéíóú",
            }
        }


class Tarefa(TarefaCreate):
    id_tarefa: int
    id_usuario: int
    sincronizado: bool
    data_criacao: str
    data_alteracao: str
    is_concluida: bool
    pass

    class Config:
        from_attributes = True
