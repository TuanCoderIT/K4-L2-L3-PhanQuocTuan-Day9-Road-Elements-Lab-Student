import os
import re
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable

def main():
    font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    font_bold_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
    font_oblique_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf'

    pdfmetrics.registerFont(TTFont('DejaVu', font_path))
    pdfmetrics.registerFont(TTFont('DejaVu-Bold', font_bold_path))
    pdfmetrics.registerFont(TTFont('DejaVu-Oblique', font_oblique_path))

    pdf_filename = 'project/Pitch_Deck_Road_Marking_Guideline.pdf'
    # Use landscape letter (11 x 8.5 inches = 792 x 612 pt)
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=landscape(letter),
        leftMargin=36, rightMargin=36,
        topMargin=30, bottomMargin=30
    )

    slide_title_style = ParagraphStyle(
        'SlideTitle',
        fontName='DejaVu-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0284c7'),
        spaceAfter=10
    )

    slide_subtitle_style = ParagraphStyle(
        'SlideSubtitle',
        fontName='DejaVu-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#38bdf8'),
        spaceAfter=6
    )

    normal_style = ParagraphStyle(
        'NormalText',
        fontName='DejaVu',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#334155')
    )

    bullet_style = ParagraphStyle(
        'BulletText',
        fontName='DejaVu',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#1e293b'),
        leftIndent=12
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        fontName='DejaVu-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    table_body_style = ParagraphStyle(
        'TableBody',
        fontName='DejaVu',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor('#1e293b')
    )

    blockquote_style = ParagraphStyle(
        'Blockquote',
        fontName='DejaVu-Oblique',
        fontSize=9,
        leading=12.5,
        textColor=colors.HexColor('#0369a1'),
        leftIndent=10, rightIndent=10,
        spaceBefore=6, spaceAfter=6
    )

    def clean_text(text):
        text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
        text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
        text = re.sub(r'`(.*?)`', r'<font face="DejaVu-Bold" color="#0369a1">\1</font>', text)
        text = text.replace('&lt;br&gt;', '<br/>').replace('&lt;br/&gt;', '<br/>')
        return text

    with open('project/pitch_deck_presentation.md', 'r', encoding='utf-8') as f:
        content = f.read()

    slides = content.split('---')
    story = []

    for idx, raw_slide in enumerate(slides):
        lines = [line.strip() for line in raw_slide.splitlines() if line.strip()]
        if not lines:
            continue
        # Skip YAML frontmatter slide
        if any(line.startswith('marp:') or line.startswith('theme:') for line in lines):
            continue

        in_table = False
        table_data = []

        def flush_table():
            nonlocal in_table, table_data
            if table_data:
                t_cells = []
                for r_idx, row in enumerate(table_data):
                    r_cells = []
                    for cell in row:
                        p_style = table_header_style if r_idx == 0 else table_body_style
                        r_cells.append(Paragraph(clean_text(cell), p_style))
                    t_cells.append(r_cells)
                t = Table(t_cells, repeatRows=1)
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0284c7')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
                    ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#0284c7')),
                    ('TOPPADDING', (0, 0), (-1, -1), 4),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                    ('LEFTPADDING', (0, 0), (-1, -1), 5),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 5),
                ]))
                story.append(t)
                story.append(Spacer(1, 8))
                in_table = False
                table_data = []

        for line in lines:
            if line.startswith('|') and '|' in line[1:]:
                if '---' in line:
                    continue
                in_table = True
                cells = [c.strip() for c in line.strip('|').split('|')]
                table_data.append(cells)
                continue
            elif in_table:
                flush_table()

            if line.startswith('# '):
                story.append(Paragraph(clean_text(line[2:]), slide_title_style))
            elif line.startswith('## '):
                story.append(Paragraph(clean_text(line[3:]), slide_subtitle_style))
            elif line.startswith('- ') or line.startswith('* '):
                story.append(Paragraph('• ' + clean_text(line[2:]), bullet_style))
                story.append(Spacer(1, 2))
            elif line.startswith('> '):
                story.append(Paragraph(clean_text(line[2:]), blockquote_style))
            elif line.startswith('```'):
                continue
            else:
                story.append(Paragraph(clean_text(line), normal_style))
                story.append(Spacer(1, 4))

        if in_table:
            flush_table()

        story.append(PageBreak())

    doc.build(story)
    print('Successfully generated project/Pitch_Deck_Road_Marking_Guideline.pdf')

if __name__ == '__main__':
    main()
