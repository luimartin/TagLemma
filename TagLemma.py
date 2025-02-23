import numpy as np
import pandas as pd
from collections import Counter
import math
import re

class TagLemma:
    def __init__(self): 
        self.PREFIX_SET = [
            'nakikipag', 'panganga','makapag', 
            'nakapagpa', 'nakapag', 'nakipag', 'tigapag', 
            'napaka', 'pinaka', 'ipinag', 'pinag',
            'tiga', 'pang', 'pinakipag','pakipag', 'pagka',  'pag', 'pa',
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
            'gusto', 'habang', 'hanggang', 'hindi', 'huwag', 'iba',
            'ibaba', 'ibabaw', 'ibig', 'ikaw', 'ilan', 'inyong', 'isa',
            'ito', 'iyo', 'iyon', 'iyong', 'ka', 'kahit', 'kailanman', 'kami', 
            'kanino', 'kanya', 'kanyang', 'kapag', 'katulad', 'kaya', 'kaysa', 'ko', 'kong', 'kulang', 'kung', 'lahat',
            'lamang', 'likod', 'lima', 'maging',
            'masyado', 'may', 'mayroon', 'mga', 'minsan', 'mismo', 'mula', 'muli', 'na',
            'naging', 'nais', 'nakita', 'namin', 'napaka', 'narito', 'nasaan',
            'ng', 'ngayon', 'ni', 'nila', 'nilang', 'nito', 'niya', 'niyang', 'noon', 'o', 'pa', 'pang'
            'panahon', 'pangalawa', 'para', 'paraan', 'pareho', 'pero',
            'sa', 'saan', 'sarili', 'sila', 'sino', 'siya', 'tatlo', 'tayo',
            'tulad', 'tungkol', 'una', 'walang', 'ba', 'eh','kasi', 'lang','mo','naman','opo','po','si','talaga',
            'yung', 'pwede', 'pwede', 'uli', 'makita', 'noong', 'nasa' 
        ]

        self.raw_lemmas = None
        self.lemma_size = None
        self.formal_words = None
        self.to_lemmatize_tokens = None
        self.not_to_lemmatize_tokens_index = None
        self.morpheme = None
        self.potential_lemmas = None
        self.lemmatized_text = [] 
        self.valid_tokens = None #forda UI
        self.lemma = [] #forda UI
        self.input, self.result = '', ''
    
    # =======================LOADING OF FILES=======================
    def load_lemma_to_dfame(self, file_path):
        with open(file_path, 'r') as file:
            lines = [line.strip() for line in file]
        
        df = pd.DataFrame(lines, columns=['WORDS'])
        
        self.raw_lemmas = df
        self.lemma_size = df.shape[0]
    
    def load_formal_tagalog(self, file_path):
        with open(file_path, 'r') as file:
            file_contents = file.read()
        
        self.formal_words = file_contents.split()

    # =======================MAIN ARCHITECTURE HERE=======================
    
    # =======================PRE-PROCESSING=======================
    def tokenize_input_text(self, input_text):
        tokens = re.findall(r'\w+', input_text)
        
        return tokens
    
    def remove_stop_words(self, input_tokens):
        return [token for token in input_tokens if token not in self.STOP_WORDS]
    
    # The Text Input must be Formal Tagalog Format, 
    # One Informal means Failure to Proceed to Lemmatized the Whole Text
    def validate_formal_tagalog(self, final_tokens):
        self.to_lemmatize_tokens = final_tokens
        self.not_to_lemmatize_tokens_index = [final_tokens.index(token) for token in final_tokens if token not in self.formal_words and self.STOP_WORDS]

        # Show the Element Using the Identified Index
        unable_to_lemmatize = []
        for indx in self.not_to_lemmatize_tokens_index:
            unable_to_lemmatize.append(self.to_lemmatize_tokens[indx])

        # Show the Element that can be lemmatize
        able_to_lemmatize = [token for token in self.to_lemmatize_tokens if self.to_lemmatize_tokens.index(token) not in self.not_to_lemmatize_tokens_index]

        # if len(missing_tokens) >= 1: return (False, 'FAILED! Unable to Lemmatized the Input Text')        
        
        return (True, unable_to_lemmatize, able_to_lemmatize)
     
    # To Check Whether the Input Text is Alreadly A Lemma
    # You know, to Avoid Unecessary Further Procedure and Reduce Search Space Complexity 
    def isLemmaAlready(self, token):
        if token in self.raw_lemmas['WORDS'].values: return True

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
            deduplicated_word_non_first_syl, is_duplicated_non_first_syl = self.remove_duplication_non_first_syl(deduplicated_word)

            if not is_duplicated_non_first_syl:
                # A Word without Deduplication at the First and Non-First Syllable must be Remove the Affxes First, 
                # then Proceed to Stripping of Deduplication
                morpheme_word = self.remove_one_affix(deduplicated_word_non_first_syl)
                morpheme_word, _temp = self.remove_duplication_non_first_syl(morpheme_word)
            else:
                morpheme_word = self.remove_one_affix(deduplicated_word_non_first_syl)
    
        else:
            morpheme_word = deduplicated_word

        self.morpheme = morpheme_word

        return morpheme_word

    # Reduce the Search Space by Using the Extracted Morpheme of the Word
    def reduce_search_space(self, word, pattern):
        # Patterns for Getting the Potential Lemmas
        regex_pattern = ".*".join(list(pattern))
        regex_pattern_rd = []
        regex_pattern_uo = []
        regex_pattern_mn = []
        
        # Alternate Morphophonemic System 
        if 'r' or 'd' in word:
            regex_pattern_rd = ".*".join(list(self.alternate_morphophonemic_rd(pattern)))
        
        if 'u' or 'o' in word: 
            regex_pattern_uo = ".*".join(list(self.alternate_morphophonemic_uo(pattern)))

        if 'm' or 'n' in word:     
            regex_pattern_mn = ".*".join(list(self.alternate_morphophonemic_mn(pattern)))

        # Combined All the Potential Lemmas Using All the Possible Alternate Morphophonemic Word
        combined_regex_pattern = f"({regex_pattern}|{regex_pattern_rd}|{regex_pattern_uo}|{regex_pattern_mn})"
        
        return bool(re.search(combined_regex_pattern, word))
    
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

        dot_product = sum(source_vec[key] * target_vec[key] for key in source_vec if key in target_vec)
        magnitude1 = math.sqrt(sum([val**2 for val in source_vec.values()]))
        magnitude2 = math.sqrt(sum([val**2 for val in target_vec.values()]))

        if magnitude1 == 0 or magnitude2 == 0: return 0.0

        return dot_product / (magnitude1 * magnitude2)
    
    # Unused, but it can be in the Future
    def sqrt_cosine_similarity(self, source, target):
        source_vec = Counter(source)
        target_vec = Counter(target)

        dot_product = math.sqrt(sum(source_vec[key] * target_vec[key] for key in source_vec if key in target_vec))
        magnitude1 = math.sqrt(sum([val for val in source_vec.values()]))
        magnitude2 = math.sqrt(sum([val for val in target_vec.values()]))

        if magnitude1 == 0 or magnitude2 == 0: return 0.0

        return dot_product / (magnitude1 * magnitude2)
    
    # Cosine Distance Function
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
                d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + cost)

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
        potential_lemmas['Cosine Similarity'] = potential_lemmas['WORDS'].apply(lambda x: self.cosine_similarity(token, x))
        potential_lemmas['Cosine Distance'] = potential_lemmas['WORDS'].apply(lambda x: self.cosine_distance_percentage(token, x))
        potential_lemmas['LCS'] = potential_lemmas['WORDS'].apply(lambda x: self.longestCommonSubstr(token, x))
        potential_lemmas['Jaccard'] = potential_lemmas['WORDS'].apply(lambda x: self.jaccardIndex(token, x))
        potential_lemmas['Levenshtein'] = potential_lemmas['WORDS'].apply(lambda x: self.levenshtein_distance(token, x))

        # Ranks the Fuzzy Matched Lemmas
        potential_lemmas['Rank Scores'] = (
            (.30 * potential_lemmas['Cosine Similarity']) + 
            (.20 * potential_lemmas['Cosine Distance']) + 
            (.15 * potential_lemmas['LCS']) +
            (.20 * potential_lemmas['Jaccard']) + 
            (.15 * potential_lemmas['Levenshtein'])
        )

        threshold_potential_lemmas = potential_lemmas[
            (potential_lemmas['Cosine Similarity'] >= 0.80)
        ]
    
        return threshold_potential_lemmas
    
    def show_best_lemma(self, potential_lemmas):
        if not potential_lemmas.empty: 
            sorted_lemmas = potential_lemmas.sort_values(by='Rank Scores', ascending=False)
            sorted_lemmas = sorted_lemmas.head(10)
            print("Rank ed Scored Lemmas: ", sorted_lemmas)
            return sorted_lemmas.iloc[0]['WORDS']

        return self.morpheme
        
   # =======================MAIN PROCESS OF LEMMATIZATION=======================
    def lemmatize(self, input_text):
        # Tokenized, Removed Stop Words and Validate the Input Text
        self.input = input_text
        tokenized = self.tokenize_input_text(input_text.lower())
        print('')
        print('=========================Tokenized Tagalog Text=========================')
        print("\nTokenized Input Text:")
        print(tokenized, "\n")
        print('========================================================================')
        print('')
        
        """removed_sw = self.remove_stop_words(tokenized) 
        print("After Removing Stop Words:")
        print(removed_sw, "\n")
        """
    
        isValidated = self.validate_formal_tagalog(tokenized)
        self.valid_tokens = isValidated[2]
        print(type(self.valid_tokens))
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
            #print("About to lemmatize: ", self.to_lemmatize_tokens, "\n")
            for token in self.to_lemmatize_tokens:  
                print("Token to Lem: ", token, "\n")

                if self.to_lemmatize_tokens.index(token) not in self.not_to_lemmatize_tokens_index:

                    # The Current Token Should not be in Lemma Form in Order to Lemmatize
                    if self.isLemmaAlready(token) is False:
                        # Pre-processing Stage
                        morpheme = self.get_morpheme(token)
                        print("Extracted Morpheme: ", morpheme, "\n")
                        
                   
                        potential_lemmas = self.get_potential_lemmas(token, morpheme)
                        print("Total Words in Dict: ", self.lemma_size)
                        print("Total Number of Potential Lemmas: ", potential_lemmas.shape[0])
                        print("Potential Lemma/s: \n", potential_lemmas, "\n")

                        # Whenever there are no potential lemmas found, append the normal token instead
                        if potential_lemmas.empty: best_lemma = token
                        
                        # Secret Move: If Letter D is Last
                        if 'd' in token[-1]:
                            token = self.alternate_morphophonemic_rd(token)

                        # Perform Fuzzy Matcing Algorithm to Lemmatize Token
                        fuzzy_potential_lemmas = self.fuzzy_matching(token, potential_lemmas)
                        best_lemma = self.show_best_lemma(fuzzy_potential_lemmas)

                        self.lemmatized_text.append(best_lemma)
                        self.lemma.append(best_lemma)
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
        print("==================================LEMMATIZATION===============================")
        print("\nInput Tagalog Text: ", self.input)
        print("\nLemmatized Text: ", self.result)
        print("==============================================================================")

        self.lemmatized_text = []


    def lemmatize_no_print(self, input_text):
            # Tokenized, Removed Stop Words and Validate the Input Text
            self.input = input_text
            tokenized = self.tokenize_input_text(input_text.lower())
        
            isValidated = self.validate_formal_tagalog(tokenized)
            self.valid_tokens = isValidated[2]
            while isValidated[0]:
                # Lemmatized Each Tokens and Return the Lemma after
                #print("About to lemmatize: ", self.to_lemmatize_tokens, "\n")
                for token in self.to_lemmatize_tokens:  
                    if self.to_lemmatize_tokens.index(token) not in self.not_to_lemmatize_tokens_index:

                        # The Current Token Should not be in Lemma Form in Order to Lemmatize
                        if self.isLemmaAlready(token) is False:
                            # Pre-processing Stage
                            morpheme = self.get_morpheme(token)
                            potential_lemmas = self.get_potential_lemmas(token, morpheme)
                            # Whenever there are no potential lemmas found, append the normal token instead
                            if potential_lemmas.empty: best_lemma = token
                            
                            # Secret Move: If Letter D is Last
                            if 'd' in token[-1]:
                                token = self.alternate_morphophonemic_rd(token)

                            # Perform Fuzzy Matcing Algorithm to Lemmatize Token
                            fuzzy_potential_lemmas = self.fuzzy_matching(token, potential_lemmas)
                            best_lemma = self.show_best_lemma(fuzzy_potential_lemmas)

                            self.lemmatized_text.append(best_lemma)
                            self.lemma.append(best_lemma)
                        else:
                            self.lemmatized_text.append(token)

                    else:
                        self.lemmatized_text.append(token)
                    
                break            
            temp = ''
            for word in self.lemmatized_text:
                temp += word + ' '

            self.result = temp.strip()
            #self.lemmatized_text = []
            return(self.result, self.lemma)

