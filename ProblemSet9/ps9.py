# 6.00 Problem Set 9
#
# Intelligent Course Advisor
#
# Name:
# Collaborators:
# Time:
#

import collections

SUBJECT_FILENAME = "subjects.txt"
SHORT_SUBJECT_FILENAME = "shortened_subjects.txt"
VALUE, WORK = 0, 1

# Problem 1: Building A Subject Dictionary

def loadSubjects(filename):
    """
    Returns a dictionary mapping subject name to (value, work), where the name
    is a string and the value and work are integers. The subject information is
    read from the file named by the string filename. Each line of the file
    contains a string of the form "name,value,work".

    returns: dictionary mapping subject name to (value, work)
    """
    # Reads lines from the specified file and parse the name,
    # value, and work of each subject and create a dictionary mapping the name
    # to the (value, work).
    subjects = {}
    inputFile = open(filename)
    for line in inputFile:
        newline = line.strip().split(',')
        subjects[newline[0]] = (float(newline[1]),float(newline[2]))
        
    return subjects

def printSubjects(subjects):
    """
    Prints a string containing name, value, and work of each subject in
    the dictionary of subjects and total value and work of all subjects
    """
    totalVal, totalWork = 0,0
    if len(subjects) == 0:
        return 'Empty SubjectList'
    res = 'Course\tValue\tWork\n======\t====\t=====\n'
    subNames = subjects.keys()
    subNames.sort()
    for s in subNames:
        val = subjects[s][VALUE]
        work = subjects[s][WORK]
        res = res + s + '\t' + str(val) + '\t' + str(work) + '\n'
        totalVal += val
        totalWork += work
    res = res + '\nTotal Value:\t' + str(totalVal) +'\n'
    res = res + 'Total Work:\t' + str(totalWork) + '\n'
    print res

# Problem 2: Subject Selection By Greedy Optimization

def cmpValue(subInfo1, subInfo2):
    """
    Accepts: two nested tuples of len 3 with floats for (subject,(value, work))
    Returns: 1 if value in (value, work) tuple subInfo1 is GREATER than
    value in (value, work) tuple in subInfo2, -1 if not, 0 for exceptions
    """
    if subInfo1[1][0] > subInfo2[1][0]:
        return 1
    elif subInfo1[1][0] < subInfo2[1][0]:
        return -1
    else:
        return 0

def cmpWork(subInfo1, subInfo2):
    """
    Returns 1 if work in (value, work) tuple subInfo1 is LESS than than work
    in (value, work) tuple in subInfo2
    """
    if subInfo1[1][1] < subInfo2[1][1]:
        return 1
    elif subInfo1[1][1] > subInfo2[1][1]:
        return -1
    else:  
        return 0

def cmpRatio(subInfo1, subInfo2):
    """
    Returns 1 if value/work in (value, work) tuple subInfo1 is 
    GREATER than value/work in (value, work) tuple in subInfo2
    """
    if subInfo1[1][0]/subInfo1[1][1] > subInfo2[1][0]/subInfo2[1][1]:
        return 1
    elif subInfo1[1][0]/subInfo1[1][1] < subInfo2[1][0]/subInfo2[1][1]:
        return -1
    else:
        return 0
    
def greedyAdvisor(subjects, maxWork, comparator):
    """
    Returns a dictionary mapping subject name to (value, work) which includes
    subjects selected by the algorithm, such that the total work of subjects in
    the dictionary is not greater than maxWork.  The subjects are chosen using
    a greedy algorithm (locally iterative).  
    ** The subjects dictionary should not be mutated.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    comparator: function taking two tuples and returning a bool
    returns:    dictionary mapping subject name to (value, work)
    """
    # TODO...
    # Make sure subjects is a dict and max weight >= 0
    assert type(subjects) == dict and maxWork >= 0
    
    # Use sorted() on the values to sort using comparator and create an ordered dict of subjects to hold the order
    sorted_subjects = collections.OrderedDict(sorted(subjects.items(), cmp=comparator, reverse=True))
    
    # Loop through and add to a new dict
    final_subjects = {}
    currentWork = 0
    for k,v in sorted_subjects.iteritems():
        currentWork += v[1]  # Add work to currentwork
        if currentWork <= maxWork:
            final_subjects[k] = v
        else:
            continue
    return final_subjects
    
def getValueToWorkRatio(subjectTuple):
    ''' Accepts a tuple of (value, work) and returns the value-to-work ratio'''
    return float(subjectTuple[0])/float(subjectTuple[1])
    
# Problem 3: Subject Selection By Brute Force
def bruteForceAdvisor(subjects, maxWork):
    """
    Returns a dictionary mapping subject name to (value, work), which
    represents the globally optimal selection of subjects using a brute force
    algorithm.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    returns: dictionary mapping subject name to (value, work)
    """
    # TODO...
    # First, enumerate all possibilities. We want to optimize value per weight.
    
    new_subjects = {}
    
    # All possibilities means: every dictionary of subject choices available
    
    for i in range(len(subjects)):
        pass
    
    # Then, pick top possibilities


### TESTS
print '==========================================='
print 'Testing implementation of loadSubjects'
subjects = loadSubjects(SHORT_SUBJECT_FILENAME)
printSubjects(subjects)
# print '==========================================='
## Removed cmpValue/cmpWork/cmpRatio tests after changing functions to accept nested tuples. No testing needed.
print '==========================================='
# print 'Testing implementation of greedyAdvisor: '
# final_subjects1 = greedyAdvisor(subjects, maxWork=10, comparator=cmpValue)
# printSubjects(final_subjects1)
# final_subjects2 = greedyAdvisor(subjects, maxWork=20, comparator=cmpValue)
# printSubjects(final_subjects2)
# final_subjects3 = greedyAdvisor(subjects, maxWork=30, comparator=cmpValue)
# printSubjects(final_subjects3)
print '==========================================='
print 'Testing helper function getValueToWorkRatio: '
print 'Should be 2: ',getValueToWorkRatio((10,5))
print 'Should be .33: ',getValueToWorkRatio((1,3))
print '==========================================='
print 'Testing implementation of bruteForceAdvisor: ',
print bruteForceAdvisor(subjects, maxWork=30)