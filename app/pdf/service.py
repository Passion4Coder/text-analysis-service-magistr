import os
from io import BytesIO
from typing import List

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    ListFlowable,
    ListItem,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)


def create_summary_pdf(analysis_id: int, summary: str, keywords: List[str]) -> BytesIO:
    pdfmetrics.registerFont(TTFont("DejaVuSans", os.path.join("app", "pdf", "fonts", "DejaVuSans.ttf")))

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        title=f"Summary (Analysis {analysis_id})",
    )

    doc.analysis_id = analysis_id

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        textColor=HexColor("#1D3557"),
        fontSize=22,
        spaceAfter=20,
        fontName="DejaVuSans",
    )

    section_style = ParagraphStyle(
        "SectionStyle",
        parent=styles["Heading2"],
        textColor=HexColor("#1D3557"),
        fontSize=16,
        spaceAfter=10,
        fontName="DejaVuSans",
    )

    body_style = ParagraphStyle(
        "BodyStyle",
        parent=styles["Normal"],
        fontSize=12,
        leading=16,
        textColor=HexColor("#333333"),
        fontName="DejaVuSans",
        spaceAfter=6,
    )

    elements = []

    elements.append(Paragraph("Підсумок", title_style))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(summary.replace("\n", "<br/>"), body_style))
    elements.append(Spacer(1, 24))

    elements.append(Paragraph("Ключові слова:", section_style))
    elements.append(
        ListFlowable(
            [ListItem(Paragraph(keyword, body_style)) for keyword in keywords],
            bulletType="1",
            bulletFormat="%s.",
            start="1",
        )
    )

    def add_page_number(canvas, doc_obj):
        page_num = canvas.getPageNumber()
        canvas.setFont("DejaVuSans", 10)
        canvas.setFillColor(HexColor("#808080"))
        canvas.drawCentredString(A4[0] / 2, 1.2 * cm, "Згенеровано за допомогою ExtractLab")
        canvas.drawCentredString(A4[0] / 2, 0.5 * cm, str(page_num))

    def add_metadata(canvas, doc_obj):
        canvas.setAuthor("ExtractLab")
        canvas.setCreator("ExtractLab Engine")
        canvas.setTitle(f"Summary (Analysis ID: {doc_obj.analysis_id})")
        canvas.setSubject("Automatically generated summary report by ExtractLab")

        add_page_number(canvas, doc_obj)

    doc.build(elements, onFirstPage=add_metadata, onLaterPages=add_metadata)

    buffer.seek(0)

    return buffer
