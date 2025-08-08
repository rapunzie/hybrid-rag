import json
from pathlib import Path
from PyPDF2 import PdfReader

def read_pdf_text(pdf_path):
    reader = PdfReader(pdf_path)
    text = ''
    for page in reader.pages:
        text += page.extract_text() + '\n'
    return text.strip()

def main():
    base_dir = Path(__file__).resolve().parent / "item8-appl"
    pdf_files = [
        ("balance_sheets.pdf", "Balance Sheet"),
        ("cash_flows.pdf", "Cash Flow Statement"),
        ("statements_op.pdf", "Statements of Operations")
    ]

    merged_items_path = base_dir / "merged_items.jsonl"

    with open(merged_items_path, "a", encoding="utf-8") as out_file:
        for filename, section in pdf_files:
            file_path = base_dir / filename
            print(f"Processing {file_path.name}...")
            try:
                text = read_pdf_text(file_path)
                data = {
                    "section": section,
                    "source": file_path.name,
                    "content": text
                }
                out_file.write(json.dumps(data) + "\n")
            except Exception as e:
                print(f"Failed to process {filename}: {e}")

    print(f"\nDone merging PDF texts into {merged_items_path.name}")

if __name__ == "__main__":
    main()
