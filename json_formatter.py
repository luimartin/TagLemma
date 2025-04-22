import json

def load_and_clean_words(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            words = []
            for line in f:
                word = line.strip()
                if word and " " not in word and "\t" not in word:  # Keep only single-word entries
                    words.append(word)
            return words
    except FileNotFoundError:
        print(f"⚠️ File not found: {filename}")
        return []

def combine_tagalog_pos_files(output_json="tagalog_words.json"):
    data = {
        "noun": load_and_clean_words("tagalog_nouns.txt"),
        "verb": load_and_clean_words("tagalog_verbs.txt"),
        "adjective": load_and_clean_words("tagalog_adjectives.txt"),
        "adverb": load_and_clean_words("tagalog_adverbs.txt")
    }

    with open(output_json, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)

    print(f"✅ Cleaned and combined files into '{output_json}'.")

# Run the combiner
if __name__ == "__main__":
    combine_tagalog_pos_files()
