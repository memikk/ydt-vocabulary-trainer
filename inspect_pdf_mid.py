
import PyPDF2

pdf_path = "vocabulary-12.pdf"

try:
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        
        # Read pages 10-15
        for i in range(10, 16):
            if i < len(reader.pages):
                page = reader.pages[i]
                text = page.extract_text()
                print(f"\n--- Page {i+1} ---\n")
                print(text)

except Exception as e:
    print(f"Error: {e}")
