import sys
import fitz
import requests
import json
import os

# Set your OpenAI API key
api_key = os.environ['OPENAI_API_KEY']

def extract_text_from_pdf(file_path):
    with fitz.open(file_path) as doc:
        text = ""
        for page in doc:
            text += page.get_text()

    return text

def ask_openai_model(model_name, pdf_file_path, question):
    # Extract text from PDF
    pdf_text = extract_text_from_pdf(pdf_file_path)

    # Compose prompt by combining PDF text and the question
    prompt = f"PDF: {pdf_text}\n\nQuestion: {question}\nAnswer:"

    # Call the OpenAI API to generate a response
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": model_name,
        "messages": [
            {
            "role": "user",
            "content": "You are an expert researcher, I will provide you some text, and ask you questions about it"
            },
            {
            "role": "user",
            "content": prompt
            }
        ],
        "temperature": float(os.environ.get('LRMATIC_TEMPERATURE',1))
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data, timeout=(3,300))
    answer = response.json()

    return answer

def main():
    # Get command-line arguments
    model_name = sys.argv[1]
    pdf_file_path = sys.argv[2]
    question = sys.argv[3]

    # Call the function to retrieve the answer
    answer = ask_openai_model(model_name, pdf_file_path, question)

    # Output the answer
    print("Answer:", answer)

if __name__ == '__main__':
    main()
