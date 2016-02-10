# 6.00 Problem Set 4
#
# Caesar Cipher Skeleton
#

import string
import random

WORDLIST_FILENAME = "words.txt"

# -----------------------------------
def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print "  ", len(wordlist), "words loaded."
    return wordlist

wordlist = load_words()

def is_word(wordlist, word):
    """
    Determines if word is a valid word.

    wordlist: list of words in the dictionary.
    word: a possible word.
    returns True if word is in wordlist.

    Example:
    >>> is_word(wordlist, 'bat') returns
    True
    >>> is_word(wordlist, 'asdf') returns
    False
    """
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in wordlist

def random_word(wordlist):
    """
    Returns a random word.

    wordlist: list of words  
    returns: a word from wordlist at random
    """
    return random.choice(wordlist)

def random_string(wordlist, n):
    """
    Returns a string containing n random words from wordlist

    wordlist: list of words
    returns: a string of random words separated by spaces.
    """
    return " ".join([random_word(wordlist) for _ in range(n)])

def random_scrambled(wordlist, n):
    """
    Generates a test string by generating an n-word random string
    and encrypting it with a sequence of random shifts.

    wordlist: list of words
    n: number of random words to generate and scamble
    returns: a scrambled string of n random words


    NOTE:
    This function will ONLY work once you have completed your
    implementation of apply_shifts!
    """
    s = random_string(wordlist, n) + " "
    shifts = [(i, random.randint(0, 26)) for i in range(len(s)) if s[i-1] == ' ']
    return apply_shifts(s, shifts)[:-1]

def get_fable_string():
    """
    Returns a fable in encrypted text.
    """
    f = open("fable.txt", "r")
    fable = str(f.read())
    f.close()
    return fable


# -----------------------------------

#
# Problem 1: Encryption
#
def build_encoder(shift):
    """
    Returns a dict that can apply a Caesar cipher to a letter.
    The cipher is defined by the shift value. Ignores non-letter characters
    like punctuation and numbers.

    shift: -27 < int < 27
    returns: dict

    Example:
    >>> build_encoder(3)
    {' ': 'c', 'A': 'D', 'C': 'F', 'B': 'E', 'E': 'H', 'D': 'G', 'G': 'J',
    'F': 'I', 'I': 'L', 'H': 'K', 'K': 'N', 'J': 'M', 'M': 'P', 'L': 'O',
    'O': 'R', 'N': 'Q', 'Q': 'T', 'P': 'S', 'S': 'V', 'R': 'U', 'U': 'X',
    'T': 'W', 'W': 'Z', 'V': 'Y', 'Y': 'A', 'X': ' ', 'Z': 'B', 'a': 'd',
    'c': 'f', 'b': 'e', 'e': 'h', 'd': 'g', 'g': 'j', 'f': 'i', 'i': 'l',
    'h': 'k', 'k': 'n', 'j': 'm', 'm': 'p', 'l': 'o', 'o': 'r', 'n': 'q',
    'q': 't', 'p': 's', 's': 'v', 'r': 'u', 'u': 'x', 't': 'w', 'w': 'z',
    'v': 'y', 'y': 'a', 'x': ' ', 'z': 'b'}
    (The order of the key-value pairs may be different.)
    I have eliminated spaces so this works purely on alpha chars.
    """
    # note - string splitting on encoded text isn't working when you encode spaces
    
    assert shift >= 0 and shift < 27, 'shift %s is not between 0 and 27' % shift
    
    dict = {}
    
    # First, get alphabetical strings
    lower_alpha = string.ascii_lowercase
    upper_alpha = string.ascii_uppercase
    
    shifted_lowercase = lower_alpha[shift:] + lower_alpha[:shift]
    shifted_uppercase = upper_alpha[shift:] + upper_alpha[:shift]
    
    for i in range(len(upper_alpha)):
        dict[upper_alpha[i]] = shifted_uppercase[i]

    for i in range(len(lower_alpha)):
        dict[lower_alpha[i]] = shifted_lowercase[i]

    return dict

def apply_coder(text, coder):
    """
    Applies the coder to the text. Returns the encoded text.

    text: string
    coder: dict with mappings of characters to shifted characters
    returns: text after mapping coder chars to original text

    Example:
    >>> apply_coder("Hello, world!", build_encoder(3))
    'Khoor, czruog!'
    >>> apply_coder("Khoor, czruog!", build_decoder(3))
    'Hello, world!'
    """
    
    # Set an output string
    output_text = ''
    
    for char in text:
        if char in coder:
            output_text += coder[char]
        else:
            output_text += char
        
    return output_text 

def apply_shift(text, shift):
    """
    Given a text, returns a new text Caesar shifted by the given shift
    offset. The empty space counts as the 27th letter of the alphabet,
    so spaces should be replaced by a lowercase letter as appropriate.
    Otherwise, lower case letters should remain lower case, upper case
    letters should remain upper case, and all other punctuation should
    stay as it is.
    
    text: string to apply the shift to
    shift: amount to shift the text
    returns: text after being shifted by specified amount.

    Example:
    >>> apply_shift('This is a test.', 8)
    'Apq hq hiham a.'
    """
    assert shift >= 0 and shift <= 27, 'shift %d is not between -0 and 27'
    return apply_coder(text, build_encoder(shift))
   
#
# Problem 2: Codebreaking.
#
def find_best_shift(wordlist, text):
    """
    Decrypts the encoded text and returns the plaintext.

    text: string
    returns: 0 <= int 27

    Example:
    >>> s = apply_coder('Hello, world!', build_encoder(8))
    >>> s
    'Pmttw,hdwztl!'
    >>> find_best_shift(wordlist, s) returns
    8
    >>> apply_coder(s, build_decoder(8)) returns
    'Hello, world!'
    """
    
    max_real_words = 0
    best_shift = 0
    
    for shift in range(27):
        shifted_text = apply_shift(text, 26-shift)
        shift_dict = build_encoder(26-shift)
        valid = 0.
        shifted_words = shifted_text.split() 
        for word in shifted_words:
            if is_word(wordlist, word):
                valid += 1
        if valid >= max_real_words:
            max_real_words = valid
            best_shift_value = shift
    return best_shift_value

# fable = get_fable_string()
# rand_int_choice = random.randint(1,27)   #CHANGE TO 27
# shifted_fable = apply_shift(fable, rand_int_choice)    #Apply a random shift
# print 'find_best_shift recommends: ',find_best_shift(wordlist, shifted_fable)
# print 'Actual random integer shift was %d' % (rand_int_choice)

 
