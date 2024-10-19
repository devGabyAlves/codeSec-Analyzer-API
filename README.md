# CodeSec Analyzer API

This repository contains the backend API for **CodeSec Analyzer**, a tool designed to analyze source code for potential security vulnerabilities. It leverages the OpenAI API to scan code and return detailed reports on any discovered vulnerabilities, along with suggested improvements.

## Features

- **File Upload**: Accepts source code files in various programming languages.
- **Security Analysis**: Scans code using OpenAI's language models and identifies security vulnerabilities.
- **Severity Levels**: Assigns severity levels to vulnerabilities (low, medium, high, critical) based on OWASP guidelines.
- **Suggestions**: Provides detailed suggestions on how to fix vulnerabilities, including example code improvements.

## Technologies

- **Python**: Main programming language.
- **Flask**: Python micro-framework for building the REST API.
- **OpenAI API**: Used to analyze the code and generate security reports.

## Requirements

- **Python 3.8+**
- **OpenAI API Key**

## Installation

### Step 1: Clone the repository

```bash
git clone https://github.com/your-username/CodeSec-Analyzer-API.git
cd SecCode
```

## Step 2: Clone the repository

```bash
python3 -m venv venv
source venv/bin/activate 
```

## Step 3: Install dependencies

pip install -r requirements.txt

## Step 4: Set up environment variables

You need to set the OpenAI API key as an environment variable:
export OPENAI_API_KEY=your-openai-api-key

Alternatively, you can create a .env file in the root of the project and add your OpenAI key there:
OPENAI_API_KEY=your-openai-api-key

## Step 5: Run the server

python app.py

The API should now be running on http://localhost:5000.

## API Endpoints
## POST /analyze
Description: Uploads a source code file and returns a security analysis report.

URL: /analyze
Method: POST
Content-Type: multipart/form-data

Request Example:
curl -X POST http://localhost:5000/analyze \
  -F "file=@path_to_your_code_file.py"

Response Example:
{
  "result": "### Security Issues Identified\n\n1. **SQL Injection**: Vulnerability found in line 45. Use parameterized queries to avoid SQL injection.\n\n### Suggested Fix\n\n```python\ncursor.execute('SELECT * FROM users WHERE username = ?', (username,))\n```"
}

## Error Responses
- 400 Bad Request: Returned if the file is not found in the request or an invalid file type is uploaded.
- 500 Internal Server Error: Returned if something goes wrong during the analysis.