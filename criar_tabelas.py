from core.configs import settings
from core.database import engine


async def create_tables() -> None:
    import models.__all_models

    print("Criando tabelas no banco de dados...")
    print("\nTabelas que serão criadas:")
    for table in settings.DBBaseModel.metadata.tables:
        print(f"- {table}")

    async with engine.begin() as conn:
        await conn.run_sync(settings.DBBaseModel.metadata.drop_all)
        await conn.run_sync(settings.DBBaseModel.metadata.create_all)

    print("\nTabelas criadas com sucesso!")


if __name__ == "__main__":
    import asyncio

    asyncio.run(create_tables())
