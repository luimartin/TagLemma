""" 
	CONSTANTS 
"""
VOWELS = "aeiouAEIOU"
CONSONANTS = "bcdfghklmnngpqrstvwyBCDFGHKLMNNGPQRSTVWY"

""" 
	Affixes
"""
PREFIX_SET = [
	'nakikipag', 'pakikipag',
	'pinakama', 'pagpapa',
	'pinagka', 'panganga', 
	'makapag', 'nakapag', 
	'tagapag', 'makipag', 
	'nakipag', 'tigapag',
	'pakiki', 'magpa',
	'napaka', 'pinaka',
	'ipinag', 'pagka', 
	'pinag', 'mapag', 
	'mapa', 'taga', 
	'ipag', 'tiga', 
	'pala', 'pina', 
	'pang', 'naka',
	'nang', 'mang',
	'sing',
	'ipa', 'pam',
	'pan', 'pag',
	'tag', 'mai',
	'mag', 'nam',
	'nag', 'man',
	'may', 'ma',
	'na', 'ni',
	'pa', 'ka',
	'um', 'in',
	'i',
]

INFIX_SET = [
	'um', 'in',
]

SUFFIX_SET = [
	'syon','dor', 
	'ita', 'han', 
	'hin', 'ing', 
	'ang', 'ng', 
	'an', 'in', 
	'g',
]

PERIOD_FLAG = True
PASS_FLAG = False

def check_validation(token):
	with open('tagalog_roots.txt', 'r') as valid:
		data = valid.read().replace('\n', ' ').split(' ')
		# data = set([line.strip('\n') for line in valid.readlines()])

	return True if token in data else False

def check_vowel(letter):
    return letter in "aeiou"

def check_consonant(letter):
    return not check_vowel(letter)

def count_vowel(word):
    return sum(1 for char in word if check_vowel(char))

def count_consonant(word):
    return sum(1 for char in word if check_consonant(char))

def change_letter(word, index, new_letter):
    return word[:index] + new_letter + word[index + 1:]

def clean_duplication(token, DUPLICATE):

	if check_validation(token):
		return token

	if '-' in token and token.index('-') != 0 and \
		token.index('-') != len(token) -  1:

		split = token.split('-')

		if all(len(tok) >= 3 for tok in split):
			if split[0] == token[1] or split[0][-1] == 'u' and change_letter(split[0], -1, 'o') == split[1] or \
				split[0][-2] == 'u' and change_letter(split[0], -2, 'o')  == split[1]:
				DUPLICATE.append(split[0])
				return split[0]

			elif split[0] == split[1][0:len(split[0])]:
				DUPLICATE.append(split[1])
				return split[1]

			elif split[0][-2:] == 'ng':
				if split[0][-3] == 'u':
					if split[0][0:-3] + 'o' == split[1]:
						DUPLICATE.append(split[1])
						return split[1]

				if split[0][0:-2] == split[1]:
					DUPLICATE.append(split[1])
					return split[1]

		else:
			return '-'.join(split)
	
	return token


def clean_repitition(token, REPITITION):
	if check_validation(token):
		return token

	if len(token) >= 4:
		if check_vowel(token[0]):
			if token[0] == token[1]:
				REPITITION.append(token[0])
				return token[1:]

		elif check_consonant(token[0]) and count_vowel(token) >= 2:
			if token[0: 2] == token[2: 4] and len(token) - 2 >= 4:
				REPITITION.append(token[2:4])
				return token[2:]
			
			elif token[0: 3] == token[3: 6] and len(token) - 3 >= 4:
				REPITITION.append(token[3:6])
				return token[3:]

	return token


def clean_prefix(token,	 PREFIX):

	if check_validation(token):
		return token

	for prefix in PREFIX_SET:
		if len(token) - len(prefix) >= 3 and \
			count_vowel(token[len(prefix):]) >= 2:

			if prefix == ('i') and check_consonant(token[2]):
				continue

			if '-' in token:	
				token = token.split('-')

				if token[0] == prefix and check_vowel(token[1][0]):
					PREFIX.append(prefix)
					return token[1]

				token = '-'.join(token)

			if token[0: len(prefix)] == prefix:
				if count_vowel(token[len(prefix):]) >= 2:
					# if check_vowel(token[len(token) - len(prefix) - 1]):
				# 	continue

					if prefix == 'panganga':
						PREFIX.append(prefix)
						return 'ka' + token[len(prefix):]
					
					PREFIX.append(prefix)
					return token[len(prefix):]

	return token

 
def clean_infix(token, INFIX):

	if check_validation(token):
		return token

	for infix in INFIX_SET:
		if len(token) - len(infix) >= 3 and count_vowel(token[len(infix):]) >= 2:
			if token[0] == token[4] and token[1: 4] == infix:
				INFIX.append(infix)
				return token[4:]

			elif token[2] == token[4] and token[1: 3] == infix:
				INFIX.append(infix)
				return token[0] + token[3:]

			elif token[1: 3] == infix and check_vowel(token[3]):
				INFIX.append(infix)
				return token[0] + token[3:]

	return token


def clean_suffix(token, SUFFIX):

	SUF_CANDIDATE = []

	if check_validation(token):
		return token
	
	for suffix in SUFFIX_SET:
		if len(token) - len(suffix) >= 3 and count_vowel(token[0:len(token) - len(suffix)]) >= 2:
			if token[len(token) - len(suffix): len(token)] == suffix:
				if len(suffix) == 2 and not count_consonant(token[0:len(token) - len(suffix)]) >= 1:
					continue

				if count_vowel(token[0: len(token) - len(suffix)]) >= 2:
					if suffix == 'ang' and check_consonant(token[-4]) \
						and token[-4] != 'r' and token[-5] != 'u':
						continue

					# if check_vowel(suffix[0]) and check_consonant(token[len])

					print(token[0: len(token) - len(suffix)] + " : " + suffix)

					if check_validation(token[0: len(token) - len(suffix)]):
						SUFFIX.append(suffix)
						return token[0: len(token) - len(suffix)] + 'a' if SUFFIX == 'ita' \
							else  token[0: len(token) - len(suffix)]

					elif len(SUF_CANDIDATE) == 0:
						SUF_CANDIDATE.append(suffix)
						SUF_CANDIDATE.append(token[0: len(token) - len(suffix)])

	if(len(SUF_CANDIDATE) == 2):
		SUFFIX = SUF_CANDIDATE[0]
		return SUF_CANDIDATE[1][0: len(token) - len(suffix)] + 'a' if SUFFIX == 'ita' \
			else  SUF_CANDIDATE[1][0: len(token) - len(suffix)]

	return token

def check_vowel(substring):
	return all(letter in VOWELS for letter in substring)


def check_consonant(substring):
	return all(letter in CONSONANTS for letter in substring)

def count_vowel(token):
	count = 0

	for tok in token:
		if check_vowel(tok):
			count+=1

	return count


def count_consonant(token):
	count = 0

	for tok in token:
		if check_consonant(tok):
			count+=1

	return count


def change_letter(token, index, letter):
	_list = list(token)
	_list[index] = letter

	return ''.join(_list)


def clean_stemmed(token, CLEANERS, REPITITION):

	global PERIOD_FLAG
	global PASS_FLAG

	CC_EXP = ['dr', 'gl', 'gr', 'ng', 'kr', 'kl', 'kw', 'ts', 'tr', 'pr', 'pl', 'pw', 'sw', 'sy'] # Consonant + Consonant Exceptions

	if token[-1] == '.' and PASS_FLAG == False:
		PERIOD_FLAG = True

	if not check_vowel(token[-1]) and not check_consonant(token[-1]):
		CLEANERS.append(token[-1])
		token = token[0:-1]

	if not check_vowel(token[0]) and not check_consonant(token[0]):
		CLEANERS.append(token[0])
		token = token[1:]

	if check_validation(token):
		return token

	if len(token) >= 3 and count_vowel(token) >= 2:
		token = clean_repitition(token,	REPITITION)

		if check_consonant(token[-1]) and token[- 2] == 'u':
			CLEANERS.append('u')
			token = change_letter(token, -2, 'o')

		if token[len(token) - 1] == 'u':
			CLEANERS.append('u')
			token = change_letter(token, -1, 'o')

		if token[-1] == 'r':
			CLEANERS.append('r')
			token = change_letter(token, -1, 'd')

		if token[-1] == 'h' and check_vowel(token[-1]):
			CLEANERS.append('h')
			token = token[0:-1]

		# if token[0] == 'i':
		# 	token = token[1:]

		if token[0] == token[1]:
			CLEANERS.append(token[0])
			token = token[1:]

		if (token[0: 2] == 'ka' or token[0: 2] == 'pa') and check_consonant(token[2]) \
			and count_vowel(token) >= 3:
			
			CLEANERS.append(token[0: 2])
			token = token[2:]

		if(token[-3:]) == 'han' and count_vowel(token[0:-3]) == 1:
			CLEANERS.append('han')
			token = token[0:-3] + 'i'

		if(token[-3:]) == 'han' and count_vowel(token[0:-3]) > 1:
			CLEANERS.append('han')
			token = token[0:-3]

		if len(token) >= 2 and count_vowel(token) >= 3:
			if token[-1] == 'h' and check_vowel(token[-2]):
				CLEANERS.append('h')
				token = token[0:-1]

		if len(token) >= 6 and token[0:2] == token[2:4]:
			CLEANERS.append('0:2')
			token = token[2:]

		if any(REP[0] == 'r' for REP in REPITITION):
			CLEANERS.append('r')
			token = change_letter(token, 0, 'd')

		if token[-2:] == 'ng' and token[-3] == 'u':
			CLEANERS.append('u')
			token = change_letter(token, -3, 'o')

		if token[-1] == 'h':
			CLEANERS.append('h')
			token = token[0:-1]

		if any(token[0:2] != CC for CC in CC_EXP) and check_consonant(token[0:2]):
			CLEANERS.append(token[0:2])
			token = token[1:]

	return token


def get_morpheme(token):
    global PERIOD_FLAG, PASS_FLAG

    # Ensure flags are reset at the start
    PASS_FLAG = False
    PERIOD_FLAG = False

    PREFIX = []
    INFIX = []
    SUFFIX = []
    DUPLICATE = []
    REPITITION = []
    CLEANERS = []

    print(f"Processing word: {token}")

    if (PERIOD_FLAG and token[0].isupper()) or (not PERIOD_FLAG and token[0].islower()):
        token = token.lower()

        # First pass
        du1_stem = clean_duplication(token, DUPLICATE)
        pre_stem = clean_prefix(du1_stem, PREFIX)
        rep_stem = clean_repitition(pre_stem, REPITITION)
        inf_stem = clean_infix(rep_stem, INFIX)
        rep_stem = clean_repitition(inf_stem, REPITITION)
        suf_stem = clean_suffix(rep_stem, SUFFIX)
        du2_stem = clean_duplication(suf_stem, DUPLICATE)
        cle_stem = clean_stemmed(du2_stem, CLEANERS, REPITITION)
        cle_stem = clean_duplication(cle_stem, DUPLICATE)

        # Remove hyphen if present
        cle_stem = cle_stem.replace('-', '')

        print(f"First pass result: {cle_stem}")

        # Second pass if validation fails
        if not check_validation(cle_stem):
            print("Validation failed. Performing second pass...")
            PASS_FLAG = True
            du1_stem = clean_duplication(cle_stem, DUPLICATE)
            pre_stem = clean_prefix(du1_stem, PREFIX)
            rep_stem = clean_repitition(pre_stem, REPITITION)
            inf_stem = clean_infix(rep_stem, INFIX)
            rep_stem = clean_repitition(inf_stem, REPITITION)
            suf_stem = clean_suffix(rep_stem, SUFFIX)
            du2_stem = clean_duplication(suf_stem, DUPLICATE)
            cle_stem = clean_stemmed(du2_stem, CLEANERS, REPITITION)
            cle_stem = clean_duplication(cle_stem, DUPLICATE)


    else:
        PERIOD_FLAG = False
        cle_stem = clean_stemmed(token, CLEANERS, REPITITION)

    # Do NOT reset PERIOD_FLAG and PASS_FLAG at the end
    return cle_stem


