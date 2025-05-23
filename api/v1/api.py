from fastapi import APIRouter

from api.v1.endpoints import (
    usuario,
    tarefas,
)

api_router = APIRouter()

api_router.include_router(usuario.router)
api_router.include_router(tarefas.router)
