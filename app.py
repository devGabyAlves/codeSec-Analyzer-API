from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import openai
from flask_cors import CORS  

app = Flask(__name__)
CORS(app)  

app.config['UPLOAD_FOLDER'] = './uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024 

def initialize_openai_api():
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise EnvironmentError("OPENAI_API_KEY environment variable not set")
    openai.api_key = openai_api_key

initialize_openai_api()

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def sanitize_code(code):
    sanitized_code = code.replace("password", "*****").replace("api_key", "*****")
    return sanitized_code

def analyze_code(file_path):
    file_size = os.path.getsize(file_path)
    max_size = 5 * 1024 * 1024  # 5MB
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

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        try:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            if not os.path.exists(file_path):
                return jsonify({'error': 'File could not be saved'}), 500

            analysis_result = analyze_code(file_path)

            return jsonify({'result': analysis_result}), 200
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            print(f"Erro inesperado: {e}")
            return jsonify({'error': f'An unexpected error occurred: {e}'}), 500

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False) 
