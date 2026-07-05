from pypdf import PdfReader

def read_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page_number, page in enumerate(reader.pages, start=1):
        pdf_text = page.extract_text() or "[No text found on this page]"
        text += f"Page {page_number}: {pdf_text}\n\n"    
    return text