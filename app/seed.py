import asyncio
from sqlalchemy.future import select

from core.database import async_session_factory
from methods.models import MethodOrm
from texts.models import TextOrm
from analysis.models import AnalysisResultOrm
from notes.models import NoteOrm


async def seed_database():
    async with async_session_factory() as session:
        existing_methods = await session.execute(select(MethodOrm))
        if not existing_methods.scalars().first():
            methods = [
                MethodOrm(
                    name="keyword_extraction",
                    description="Виділяє основні ключові слова з наданого тексту.",
                    parameters={"max_keywords": 10, "language_support": True},
                ),
                MethodOrm(
                    name="definition_extraction",
                    description="Витягує визначення термінів із тексту.",
                    parameters={"min_confidence": 0.7},
                ),
            ]
            session.add_all(methods)
            await session.commit()
            print("Методи додано")

        existing_texts = await session.execute(select(TextOrm))
        if not existing_texts.scalars().first():
            texts = [
                TextOrm(
                    title="Огляд машинного навчання",
                    content="Машинне навчання — це галузь штучного інтелекту, яка дозволяє системам навчатися на основі даних.",
                    language="uk",
                    source_type="manual_upload",
                ),
                TextOrm(
                    title="Обробка природної мови",
                    content="Обробка природної мови — це напрям штучного інтелекту, який зосереджений на розумінні та генерації людської мови.",
                    language="uk",
                    source_type="manual_upload",
                ),
            ]
            session.add_all(texts)
            await session.commit()
            print("Тексти додано")

        methods = (await session.execute(select(MethodOrm))).scalars().all()
        texts = (await session.execute(select(TextOrm))).scalars().all()

        existing_results = await session.execute(select(AnalysisResultOrm))
        if not existing_results.scalars().first() and methods and texts:
            results = [
                AnalysisResultOrm(
                    text_id=texts[0].id,
                    method_id=methods[0].id,
                    keywords=["машинне навчання", "штучний інтелект", "дані"],
                    definitions=[
                        {
                            "термін": "Машинне навчання",
                            "визначення": "Підгалузь ШІ, яка навчає системи працювати на основі даних.",
                        }
                    ],
                    metrics={"precision": 0.91, "recall": 0.87},
                ),
                AnalysisResultOrm(
                    text_id=texts[1].id,
                    method_id=methods[1].id,
                    keywords=["мовна модель", "ШІ", "обробка тексту"],
                    definitions=[
                        {
                            "термін": "Обробка природної мови",
                            "визначення": "Сфера, що займається взаємодією між людьми та комп’ютерами через мову.",
                        }
                    ],
                    metrics={"precision": 0.89, "recall": 0.85},
                ),
            ]
            session.add_all(results)
            await session.commit()
            print("Результати аналізу додано")

        results = (await session.execute(select(AnalysisResultOrm))).scalars().all()
        if results:
            existing_notes = await session.execute(select(NoteOrm))
            if not existing_notes.scalars().first():
                notes = [
                    NoteOrm(
                        text_id=results[0].text_id,
                        analysis_result_id=results[0].id,
                        structure={
                            "вступ": "Огляд концепції",
                            "деталі": "Описує основи машинного навчання",
                        },
                        summary="Машинне навчання вчить комп’ютери приймати рішення на основі даних.",
                    ),
                    NoteOrm(
                        text_id=results[1].text_id,
                        analysis_result_id=results[1].id,
                        structure={
                            "вступ": "Мовні технології",
                            "деталі": "Застосовується у перекладах, чат-ботах, аналізі тексту",
                        },
                        summary="Обробка природної мови дозволяє комп’ютерам розуміти людську мову.",
                    ),
                ]
                session.add_all(notes)
                await session.commit()
                print("Нотатки додано")

        print("Початкові дані успішно створено або вже були додані!")


if __name__ == "__main__":
    asyncio.run(seed_database())
