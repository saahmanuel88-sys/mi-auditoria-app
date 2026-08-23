import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import io

# Configuración de la página
st.set_page_config(page_title="Auditoría de Seguridad", page_icon="🛡️")

st.title("🛡️ Generador de Reporte de Auditoría")
st.write("Introduce los datos del análisis para generar el informe en PDF.")

# Formulario de entrada de datos
cliente = st.text_input("Nombre del Cliente / Empresa", "Empresa Cliente S.A.")
evaluador = st.text_input("Nombre del Auditor", "Ing. Juan Pérez")

st.subheader("Resultados de Puertos")
p80 = st.selectbox("Puerto 80 (HTTP)", ["Abierto (Alto Riesgo)", "Cerrado (Seguro)"])
p21 = st.selectbox("Puerto 21 (FTP)", ["Abierto (Alto Riesgo)", "Cerrado (Seguro)"])
p22 = st.selectbox("Puerto 22 (SSH)", ["Abierto (Riesgo Medio)", "Cerrado (Seguro)"])

def generar_pdf():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=18, textColor=colors.HexColor('#1A365D'), spaceAfter=12)
    normal_style = styles['Normal']
    
    story.append(Paragraph("<b>REPORTE DE AUDITORÍA DE SEGURIDAD</b>", title_style))
    story.append(Paragraph(f"<b>Cliente:</b> {cliente} | <b>Auditor:</b> {evaluador}", normal_style))
    story.append(Spacer(1, 15))
    
    # Procesar hallazgos
    hallazgos = [
        ["Puerto", "Servicio", "Estado", "Nivel de Riesgo"],
        ["80", "HTTP", p80.split()[0], "Alto" if "Alto" in p80 else "Bajo"],
        ["21", "FTP", p21.split()[0], "Alto" if "Alto" in p21 else "Bajo"],
        ["22", "SSH", p22.split()[0], "Medio" if "Medio" in p22 else "Bajo"]
    ]
    
    t = Table(hallazgos, colWidths=[60, 100, 150, 150])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1A365D')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
    ]))
    
    story.append(t)
    doc.build(story)
    buffer.seek(0)
    return buffer

if st.button("📄 Generar Informe PDF"):
    pdf = generar_pdf()
    st.download_button(
        label="⬇️ Descargar PDF",
        data=pdf,
        file_name=f"Auditoria_{cliente.replace(' ', '_')}.pdf",
        mime="application/pdf"
    )
