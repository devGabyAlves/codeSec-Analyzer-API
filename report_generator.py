# report_generator.py
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
import os

def generate_pdf_report(analysis_result, output_pdf):
    doc = SimpleDocTemplate(output_pdf, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    logo_path = os.getenv('LOGO_PATH', 'assets/logo.png')
    title = "SecCode Analyzer"

    if os.path.exists(logo_path):
        img = Image(logo_path, width=100, height=100)
        img.hAlign = 'CENTER'
        story.append(img)

    title_style = styles['Title']
    title_style.alignment = TA_CENTER
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 24))

    analysis_title = "Analysis Results"
    analysis_title_style = styles['Heading1']
    story.append(Paragraph(analysis_title, analysis_title_style))
    story.append(Spacer(1, 12))

    sections = analysis_result.split("\n\n")
    section_styles = {
        "Title": styles['Heading2'],
        "Content": styles['BodyText']
    }

    for section in sections:
        if ":" in section:
            section_title, section_content = section.split(":", 1)
            story.append(Paragraph(section_title.strip(), section_styles["Title"]))
            story.append(Spacer(1, 6))

            if "\n" in section_content.strip():
                items = section_content.strip().split("\n")
                for item in items:
                    story.append(Paragraph(item.strip(), section_styles["Content"]))
                    story.append(Spacer(1, 6))  
            else:
                story.append(Paragraph(section_content.strip(), section_styles["Content"]))
            
            story.append(Spacer(1, 12))
        else:
            story.append(Paragraph(section.strip(), section_styles["Content"]))
            story.append(Spacer(1, 12))

    doc.build(story)
