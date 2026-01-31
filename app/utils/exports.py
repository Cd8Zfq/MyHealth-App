from io import BytesIO
from datetime import datetime
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_measurements_pdf(measurements, user_email):
    """
    Génère un PDF avec l'historique des mesures.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    elements.append(Paragraph('Historique de Santé', styles['Title']))
    elements.append(Paragraph(f'Patient: {user_email}', styles['Normal']))
    elements.append(Paragraph(f'Date: {datetime.now().strftime("%d/%m/%Y")}', styles['Normal']))
    
    data = [['Date', 'Type', 'Valeur 1', 'Valeur 2', 'Unité']]
    for m in measurements:
        val2 = str(m.value2) if m.value2 else '-'
        data.append([
            m.date.strftime('%d/%m/%Y %H:%M'),
            m.type.capitalize(),
            str(m.value1),
            val2,
            m.unit
        ])
        
    t = Table(data)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(t)
    
    doc.build(elements)
    buffer.seek(0)
    return buffer

def generate_measurements_excel(measurements):
    """
    Génère un fichier Excel avec l'historique des mesures.
    """
    data = []
    for m in measurements:
        data.append({
            'Date': m.date.strftime('%Y-%m-%d %H:%M:%S'),
            'Type': m.type,
            'Valeur 1': m.value1,
            'Valeur 2': m.value2,
            'Unité': m.unit,
            'Notes': m.notes
        })
        
    df = pd.DataFrame(data)
    
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Mesures')
        
    output.seek(0)
    return output
