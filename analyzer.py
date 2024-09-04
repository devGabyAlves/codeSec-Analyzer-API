import openai
import os
from dotenv import load_dotenv
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, ListFlowable, ListItem

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def analisar_codigo(caminho_arquivo):
    with open(caminho_arquivo, 'r') as file:
        codigo = file.read()
    
    prompt = f"""Você é um especialista em segurança de software. Vou te fornecer um trecho de código, e você deve identificar possíveis vulnerabilidades de segurança e sugerir melhorias que podem ser implementadas. 
    Aqui está o código:

    {codigo}

    Por favor, forneça uma análise detalhada dos problemas de segurança, das possíveis melhorias, e exemplos de como implementar essas melhorias no código em questão:
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  
        messages=[
            {"role": "system", "content": "Você é um especialista em segurança de software."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=2000,  
        temperature=0.5,
    )

    return response['choices'][0]['message']['content']

def gerar_relatorio_pdf(caminho_arquivo, output_pdf):
    resultado_analise = analisar_codigo(caminho_arquivo)
    
    doc = SimpleDocTemplate(output_pdf, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    logo_path = "assets/logo.png"
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

    sections = resultado_analise.split("\n\n")
    section_styles = {
        "Title": styles['Heading2'],
        "Subtitle": styles['Heading3'],
        "Content": styles['BodyText']
    }
    
    for section in sections:
        if ":" in section:
            section_title, section_content = section.split(":", 1)
            story.append(Paragraph(section_title.strip(), section_styles["Title"]))
            story.append(Spacer(1, 6))

            if "\n" in section_content.strip():
                items = section_content.strip().split("\n")
                list_items = [ListItem(Paragraph(item.strip(), section_styles["Content"])) for item in items]
                story.append(ListFlowable(list_items, bulletType='bullet'))
            else:
                story.append(Paragraph(section_content.strip(), section_styles["Content"]))
            
            story.append(Spacer(1, 12))
        else:
            story.append(Paragraph(section.strip(), section_styles["Content"]))
            story.append(Spacer(1, 12))

    doc.build(story)


if __name__ == "__main__":
    caminho_arquivo = "sample.py"
    output_pdf = "relatorio_sec_code_analyzer.pdf"

    codigo = open(caminho_arquivo).read()
    analise = analisar_codigo(caminho_arquivo)
    
    gerar_relatorio_pdf(caminho_arquivo, output_pdf)
    