from reader import read_pdf

pdf_path = "sample/pdflatex-4-pages.pdf"
content = read_pdf(pdf_path)
print(content)