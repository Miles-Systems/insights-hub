import sys
from reader import read_pdf

if len(sys.argv) < 2:
    raise SystemExit("Please provide a PDF path, for example: python app/main.py sample/[file_name].pdf")

content = read_pdf(sys.argv[1])
print(content)