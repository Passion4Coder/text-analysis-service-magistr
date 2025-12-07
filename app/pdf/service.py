import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from io import BytesIO


class PdfService:
    @staticmethod
    def create_summary_pdf(
        summary: str, note_id: int, method: str = "hybrid", glossary: dict | None = None
    ) -> BytesIO:
        pdfmetrics.registerFont(
            TTFont("DejaVuSans", os.path.join("app", "pdf", "fonts", "DejaVuSans.ttf"))
        )

        buffer = BytesIO()

        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            leftMargin=2 * cm,
            rightMargin=2 * cm,
            topMargin=2 * cm,
            bottomMargin=2 * cm,
            title=f"Summary (Note {note_id})",
        )

        doc.note_id = note_id

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

        footer_style = ParagraphStyle(
            "FooterStyle",
            parent=styles["Normal"],
            alignment=TA_CENTER,
            textColor=HexColor("#457B9D"),
            fontSize=10,
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

        docs = [summary]
        # if method.lower() == "tfidf":
        #     keywords_list = extract_keywords_tfidf(docs)[0]
        # elif method.lower() == "rake":
        #     keywords_list = extract_keywords_rake(docs)[0]
        # else:
        #     keywords_list = combine_tfidf_rake(docs)[0]

        # keywords_text = ", ".join([kw for kw, _ in keywords_list])

        elements = []

        elements.append(Paragraph("Підсумок", title_style))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(summary.replace("\n", "<br/>"), body_style))
        elements.append(Spacer(1, 24))

        elements.append(Paragraph("Ключові слова:", section_style))
        # elements.append(Paragraph(keywords_text, body_style))
        elements.append(Spacer(1, 24))

        if glossary:
            elements.append(Paragraph("Глосарій:", section_style))
            for term, definition in glossary.items():
                elements.append(Paragraph(f"{term.upper()}: {definition}", body_style))
            elements.append(Spacer(1, 12))

        elements.append(Paragraph("Згенеровано за допомогою ExtractLab", footer_style))

        def add_page_number(canvas, doc_obj):
            page_num = canvas.getPageNumber()
            canvas.setFont("DejaVuSans", 10)
            canvas.setFillColor(HexColor("#457B9D"))
            canvas.drawCentredString(A4[0] / 2, 1 * cm, str(page_num))

        def add_metadata(canvas, doc_obj):
            canvas.setAuthor("ExtractLab")
            canvas.setCreator("ExtractLab Engine")
            canvas.setTitle(f"Summary (Note ID: {doc_obj.note_id})")
            canvas.setSubject("Automatically generated summary report by ExtractLab")

            add_page_number(canvas, doc_obj)

        doc.build(elements, onFirstPage=add_metadata, onLaterPages=add_metadata)

        buffer.seek(0)
        return buffer
