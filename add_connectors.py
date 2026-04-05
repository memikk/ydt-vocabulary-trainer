
import json

# Curated List of YDT Connectors / Transition Words
# Categories: Contrast, Cause-Effect, Addition, Condition, Time, Example
CONNECTORS = [
    # Contrast / Zıtlık
    {"word": "however", "meaning": "ancak, yine de", "type": "connector (contrast)"},
    {"word": "although", "meaning": "olmasına rağmen", "type": "connector (contrast)"},
    {"word": "though", "meaning": "olmasına rağmen, -sa da", "type": "connector (contrast)"},
    {"word": "even though", "meaning": "olsa bile, -e rağmen", "type": "connector (contrast)"},
    {"word": "much as", "meaning": "her ne kadar ... ise de", "type": "connector (contrast)"},
    {"word": "whereas", "meaning": "oysa, halbuki", "type": "connector (contrast)"},
    {"word": "while", "meaning": "iken, oysa", "type": "connector (contrast)"},
    {"word": "despite", "meaning": "rağmen", "type": "connector (contrast)"},
    {"word": "in spite of", "meaning": "rağmen", "type": "connector (contrast)"},
    {"word": "nevertheless", "meaning": "yine de, buna rağmen", "type": "connector (contrast)"},
    {"word": "nonetheless", "meaning": "yine de, buna rağmen", "type": "connector (contrast)"},
    {"word": "on the contrary", "meaning": "aksine, tam tersine", "type": "connector (contrast)"},
    {"word": "conversely", "meaning": "bunun aksine", "type": "connector (contrast)"},
    {"word": "on the other hand", "meaning": "öte yandan", "type": "connector (contrast)"},
    {"word": "still", "meaning": "yine de, hala", "type": "connector (contrast)"},
    {"word": "yet", "meaning": "yine de, ancak", "type": "connector (contrast)"},

    # Cause - Effect / Sebep - Sonuç
    {"word": "because", "meaning": "çünkü, -diği için", "type": "connector (cause)"},
    {"word": "since", "meaning": "-den beri, çünkü", "type": "connector (cause)"},
    {"word": "as", "meaning": "olarak, gibi, -dığı için", "type": "connector (cause)"},
    {"word": "due to", "meaning": "-den dolayı, nedeniyle", "type": "connector (cause)"},
    {"word": "owing to", "meaning": "-den dolayı, sayesinde", "type": "connector (cause)"},
    {"word": "because of", "meaning": "-den dolayı", "type": "connector (cause)"},
    {"word": "on account of", "meaning": "-den dolayı, yüzünden", "type": "connector (cause)"},
    {"word": "thanks to", "meaning": "sayesinde", "type": "connector (cause)"},
    {"word": "therefore", "meaning": "bu nedenle, dolayısıyla", "type": "connector (result)"},
    {"word": "thus", "meaning": "böylece, bu nedenle", "type": "connector (result)"},
    {"word": "hence", "meaning": "bu yüzden, bundan dolayı", "type": "connector (result)"},
    {"word": "consequently", "meaning": "sonuç olarak", "type": "connector (result)"},
    {"word": "as a result", "meaning": "sonuç olarak", "type": "connector (result)"},
    {"word": "thereby", "meaning": "dolayısıyla, böylece", "type": "connector (result)"},
    {"word": "accordingly", "meaning": "buna göre, bu doğrultuda", "type": "connector (result)"},

    # Addition / Ekleme
    {"word": "moreover", "meaning": "dahası, ayrıca", "type": "connector (addition)"},
    {"word": "furthermore", "meaning": "dahası, ayrıca", "type": "connector (addition)"},
    {"word": "in addition", "meaning": "buna ek olarak", "type": "connector (addition)"},
    {"word": "besides", "meaning": "bunun yanı sıra, ayrıca", "type": "connector (addition)"},
    {"word": "also", "meaning": "ayrıca, de/da", "type": "connector (addition)"},
    {"word": "what is more", "meaning": "dahası", "type": "connector (addition)"},
    {"word": "not only... but also", "meaning": "sadece ... değil, aynı zamanda ...", "type": "connector (addition)"},

    # Condition / Koşul
    {"word": "unless", "meaning": "-medikçe, olmazsa", "type": "connector (condition)"},
    {"word": "provided that", "meaning": "şartıyla", "type": "connector (condition)"},
    {"word": "providing", "meaning": "şartıyla", "type": "connector (condition)"},
    {"word": "on condition that", "meaning": "şartıyla", "type": "connector (condition)"},
    {"word": "as long as", "meaning": "-diği sürece", "type": "connector (condition)"},
    {"word": "so long as", "meaning": "-diği sürece", "type": "connector (condition)"},
    {"word": "in case", "meaning": "olur diye, durumunda", "type": "connector (condition)"},
    {"word": "otherwise", "meaning": "aksi takdirde", "type": "connector (condition)"},
    {"word": "if", "meaning": "eğer", "type": "connector (condition)"},

    # Example / Purpose / Others
    {"word": "for example", "meaning": "örneğin", "type": "connector (example)"},
    {"word": "for instance", "meaning": "örneğin", "type": "connector (example)"},
    {"word": "such as", "meaning": "gibi", "type": "connector (example)"},
    {"word": "in order to", "meaning": "-mek için", "type": "connector (purpose)"},
    {"word": "so that", "meaning": "-sin diye", "type": "connector (purpose)"},
    {"word": "that is", "meaning": "yani", "type": "connector (clarification)"},
    {"word": "in other words", "meaning": "başka bir deyişle", "type": "connector (clarification)"},
    {"word": "meanwhile", "meaning": "bu arada", "type": "connector (time)"},
    {"word": "subsequently", "meaning": "sonrasında, akabinde", "type": "connector (time)"}
]

vocab_path = "vocab-app/vocabulary.json"

try:
    # Load existing
    with open(vocab_path, 'r', encoding='utf-8') as f:
        existing_vocab = json.load(f)
    
    # Create set of existing words to avoid duplicates
    # Create lookup for existing items
    existing_map = {item['word'].lower(): item for item in existing_vocab}
    
    added_count = 0
    updated_count = 0
    
    for conn in CONNECTORS:
        word_key = conn['word'].lower()
        if word_key in existing_map:
            # Update existing entry to be a connector
            existing_map[word_key]['type'] = conn['type']
            existing_map[word_key]['meaning'] = conn['meaning'] # Use curated meaning
            updated_count += 1
        else:
            existing_vocab.append(conn)
            added_count += 1
            
    print(f"Added {added_count} new connectors, updated {updated_count} existing ones.")
    
    # Sort A-Z
    existing_vocab.sort(key=lambda x: x['word'])
    
    # Save
    with open(vocab_path, 'w', encoding='utf-8') as f:
        json.dump(existing_vocab, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully added {added_count} connectors to the vocabulary.")

except Exception as e:
    print(f"Error: {e}")
