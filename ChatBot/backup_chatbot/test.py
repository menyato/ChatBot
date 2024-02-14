import PyPDF2

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text

pdf_path = "saudi_law.pdf"
saudi_law_text = extract_text_from_pdf(pdf_path)

# Print a snippet of the extracted text for verification
print(saudi_law_text[:500])  # Print the first 500 characters as a snippet
