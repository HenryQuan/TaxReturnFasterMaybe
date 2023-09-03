import pdfplumber
import os
import re

KEYWORDS_DICT = {}

# add a keywords.txt file to config/
with open(os.path.join(os.getcwd(), 'config/keywords.txt')) as keywords:
    KEYWORDS = keywords.read().split('\n')

def pdf2txt(pdf_path: str):
    input_path = os.path.join(os.getcwd(), f'documents/{pdf_path}')
    output_path = os.path.join(os.getcwd(), f'processed/{pdf_path}.txt')
    # find numbers like 1.0, 2,312,00, 100.00
    number_regex = r'(\d+\.\d+)'
    with open(output_path, 'w') as output:
        with pdfplumber.open(input_path) as pdf:
            for page in pdf.pages:
                pdf_text = page.extract_text()
                lines = pdf_text.split('\n')
                for line in lines:
                    if re.search(number_regex, line):
                        output.write(line + '\n')
                    for keyword in KEYWORDS:
                        if keyword in line:
                            # try getting the last two matches with the number regex
                            # if it fails, get the last match
                            try:
                                matches = re.findall(number_regex, line)[-2:]
                            except IndexError:
                                matches = re.findall(number_regex, line)[-1:]
                            try:
                                matches = matches[0]
                            except IndexError:
                                continue

                            if keyword not in KEYWORDS_DICT:
                                KEYWORDS_DICT[keyword] = []
                            KEYWORDS_DICT[keyword].append(matches)     

def pdfs2txt(pdf_paths: list[str]):
    for pdf_path in pdf_paths:
        pdf2txt(pdf_path)

def documentsInFolder(folder: str):
    documents = os.listdir(os.path.join(os.getcwd(), folder))
    documents = [document for document in documents if not document.startswith('.')]
    return documents

if __name__ == '__main__':
    pdfs2txt(documentsInFolder('documents'))
    for key in KEYWORDS_DICT:
        print(key)
        for value in KEYWORDS_DICT[key]:
            print(value)
