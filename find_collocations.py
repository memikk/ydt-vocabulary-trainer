
import PyPDF2

pdf_path = "vocabulary-12.pdf"
kw = "COLLOCATIONS"

try:
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        
        found = False
        for i in range(len(reader.pages)):
            text = reader.pages[i].extract_text()
            if kw in text or kw.lower() in text: # Case sensitive usually formatted uppercase in headers
                 print(f"Found '{kw}' on page {i+1}")
                 print(text[:500])
                 found = True
        
        if not found:
            print("No COLLOCATIONS header found.")

except Exception as e:
    print(f"Error: {e}")
