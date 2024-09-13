# main.py
import os
from openai_api import initialize_openai_api, analyze_code
from report_generator import generate_pdf_report

def main():
    initialize_openai_api()

    file_path = os.getenv('FILE_PATH', 'sample.py')
    output_pdf = "sec_code_analyzer_report.pdf"

    analysis_result = analyze_code(file_path)
    generate_pdf_report(analysis_result, output_pdf)

    print(f"Report generated: {output_pdf}")

if __name__ == "__main__":
    main()
