import openai
import os
from dotenv import load_dotenv
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Preformatted, PageBreak, Frame, PageTemplate
from reportlab.lib.utils import ImageReader

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

def gerar_relatorio_com_logo(analise, codigo, caminho_relatorio, logo_path):
    doc = SimpleDocTemplate(caminho_relatorio, pagesize=A4)

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Title'],
        fontSize=28,
        textColor=colors.HexColor("#90fff9"),
        spaceAfter=14,
        alignment=1, 
    )

    company_style = ParagraphStyle(
        'CompanyStyle',
        parent=styles['Heading1'],
        fontSize=22,
        textColor=colors.HexColor("#0066CC"), 
        spaceAfter=12,
        alignment=1, 
    )

    date_style = ParagraphStyle(
        'DateStyle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor("#333333"),
        alignment=1, 
    )

    def add_background(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(colors.HexColor("#b2b7b6")) 
        canvas.rect(0, 0, A4[0], A4[1], stroke=0, fill=1)
        canvas.restoreState()

    story = []

    story.append(Spacer(1, 2 * inch))

    logo = Image(logo_path)
    logo.drawHeight = 1.8 * inch
    logo.drawWidth = 1.8 * inch
    logo.hAlign = 'CENTER'
    story.append(logo)
    
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph("Relatório de Análise de Segurança", title_style))
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph("SecCode Analyzer", company_style))
    
    story.append(Spacer(1, 6 * inch))
    story.append(Paragraph("Data: 2024-08-30", date_style))
    story.append(PageBreak())

    story.append(Paragraph("Introdução", title_style))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("Este relatório fornece uma análise de segurança detalhada do código fornecido, identificando vulnerabilidades potenciais e sugerindo melhorias.", styles['BodyText']))
    story.append(Spacer(1, 0.3 * inch))

    story.append(Paragraph("Código Analisado", title_style))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Preformatted(codigo, style=styles['Code']))
    story.append(PageBreak())

    story.append(Paragraph("Análise de Segurança", title_style))
    story.append(Spacer(1, 0.2 * inch))
    analise_formatada = analise.split('\n\n')
    
    for paragrafo in analise_formatada:
        if paragrafo.strip().startswith('Linha'):
            story.append(Paragraph(paragrafo, styles['BodyText']))
            story.append(Spacer(1, 0.2 * inch))
        elif paragrafo.strip().startswith('Sugestão:'):
            story.append(Paragraph("Sugestão de Melhoria", styles['Heading2']))
            story.append(Spacer(1, 0.1 * inch))
            story.append(Preformatted(paragrafo.replace("Sugestão:", "").strip(), style=styles['Code']))
            story.append(Spacer(1, 0.3 * inch))
        else:
            story.append(Preformatted(paragrafo, style=styles['Code']))
            story.append(Spacer(1, 0.3 * inch))

    story.append(PageBreak())
    story.append(Paragraph("Conclusão", title_style))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("A análise revelou várias áreas que podem ser melhoradas para garantir a segurança do código. As sugestões fornecidas devem ser implementadas para mitigar os riscos identificados.", styles['BodyText']))
    
    frame = Frame(
        doc.leftMargin, doc.bottomMargin,
        doc.width, doc.height,
        id='normal'
    )

    template = PageTemplate(id='template_com_frame', frames=[frame], onPage=add_background)

    doc.addPageTemplates([template])

    doc.build(story)

if __name__ == "__main__":
    caminho_arquivo = "sample.py"
    caminho_relatorio = "relatorio_seguranca_com_logo_e_fundo_estilizado.pdf"
    logo_path = "assets/SecCode.webp"  
    
    codigo = open(caminho_arquivo).read()
    analise = analisar_codigo(caminho_arquivo)
    
    gerar_relatorio_com_logo(analise, codigo, caminho_relatorio, logo_path)
    
    print(f"Relatório gerado com sucesso: {caminho_relatorio}")