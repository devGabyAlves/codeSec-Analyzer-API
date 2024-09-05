import openai
import os
from dotenv import load_dotenv
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise EnvironmentError("OPENAI_API_KEY environment variable not set")

openai.api_key = openai_api_key

def analyze_code(file_path):
    file_size = os.path.getsize(file_path)
    max_size = 5 * 1024 * 1024  
    if file_size > max_size:
        raise ValueError("File too large. Max size is 5MB.")
    
    with open(file_path, 'r') as file:
        code = file.read()

    sanitized_code = sanitize_code(code)

    prompt = f"""You are a software security expert. I will provide you with a code snippet, and you must identify possible security vulnerabilities and suggest improvements that can be implemented.
    Additionally, for each identified vulnerability, assign a severity level according to OWASP guidelines: low, medium, high, or critical. Whenever possible, provide corrected code examples for each identified vulnerability.
    
    Here is the code:

    {sanitized_code}

    Please provide a detailed analysis of the security issues, assign a severity level to each problem, and suggest improvements, including examples of how to implement these improvements in the code.
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a software security expert."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=4000,
            temperature=0.5,
        )
        return response['choices'][0]['message']['content']

    except openai.error.OpenAIError as e:
        print(f"Error during OpenAI API call: {e}")
        return "Error: Unable to analyze the code."
    except Exception as e:
        print(f"General error: {e}")
        return "An unexpected error occurred."


def sanitize_code(code):
    sanitized_code = code.replace("password", "*****").replace("api_key", "*****")
    return sanitized_code


def generate_pdf_report(file_path, output_pdf):
    analysis_result = analyze_code(file_path)

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
        "Subtitle": styles['Heading3'],
        "Content": styles['BodyText']
    }

    for section in sections:
        if ":" in section:
            section_title, section_content = section.split(":", 1)
            story.append(Paragraph(section_title.strip(), section_styles["Title"]))
            story.append(Spacer(1, 6))

            if "Severity" in section_title:  
                severity_text = f"<b>Severity:</b> {section_content.strip()}"
                story.append(Paragraph(severity_text, section_styles["Content"]))
            else:
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

    # Generate PDF
    doc.build(story)


if __name__ == "__main__":
    file_path = os.getenv('FILE_PATH', 'sample.py')
    output_pdf = "sec_code_analyzer_report.pdf"

    generate_pdf_report(file_path, output_pdf)
