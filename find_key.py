
import PyPDF2

pdf_path = "vocabulary-12.pdf"
keywords = ["Answer Key", "Cevap Anahtarı", "ANSWERS", "DOĞRU SEÇENEKLER", "YANITLAR"]

try:
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        
        found = False
        for i in range(len(reader.pages)):
            text = reader.pages[i].extract_text()
            for kw in keywords:
                if kw in text or kw.upper() in text:
                    print(f"Found '{kw}' on page {i+1}")
                    print(text[:500]) # Print context
                    found = True
        
        if not found:
            print("No Answer Key keywords found.")

except Exception as e:
    print(f"Error: {e}")
