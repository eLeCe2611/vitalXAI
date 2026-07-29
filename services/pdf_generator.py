import os
from datetime import datetime

from fpdf import FPDF, XPos, YPos


class PDFReport(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 15)
        self.set_text_color(41, 128, 185) # Azul médico
        self.cell(0, 10, 'X-Ray AI Consultant - Reporte de Diagnostico', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Pagina {self.page_no()}', align='C')

def generate_medical_report(image_path, xai_path, label, confidence, model_name):
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_font('helvetica', '', 12)

    # Datos de la consulta
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(0, 10, f" Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L', fill=True)
    pdf.cell(0, 10, f" Modelo de IA Utilizado: {model_name}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L', fill=True)
    pdf.ln(10)

    # Resultado
    pdf.set_font('helvetica', 'B', 14)
    if label == "Neumonía":
        pdf.set_text_color(192, 57, 43) # Rojo
    else:
        pdf.set_text_color(39, 174, 96) # Verde

    pdf.cell(0, 10, f"DIAGNOSTICO: {label.upper()}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.set_text_color(0)
    pdf.set_font('helvetica', '', 12)
    pdf.cell(0, 10, f"Nivel de Confianza: {confidence}%", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.ln(10)

    # Imágenes
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(90, 10, 'Radiografia Original', align='C')
    pdf.cell(90, 10, 'Mapa de Calor (XAI)', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')

    # Insertar imágenes ajustando tamaño
    # (Coordenadas x, y, ancho)
    try:
        pdf.image(image_path, 20, 100, 70)
        pdf.image(xai_path, 110, 100, 70)
    except Exception as e:
        pdf.cell(0, 10, 'Error cargando imagenes', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')

    # Guardar PDF
    os.makedirs(os.path.join("static", "reports"), exist_ok=True)
    filename = f"report_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    filepath = os.path.join("static", "reports", filename)
    pdf.output(filepath, 'F')

    return filepath
