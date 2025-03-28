import numpy as np
import pandas as pd
from collections import Counter
import math
import re
import inf_morph_stripping as ms
from functools import lru_cache

class TagLemma:
    def __init__(self):
        self.PREFIX_SET = [
            'nakikipag', 'panganga', 'makapag',
            'nakapagpa', 'nakapag', 'nakipag', 'tigapag',
            'napaka', 'pinaka', 'ipinag', 'pinag',
            'tiga', 'pang', 'pinakipag', 'pakipag', 'pagka',  'pag', 'pa',
            'nang', 'makipag', 'mag', 'magpa', 'ma',
            'tag', 'nam', 'nag',
            'may', 'ni', 'in',
            'de-', 'des-', 'di-', 'ekstra-', 'elektro',
            'ipa', 'ikapakapagpaka', 'ikapakapagpa', 'ikapakapang', 'ikapakapag', 'ikapakapam',
            'ikapakapan', 'ikapagpaka', 'ikapakipan', 'ikapakipag', 'ikapakipam',
            'ikapakipa', 'ipakipag', 'ipagkang', 'ikapagpa', 'ikapaka', 'ikapaki',
            'ikapang', 'ipakipa', 'ikapag', 'ikapam', 'ikapan', 'ipagka', 'ipagpa',
            'ipaka', 'ipaki', 'ikapa', 'ipang', 'ikang', 'ipag', 'ikam', 'ikan',
            'isa', 'kasing', 'kamaka', 'kanda', 'kasim', 'kasin', 'kamag', 'ka',
            'kaka', 'mangagsipagpaka', 'mangagsipag', 'mangagpaka', 'magsipagpa',
            'makapagpa', 'mangagsi', 'mangagpa', 'magsipag', 'mangagka', 'magkang',
            'magpaka', 'magpati', 'mapapag', 'mapang', 'mapasa',
            'mapapa', 'mangag', 'manga', 'magka', 'magsa',
            'mapam', 'mapan', 'maka', 'maki', 'mam',
            'nangagsipagpaka', 'nangagsipagpa', 'nagsipagpaka', 'nakapagpaka',
            'nangagsipag', 'nangagpaka', 'nangagkaka', 'nagsipagpa',
            'nagsipag', 'nangagpa', 'nangagka', 'nangagsi',
            'napapag', 'nagpaka', 'nagpati', 'nangag', 'napasa',
            'nanga', 'nagka', 'nagpa', 'nagsa', 'nagsi', 'napag',
            'naki', 'napa', 'na', 'pagpapati', 'pagpapaka', 'pagpaka',
            'pagsasa', 'pasasa', 'papag', 'pampa', 'panag', 'paka',
            'pani', 'papa', 'para', 'pasa', 'pati',
        ]
        self.INFIX_SET = [
            'um',
            'in'
        ]
        self.SUFFIX_SET = [
            'syon', 'dor', 'ita',
            'hin', 'ing', 'han', 'an',
            'ang', 'ng',
            'in', 'g'
        ]

        self.STOP_WORDS = [
            'akin', 'aking', 'ako', 'alin', 'am', 'amin', 'aming', 'ang', 'ano', 'anumang',
            'apat', 'at', 'atin', 'ating', 'ay', 'bababa', 'bago', 'bakit', 'bawat', 'bilang',
            'dahil', 'dapat', 'din', 'dito', 'doon', 'gagawin', 'gayunman',
             'habang', 'hanggang', 'hindi', 'huwag', 'iba',
             'ibig', 'ikaw', 'ilan', 'inyong', 'isa',
            'ito', 'iyo', 'iyon', 'iyong', 'ka', 'kahit', 'kailanman', 'kami',
            'kanino', 'kanya', 'kanyang', 'kapag', 'katulad', 'kaya', 'kaysa', 'ko', 'kong', 'kulang', 'kung', 'lahat',
            'lamang', 'likod', 'lima', 'maging',
            'masyado', 'may', 'mayroon', 'mga', 'minsan', 'mismo', 'mula', 'muli', 'na',
            'naging', 'nakita', 'namin', 'napaka', 'narito', 'nasaan',
            'ng', 'ngayon', 'ni', 'nila', 'nilang', 'nito', 'niya', 'niyang', 'noon', 'o', 'pa', 'pang'
            'panahon', 'pangalawa', 'para', 'paraan', 'pareho', 'pero',
            'sa', 'saan', 'sarili', 'sila', 'sino', 'siya', 'tatlo', 'tayo',
            'tulad', 'tungkol', 'una', 'walang', 'ba', 'eh', 'kasi', 'lang', 'mo', 'naman', 'opo', 'po', 'si', 'talaga',
            'yung', 'pwede', 'pwedeng', 'uli', 'makita', 'noong', 'nasa', 'nang', 'mong', 'ring', 'rin', 'pang', 'siyang', 'iyong', 'kaming'
            , 'ding', 'kundi', 'kundiman'
        ]

        self.dframe = None
        self.raw_lemmas = None
        self.lemma_size = None
        self.formal_words = None
        self.found_stop_words = None
        self.to_lemmatize_tokens = None
        self.not_to_lemmatize_tokens_index = None
        self.morpheme = None
        self.list_of_morphemes = []
        self.list_of_lemmatizable_tokens = []
        self.potential_lemmas = {}
        self.lemma_ranking_list = {}
        self.lemmatized_text = []
        self.source_to_target = {}
        self.valid_tokens = None  # forda UI
        self.invalid_tokens = None  # forda UI
        self.lemma = []  # forda UI
        self.annotated_lemma = {}
        self.curr_token = None
        self.input, self.result = '', ''

    # =======================LOADING OF FILES=======================

    def load_lemma_to_dfame(self, file_path):
        with open(file_path, 'r') as file:
            lines = [line.strip() for line in file]

        self.dframe = pd.DataFrame(lines, columns=['WORDS'])

        self.raw_lemmas = self.dframe 
        self.lemma_size = self.dframe.shape[0]

    def load_formal_tagalog(self, file_path):
        with open(file_path, 'r') as file:
            file_contents = file.read()

        self.formal_words = file_contents.split()

    # =======================MAIN ARCHITECTURE HERE=======================

    # =======================PRE-PROCESSING=======================
    def tokenize_input_text(self, input_text):
        # Updated regex to include hyphen (-) as part of the word
        tokens = re.findall(r'\w+(?:-\w+)*', input_text)

        return tokens

    def remove_stop_words(self, input_tokens):
        self.found_stop_words = [
            token for token in input_tokens if token in self.STOP_WORDS]

        cleaned_tokens = [
            token for token in input_tokens if token not in self.STOP_WORDS]
        return cleaned_tokens
    # The Text Input must be Formal Tagalog Format,
    # One Informal means Failure to Proceed to Lemmatized the Whole Text

    def validate_formal_tagalog(self, final_tokens):
        self.to_lemmatize_tokens = final_tokens
        self.not_to_lemmatize_tokens_index = [final_tokens.index(
            token) for token in final_tokens if token not in self.formal_words and self.STOP_WORDS]

        # Show the Element Using the Identified Index
        unable_to_lemmatize = []
        for indx in self.not_to_lemmatize_tokens_index:
            unable_to_lemmatize.append(self.to_lemmatize_tokens[indx])

        # Show the Element that can be lemmatize
        able_to_lemmatize = [token for token in self.to_lemmatize_tokens if self.to_lemmatize_tokens.index(
            token) not in self.not_to_lemmatize_tokens_index]
        # if len(missing_tokens) >= 1: return (False, 'FAILED! Unable to Lemmatized the Input Text')
        return (True, unable_to_lemmatize, able_to_lemmatize)

    # To Check Whether the Input Text is Alreadly A Lemma
    # You know, to Avoid Unecessary Further Procedure and Reduce Search Space Complexity
    @lru_cache(maxsize=None)
    def isLemmaAlready(self, token):
        if token in self.raw_lemmas['WORDS'].values:
            return True

        return False

    # Remove Deduplication in First Sysllable
    def remove_duplication(self, word):
        first_two_syllables = word[:2]

        if word.startswith(first_two_syllables * 2):
            return word[2:], True

        return word, False

    # Remove Deduplication in Any Part of the Word
    def remove_duplication_non_first_syl(self, word):
        # Regex to find and remove adjacent duplicate substrings
        pattern = re.compile(r'(\w+)\1')
        found_duplication = False

        while pattern.search(word):
            word = pattern.sub(r'\1', word)
            found_duplication = True

        return word, found_duplication

    # Remove One Affix Only, Not Thrice nor Twicec, but Once Only
    def remove_one_affix(self, word):
        for prefix in self.PREFIX_SET:
            if word.startswith(prefix):
                return word[len(prefix):]

        for infix in self.INFIX_SET:
            if infix in word:
                return word.replace(infix, '', 1)

        for suffix in self.SUFFIX_SET:
            if word.endswith(suffix):
                return word[:-len(suffix)]

        return word

    # This Code is Complicated and not Clean, but it Rightfully Serves its Purpose
    # Don't You Dare to Update this Unless Stated
    def get_morpheme(self, token):
        # A Word with Deduplication in First Syllable must be Stripped One Time Only
        deduplicated_word, is_duplicated = self.remove_duplication(token)

        if not is_duplicated:
            # A Word with Non-First Syllable Deduplication must be Stripped,
            # then Proceed to Affix Removal
            deduplicated_word_non_first_syl, is_duplicated_non_first_syl = self.remove_duplication_non_first_syl(
                deduplicated_word)

            if not is_duplicated_non_first_syl:
                # A Word without Deduplication at the First and Non-First Syllable must be Remove the Affxes First,
                # then Proceed to Stripping of Deduplication
                morpheme_word = self.remove_one_affix(
                    deduplicated_word_non_first_syl)
                morpheme_word, _temp = self.remove_duplication_non_first_syl(
                    morpheme_word)
            else:
                morpheme_word = self.remove_one_affix(
                    deduplicated_word_non_first_syl)

        else:
            morpheme_word = deduplicated_word

        self.morpheme = morpheme_word

        # Save the morpheme in the list 
        self.list_of_morphemes.append(morpheme_word)

        return morpheme_word

    def get_morpheme_of_inf(self, token):
        self.morpheme = ms.get_morpheme(token)
        self.list_of_morphemes.append(self.morpheme)
        return self.morpheme

    # Reduce the Search Space by Using the Extracted Morpheme of the Word
    @lru_cache(maxsize=None)
    def reduce_search_space(self, word, pattern):
        # Patterns for Getting the Potential Lemmas
        regex_pattern = ".*".join(list(pattern))
        regex_pattern_rd = []
        regex_pattern_uo = []
        regex_pattern_mn = []

        # Alternate Morphophonemic System
        if 'r' or 'd' in word:
            regex_pattern_rd = ".*".join(
                list(self.alternate_morphophonemic_rd(pattern)))

        if 'u' or 'o' in word:
            regex_pattern_uo = ".*".join(
                list(self.alternate_morphophonemic_uo(pattern)))

        if 'm' or 'n' in word:
            regex_pattern_mn = ".*".join(
                list(self.alternate_morphophonemic_mn(pattern)))

        # Combined All the Potential Lemmas Using All the Possible Alternate Morphophonemic Word
        combined_regex_pattern = f"({regex_pattern}|{regex_pattern_rd}|{regex_pattern_uo}|{regex_pattern_mn})"

        return bool(re.search(combined_regex_pattern, word))

    @lru_cache(maxsize=None)
    def get_potential_lemmas(self, token, morpheme):
        filtered_lemmas = self.raw_lemmas[self.raw_lemmas['WORDS'].str.len() <= len(token)]
        potential_lemmas = filtered_lemmas[filtered_lemmas['WORDS'].apply(lambda x: self.reduce_search_space(x, morpheme))]
        
        return potential_lemmas

    # This Part if for Interchanging the Letters
    # Its part of Tagalog System, and for Pre-processing Stage of this Lemmatization
    # Dont't Question it Further, Please
    def alternate_morphophonemic_rd(self, token):
        translation_table = str.maketrans("rd", "dr")
        translated_token = token.translate(translation_table)

        return translated_token


    def alternate_morphophonemic_uo(self, token):
        translation_table = str.maketrans("ou", "uo")
        translated_token = token.translate(translation_table)

        return translated_token


    def alternate_morphophonemic_mn(self, token):
        translation_table = str.maketrans("nm", "mn")
        translated_token = token.translate(translation_table)

        return translated_token


    # =======================FUZZY MATICHING ALGRITHMS=======================
    # Cosine Similarity Function
    # To get the Morpho-Syntactic Structure of the Word and Potential Lemma
    def cosine_similarity(self, source, target):
        source_vec = Counter(source)
        target_vec = Counter(target)

        dot_product = sum(source_vec[key] * target_vec[key]
                          for key in source_vec if key in target_vec)
        magnitude1 = math.sqrt(sum([val**2 for val in source_vec.values()]))
        magnitude2 = math.sqrt(sum([val**2 for val in target_vec.values()]))

        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0

        return dot_product / (magnitude1 * magnitude2)


    # Unused, but it can be in the Future
    def sqrt_cosine_similarity(self, source, target):
        source_vec = Counter(source)
        target_vec = Counter(target)

        dot_product = math.sqrt(
            sum(source_vec[key] * target_vec[key] for key in source_vec if key in target_vec))
        magnitude1 = math.sqrt(sum([val for val in source_vec.values()]))
        magnitude2 = math.sqrt(sum([val for val in target_vec.values()]))

        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0

        return dot_product / (magnitude1 * magnitude2)


    # unused, Cosine Distance Function
    def cosine_distance_percentage(self, source, target):
        cosine_sim = self.cosine_similarity(source, target)
        cosine_dist = 1 - cosine_sim

        # Convert Cosine Distance to a Percentage
        # Closer to 0 means Higher Similarity Percentage
        similarity_percentage = (2 - cosine_dist) / 2

        return similarity_percentage

     # Levenshtein Distance Function
     # To get the Edit Distance (Deletion, Substitution, Insertion) to Turn the Input Word into its Potential Lemma
    
    
    def levenshtein_distance(self, source, target):
        m, n = len(source), len(target)
        d = np.zeros((m + 1, n + 1), dtype=int)

        for i in range(m + 1):
            d[i][0] = i

        for j in range(n + 1):
            d[0][j] = j

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                cost = 0 if source[i - 1] == target[j - 1] else 1
                d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] +
                              1, d[i - 1][j - 1] + cost)

        distance = d[m][n]
        max_len = max(len(source), len(target))

        return 1 - (distance / max_len) if max_len > 0 else 1.0


    # lCS Function
    # To get the Longest Consecutively Appearing Characters of the Input Word and Potential Lemma
    def longestCommonSubstr(self, source, target):
        m = len(source)
        n = len(target)

        # Create a 1D array to store the previous row's results
        prev = [0] * (n + 1)

        res = 0
        for i in range(1, m + 1):

            # Create a temporary array to store the current row
            curr = [0] * (n + 1)
            for j in range(1, n + 1):
                if source[i - 1] == target[j - 1]:
                    curr[j] = prev[j - 1] + 1
                    res = max(res, curr[j])
                else:
                    curr[j] = 0

            # Move the current row's data to the previous row
            prev = curr

        # Normalize
        max_len = max(m, n)
        normalized_res = (res / max_len) if max_len > 0 else 1

        return normalized_res

    # Jaccard Index Function
    def jaccardIndex(self, x, y):
        intersection = len(list(set(x).intersection((set(y)))))
        union = len(list(set(x).union((set(y)))))

        return intersection/union

    def fuzzy_matching(self, token, potential_lemmas):
        # Fuzzy Matching Algorithm Implementations
        potential_lemmas['Cosine Similarity'] = potential_lemmas['WORDS'].apply(
            lambda x: self.cosine_similarity(token, x))
        #potential_lemmas['Cosine Distance'] = potential_lemmas['WORDS'].apply(
            #lambda x: self.cosine_distance_percentage(token, x))
        potential_lemmas['Levenshtein Distance'] = potential_lemmas['WORDS'].apply(
            lambda x: self.levenshtein_distance(token, x))
        potential_lemmas['Longest Common Substring'] = potential_lemmas['WORDS'].apply(
            lambda x: self.longestCommonSubstr(token, x))
        #potential_lemmas['Jaccard'] = potential_lemmas['WORDS'].apply(
            #lambda x: self.jaccardIndex(token, x))
  

        # Ranks the Fuzzy Matched Lemmas
        potential_lemmas['Rank Scores'] = (
            (.75 * potential_lemmas['Cosine Similarity']) +
            (.20 * potential_lemmas['Levenshtein Distance']) +
            (.05 * potential_lemmas['Longest Common Substring']) 
        )

        threshold_potential_lemmas = potential_lemmas[
            (potential_lemmas['Cosine Similarity'] >= 0)
        ]

        return threshold_potential_lemmas

# =======================CODE FOR DISPLAY RELEVANT INFO IN LEMMATIZATION SYSTEM=======================
    def show_best_lemma(self, potential_lemmas):
        if not potential_lemmas.empty:
            # Sort lemmas by Rank Scores in Descending Order
            sorted_lemmas = potential_lemmas.sort_values(by='Rank Scores', ascending=False)

            # Only Apply Filtering if it is aldready a lemma
            # For Infinitive to Root Only
            if self.isLemmaAlready(self.curr_token):  
                
                if self.morpheme in potential_lemmas['WORDS'].values:
                    morpheme_row = potential_lemmas[potential_lemmas['WORDS'] == self.morpheme]
                    cosine_similarity = morpheme_row['Cosine Similarity'].values[0]

                    # If greater then 85, then Prioritize the Highest Rank duh
                    if cosine_similarity > 0.85:  
                        return self.curr_token, sorted_lemmas 
                    

                    else: 
                        below_threshold = sorted_lemmas[sorted_lemmas['Cosine Similarity'] <= 0.85]

                         # Update list to only include filtered lemmas
                        if not below_threshold.empty:
                            sorted_lemmas = below_threshold 

                     
                        return sorted_lemmas.iloc[0]['WORDS'], sorted_lemmas  

                else:
                    # If morpheme does not exist in potential lemmas, return highest-ranked lemma
                    return sorted_lemmas.iloc[0]['WORDS'], sorted_lemmas

            # If token is NOT already a lemma, return the full sorted list without filtering
            return sorted_lemmas.iloc[0]['WORDS'], sorted_lemmas

        return self.curr_token, potential_lemmas  # If empty, return original token and empty lemmas

    def annotate(self, inf_input, lemm_output):
        if inf_input == lemm_output:
            return

        if lemm_output in self.annotated_lemma:
            if inf_input not in self.annotated_lemma[lemm_output]:
                self.annotated_lemma[lemm_output].append(inf_input)
        else:
            self.annotated_lemma[lemm_output] = [inf_input]

    def show_annotation(self):
        return self.annotated_lemma

    def show_inflection_and_morpheme(self):
        temp = []
        seen_tokens = set()  # To track already processed tokens

        for i in range(len(self.list_of_lemmatizable_tokens)):
            current_token = self.list_of_lemmatizable_tokens[i]
            
            # Skip if we've already processed this token
            if current_token in seen_tokens:
                continue
                
            # Add to seen_tokens and process
            seen_tokens.add(current_token)
            inf_and_morph_string = f"{current_token} -> {self.list_of_morphemes[i]}"
            temp.append(inf_and_morph_string)

        return temp
    
    # Creating of morpheme : potential lemmas key value pair
    def create_morpheme_to_potential_lemmas(self, morpheme, potential_lemmas):

        # Ensure potential_lemmas is a DataFrame
        if isinstance(potential_lemmas, pd.DataFrame):
            # Turn Potential Lemmas---which is a DataFrame type---Into an Array 
            converted_potential_lemmas_to_array = potential_lemmas['WORDS'].tolist()
        else:
            converted_potential_lemmas_to_array = []

        # The Key : Value pair of the morpheme and potential lemmas of the input
        self.potential_lemmas[morpheme] = converted_potential_lemmas_to_array
    
    def create_source_to_target(self, token, lemma):
        self.source_to_target[token] = lemma

    # Display potential lemmas basedon the chosen morpheme
    def show_potential_lemmas(self, lemmatizable_token):

        morpheme_index = self.list_of_lemmatizable_tokens.index(lemmatizable_token)
        
        morpheme = self.list_of_morphemes[morpheme_index]
       
        return self.potential_lemmas[morpheme]
    
    # Display the process of the algorithm based on the highest lemma only, not the entire lemma output
    # Applied to all fuzzy algorithms below
    def show_cosine_similarity(self, source, target):
        source_vec = Counter(source)
        target_vec = Counter(target)
        
        output = []
        output.append("\n==== Cosine Similarity Process ====\n")
        output.append(f"Source: {source}")
        output.append(f"Target: {target}\n")
        
        unique_chars_source = set(source)
        unique_chars_target = set(target)
        output.append("Step 1: Extract Unique Characters")
        output.append(f"Unique Characters in Source: {unique_chars_source}")
        output.append(f"Unique Characters in Target: {unique_chars_target}\n")
        
        output.append("Step 2: Convert Text to Frequency Vectors")
        output.append(f"Source Vector: {dict(source_vec)}")
        output.append(f"Target Vector: {dict(target_vec)}\n")
        
        output.append("Step 3: Compute Dot Product")
        dot_product = sum(source_vec[key] * target_vec[key] for key in source_vec if key in target_vec)
        output.append(f"Dot Product: {dot_product}\n")
        
        output.append("Step 4: Compute Magnitude of Vectors")
        magnitude1 = math.sqrt(sum([val**2 for val in source_vec.values()]))
        magnitude2 = math.sqrt(sum([val**2 for val in target_vec.values()]))
        output.append(f"||Source|| = {magnitude1:.2f}")
        output.append(f"||Target|| = {magnitude2:.2f}\n")
        
        output.append("Step 5: Compute Cosine Similarity")
        if magnitude1 == 0 or magnitude2 == 0:
            similarity = 0.0
        else:
            similarity = dot_product / (magnitude1 * magnitude2)
        output.append(f"Cosine Similarity = {dot_product:.2f} / ({magnitude1:.2f} x {magnitude2:.2f})")
        output.append(f"= {dot_product:.2f} / {magnitude1 * magnitude2:.2f}")
        output.append(f"= {similarity:.4f}\n")
        output.append(f"The word '{source}' is {(similarity * 100):.2f}% morphologically similar for the '{target}' which is the lemma\n")
        output.append("===================================\n")
  
        return "\n".join(output)

    def show_lev_distance(self,source, target):
        m, n = len(source), len(target)
        d = np.zeros((m + 1, n + 1), dtype=int)
        
        result = []
        result.append("\n==== Levenshtein Distance Process ====\n")
        result.append(f"Source: {source}")
        result.append(f"Target: {target}\n")
        
        result.append("Step 1: Initialize Distance Matrix")
        for i in range(m + 1):
            d[i][0] = i
        for j in range(n + 1):
            d[0][j] = j
        
        result.append("\nInitial Matrix:\n")
        result.append(self.print_matrix(d, source, target))
        
        result.append("\nStep 2: Compute Distance Matrix\n")
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                cost = 0 if source[i - 1] == target[j - 1] else 1
                d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + cost)
        
        distance = d[m][n]
        max_len = max(len(source), len(target))
        similarity = 1 - (distance / max_len) if max_len > 0 else 1.0
        result.append(self.print_matrix(d, source, target))
        
        result.append("\nStep 3: Compute Similarity Score\n")
        result.append(f"Levenshtein Distance: {distance}")
        result.append(f"Max Length of Words: {max_len}")
        result.append(f"Similarity Score = 1 - ({distance} / {max_len}) = {similarity:.4f}\n")
        result.append(f"The word '{source}' is {(similarity * 100):.2f}% morphologically similar for the '{target}' which is the lemma\n")
        result.append("===================================\n")
        
        return "\n".join(result)
    
    def show_lcs(self, source, target):
        m, n = len(source), len(target)
        prev = np.zeros(n + 1, dtype=int)
        
        result = []
        result.append("\n==== Longest Common Substring Process ====\n")
        result.append(f"Source: {source}")
        result.append(f"Target: {target}\n")
        
        result.append("Step 1: Initialize DP Table")
        max_len = max(m, n)
        res = 0  # Store max LCS length
        lcs_matrix = np.zeros((m + 1, n + 1), dtype=int)
        
        result.append("\nStep 2: Compute LCS Table\n")
        for i in range(1, m + 1):
            curr = np.zeros(n + 1, dtype=int)
            for j in range(1, n + 1):
                if source[i - 1] == target[j - 1]:
                    curr[j] = prev[j - 1] + 1
                    res = max(res, curr[j])
                else:
                    curr[j] = 0
                lcs_matrix[i][j] = curr[j]
            prev = curr
        
        # Display the LCS DP table
        result.append(self.print_matrix(lcs_matrix, source, target))
        
        # Normalize
        normalized_res = (res / max_len) if max_len > 0 else 1
        
        result.append("\nStep 3: Compute Similarity Score\n")
        result.append(f"Longest Common Substring Length: {res}")
        result.append(f"Max Length of Words: {max_len}")
        result.append(f"Similarity Score = ({res} / {max_len}) = {normalized_res:.4f}\n")
        result.append(f"The word '{source}' is {(normalized_res * 100):.2f}% morphologically similar for the '{target}' which is the lemma\n")
        result.append("===================================\n")
        
        return "\n".join(result)    

    def print_matrix(self, matrix, source, target):
        source = " " + source
        target = " " + target

        # Create the top border of the grid
        matrix_str = []
        top_border = "\t\t+" + ("\t-------" * len(target)) + "\t+"


        # Add the header row (target characters)
        header_row = "\t\t" + "\t".join(f"\t  {char}\t" for char in target) + "\t"
        matrix_str.append(header_row)
        matrix_str.append(top_border)

        # Add each row of the matrix with source characters
        for i, row in enumerate(matrix):
            row_str = f" {source[i]}\t\t" + "\t".join(f"\t{val:3}\t" for val in row) + "\t"
            matrix_str.append(row_str)
            matrix_str.append(top_border)

        return "\n".join(matrix_str)

    # Show the Lemma Ranking Based on the Available Lemmatizable Token
    def store_lemma_ranking_in_dict(self, lemmatizable_token, potential_lemmas):
        if not hasattr(self, "lemma_ranking_list"):
            self.lemma_ranking_list = {}  # Initialize if not exists

        # Store a copy of the DataFrame to prevent accidental modification
        sorted_lemmas = potential_lemmas.sort_values(by='Rank Scores', ascending=False)
        sorted_lemmas = sorted_lemmas.head(10)

        self.lemma_ranking_list[lemmatizable_token] = sorted_lemmas.copy()

    def show_lemma_ranking(self, lemmatizable_token):
        return self.lemma_ranking_list.get(lemmatizable_token, "Lemma not found")
            
   # =======================MAIN PROCESS OF LEMMATIZATION=======================

    def lemmatize(self, input_text):
        # Tokenized, Removed Stop Words and Validate the Input Text
        self.input = input_text
        self.tokenized = self.tokenize_input_text(input_text.lower())
        
        print('')
        print('=========================Tokenized Tagalog Text=========================')
        print("\nTokenized Input Text:")
        print(self.tokenized, "\n")
        print('========================================================================')
        print('')

        removed_sw = self.remove_stop_words(self.tokenized)
        print("After Removing Stop Words:")
        print(removed_sw, "\n")

        isValidated = self.validate_formal_tagalog(self.tokenized)
        self.valid_tokens = isValidated[2]
        self.invalid_tokens = isValidated[1]
        print('')
        print('=========================Validate Token if Formal Tagalog Word=========================')
        print("\nResult for Validating Formal Tagalog: ")
        print('Valid Tokens: ', isValidated[2])
        print('Invalid Tokens: ', isValidated[1], '\n')
        print('=======================================================================================')
        print('')

        print('')
        print('=================================Lemmatization Process=================================')
        while isValidated[0]:
            # Lemmatized Each Tokens and Return the Lemma after
            # print("About to lemmatize: ", self.to_lemmatize_tokens, "\n")
            for token in self.to_lemmatize_tokens:
                inf_input = token
                print("Token to Lem: ", token, "\n")
                print(self.list_of_lemmatizable_tokens)
                if self.to_lemmatize_tokens.index(token) not in self.not_to_lemmatize_tokens_index:

                    # The Current Token Should not be in Lemma Form in Order to Lemmatize
                    if self.isLemmaAlready(token) is False:
                        # Insert lemmatizable token
                        self.list_of_lemmatizable_tokens.append(token)

                        # Pre-processing Stage
                        morpheme = self.get_morpheme(token)
                        print("Extracted Morpheme: ", morpheme, "\n")

                        potential_lemmas = self.get_potential_lemmas(
                            token, morpheme)

                        print("Total Words in Dict: ", self.lemma_size)
                        print("Total Number of Potential Lemmas: ",
                              potential_lemmas.shape[0])
                        print("Potential Lemma/s: \n", potential_lemmas, "\n")

                        # Whenever there are no potential lemmas found, append the normal token instead
                        if potential_lemmas.empty:
                            best_lemma = token

                        # Storing morphem : potential lemmas key value pair
                        self.create_morpheme_to_potential_lemmas(morpheme, potential_lemmas)

                        
                        # Secret Move: If Letter D is Last
                        temp_token = token
                        if 'd' in token[-1]:
                            temp_token = self.alternate_morphophonemic_rd(token)

                        # Perform Fuzzy Matcing Algorithm to Lemmatize Token
                        fuzzy_potential_lemmas = self.fuzzy_matching(
                            temp_token, potential_lemmas)
                        
                        best_lemma = self.show_best_lemma(  
                            fuzzy_potential_lemmas)
                        
                        self.store_lemma_ranking_in_dict(token, fuzzy_potential_lemmas)
                        
                        self.create_source_to_target(token, best_lemma)
        
                        #self.show_cosine_similarity(token, best_lemma)
                        #self.show_lev_distance(token, best_lemma)

                        self.lemmatized_text.append(best_lemma)
                        self.lemma.append(best_lemma)
                        self.annotate(inf_input, best_lemma)
                        

                    else:
                        

                        self.lemmatized_text.append(token)
                else:
                    self.lemmatized_text.append(token)
            break

        temp = ''
        for word in self.lemmatized_text:
            temp += word + ' '

        self.result = temp.strip()
        print('======================================================================================')
        print('')
        print(
            "==================================LEMMATIZATION===============================")
        print("\nInput Tagalog Text: ", self.input)
        print("\nLemmatized Text: ", self.result)
        print(
            "==============================================================================")
        self.result_removed_sw = self.remove_stop_words(self.lemmatized_text)
        #self.lemmatized_text = []

    @lru_cache(maxsize=None)
    def lemmatize_no_print(self, input_text):

        # Tokenized, Removed Stop Words and Validate the Input Text
        self.input = input_text
        self.tokenized = self.tokenize_input_text(input_text.lower())

        removed_sw = self.remove_stop_words(self.tokenized)

        isValidated = self.validate_formal_tagalog(self.tokenized)
        self.valid_tokens = isValidated[2]
        self.invalid_tokens = isValidated[1]
        while isValidated[0]:
            # Lemmatized Each Tokens and Return the Lemma after
            # print("About to lemmatize: ", self.to_lemmatize_tokens, "\n")
            for token in self.to_lemmatize_tokens:
                inf_input = token
                if self.to_lemmatize_tokens.index(token) not in self.not_to_lemmatize_tokens_index:

                    # The Current Token Should not be in Lemma Form in Order to Lemmatize
                    if True:
                        # Base variable for handling token
                        self.curr_token = token

                        self.list_of_lemmatizable_tokens.append(token)

                        # Pre-processing Stage
                        morpheme = self.get_morpheme_of_inf(token)
                        
                        potential_lemmas = self.get_potential_lemmas(
                            token, morpheme)

                        # Whenever there are no potential lemmas found, append the normal token instead
                        if potential_lemmas.empty:
                            best_lemma = token

                         # Storing morpheme : potential lemmas key value pair
                        self.create_morpheme_to_potential_lemmas(morpheme, potential_lemmas)

                        # Secret Move: If Letter D is Last
                        temp_token = token
                        if 'd' in token[-1]:
                            temp_token = self.alternate_morphophonemic_rd(token)

                        # Perform Fuzzy Matcing Algorithm to Lemmatize Token
                        fuzzy_potential_lemmas = self.fuzzy_matching(
                            temp_token, potential_lemmas)
                        
                        best_lemma, temp_fp_lemmas = self.show_best_lemma(
                            fuzzy_potential_lemmas)
                        
                        self.store_lemma_ranking_in_dict(token, temp_fp_lemmas)
                            
                        self.create_source_to_target(token, best_lemma)
                        #self.show_cosine_similarity(token, best_lemma)
                        self.lemmatized_text.append(best_lemma)
                        self.lemma.append(best_lemma)
                        self.annotate(inf_input, best_lemma)
                    else:
                        self.lemmatized_text.append(token)

                else:
                    self.lemmatized_text.append(token)

            break
        temp = ''
        for word in self.lemmatized_text:
            temp += word + ' '

        self.result = temp.strip()

        self.result_removed_sw = self.remove_stop_words(self.lemmatized_text)
        # self.lemmatized_text = []

        return (self.result, self.lemma, self)

    def exclude_invalid(self):
        result = []
        for token in self.lemmatized_text:
            if token in self.formal_words:
                result.append(token)
        return result

if __name__ == "__main__":
    t = TagLemma()
    str_input = "kumakain kumakain tumakbo tumakbo"
    t.load_lemma_to_dfame('dataset/tagalog_lemmas.txt')
    t.load_formal_tagalog('dataset/formal_tagalog.txt')
    t.lemmatize(str_input)
    #print(t.show_annotation())
    #print(t.show_inflection_and_morpheme())
    #print(t.result_removed_sw)
    #print(t.exclude_invalid())

    """print("List of lemmatizable tokens: ")
    print(t.list_of_lemmatizable_tokens)
    print("List of Morphemes based on Lemmatizable Tokens")
    print(t.list_of_morphemes)
    print("Potential lemmas of kumakain based on its approximate morpheme pattern")"""
    