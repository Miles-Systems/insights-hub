from pypdf import PdfReader
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent
pdf_path = base_dir / "sample" / "minimal-document.pdf"

pdf_reader = PdfReader(pdf_path)

# for page_number, page in enumerate(pdf_reader.pages, start=1):
#     text = page.extract_text()
#     print(f"\n--- Page {page_number} ---")
#     print(text or "[No text found on this page]")

for page in pdf_reader.pages:
     print(page.extract_text())

# content = pdf_reader.pages[0].extract_text()
# print(content)