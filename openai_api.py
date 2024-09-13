# openai_api.py
import openai
import os

def initialize_openai_api():
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise EnvironmentError("OPENAI_API_KEY environment variable not set")

    openai.api_key = openai_api_key

def sanitize_code(code):
    sanitized_code = code.replace("password", "*****").replace("api_key", "*****")
    return sanitized_code

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
