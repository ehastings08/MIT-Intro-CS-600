# 6.00 Problem Set 3A Solutions
#
# The 6.00 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
# Implemented by: Ellie Hastings
#

import random
import string

# DEFINE GLOBALS
VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7
SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}
TOTAL_SCORE = 0

# -----------------------------------
# Helper code

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    Depending on the size of the word list, this function may take a while to finish.
    """
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print "  ", len(wordlist), "words loaded."
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.
    sequence: string or list 
    return: dictionary
    """
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

	The score for a word is the sum of the points for letters
	in the word multiplied by the length of the word, plus 50
	points if all n letters are used on the first go.

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string (lowercase letters)
    returns: int >= 0
    """

    # Set a score integer to add to and then output back
    score = 0
    
    # First calculate the individual character score
    for letter in word:
        score += SCRABBLE_LETTER_VALUES[letter]
    
    # Then multiply by the length
    score = score * len(word)
    
    # Then check to see if you get a 50 point bonus for using n letters
    if len(word) == n:
        score += 50
        
    return score
    
# Display_hand
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    for letter in hand.keys():
        for j in range(hand[letter]):
             print letter,              # print all on the same line
    print                               # print an empty line

#
# Make sure you understand how this function works and what it does!
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    At least n/3 the letters in the hand should be VOWELS.

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    hand={}
    num_vowels = n / 3
    
    for i in range(num_vowels):
        x = VOWELS[random.randrange(0,len(VOWELS))]
        hand[x] = hand.get(x, 0) + 1
        
    for i in range(num_vowels, n):    
        x = CONSONANTS[random.randrange(0,len(CONSONANTS))]
        hand[x] = hand.get(x, 0) + 1
        
    return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Assumes that 'hand' has all the letters in word.
	In other words, this assumes that however many times
	a letter appears in 'word', 'hand' has at least as
	many of that letter in it. 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    word_dict = get_frequency_dict(word)
    
    # Create a new hand as a copy of the old
    new_hand = {}
    
    for letter in hand.keys():
        # if letter is in word but not all letters are used, add key and value - n to new hand
        if letter in word:
            new_value = hand[letter] - word_dict[letter]
            # only add to the new hand if > 0
            if new_value > 0:
                new_hand[letter] = hand[letter] - word_dict[letter]
        # if letter is not in word, add key + value to new_hand
        if letter not in word:  
            new_hand[letter] = hand[letter]

    return new_hand
    
#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
    
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    """
    # TO DO...
    
    word_dict = get_frequency_dict(word)
    hand_length = 0

    # 1. Is the word in the word_list?
    if word in word_list:
        # print 'Word is in word list'
        ans1 = True
    else:  
        ans1 = False
        print 'You have played an invalid word.'
        
    # 2. Is the word length <= hand length?
    for letter in hand.keys():
        hand_length += hand[letter]
    
    if len(word) > hand_length:
        ans2 = False
        # print 'Error: You have played more letters than you have in your hand!'
    else:
        # print 'Word is the right length'
        ans2 = True
        
    # 3. Is the word valid from hand?
    for letter in word_dict.keys():
        # print 'Looping through letters; at letter: ',letter
        if letter not in hand:
            ans3 = False
            break
            # print 'Error: You have played a letter that is not in your hand!'
        elif word_dict[letter] > hand[letter]:
            ans3 = False
            break
            print 'Error: You have played more letters than you have available in your hand'
        # This code is the problem; ans3 is returning false
        elif letter in hand and word_dict[letter] <= hand[letter]:
            # print 'letter in hand? ',letter in hand
            # print 'word_dict[letter] <= hand[letter]?', word_dict[letter] <= hand[letter]
            ans3 = True
            # print 'Word is valid from hand'
            
    # print ans1,ans2,ans3
    # Return a Boolean as to whether hand is valid. If it is, True. If any of the 3 conditions
    # are not met, it will be False.
    return ans1 and ans2 and ans3

def calculate_handlen(hand):
    handlen = 0
    for v in hand.values():
        handlen += v
    return handlen

#
# Problem #4: Playing a hand
#
def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    * The user may input a word.
    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.
    * When a valid word is entered, it uses up letters from the hand.
    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.
    * The sum of the word scores is displayed when the hand finishes.
    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing a single
      period (the string '.') instead of a word.
      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      
    """
    global TOTAL_SCORE
    
    # Create a copy of the hand to update
    new_hand = hand
    
    # The hand is displayed
    display_hand(new_hand)
    
    # The user may input a word
    word = raw_input('Enter word, or a "." to indicate that you are finished: ',)
    
    # Check for validity, calculate score, and ask user to input another word
    # Continue until there are no unused letters OR user inputs string '.'
    if word == '.':
        print 'All done.'
        print 'Total score is: ',TOTAL_SCORE
    elif new_hand == {}:
        print 'All done.'
    elif is_valid_word(word, new_hand, word_list):
        # get word score
        word_score = get_word_score(word, HAND_SIZE)
        TOTAL_SCORE += word_score
        
        print '"'+word+'" earned '+str(word_score)+' points. Total: '+str(TOTAL_SCORE)
        
        new_hand = update_hand(new_hand, word)
        
        play_hand(new_hand, word_list)
    else:
        print 'Please enter a valid word'


word_list = load_words()
hand = {'a':1,'c':1,'i':2,'m':2,'z':1,'h':1}
# new_hand = hand
# word = "rapture"
# print update_hand(new_hand,word)    #Works correctly
# print is_valid_word(word, hand, word_list)    #Works correctly
play_hand(hand, word_list)
