
import PyPDF2

pdf_path = "vocabulary-12.pdf"

try:
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        print(f"Total Pages: {num_pages}")
        
        # Read first 3 pages
        for i in range(min(3, num_pages)):
            page = reader.pages[i]
            text = page.extract_text()
            print(f"\n--- Page {i+1} ---\n")
            print(text[:1000]) # Print first 1000 chars

except Exception as e:
    print(f"Error: {e}")
