
input_file = "vocabulary.json" # Use the json file directly
output_file = "data.js"

try:
    with open(input_file, 'r', encoding='utf-8') as f_in:
        content = f_in.read()

    with open(output_file, 'w', encoding='utf-8') as f_out:
        f_out.write("const VOCAB_DATA = ")
        f_out.write(content)
        f_out.write(";")

    print("Created data.js successfully.")
except Exception as e:
    print(f"Error: {e}")
