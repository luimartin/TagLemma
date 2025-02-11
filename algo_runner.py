import TagLemma

t = TagLemma.TagLemma()
 # Load All Resources for Lemmatization 
t.load_lemma_to_dfame('tagalog_lemmas.txt')
t.load_formal_tagalog('formal_tagalog.txt')

while True: 
    input_text = input("Enter Formal Tagalog Text to Lemmatize:")
    if input_text == '0': break
    t.lemmatize(input_text)
