import sys

from app.reader import read_pdf

if len(sys.argv) < 2:
    raise SystemExit(
        "Please provide a PDF path, for example: python app/main.py sample/minimal-document.pdf"
    )

try:
    content = read_pdf(sys.argv[1])
except FileNotFoundError as exc:
    raise SystemExit(f"Error: {exc}") from exc
except ValueError as exc:
    raise SystemExit(f"Error: {exc}") from exc

print(content)