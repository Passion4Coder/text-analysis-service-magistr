import asyncio

from sqlalchemy.future import select

from app.core.database import async_session_factory
from app.texts.models import TextOrm


async def seed_database():
    async with async_session_factory() as session:
        existing_texts = await session.execute(select(TextOrm))
        if not existing_texts.scalars().first():
            texts = [
                TextOrm(
                    title="Огляд машинного навчання",
                    content="Машинне навчання — це галузь штучного інтелекту, яка дозволяє системам навчатися на основі даних.",
                    language="uk",
                    source_type="upload",
                ),
                TextOrm(
                    title="Обробка природної мови",
                    content="Обробка природної мови — це напрям штучного інтелекту, який зосереджений на розумінні та генерації людської мови.",
                    language="uk",
                    source_type="upload",
                ),
            ]
            session.add_all(texts)
            await session.commit()
            print("Тексти додано")

        print("Початкові дані успішно створено або вже були додані!")


if __name__ == "__main__":
    asyncio.run(seed_database())
