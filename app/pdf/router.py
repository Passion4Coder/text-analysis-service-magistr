from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.analysis.service import get_analysis_result_by_id
from app.core.database import get_session
from app.pdf.service import create_summary_pdf

router = APIRouter(prefix="/pdf", tags=["PDF 📄"])


@router.get(
    "/{analysis_id}",
    summary="Завантажити summary у форматі PDF",
    response_description="PDF файл зі summary",
)
async def download_summary_pdf(
    analysis_id: int,
    session: AsyncSession = Depends(get_session),
):
    analysis_result = await get_analysis_result_by_id(session, analysis_id)

    if not analysis_result:
        raise HTTPException(status_code=404, detail="Запис не знайдено.")

    if not analysis_result.summary_text:
        raise HTTPException(status_code=400, detail="Для цього запису summary відсутнє.")

    pdf_stream = create_summary_pdf(analysis_result.id, analysis_result.summary_text, analysis_result.keywords)

    return StreamingResponse(
        pdf_stream,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="summary_{analysis_id}.pdf"'},
    )
