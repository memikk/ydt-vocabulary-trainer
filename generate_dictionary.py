
import json
import os

input_path = "vocab_clean.txt"
output_path = "vocabulary.json"
dict_path = "full_dict.json"

def clean_input_word(word_line):
    return word_line.strip().lower()

def load_dictionary():
    if os.path.exists(dict_path):
        with open(dict_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def guess_meaning(word, dictionary):
    # Direct check first logic is in main loop, but here we check variations
    
    # 1. Standard Inflections
    if word.endswith("s"):
        base = word[:-1]
        if base in dictionary: return dictionary[base]
        if word.endswith("ies"):
            base = word[:-3] + "y"
            if base in dictionary: return dictionary[base]
        if word.endswith("es"):
            base = word[:-2]
            if base in dictionary: return dictionary[base]
            
    if word.endswith("ed"):
        base = word[:-2] # worked -> work
        if base in dictionary: return dictionary[base]
        base = word[:-1] # lived -> live
        if base in dictionary: return dictionary[base]
        if len(word) > 3 and word[-3] == word[-4]: # stopped -> stop
             base = word[:-3]
             if base in dictionary: return dictionary[base]

    if word.endswith("ing"):
        base = word[:-3] # playing -> play
        if base in dictionary: return dictionary[base]
        base = word[:-3] + "e" # making -> make
        if base in dictionary: return dictionary[base]
        if len(word) > 4 and word[-4] == word[-5]: # sitting -> sit
             base = word[:-4]
             if base in dictionary: return dictionary[base]

    # 2. Adverbs (-ly)
    if word.endswith("ly"):
        base = word[:-2] # quickly -> quick
        if base in dictionary: return dictionary[base]
        if word.endswith("ily"):
             base = word[:-3] + "y" # happily -> happy
             if base in dictionary: return dictionary[base]
        # Try to strip suffix from the base too? (abusively -> abusive -> abuse)
        # Recursive attempt?
        
    # 3. Noun/Adjective Suffixes (approximate mapping)
    # -tion, -ment, -ance, -ence, -able, -ible, -ness, -ity
    
    suffixes = [
        ("tion", ""), ("tion", "te"), ("ation", "e"), # creation -> create, population -> populate
        ("ment", ""), # achievement -> achieve
        ("ance", ""), ("ance", "e"), # resistance -> resist
        ("ence", ""), ("ence", "e"), # dependence -> depend
        ("able", ""), ("able", "e"), # adaptable -> adapt
        ("ible", ""), ("ible", "e"),
        ("ness", ""), # happiness -> happy (handled by y->i rule often but let's see)
        ("ity", "e"), ("ity", ""), # activity -> active
        ("ive", ""), ("ive", "e"), # active -> act
        ("al", ""), ("al", "e"), # accidental -> accident
        ("ful", ""), # careful -> care
        ("less", ""), # careless -> care
        ("ous", ""), ("ous", "e"), # famous -> fame
    ]
    
    for suffix, replacement in suffixes:
        if word.endswith(suffix):
            base = word[:-len(suffix)] + replacement
            if base in dictionary: return dictionary[base]
            
            # Double suffix check? (realistically too expensive/noisy)
            
    return None

def main():
    final_dict = []
    
    # Load Dict
    DICTIONARY = load_dictionary()
    print(f"Loaded dictionary with {len(DICTIONARY)} entries.")

    with open(input_path, 'r', encoding='utf-8') as f:
        words = [clean_input_word(line) for line in f if line.strip()]

    print(f"Loading {len(words)} candidates from PDF extraction...")
    
    found_count = 0
    missing_count = 0
    
    processed_words = set()

    for word in words:
        if word in processed_words: continue
        
        meaning = DICTIONARY.get(word)
        if not meaning:
            meaning = guess_meaning(word, DICTIONARY)
            
        word_type = "word"
        if " " in word: word_type = "phrasal_verb"
        
        if meaning:
            final_dict.append({
                "word": word,
                "meaning": meaning,
                "type": word_type
            })
            found_count += 1
            processed_words.add(word)
        else:
            missing_count += 1
            # Optional: Print typical missing words to debug
            # if missing_count < 10: print(f"Missing: {word}")
            
    # Sort
    final_dict.sort(key=lambda x: x['word'])

    # Save
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(final_dict, f, ensure_ascii=False, indent=2)
        
    print(f"Generated {len(final_dict)} dictionary entries.")
    print(f"Found: {found_count}, Missing: {missing_count}")

if __name__ == "__main__":
    main()
