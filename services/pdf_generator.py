import os
from datetime import datetime

from fpdf import FPDF, XPos, YPos

from services.lang import get_text


class PDFReport(FPDF):
    def __init__(self, lang="es"):
        super().__init__()
        self._lang = lang

    def header(self):
        self.set_font('helvetica', 'B', 15)
        self.set_text_color(41, 128, 185)
        self.cell(0, 10, get_text("pdf_title", self._lang), new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Pagina {self.page_no()}', align='C')


def generate_medical_report(image_path, xai_path, label, confidence, model_name, lang="es"):
    pdf = PDFReport(lang=lang)
    pdf.add_page()
    pdf.set_font('helvetica', '', 12)

    pdf.set_fill_color(240, 240, 240)
    pdf.cell(0, 10, f" {get_text('pdf_date', lang)} {datetime.now().strftime('%Y-%m-%d %H:%M')}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L', fill=True)
    pdf.cell(0, 10, f" {get_text('pdf_model', lang)} {model_name}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L', fill=True)
    pdf.ln(10)

    pdf.set_font('helvetica', 'B', 14)
    if "neumonía" in label.lower() or "pneumonia" in label.lower() or "肺炎" in label or "न्यूमोनिया" in label:
        pdf.set_text_color(192, 57, 43)
    else:
        pdf.set_text_color(39, 174, 96)

    pdf.cell(0, 10, get_text("pdf_diagnosis", lang).format(label=label.upper()), new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.set_text_color(0)
    pdf.set_font('helvetica', '', 12)
    pdf.cell(0, 10, get_text("pdf_confidence", lang).format(confidence=confidence), new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.ln(10)

    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(90, 10, get_text("pdf_original", lang), align='C')
    pdf.cell(90, 10, get_text("pdf_heatmap", lang), new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')

    try:
        pdf.image(image_path, 20, 100, 70)
        pdf.image(xai_path, 110, 100, 70)
    except Exception:
        pdf.cell(0, 10, get_text("pdf_error_images", lang), new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')

    os.makedirs(os.path.join("static", "reports"), exist_ok=True)
    filename = f"report_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    filepath = os.path.join("static", "reports", filename)
    pdf.output(filepath, 'F')

    return filepath
