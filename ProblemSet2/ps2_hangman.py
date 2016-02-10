# 6.00 Problem Set 3
# 
# Hangman
#


# -----------------------------------
# Helper code
import random
import string
import re

WORDLIST_FILENAME = "words.txt"

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
    wordlist = string.split(line)
    print "  ", len(wordlist), "words loaded."
    return wordlist

def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code
# -----------------------------------

# actually load the dictionary of words and point to it with 
# the wordlist variable so that it can be accessed from anywhere
# in the program
wordlist = load_words()

# -----------------------------------

# Select a word at random to be picked as the game word
chosen_word = choose_word(wordlist)
print chosen_word

# Choose number of guesses a player gets and how many they have used
guesses_allowed = 15
guesses_used = 0

# Create a string that contains the 'shown word'
shown_word = '_'*len(chosen_word)
available_letters = 'abcdefghijklmnopqrstuvwxyz'
line_break = '---------------------'
print shown_word

# Helper functions
def update_shown_word(chosen_word, shown_word, guessed_letter):
    ''' Takes the current version of the shown word and a letter guess,
    checks to see if the guessed letter is in the word, and if so displays that letter.
    Keep in mind this function needs to update ALL letters'''
    letter_count = chosen_word.count(guessed_letter)
    shown_word_list = list(shown_word)
    letter_list = [x.start() for x in re.finditer(guessed_letter,chosen_word)]
    
    for x in letter_list:
        shown_word_list[x] = guessed_letter
    
    shown_word = ''.join(x for x in shown_word_list)    
    return shown_word


def update_letters(available_letters, guessed_letter):
    ''' Takes the alphabet string of available letters and removes the letter that
    was just guessed'''
    available_letters = available_letters.replace(guessed_letter,'')
    return available_letters

# Game beginning
def begin_game(chosen_word):
    print 'Welcome to the game, Hangman!'
    print 'I am thinking of a word that is '+str(len(chosen_word))+' letters long'
    print line_break

    
# Main game of guesses - loop through until person wins or runs out of guesses
begin_game(chosen_word)
while guesses_used < guesses_allowed:
    print 'You have '+str(guesses_allowed-guesses_used)+' guesses left'
    print 'Available letters: ',available_letters
    guessed_letter = raw_input('Please guess a letter: ')
    available_letters = update_letters(available_letters, guessed_letter)
    guesses_used += 1
    if guessed_letter in chosen_word:
        shown_word = update_shown_word(chosen_word, shown_word, guessed_letter)
        print 'Good guess: ' + shown_word
        print line_break
        # Check if person has won
        if shown_word.find('_') == -1:
            print 'Congratulations, you won!'
            break
    else:
        print 'Oops! That letter is not in my word: ' + shown_word
        print line_break
else:
    print "Oh no! You're out of guesses! You lost."
    print 'The word I was thinking of was: ',chosen_word