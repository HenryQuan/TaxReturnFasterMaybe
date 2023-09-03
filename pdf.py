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
    # 01 Jan, 20 Aug, 31 Dec
    date_regex = r'(\d{2}\s[A-Z][a-z]{2})'
    with open(output_path, 'w') as output:
        with pdfplumber.open(input_path) as pdf:
            merged_line = []
            for page in pdf.pages:
                pdf_text = page.extract_text()
                lines = pdf_text.split('\n')
                merged_line.extend(lines)
            # use iterator to get a few lines before finding a new date
            start_index = None
            for index, line in enumerate(merged_line):
                if '16 Aug' in line:
                    pass
                if re.search(date_regex, line):
                    if start_index is None:
                        start_index = index
                    if start_index != index:
                        full_line = '|'.join(merged_line[start_index:index])
                        start_index = index
                        output.write(full_line)
                        output.write('\n')

                        for keyword in KEYWORDS:
                            if keyword in full_line:
                                # this line can be extremely long, let's split it into a list
                                line_of_focus = [x for x in full_line.split('|') if keyword in x][0]
                                try:
                                    matches = re.findall(number_regex, line_of_focus)[-2:]
                                except IndexError:
                                    matches = re.findall(number_regex, line_of_focus)[-1:]
                                try:
                                    matches = matches[0]
                                except IndexError:
                                    matches = None

                                # try to find it in the full_line
                                if matches == None:
                                    try:
                                        matches = re.findall(number_regex, full_line)[-2:]
                                    except IndexError:
                                        matches = re.findall(number_regex, full_line)[-1:]
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
