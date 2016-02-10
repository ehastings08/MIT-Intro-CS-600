# ps7b

# Problem 1
# 1/2 ^ 3 = 1/8
# 1/8
# 1/8
# 1/2

import random

# Problem 2 
# .0001 (1/6 ^ 5)

# Problem 3
def rollDie():
    """returns a random int between 1 and 6"""
    return random.choice([1,2,3,4,5,6])

def checkYahtzee(numTrials):
    '''Checks the probability of rolling 5 sixes in 1 rolls per trial in numTrials'''
    yes = 0.0
    
    # Decide how many trials you want to run / sample size
    for i in range(numTrials):
        # Roll two die 24 times
        for j in range(1):
            d1 = rollDie()
            d2 = rollDie()
            d3 = rollDie()
            d4 = rollDie()
            d5 = rollDie()
            if d1 == 6 and d2 == 6 and d3 == 6 and d4 == 6 and d5 == 6:
                yes += 1
                break   # Breaks out of inner loop
    print 'Probability of winning = ' + str(yes/numTrials)
    
checkYahtzee(100000)