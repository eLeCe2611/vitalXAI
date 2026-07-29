import csv
import datetime
import json
import os

from fastapi.responses import FileResponse, JSONResponse
from fpdf import FPDF, XPos, YPos


class MedicalReport(FPDF):
    def header(self):
        self.set_fill_color(30, 41, 59)
        self.rect(0, 0, 210, 35, "F")
        self.set_text_color(255, 255, 255)
        self.set_font("helvetica", "B", 16)
        self.cell(0, 10, "X-RAY CONSULTANT AI - MEDICAL REPORT", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="L")
        self.set_font("helvetica", "", 10)
        self.cell(0, 5, "Protocolo MLOps: Deep Learning para Detecci\u00f3n de Neumon\u00eda", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="L")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"P\u00e1gina {self.page_no()} | Informe generado autom\u00e1ticamente por X-Ray Consultant Platform", align="C")

    def section_title(self, title):
        self.ln(5)
        self.set_fill_color(241, 245, 249)
        self.set_text_color(30, 41, 59)
        self.set_font("helvetica", "B", 12)
        self.cell(0, 10, f"  {title}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, fill=True)
        self.ln(3)


async def generate_pdf_report(session_id: str):
    session_dir = f"training_results/{session_id}"
    if not os.path.exists(session_dir):
        return JSONResponse(status_code=404, content={"message": "Sesi\u00f3n no encontrada"})

    pdf = MedicalReport()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    pdf.section_title("1. CONFIGURACI\u00d3N DEL SISTEMA Y PAR\u00c1METROS")
    pdf.set_font("helvetica", "", 10)
    pdf.set_text_color(50, 50, 50)

    config_path = os.path.join(session_dir, "config.json")
    if os.path.exists(config_path):
        with open(config_path, encoding="utf-8") as f:
            cfg = json.load(f)
        data = [
            ["ID Sesi\u00f3n", session_id],
            ["Fecha", datetime.datetime.now().strftime("%d/%m/%Y %H:%M")],
            ["Dataset", cfg.get("dataset_path", "-")],
            ["Modelos", ", ".join(cfg.get("models", []))],
            ["Hiperpar\u00e1metros", f"Epochs: {cfg.get('epochs', '-')} | Batch: {cfg.get('batch_size', '-')} | LR: {cfg.get('learning_rate', '-')}"],
        ]
        for row in data:
            pdf.set_font("helvetica", "B", 9)
            pdf.cell(40, 7, f"{row[0]}:", border="B")
            pdf.set_font("helvetica", "", 9)
            pdf.cell(0, 7, f" {row[1]}", border="B", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    ranking_csv = os.path.join(session_dir, "session_ranking.csv")
    if os.path.exists(ranking_csv):
        pdf.section_title("2. RENDIMIENTO GLOBAL (K-FOLD CROSS-VALIDATION)")
        pdf.set_fill_color(71, 85, 105)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("helvetica", "B", 9)
        pdf.cell(80, 8, " Arquitectura de Modelo", border=1, fill=True)
        pdf.cell(50, 8, " Media AUC", border=1, fill=True)
        pdf.cell(50, 8, " Desviaci\u00f3n Est\u00e1ndar", border=1, fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_text_color(30, 41, 59)
        pdf.set_font("helvetica", "", 9)
        with open(ranking_csv, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                fill = i % 2 == 0
                if fill:
                    pdf.set_fill_color(248, 250, 252)
                pdf.cell(80, 8, f" {row['Model']}", border=1, fill=fill)
                pdf.cell(50, 8, f" {row['Mean']}", border=1, fill=fill)
                pdf.cell(50, 8, f" {row['Std']}", border=1, fill=fill, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    wilcoxon_img = os.path.join(session_dir, "wilcoxon_heatmap.png")
    if os.path.exists(wilcoxon_img):
        pdf.ln(5)
        pdf.set_font("helvetica", "B", 10)
        pdf.cell(0, 10, "Matriz de Significancia Estad\u00edstica (P-Values):", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.image(wilcoxon_img, x=35, w=140)

    ext_dir = os.path.join(session_dir, "external_validation")
    if os.path.exists(ext_dir):
        pdf.add_page()
        pdf.section_title("3. VALIDACI\u00d3N EXTERNA (DATASET INDEPENDIENTE)")
        ext_csv = os.path.join(ext_dir, "external_validation_metrics.csv")
        if os.path.exists(ext_csv):
            pdf.set_font("helvetica", "B", 9)
            pdf.cell(60, 8, " Modelo", border=1)
            pdf.cell(40, 8, " Accuracy", border=1)
            pdf.cell(40, 8, " F1-Score", border=1)
            pdf.cell(40, 8, " AUC", border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_font("helvetica", "", 9)
            with open(ext_csv, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    pdf.cell(60, 7, row["Model"], border=1)
                    pdf.cell(40, 7, row["Accuracy"], border=1)
                    pdf.cell(40, 7, row["F1-score"], border=1)
                    pdf.cell(40, 7, row["AUC"], border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        roc_img = os.path.join(ext_dir, "roc_external_validation.png")
        delong_img = os.path.join(ext_dir, "delong_heatmap.png")
        if os.path.exists(roc_img):
            pdf.ln(5)
            pdf.image(roc_img, x=10, w=90)
            if os.path.exists(delong_img):
                pdf.image(delong_img, x=110, y=pdf.get_y(), w=90)
            pdf.ln(70)

    for model_name in os.listdir(session_dir):
        m_path = os.path.join(session_dir, model_name)
        if os.path.isdir(m_path) and model_name != "external_validation":
            pdf.add_page()
            pdf.section_title(f"DETALLE T\u00c9CNICO: {model_name}")
            xai_cuanti = os.path.join(m_path, "xai_metrics_comparison.csv")
            if os.path.exists(xai_cuanti):
                pdf.set_font("helvetica", "B", 10)
                pdf.cell(0, 8, "M\u00e9tricas de Fidelidad XAI (Calculadas sobre 5 muestras):", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                pdf.set_font("helvetica", "", 8)
                with open(xai_cuanti, encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    headers = reader.fieldnames
                    col_width = 190 / len(headers)
                    for h in headers:
                        pdf.cell(col_width, 7, h, border=1, fill=True)
                    pdf.ln()
                    for row in reader:
                        for h in headers:
                            pdf.cell(col_width, 7, row[h], border=1)
                        pdf.ln()
            pdf.ln(5)
            pdf.set_font("helvetica", "B", 10)
            pdf.cell(0, 8, "Mapas de Calor de Interpretabilidad Visual:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            xai_imgs = sorted([f for f in os.listdir(m_path) if f.startswith("xai_example_") and f.endswith(".png")])
            for i in range(0, len(xai_imgs), 2):
                img1 = os.path.join(m_path, xai_imgs[i])
                pdf.image(img1, x=10, w=90)
                if i + 1 < len(xai_imgs):
                    img2 = os.path.join(m_path, xai_imgs[i + 1])
                    pdf.image(img2, x=105, y=pdf.get_y(), w=90)
                pdf.ln(35)

    pdf_output_path = os.path.join(session_dir, f"Informe_Completo_{session_id}.pdf")
    pdf.output(pdf_output_path)
    return FileResponse(pdf_output_path, filename=f"Reporte_MLOps_{session_id}.pdf")
