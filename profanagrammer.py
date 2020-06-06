import string

with open('profanities.txt') as f:
    all_words = f.read().splitlines()

with open('secondary_words.txt') as f:
    secondary_words = f.read().splitlines()

with open('input_words.txt', encoding="utf8") as f:
    input_words = f.read().splitlines()
    
input_words=list(set(input_words))#removes duplicates
input_words.sort(key=len)#do the short ones first, so that easy results aren't held up by an unreasonably long input word

unusedletters_reported=2
supress_repeats=True#can the same word be repeated with a profanagram? Enabling this speeds things up LOTS for long inputs

alphabet=string.ascii_lowercase

def word_to_letters (word):
    letters={}
    for letter in alphabet:
        letters[letter]=0
    for letter in word:
        if letter in alphabet:
            letters[letter]+=1
    return letters

def letters_required(word):
    #alphabet=string.ascii_lowercase
    word=word.lower()
    required={}
    for letter in alphabet:
        required[letter]=0
        for i in word: 
            if i == letter: 
                required[letter] += 1
    return required

def remove_impossible_words(words,letters):
    possible_words={}
    for word in words:
        required_letters=words[word]
        possible=True
        for letter in letters:
            available_letters=letters[letter]
            if available_letters<required_letters[letter]:
                possible=False
        if possible:
            possible_words[word]=words[word]
    return possible_words

def phrase_length(phrase):
    length=0
    for word in phrase:
        length+=len(word)
    return length

def find_unused_letters(letters,words):
    letter_count_in_dictionary={}
    for letter in letters:
        letter_count_in_dictionary[letter]=0

    for word in words:
        for letter in word:
            if letter in letters:
                letter_count_in_dictionary[letter]+=1

    unused_letters=[]
    for letter in letter_count_in_dictionary:
        if letter_count_in_dictionary[letter]==0:
            unused_letters.append(letter)
            
    return unused_letters

unused_letters=find_unused_letters (alphabet,all_words)   


def add_word(existing_phrase,dictionary,letters_available,interesting_length,secondary_words={}):
    progress=0
    words=list(dictionary.keys())
    for new_word in words:
        progress+=1
        #if(existing_phrase==[]):
            #print('\r'+str(100*progress/valid_word_count)[:6]+'%',end='')
        new_phrase=existing_phrase+[new_word]
        new_letters_available={}
        for letter in alphabet:
            new_letters_available[letter]=letters_available[letter]-dictionary[new_word][letter]
        new_remaining_words=dictionary
        new_remaining_words.update(secondary_words)#adds in the other words
        if supress_repeats:
            del(new_remaining_words[new_word])
        new_remaining_words=remove_impossible_words(new_remaining_words,new_letters_available)
        if len(new_remaining_words)>0:
            add_word(new_phrase,new_remaining_words,new_letters_available,interesting_length)
        else:
            if phrase_length(new_phrase) >= interesting_length:
                if sum(new_letters_available.values()) > 0:
                    left_over_letters=''
                    for letter in new_letters_available:
                        for i in range(new_letters_available[letter]):
                            left_over_letters+=letter
                    new_phrase+= [left_over_letters]
                if not supress_repeats:
                    new_phrase.sort()
                if new_phrase not in possible_phrases:
                    possible_phrases.append(new_phrase)

all_possible_phrases={}

for input_word in input_words:
    possible_phrases=[]
    letter_list=word_to_letters(input_word.lower())
      
    cleaned_words={}
    for word in all_words:
        cleaned_words[word]=letters_required(word)
    cleaned_words=remove_impossible_words(cleaned_words,letter_list)
    valid_word_count=len(cleaned_words)

    cleaned_sec_words={}
    for word in secondary_words:
        cleaned_sec_words[word]=letters_required(word)
    cleaned_sec_words=remove_impossible_words(cleaned_sec_words,letter_list)

    add_word([],cleaned_words,letter_list,sum(letter_list.values())-unusedletters_reported,secondary_words=cleaned_sec_words)

    if len(possible_phrases)>0:
        print(input_word)
        print(possible_phrases)
        all_possible_phrases[input_word]=possible_phrases


