import pdfplumber
import os
import re

def pdf2txt(pdf_path: str):
    input_path = os.path.join(os.getcwd(), f'documents/{pdf_path}')
    output_path = os.path.join(os.getcwd(), f'processed/{pdf_path}.txt')
    # find numbers like 1.0, 2,312,00, 100.00
    number_regex = r'(\d+\.\d+)'
    with open(output_path, 'w') as output:
        with pdfplumber.open(input_path) as pdf:
            for page in pdf.pages:
                pdf_text = page.extract_text()
                for line in pdf_text.split('\n'):
                    if re.search(number_regex, line):
                        output.write(line + '\n')
                    

def pdfs2txt(pdf_paths: list[str]):
    for pdf_path in pdf_paths:
        pdf2txt(pdf_path)

def documentsInFolder(folder: str):
    documents = os.listdir(os.path.join(os.getcwd(), folder))
    documents = [document for document in documents if not document.startswith('.')]
    return documents

if __name__ == '__main__':
    pdfs2txt(documentsInFolder('documents'))
