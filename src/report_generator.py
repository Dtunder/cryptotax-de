import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_pdf(tax_events: list[dict], tax_year: int, output_path: str) -> str:
    """
    Generates a German-language PDF report for the given tax_events.
    Calculates total taxable gain, estimated tax @25% + Soli (5.5%), and adds an Anlage SO reference.
    Returns the output path.
    """
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    title_style = styles['Heading1']
    elements.append(Paragraph(f"Kryptowährungen Steuerbericht (FIFO) - {tax_year}", title_style))
    elements.append(Spacer(1, 20))

    # Calculate totals
    total_taxable_gain = sum(event['gain_eur'] for event in tax_events if event['taxable'])
    total_tax_free_gain = sum(event['gain_eur'] for event in tax_events if not event['taxable'])

    # 25% Abgeltungssteuer + 5.5% Solidaritätszuschlag (on the tax amount) = 26.375%
    estimated_tax = total_taxable_gain * 0.26375 if total_taxable_gain > 0 else 0

    # Summary
    elements.append(Paragraph("<b>Zusammenfassung:</b>", styles['Normal']))
    elements.append(Paragraph(f"Gesamter steuerpflichtiger Gewinn: {total_taxable_gain:.2f} EUR", styles['Normal']))
    elements.append(Paragraph(f"Gesamter steuerfreier Gewinn (>365 Tage): {total_tax_free_gain:.2f} EUR", styles['Normal']))
    elements.append(Paragraph(f"Geschätzte Steuer (25% + Soli): {estimated_tax:.2f} EUR", styles['Normal']))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("<i>Referenz: Anlage SO (Sonstige Einkünfte) gem. § 23 EStG</i>", styles['Normal']))
    elements.append(Spacer(1, 20))

    # Table of Events
    data = [["Datum", "Asset", "Menge", "Kaufpreis\n(EUR)", "Verkaufspreis\n(EUR)", "Gewinn\n(EUR)", "Tage", "Steuerpflichtig"]]

    for e in tax_events:
        data.append([
            e['sell_date'],
            e['asset'],
            f"{e['amount']:.4f}",
            f"{e['buy_price_eur']:.2f}",
            f"{e['sell_price_eur']:.2f}",
            f"{e['gain_eur']:.2f}",
            str(e['holding_days']),
            "Ja" if e['taxable'] else "Nein"
        ])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
    ]))

    elements.append(table)
    doc.build(elements)

    return output_path
