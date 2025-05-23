from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.tarefa_model import TarefaModel
from schemas.tarefa_schema import Tarefa, TarefaCreate
from models.usuario_model import UsuarioModel
from core.deps import get_current_user, get_session
from datetime import datetime
from fastapi import status


router = APIRouter(prefix="/tarefas", tags=["tarefas"])


@router.get("/", response_model=List[Tarefa])
async def get_tarefas(
    db: AsyncSession = Depends(get_session),
    usuario_logado: UsuarioModel = Depends(get_current_user),
):
    async with db as session:
        query = select(TarefaModel).where(
            TarefaModel.id_usuario == usuario_logado.id_usuario
        )
        result = await session.execute(query)
        tarefas: List[TarefaModel] = result.scalars().all()
        return tarefas


@router.get("/{tarefa_id}", response_model=Tarefa)
async def get_tarefa_by_id(
    tarefa_id: int,
    db: AsyncSession = Depends(get_session),
    usuario_logado: UsuarioModel = Depends(get_current_user),
):
    if usuario_logado.id_usuario != tarefa_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você só pode acessar suas próprias tarefas",
        )

    async with db as session:
        query = select(TarefaModel).where(
            TarefaModel.id_tarefa == tarefa_id,
            TarefaModel.id_usuario == usuario_logado.id_usuario,
        )
        result = await session.execute(query)
        tarefa: TarefaModel = result.scalar_one_or_none()
        if tarefa:
            return tarefa
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")


@router.post("/", response_model=Tarefa, status_code=status.HTTP_201_CREATED)
async def post_tarefa(
    tarefa: TarefaCreate,
    db: AsyncSession = Depends(get_session),
    usuario_logado: UsuarioModel = Depends(get_current_user),
):

    async with db as session:
        tarefa = TarefaModel(
            titulo=tarefa.titulo,
            descricao=tarefa.descricao,
            id_usuario=usuario_logado.id_usuario,
            api_status="pendente",
            is_concluida=False,
            data_criacao=datetime.now().isoformat(),
            data_alteracao=datetime.now().isoformat(),
        )
        session.add(tarefa)
        await session.commit()
        await session.refresh(tarefa)
        return tarefa


# PUT Tarefa
@router.put("/{tarefa_id}", response_model=Tarefa)
async def put_tarefa(
    tarefa_id: int,
    tarefa: Tarefa,
    db: AsyncSession = Depends(get_session),
    usuario_logado: UsuarioModel = Depends(get_current_user),
):
    if usuario_logado.id_usuario != tarefa.id_usuario:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você só pode atualizar suas próprias tarefas",
        )

    async with db as session:
        tarefa_bd = await session.get(TarefaModel, tarefa_id)

        for key, value in tarefa.model_dump(exclude_unset=True).items():
            if key != "data_alteracao":
                setattr(tarefa_bd, key, value)

        tarefa_bd.data_alteracao = datetime.now().isoformat()

        await session.commit()
        await session.refresh(tarefa_bd)
        return tarefa_bd


# DELETE Tarefa
@router.delete("/{tarefa_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tarefa(
    tarefa_id: int,
    db: AsyncSession = Depends(get_session),
    usuario_logado: UsuarioModel = Depends(get_current_user),
):
    async with db as session:
        tarefa_bd = await session.get(TarefaModel, tarefa_id)

        if not tarefa_bd:
            raise HTTPException(status_code=404, detail="Tarefa não encontrada")

        if usuario_logado.id_usuario != tarefa_bd.id_usuario:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você só pode deletar suas próprias tarefas",
            )

        await session.delete(tarefa_bd)
        await session.commit()
