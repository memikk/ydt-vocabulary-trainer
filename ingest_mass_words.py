
import json
import os

input_file = "mass_data.txt"
output_file = "full_dict.json"

try:
    with open(input_file, 'r', encoding='utf-8') as f:
        raw_data = f.read().replace('\n', '')
    
    dict_map = {}
    for pair in raw_data.split('|'):
        if ':' in pair:
            w, m = pair.split(':', 1)
            dict_map[w] = m
    
    print(f"Parsed {len(dict_map)} new words.")
    
    existing = {}
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            try:
                existing = json.load(f)
            except:
                pass
    
    existing.update(dict_map)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)
        
    print(f"Total dictionary size: {len(existing)}")

except Exception as e:
    print(f"Error: {e}")
