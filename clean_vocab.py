
import re

input_path = "vocab_full_raw.txt"
output_path = "vocab_clean.txt"

def get_base_candidates(word):
    candidates = set()
    candidates.add(word)
    # Remove 's' or 'es'
    if word.endswith('s') and not word.endswith('ss'):
        candidates.add(word[:-1])
        if word.endswith('ies'): candidates.add(word[:-3] + 'y')
        if word.endswith('es'): candidates.add(word[:-2])
    # Remove 'ed'
    if word.endswith('ed'):
        candidates.add(word[:-2])
        if word.endswith('ied'): candidates.add(word[:-3] + 'y')
        candidates.add(word[:-1]) # e.g. cared -> care
    # Remove 'ing'
    if word.endswith('ing'):
        candidates.add(word[:-3])
        candidates.add(word[:-3] + 'e')
    # Remove 'ly'
    if word.endswith('ly'):
        candidates.add(word[:-2])
    return candidates

def main():
    with open(input_path, 'r', encoding='utf-8') as f:
        raw_words = [line.strip() for line in f if line.strip()]

    # First pass: Count occurrences or just set existence?
    # Actually, we want to KEEP the shortest/simplest form if multiple variations exist.
    # But if only "abundantly" exists, maybe we keep it? Or try to reduce it?
    # The requirement is "Normalize words (base form when possible)".
    
    # Let's collect all raw words into a set first for lookup
    raw_set = set(raw_words)
    final_words = set()

    for word in raw_words:
        # If word is "accounts", check if "account" is in raw_set.
        # If "account" is there, we skip "accounts".
        # If "account" is NOT there, we might want to stem it anyway?
        # User said "Normalize".
        
        # Simple stemming logic
        keep = True
        
        # If it's a plural/verb form and the base exists, drop this one
        if word.endswith('s') and word[:-1] in raw_set and not word.endswith('ss'):
            keep = False
        elif word.endswith('ed') and (word[:-2] in raw_set or word[:-1] in raw_set):
            keep = False
        elif word.endswith('ing') and (word[:-3] in raw_set or word[:-3]+'e' in raw_set):
            keep = False
        elif word.endswith('ly') and (word[:-2] in raw_set):
            keep = False
            
        if keep:
            final_words.add(word)

    # Further cleanup: remove short noise
    final_sorted = sorted([w for w in final_words if len(w) > 2])
    
    with open(output_path, 'w', encoding='utf-8') as f:
        for w in final_sorted:
            f.write(w + "\n")
            
    print(f"Cleaned vocabulary: {len(final_sorted)} words (from {len(raw_words)})")

if __name__ == "__main__":
    main()
