import sys
import PyPDF2
import openai

# Set your OpenAI API key
openai.api_key = 'YOUR_OPENAI_API_KEY'

def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        num_pages = reader.numPages
        text = ""

        for page in range(num_pages):
            page_obj = reader.getPage(page)
            text += page_obj.extractText()

    return text

def ask_openai_model(model_name, pdf_file_path, question):
    # Extract text from PDF
    pdf_text = extract_text_from_pdf(pdf_file_path)

    # Compose prompt by combining PDF text and the question
    prompt = f"PDF: {pdf_text}\n\nQuestion: {question}\nAnswer:"

    # Call the OpenAI API to generate a response
    response = openai.Completion.create(
        engine=model_name,
        prompt=prompt,
        max_tokens=100,
        temperature=0.7,
        n=1,
        stop=None,
        echo=True
    )

    # Extract the generated answer from the response
    answer = response.choices[0].text.strip()

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
