
import PyPDF2

pdf_path = "vocabulary-12.pdf"

try:
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        # Read page 9 (index 8)
        page = reader.pages[8]
        text = page.extract_text()
        print(f"\n--- Page 9 ---\n")
        print(text)

except Exception as e:
    print(f"Error: {e}")
