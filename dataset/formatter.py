import re
tagalog_stop_words = [
    'akin', 'aking', 'ako', 'alin', 'am', 'amin', 'aming', 'ang', 'ano', 'anumang',
    'apat', 'at', 'atin', 'ating', 'ay', 'bababa', 'bago', 'bakit', 'bawat', 'bilang',
    'dahil', 'dapat', 'din', 'dito', 'doon', 'gagawin', 'gayunman',
    'gusto', 'habang', 'hanggang', 'hindi', 'huwag', 'iba',
    'ibaba', 'ibabaw', 'ibig', 'ikaw', 'ilagay', 'ilan', 'inyong', 'isa',
    'itaas', 'ito', 'iyo', 'iyon', 'iyong', 'ka', 'kahit', 'kailanman', 'kami',
 'kanino', 'kanya', 'kanyang', 'kapag', 'kapwa', 'katulad', 'kaya', 'kaysa', 'ko', 'kong', 'kulang', 'kung', 'lahat',
    'lamang', 'likod', 'lima', 'maging',
    'masyado', 'may', 'mayroon', 'mga', 'minsan', 'mismo', 'mula', 'muli', 'na',
 'naging', 'nagkaroon', 'nais', 'nakita', 'namin', 'napaka', 'narito', 'nasaan',
    'ng', 'ngayon', 'ni', 'nila', 'nilang', 'nito', 'niya', 'niyang', 'noon', 'o', 'pa', 'pang'
    'panahon', 'pangalawa', 'para', 'paraan', 'pareho', 'pero',
    'sa', 'saan', 'sarili', 'sila', 'sino', 'siya', 'tatlo', 'tayo',
    'tulad', 'tungkol', 'una', 'walang', 'ba', 'eh','kasi', 'lang','mo','naman','opo','po','si','talaga',
    'yung', 'pwede', 'pwede', 'uli', 'makita', 'noong', 'nasa', 'mong', 'nang'
]

def ilagay(input_file, output_file):
    unique = set()
    word_pattern = re.compile(r'^[a-zA-Z]+(-[a-zA-Z]+)*$')  # Regex to match words with letters and hyphens
    with open(input_file, 'r', encoding='utf-8') as infile:
        for line in infile:
            words = line.split() 
            words_lowercase = [word.lower() for word in words]
            for word in words_lowercase:
                if word not in tagalog_stop_words and word not in unique and word_pattern.match(word):
                    unique.add(word)
    
    # Sort the unique words 
    sorted_words = sorted(unique)
    
    # Write the sorted words to the output file
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for word in sorted_words:
            outfile.write(f"{word}\n")


def combine_and_sort(file1, file2, output_file):
    unique_words = set()

    # Read the first file and add words to the set
    with open(file1, 'r', encoding='utf-8') as f1:
        for line in f1:
            unique_words.add(line.strip())

    # Read the second file and add words to the set
    with open(file2, 'r', encoding='utf-8') as f2:
        for line in f2:
            unique_words.add(line.strip())

    # Sort the unique words alphabetically
    sorted_words = sorted(unique_words)

    # Write the sorted words to the output file
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for word in sorted_words:
            outfile.write(f"{word}\n")


def remove_sentences_or_phrases(input_file, output_file):
    """
    Removes entries that are sentences or phrases (contain spaces) from the input file.
    Writes only single-word entries to the output file.
    """
    filtered_words = set()

    with open(input_file, 'r', encoding='utf-8') as infile:
        for line in infile:
            word = line.strip()
            # Include only single words (no spaces)
            if " " not in word:
                filtered_words.add(word)
    filtered_words = sorted(filtered_words)
    # Write the filtered words to the output file
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for word in filtered_words:
            outfile.write(f"{word}\n")


"""input_file = "dataset/konstitusyon.txt"
output_file = input('Enter Output Filename: ')
ilagay(input_file, output_file)"""
remove_sentences_or_phrases('dataset/tagalog_lemmas.txt', 'tagalog_lemmas.txt')
#combine_and_sort("dataset/bible.txt", "dataset/line_konstitusyon.txt", "dataset/formal_tagalog.txt")
