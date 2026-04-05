
import PyPDF2

pdf_path = "vocabulary-12.pdf"

try:
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        
        # Read last 5 pages
        start_page = max(0, num_pages - 5)
        for i in range(start_page, num_pages):
            page = reader.pages[i]
            text = page.extract_text()
            print(f"\n--- Page {i+1} ---\n")
            print(text)

except Exception as e:
    print(f"Error: {e}")
