import os
import re
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable

def main():
    font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    font_bold_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
    font_oblique_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf'

    pdfmetrics.registerFont(TTFont('DejaVu', font_path))
    pdfmetrics.registerFont(TTFont('DejaVu-Bold', font_bold_path))
    pdfmetrics.registerFont(TTFont('DejaVu-Oblique', font_oblique_path))

    pdf_filename = 'project/QA_QC_Reviewer_Note.pdf'
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=36, rightMargin=36,
        topMargin=36, bottomMargin=36
    )

    normal_style = ParagraphStyle(
        'NormalText',
        fontName='DejaVu',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#1f2937')
    )

    h1_style = ParagraphStyle(
        'Heading1Text',
        fontName='DejaVu-Bold',
        fontSize=15,
        leading=18,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=10, spaceAfter=6
    )

    h2_style = ParagraphStyle(
        'Heading2Text',
        fontName='DejaVu-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor('#1e3a8a'),
        spaceBefore=8, spaceAfter=4
    )

    h3_style = ParagraphStyle(
        'Heading3Text',
        fontName='DejaVu-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#2563eb'),
        spaceBefore=6, spaceAfter=2
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        fontName='DejaVu-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white
    )

    table_body_style = ParagraphStyle(
        'TableBody',
        fontName='DejaVu',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor('#1f2937')
    )

    blockquote_style = ParagraphStyle(
        'Blockquote',
        fontName='DejaVu-Oblique',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#374151'),
        leftIndent=10, rightIndent=10,
        spaceBefore=4, spaceAfter=4
    )

    def clean_text(text):
        text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
        text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
        text = re.sub(r'`(.*?)`', r'<font face="DejaVu-Bold" color="#1e40af">\1</font>', text)
        text = text.replace('&lt;br&gt;', '<br/>').replace('&lt;br/&gt;', '<br/>')
        return text

    with open('project/QA_QC_Reviewer_Note.md', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    in_table = False
    table_data = []
    story = []

    def flush_table():
        nonlocal in_table, table_data
        if table_data:
            t_cells = []
            for row_idx, row in enumerate(table_data):
                r_cells = []
                for cell in row:
                    p_style = table_header_style if row_idx == 0 else table_body_style
                    r_cells.append(Paragraph(clean_text(cell), p_style))
                t_cells.append(r_cells)
            t = Table(t_cells, repeatRows=1)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
                ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#94a3b8')),
                ('TOPPADDING', (0, 0), (-1, -1), 3),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
                ('LEFTPADDING', (0, 0), (-1, -1), 4),
                ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ]))
            story.append(t)
            story.append(Spacer(1, 6))
            in_table = False
            table_data = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            if in_table:
                flush_table()
            continue

        if stripped.startswith('|') and '|' in stripped[1:]:
            if '---' in stripped:
                continue
            in_table = True
            cells = [c.strip() for c in stripped.strip('|').split('|')]
            table_data.append(cells)
            continue
        elif in_table:
            flush_table()

        if stripped.startswith('# '):
            story.append(Paragraph(clean_text(stripped[2:]), h1_style))
        elif stripped.startswith('## '):
            story.append(Paragraph(clean_text(stripped[3:]), h2_style))
        elif stripped.startswith('### '):
            story.append(Paragraph(clean_text(stripped[4:]), h3_style))
        elif stripped.startswith('> '):
            story.append(Paragraph(clean_text(stripped[2:]), blockquote_style))
        elif stripped.startswith('---'):
            story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cbd5e1'), spaceBefore=6, spaceAfter=6))
        else:
            story.append(Paragraph(clean_text(stripped), normal_style))
            story.append(Spacer(1, 2))

    if in_table:
        flush_table()

    doc.build(story)
    print('Successfully generated project/QA_QC_Reviewer_Note.pdf')

if __name__ == '__main__':
    main()
