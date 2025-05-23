from core.configs import settings
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean


class TarefaModel(settings.DBBaseModel):

    __tablename__ = "tarefas"

    id_tarefa: int = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario: int = Column(
        Integer,
        ForeignKey("usuarios.id_usuario"),
        nullable=False,
    )
    titulo: str = Column(String(256), nullable=False)
    descricao: str = Column(String(256), nullable=False)
    is_concluida: bool = Column(Boolean, nullable=False)
    api_status = Column(String(256), nullable=False)
    data_criacao = Column(String(256), nullable=False)
    data_alteracao = Column(String(256), nullable=False)
