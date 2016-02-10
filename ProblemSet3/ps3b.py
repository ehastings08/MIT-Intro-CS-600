# 6.00 Problem Set 3A Solutions
#
# The 6.00 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
# Implemented by: Ellie Hastings
#

import random
import string
import time
from perm import *


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
    if word not in word_list:
        #print 'You have played an invalid word.'
        return False
    
    # 2. Is the word length <= hand length?
    for letter in hand.keys():
        hand_length += hand[letter]
        
    if len(word) > hand_length:
        return False
        #print 'Error: You have played more letters than you have in your hand!'
    else:
    # 3. Is the word valid from hand?
        for letter in word_dict.keys():
            if letter not in hand:
                return False
                #print 'Error: You have played a letter that is not in your hand!'
            elif word_dict[letter] > hand[letter]:
                return False
                #print 'Error: You have played more letters than you have available in your hand'
            elif letter in hand and word_dict[letter] <= hand[letter]:
                return True

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
    # Set total score
    total_score = 0
    
    # Check original hand length
    orig_hand_len = calculate_handlen(hand)

    # Check for validity, calculate score, and ask user to input another word
    # Continue until there are no unused letters OR user inputs string '.'
    while calculate_handlen(hand) > 0:
        print 'Current hand: ', 
        display_hand(hand)
        word = raw_input('Enter word, or a "." to indicate that you are finished: ')
        if word == '.':
            print 'Total score is: ',total_score
            return
        else:
            isValid = is_valid_word(word, hand, word_list)
            if not isValid:
                print 'Please choose a valid word.'
            else:
                word_score = get_word_score(word, HAND_SIZE)
                total_score += word_score
                print '"%s" earned %d points. Total: %d' % (word, word_score, total_score)
                hand = update_hand(hand, word)
    print 'No more letters. Total score: %d' % (total_score)


#
# Problem #5: Playing a game
# Make sure you understand how this code works!
# 
def play_game(word_list):
    """
    Allow the user to play an arbitrary number of hands.

    * Asks the user to input 'n' or 'r' or 'e'.

    * If the user inputs 'n', let the user play a new (random) hand.
      When done playing the hand, ask the 'n' or 'e' question again.

    * If the user inputs 'r', let the user play the last hand again.

    * If the user inputs 'e', exit the game.

    * If the user inputs anything else, ask them again.
    """
    # TO DO...
    
    hand = deal_hand(HAND_SIZE) # random init
    
    while True:
        input = raw_input('Please enter "n" for new hand, "r" for last hand, or "e" for exit. >> ')
        if input == 'n':
            hand = deal_hand(HAND_SIZE)
            play_hand(hand.copy(), word_list)
            print
        elif input == 'r':
            play_hand(hand.copy(), word_list)
            print
        elif input == 'e':
            break
        else:
            print 'Please enter a valid letter'


            
            
#
# Start Problem Set 3b
# 


#
#
# Problem #6A: Computer chooses a word
#
#
def comp_choose_word(hand, word_list):
    """
	Given a hand and a word_dict, find the word that gives the maximum value score, and return it.
   	This word should be calculated by considering all possible permutations of lengths 1 to HAND_SIZE.

    hand: dictionary (string -> int)
    word_list: list (string)
    """
    
    print 'hand is :',
    display_hand(hand)
    hand_len = calculate_handlen(hand)
    perms_list = []
    
    # First, get permutations of the hand. Use get_perms(hand,1 thru n) to do this
    # Keep in mind that you need to mutate n!
    for n in range(0,hand_len):
        perms_list += get_perms(hand,n)
    
    # Set variables for highest word + score
    highest_word = None
    highest_score = 0
    
    # Next, for each permutation check to see if 1) it is valid (in word list)
    # and 2) what the score is. Keep a score_dict.
    # print 'Computer is choosing a word...'
    
    for perm in perms_list:
        if is_valid_word(perm,hand,word_list):
            word_score = get_word_score(perm, hand_len)
            if word_score >= highest_score:
                highest_score = word_score
                highest_word = perm
    
    return highest_word
#
# Problem #6B: Computer plays a hand
#
def comp_play_hand(hand, word_list):
    """
     Allows the computer to play the given hand, as follows:
     * The hand is displayed.
     * The computer chooses a word using comp_choose_words(hand, word_list).
     * After every valid word: the score for that word is displayed, 
       the remaining letters in the hand are displayed, and the computer 
       chooses another word.
     * The sum of the word scores is displayed when the hand finishes.
     * The hand finishes when the computer has exhausted its possible choices (i.e. comp_play_hand returns None).

     hand: dictionary (string -> int)
     word_list: list (string)
    """
    
    orig_hand_len = calculate_handlen(hand)
    comp_total_score = 0
    
    while calculate_handlen(hand) > 0:
        # Hand is displayed
        print 'Computer\'s current hand:', display_hand(hand)
    
        # Computer chooses word, score for hand is displayed, and computer chooses another word
        print 'Computer is choosing a word.'
        word = comp_choose_word(hand, word_list)
        if word == None:
            print 'No options left. Computer finishes turn.'
            print 'Total score: %d' % (comp_total_score)
            break
        else:
            print 'Computer chooses: %s' % (word)
            comp_total_score += get_word_score(word, orig_hand_len)    
            hand = update_hand(hand, word)
            print 'Total score: %d' % (comp_total_score)
#
# Problem #6C: Playing a games
#
#
def play_game(word_list):
    """Allow the user to play an arbitrary number of hands.

    1) Asks the user to input 'n' or 'r' or 'e'.
    * If the user inputs 'n', play a new (random) hand.
    * If the user inputs 'r', play the last hand again.
    * If the user inputs 'e', exit the game.
    * If the user inputs anything else, ask them again.

    2) Ask the user to input a 'u' or a 'c'.
    * If the user inputs 'u', let the user play the game as before using play_hand.
    * If the user inputs 'c', let the computer play the game using comp_play_hand (created above).
    * If the user inputs anything else, ask them again.

    3) After the computer or user has played the hand, repeat from step 1

    word_list: list (string)
    """
    # TO DO...
        
    # Step 1 - User hand
    hand = deal_hand(HAND_SIZE) # random init
    play_hand(hand, word_list)
            
    while True:
        input = raw_input('Please enter "u" for user hand, "c" for computer hand: ')
        if input not in ['u','c']:
            print 'Please enter a valid letter'
        elif input == 'u':
            play_hand(deal_hand(HAND_SIZE), word_list)
        elif input == 'c':
            comp_play_hand(deal_hand(HAND_SIZE), word_list)
            
            
#
# Build data structures used for entire session and play game
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
    
# word_list = load_words()    
# print comp_choose_word(deal_hand(7), word_list)
# print comp_play_hand(deal_hand(7),word_list)
# print play_hand(deal_hand(7),word_list)