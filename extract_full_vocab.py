
import PyPDF2
import re

pdf_path = "vocabulary-12.pdf"
output_path = "vocab_full_raw.txt"

def clean_word(word):
    # Remove leading/trailing non-alpha chars
    word = re.sub(r'^[^a-zA-Z]+', '', word)
    word = re.sub(r'[^a-zA-Z]+$', '', word)
    return word.strip().lower()

def is_valid_word(word):
    if len(word) < 2: return False
    if re.search(r'\d', word): return False
    if word in ["the", "and", "but", "for", "with", "this", "that", "from", "into", "onto"]: return False
    # Filter out single letters that aren't 'a' or 'i' (though even those are usually noise in this context)
    if len(word) == 1 and word not in ['a', 'i']: return False
    return True

extracted_words = set()

try:
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        print(f"Scanning {num_pages} pages...")

        for i in range(num_pages):
            text = reader.pages[i].extract_text()
            if not text: continue
            
            # 1. Target Lists often have just words on lines, or multiple columns
            lines = text.split('\n')
            for line in lines:
                # Basic cleaning
                line = line.strip()
                if not line: continue
                
                # Check for "A) word" pattern specifically
                # Matches: "A) word", "A)word", "A. word"
                matches = re.findall(r'(?:^|\s)[A-E]\)\s*([a-zA-Z\s]+?)(?=\s+[A-E]\)|\s*$)', line)
                if matches:
                    for m in matches:
                        w = clean_word(m)
                        if is_valid_word(w): extracted_words.add(w)
                
                # If page > 117 (Target List area), assume words are listed directly
                if i >= 117:
                    # Exclude headers
                    if "VERBS" in line or "PHRASAL" in line or "VOCABULARY" in line: continue
                    if ".." in line: continue # TOC
                    
                    # Split by multiple spaces to handle columns (e.g. "word1    word2")
                    parts = re.split(r'\s{2,}', line) # Split by 2+ spaces
                    for part in parts:
                        w = clean_word(part)
                        if is_valid_word(w):
                            extracted_words.add(w)

        print(f"Total unique vocabulary items: {len(extracted_words)}")

    sorted_vocab = sorted(list(extracted_words))
    with open(output_path, 'w', encoding='utf-8') as f:
        for w in sorted_vocab:
            f.write(w + "\n")
            
    print(f"Saved to {output_path}")
    # Print sample
    print("Sample extracted words:", sorted_vocab[:10])

except Exception as e:
    print(f"Error: {e}")
