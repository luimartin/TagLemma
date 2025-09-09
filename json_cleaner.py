import json
import re

# Markers to split the definition on
MARKERS = ['n\\.', 'inf\\.', 'adj\\.', 'adv\\.', 'intrj\\.']

# Compile a regex pattern that matches any of the markers
MARKER_PATTERN = re.compile(rf"({'|'.join(MARKERS)})\s*(.*)", re.IGNORECASE)

def clean_json_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    cleaned_data = []
    for entry in data:
        word = entry.get("word")
        definition = entry.get("definition", "")
        match = MARKER_PATTERN.search(definition)

        if match:
            cleaned_definition = match.group(2).strip()
        else:
            cleaned_definition = definition.strip()

        cleaned_data.append({
            "word": word,
            "definition": cleaned_definition
        })

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=4)

    print(f"✅ Cleaning complete! Saved to '{output_file}'.")

# Example usage
if __name__ == "__main__":
    clean_json_file("dataset/tagalog_dictionary.json", "cleaned_definitions.json")
