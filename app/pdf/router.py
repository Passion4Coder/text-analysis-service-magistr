from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse

from app.pdf.service import PdfService
from app.notes.service import get_note_by_id

router = APIRouter(
    prefix="/pdf",
    tags=["PDF 📄"],
)


@router.get(
    "/summary/{note_id}",
    summary="Завантажити summary у форматі PDF",
    response_description="PDF файл зі summary",
)
async def download_summary_pdf(
    note_id: int,
    method: str = Query(
        "hybrid",
        enum=["tfidf", "rake", "hybrid"],
        description="Метод для вибору ключових слів",
    ),
):
    note = await get_note_by_id(note_id)

    if not note:
        raise HTTPException(status_code=404, detail="Запис не знайдено.")

    if not note.summary:
        raise HTTPException(
            status_code=400,
            detail="Для цього запису summary відсутнє.",
        )

    analysis_result = note.analysis_result

    glossary = None
    if analysis_result and analysis_result.definitions:
        glossary = {}
        for d in analysis_result.definitions:
            glossary.update(d)

    pdf_stream = PdfService.create_summary_pdf(
        summary=note.summary, note_id=note_id, method=method, glossary=glossary
    )

    return StreamingResponse(
        pdf_stream,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="summary_{note_id}.pdf"'
        },
    )
