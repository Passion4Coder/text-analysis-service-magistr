import asyncio
from sqlalchemy.future import select

from app.core.database import async_session_factory
from app.texts.models import TextOrm
from app.analysis.models import AnalysisResultOrm
from app.notes.models import NoteOrm


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

        texts = (await session.execute(select(TextOrm))).scalars().all()

        existing_results = await session.execute(select(AnalysisResultOrm))
        if not existing_results.scalars().first() and texts:
            results = [
                AnalysisResultOrm(
                    text_id=texts[0].id,
                    lemmas={"машинне навчання": "машинний_навчання"},
                    keywords=["машинне навчання", "штучний інтелект", "дані"],
                    embeddings=None,
                    duration_ms=120,
                ),
                AnalysisResultOrm(
                    text_id=texts[1].id,
                    lemmas={"обробка": "обробка", "мова": "мова"},
                    keywords=["мовна модель", "ШІ", "обробка тексту"],
                    embeddings=None,
                    duration_ms=110,
                ),
            ]
            session.add_all(results)
            await session.commit()
            print("Результати аналізу додано")

        results = (await session.execute(select(AnalysisResultOrm))).scalars().all()

        existing_notes = await session.execute(select(NoteOrm))
        if not existing_notes.scalars().first() and results:
            notes = [
                NoteOrm(
                    text_id=results[0].text_id,
                    analysis_result_id=results[0].id,
                    structured_notes={
                        "вступ": "Огляд концепції",
                        "деталі": "Описує основи машинного навчання",
                    },
                    summary_text="Машинне навчання вчить комп’ютери приймати рішення на основі даних.",
                ),
                NoteOrm(
                    text_id=results[1].text_id,
                    analysis_result_id=results[1].id,
                    structured_notes={
                        "вступ": "Мовні технології",
                        "деталі": "Застосовується у перекладах, чат-ботах, аналізі тексту",
                    },
                    summary_text="Обробка природної мови дозволяє комп’ютерам розуміти людську мову.",
                ),
            ]
            session.add_all(notes)
            await session.commit()
            print("Нотатки додано")

        print("Початкові дані успішно створено або вже були додані!")


if __name__ == "__main__":
    asyncio.run(seed_database())
