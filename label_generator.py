import os
from datetime import datetime
from reportlab.lib.pagesizes import A6
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT


def generate_label(order_item, output_dir):
    """
    Genera una viñeta (etiqueta PDF) para un ítem de orden.
    Retorna la ruta del archivo PDF generado.
    """
    order = order_item.order
    prescription = order.prescription
    patient = prescription.patient
    medication = order_item.medication

    filename = f"vineta_orden{order.id}_item{order_item.id}.pdf"
    filepath = os.path.join(output_dir, filename)

    doc = SimpleDocTemplate(
        filepath,
        pagesize=A6,
        rightMargin=10 * mm,
        leftMargin=10 * mm,
        topMargin=8 * mm,
        bottomMargin=8 * mm
    )

    styles = getSampleStyleSheet()

    # Estilos personalizados
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=14,
        textColor=colors.HexColor('#003d82'),
        alignment=TA_CENTER,
        spaceAfter=2,
        fontName='Helvetica-Bold'
    )

    subtitle_style = ParagraphStyle(
        'SubtitleStyle',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#003d82'),
        alignment=TA_CENTER,
        spaceAfter=4,
        fontName='Helvetica'
    )

    label_style = ParagraphStyle(
        'LabelStyle',
        parent=styles['Normal'],
        fontSize=7,
        textColor=colors.grey,
        alignment=TA_LEFT,
        fontName='Helvetica'
    )

    value_style = ParagraphStyle(
        'ValueStyle',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.black,
        alignment=TA_LEFT,
        spaceAfter=3,
        fontName='Helvetica-Bold'
    )

    med_style = ParagraphStyle(
        'MedStyle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#003d82'),
        alignment=TA_LEFT,
        spaceAfter=2,
        fontName='Helvetica-Bold'
    )

    info_style = ParagraphStyle(
        'InfoStyle',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.black,
        alignment=TA_LEFT,
        spaceAfter=2,
        fontName='Helvetica'
    )

    footer_style = ParagraphStyle(
        'FooterStyle',
        parent=styles['Normal'],
        fontSize=7,
        textColor=colors.grey,
        alignment=TA_CENTER,
        fontName='Helvetica'
    )

    story = []

    # Logo / Encabezado
    story.append(Paragraph("🏥 Bitfarma", title_style))
    story.append(Paragraph("Sistema de Gestion Farmaceutico", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#003d82')))
    story.append(Spacer(1, 3 * mm))

    # Datos del paciente
    story.append(Paragraph("PACIENTE", label_style))
    story.append(Paragraph(patient.nombre_completo, value_style))

    story.append(Paragraph("Identificacion", label_style))
    nss = patient.num_seguro_social if patient.num_seguro_social else 'N/A'
    story.append(Paragraph(nss, value_style))

    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.lightgrey))
    story.append(Spacer(1, 2 * mm))

    # Medicamento
    story.append(Paragraph("MEDICAMENTO", label_style))
    med_full = f"{medication.nombre}"
    story.append(Paragraph(med_full, med_style))

    conc_unit = f"{medication.concentracion} {medication.unidad}"
    story.append(Paragraph(conc_unit, info_style))

    story.append(Spacer(1, 2 * mm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.lightgrey))
    story.append(Spacer(1, 2 * mm))

    # Indicaciones
    data = [
        [Paragraph("Cantidad:", label_style), Paragraph(f"{order_item.cantidad} {medication.unidad}", info_style)],
        [Paragraph("Dosis:", label_style), Paragraph(order_item.dosis_indicada, info_style)],
        [Paragraph("Frecuencia:", label_style), Paragraph(order_item.frecuencia, info_style)],
        [Paragraph("Duración:", label_style), Paragraph(order_item.duracion, info_style)],
    ]

    table = Table(data, colWidths=[25 * mm, None])
    table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('TOPPADDING', (0, 0), (-1, -1), 1),
    ]))
    story.append(table)

    story.append(Spacer(1, 2 * mm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.lightgrey))
    story.append(Spacer(1, 2 * mm))

    # Pie de página
    fecha_str = datetime.utcnow().strftime('%d/%m/%Y %H:%M')
    story.append(Paragraph(f"Orden N°: {order.id:05d}  |  Ítem: {order_item.id}", footer_style))
    story.append(Paragraph(f"Generado: {fecha_str}", footer_style))
    story.append(Spacer(1, 1 * mm))
    story.append(Paragraph("Conserve este recibo. Válido solo para esta dispensación.", footer_style))

    doc.build(story)
    return filepath
