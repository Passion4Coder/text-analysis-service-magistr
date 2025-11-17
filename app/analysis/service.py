from sqlalchemy import select
from app.analysis.definitions_dict import DEFINITIONS
from app.notes.models import NoteOrm
from app.texts.models import TextOrm
from app.methods.hybrid_extractor import combine_tfidf_rake
from app.analysis.utils import preprocess_text, lemmatize_text
from app.core.database import async_session_factory
from app.analysis.models import AnalysisResultOrm
from app.methods.models import MethodOrm


def generate_definitions(keywords: list[str]) -> list[dict]:
    """Повертає визначення для знайдених ключових слів."""
    results = []
    for kw in keywords:
        for term, definition in DEFINITIONS.items():
            if kw in term or term in kw:
                results.append({"term": term, "definition": definition})
    return results


def generate_note_structure(content: str, keywords: list[str]) -> dict:
    """Створює базову структуру нотатки: речення з ключовими словами."""
    sentences = [s.strip() for s in content.split(".") if s.strip()]
    relevant_sentences = [s for s in sentences if any(k in s for k in keywords)]
    return {"keywords": keywords, "sentences_with_keywords": relevant_sentences}


def generate_summary(structure: dict, max_sentences: int = 3) -> str:
    """Простий summary: об’єднуємо ключові речення до max_sentences."""
    sentences = structure.get("sentences_with_keywords", [])
    return ". ".join(sentences[:max_sentences]) + ("." if sentences else "")


def postprocess_keywords(keywords):
    """Очистка, нормалізація та видалення дублікатів ключових слів."""
    cleaned = []
    seen = set()

    corrections = {
        "стадіонь": "стадіон",
        "машийнний": "машинний",
        "навча": "навчання",
        "ння": "навчання",
    }

    for term, score in keywords:
        term = term.strip().lower()

        if term in corrections:
            term = corrections[term]

        if not term or term in seen:
            continue

        tokens = term.split()
        if any(tok == prev for prev, tok in zip(tokens, tokens[1:])):
            continue

        seen.add(term)
        cleaned.append((term, float(score)))

    cleaned = [(t, s) for t, s in cleaned if s > 0]

    return cleaned


async def analyze_and_save(
    content: str,
    title: str | None = None,
    text_id: int | None = None,
    method_name: str = "hybrid",
):
    """Аналізує текст, створює запис у texts та analysis_results, повертає результати."""

    clean = preprocess_text(content)
    lem = lemmatize_text(clean)
    docs = [lem if lem else clean]

    combined = combine_tfidf_rake(docs, top_n=15)[0]
    combined = postprocess_keywords(combined)
    keywords = [t for t, _ in combined]

    definitions = generate_definitions(keywords)
    metrics = {"n_terms": len(combined)}

    async with async_session_factory() as session:
        q = await session.execute(
            select(MethodOrm).where(MethodOrm.name == method_name)
        )
        method = q.scalar_one_or_none()

        if method is None:
            method = MethodOrm(name=method_name, description="Hybrid TF-IDF + RAKE")
            session.add(method)
            await session.commit()
            await session.refresh(method)
        method_id = method.id

        if text_id is None:
            new_text = TextOrm(content=content, title=title)
            session.add(new_text)
            await session.commit()
            await session.refresh(new_text)
            text_id = new_text.id

        ar = AnalysisResultOrm(
            text_id=text_id,
            method_id=method_id,
            keywords=keywords,
            definitions=definitions,
            metrics=metrics,
        )
        session.add(ar)
        await session.commit()
        await session.refresh(ar)

        note_structure = generate_note_structure(content, keywords)
        note_summary = generate_summary(note_structure, max_sentences=3)

        note = NoteOrm(
            text_id=text_id,
            analysis_result_id=ar.id,
            structure=note_structure,
            summary=note_summary,
        )
        session.add(note)
        await session.commit()
        await session.refresh(note)

    return {
        "analysis_result_id": ar.id,
        "text_id": text_id,
        "note_id": note.id,
        "keywords": [{"term": t, "score": float(s)} for t, s in combined],
        "definitions": definitions,
        "metrics": metrics,
        "note_structure": note_structure,
        "note_summary": note_summary,
    }


async def fetch_all_analyses():
    """Повертає список всіх текстів + базову інформацію про аналіз."""
    async with async_session_factory() as session:
        q = await session.execute(
            select(
                AnalysisResultOrm.id,
                AnalysisResultOrm.text_id,
                AnalysisResultOrm.keywords,
                AnalysisResultOrm.metrics,
                AnalysisResultOrm.created_at,
                TextOrm.title,
                TextOrm.content,
                MethodOrm.name.label("method_name"),
            )
            .join(TextOrm, TextOrm.id == AnalysisResultOrm.text_id)
            .join(MethodOrm, MethodOrm.id == AnalysisResultOrm.method_id)
            .order_by(AnalysisResultOrm.created_at.desc())
        )
        rows = q.mappings().all()
        return [dict(r) for r in rows]


async def fetch_analysis_by_text_id(text_id: int):
    """Повертає повний результат аналізу разом із нотатками."""
    async with async_session_factory() as session:
        q = await session.execute(
            select(AnalysisResultOrm, TextOrm, MethodOrm, NoteOrm)
            .join(TextOrm, TextOrm.id == AnalysisResultOrm.text_id)
            .join(MethodOrm, MethodOrm.id == AnalysisResultOrm.method_id)
            .join(NoteOrm, NoteOrm.analysis_result_id == AnalysisResultOrm.id)
            .where(AnalysisResultOrm.text_id == text_id)
        )

        row = q.mappings().first()

        if not row:
            return None

        ar: AnalysisResultOrm = row["AnalysisResultOrm"]
        text: TextOrm = row["TextOrm"]
        method: MethodOrm = row["MethodOrm"]
        note: NoteOrm = row["NoteOrm"]

        return {
            "analysis_result_id": ar.id,
            "text_id": text.id,
            "title": text.title,
            "content": text.content,
            "method": method.name,
            "keywords": ar.keywords,
            "definitions": ar.definitions,
            "metrics": ar.metrics,
            "note_structure": note.structure,
            "note_summary": note.summary,
            "created_at": ar.created_at.isoformat(),
        }


async def fetch_keywords_only(text_id: int):
    """Повертає лише keywords з аналізу."""
    async with async_session_factory() as session:
        q = await session.execute(
            select(AnalysisResultOrm.keywords).where(
                AnalysisResultOrm.text_id == text_id
            )
        )

        row = q.scalar_one_or_none()
        return row
