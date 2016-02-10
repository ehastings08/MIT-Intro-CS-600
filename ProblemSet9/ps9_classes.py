# 6.00 Problem Set 9
#
# Intelligent Course Advisor
#
# Name:
# Collaborators:
# Time:
#

import collections, random, timeit, pylab

SUBJECT_FILENAME = "subjects.txt"
SHORT_SUBJECT_FILENAME = "shortened_subjects.txt"
VALUE, WORK = 0, 1

class Subject(object):
    ''' A subject object that includes a mapping of subject name to value, work tuples '''
    def __init__(self, name, value, work):
        self.name = name
        self.value = value
        self.work = work
        
    def getName(self):
        return self.name
    
    def getValue(self):
        return self.value
    
    def getWork(self):
        return self.work
       
    def getRatio(self):
        return float(self.value)/float(self.work)
        
    def __str__(self):
        return 'Course\tValue\tWork\n======\t====\t=====\n' + self.name + '\t' + str(self.value) + '\t' + str(self.work) + '\n'
    
    def __hash__(self):
        return hash(self.name)
        

# Problem 1: Building A Subject List of Classes
def loadSubjects(filename):
    """
    Returns a list of subjects. The subject information is
    read from the file named by the string filename. Each line of the file
    contains a string of the form "name,value,work".

    returns: list of subjects with name, value, work information set
    """
    # Reads lines from the specified file and parse the name,
    # value, and work of each subject and create a dictionary mapping the name
    # to the (value, work).
    subjects = []
    inputFile = open(filename)
    for line in inputFile:
        newline = line.strip().split(',')
        subjectname, subjectvalue, subjectwork = newline[0], float(newline[1]),float(newline[2])
        subjectClass = Subject(subjectname, subjectvalue, subjectwork)
        subjects.append(subjectClass)
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
    for i in range(len(subjects)):
        name = subjects[i].getName()
        val = subjects[i].getValue()
        work = subjects[i].getWork()
        res = res + name + '\t' + str(val) + '\t' + str(work) + '\n'
        totalVal += val
        totalWork += work
    res = res + '\nTotal Value:\t' + str(totalVal) +'\n'
    res = res + 'Total Work:\t' + str(totalWork) + '\n'
    print res
    

# Problem 2: Subject Selection By Greedy Optimization

def cmpValue(Subject1, Subject2):
    """
    Accepts: two subject classes
    Returns: 1 if value in subejct1 is GREATER than
    value in subject2, -1 if not, 0 for exceptions
    """
    if Subject1.getValue() > Subject2.getValue():
        return 1
    elif Subject1.getValue() < Subject2.getValue():
        return -1
    else:
        return 0

def cmpWork(Subject1, Subject2):
    """
    Returns 1 if work in subject1 is LESS than than work in subject2
    """
    if Subject1.getWork() < Subject2.getWork():
        return 1
    elif Subject1.getWork() > Subject2.getWork():
        return -1
    else:  
        return 0

def cmpRatio(Subject1, Subject2):
    """
    Returns 1 if value/work in (value, work) tuple subInfo1 is 
    GREATER than value/work in (value, work) tuple in subInfo2
    """
    if Subject1.getRatio() > Subject2.getRatio():
        return 1
    elif Subject1.getRatio() < Subject2.getRatio():
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

    subjects: list of subjects
    maxWork: int >= 0
    comparator: function taking two subjects and returning a positive or negative
    returns:    dictionary mapping subject name to (value, work)
    """
    
    # Use sorted() on the values to sort using comparator and create an ordered dict of subjects to hold the order
    sorted_subjects = sorted(subjects, cmp=comparator, reverse=True)
    
    # Loop through and add to a new list
    final_subjects = []
    currentWork = 0
    testWork = 0
    
    for subject in sorted_subjects:
        testWork += subject.getWork()  # Add work to currentwork
        if testWork <= maxWork:
            final_subjects.append(subject)
            currentWork += subject.getWork()
        else:
            continue
            
    return final_subjects
    
def pickSubjectsHelper(toConsider, avail, taken):
    '''Helper function that explores list of subjects by path 
    Parameters:
    toConsider: list of subjects to consider
    avail: maximum amount of work available
    taken: list of subjects that are already taken '''
    
    # If there are no subjects left to consider or no work available, return 0
    if toConsider == [] or avail == 0:
        result = (0, ())
        
    # If the next item adds more work than is available, move on to the next recursion
    elif toConsider[0].getWork() > avail:
        result = pickSubjectsHelper(toConsider[1:], avail, taken)
        
    # Otherwise, play out the branches with and without adding the subject
    else:
        item = toConsider[0]
        
        # If you take the subject...
        withVal, withToTake = pickSubjectsHelper(toConsider[1:], avail - item.getWork(), taken + [item])
        withVal += item.getValue()
        
        # If you do not take the subject...
        withoutVal, withoutToTake = pickSubjectsHelper(toConsider[1:], avail, taken)
        
        # Compare
        if withVal > withoutVal:
            result = (withVal, withToTake + (item,))    # --, ()
        else:
            result = (withoutVal, withoutToTake)
            
    return result
    
    
def bruteForceAdvisor(subjects, maxWork):
    '''Pick subjects to take using brute force. Use recursive backtracking
        while exploring the list of subjects in order to cut down the number
        of paths to explore, rather than exhaustive enumeration
        that evaluates every possible list of subjects from the power set.

        Parameters:
        subjects: list of Subject instances to choose from, each subject can be chosen at most once
        maxWork: maximum amount of work we are willing to take on

        Returns:
        a list of Subject instances that are chosen to take '''
        
    assert maxWork > 0
    
    bestValue, bestSubset = pickSubjectsHelper(subjects[:], maxWork, [])
    return list(bestSubset)
 
def timeGreedy(subjects, maxWork, comparator):
    start_time = timeit.default_timer()
    greedyAdvisor(subjects, maxWork, comparator)
    end_time = timeit.default_timer()
    total_time = end_time-start_time
    return total_time
    
def timeBrute(subjects, maxWork):
    start_time = timeit.default_timer()
    bruteForceAdvisor(subjects, maxWork)
    end_time = timeit.default_timer()
    total_time = end_time-start_time
    return total_time

def plotTimes(filename, maxWork, subjectSizes, numRuns):
    """
    Compare the time taken to pick subjects for each of the advisors
    subject to maxWork constraint. 
    Run different trials using different number
    of subjects as given in subjectSizes, using the subjects as loaded
    from filename. 
    Choose a random subject of subjects for each trial.
    For instance, if subjectSizes is the list [10, 20, 30], then you should
    first select 10 random subjects from the loaded subjects, 
    then run them
    through the three advisors using maxWork for numRuns times, measuring
    *the time taken for each run*, then average over the numRuns runs. 
    After that,
    pick another set of 20 random subjects from the loaded subjects,
    and run them through the advisors, etc. 
    Produce a plot afterwards
    with the x-axis showing number of subjects used, and y-axis showing
    time. Be sure you label your plots.
    """
    # Obtain subjects, a list of subjects loaded from filename parameter
    subjects = loadSubjects(filename)
    
    # Variables
    x_axis_num_subjects = []
    y_axis_avg_time_greedy = []
    y_axis_avg_time_brute = []
    runs, total_time_greedy, total_time_brute = 0, 0, 0
    
    # Run a different # of subject sizes based on subjectSizes
    for size in subjectSizes:
        x_axis_num_subjects += [size]
    # Run a different # of trials based on numRuns
        for run in range(1,numRuns+1):
            # Choose a random set of subjects for each trial.
            trial_subjects = random.sample(subjects, size)
            
            # Test greedy
            run_time_greedy = float(timeGreedy(trial_subjects, maxWork, cmpRatio))
            total_time_greedy += run_time_greedy
            
            # Test brute
            run_time_brute = float(timeBrute(trial_subjects, maxWork))
            total_time_brute += run_time_brute
            
        avg_time_greedy = total_time_greedy/numRuns
        avg_time_brute = total_time_brute/numRuns
        
        y_axis_avg_time_greedy += [avg_time_greedy]
        y_axis_avg_time_brute += [avg_time_brute]
            
    
    # Plot - THIS IS PLOTTING MULTIPLE DOTS AT SAME # SUBJECTS. NEED TO AVERAGE LATER
    pylab.figure(1)
    pylab.plot(x_axis_num_subjects, y_axis_avg_time_brute)
    pylab.plot(x_axis_num_subjects, y_axis_avg_time_greedy)
    pylab.title('Average Time Per Run For Brute Force vs. Greedy Algo')
    pylab.xlabel('Number of Subjects')
    pylab.ylabel('Average Seconds Per Run')
    pylab.show()
            
    # print x_axis_num_subjects, y_axis_avg_time_brute, y_axis_avg_time_greedy
        
    
    
    
### TESTS
# print '==========================================='
# print 'Testing implementation of Subject class'
# subject1 = Subject('6.00',10.0,1.0)
# subject2 = Subject('6.01',2.0,4.0)
# print subject1
# print '==========================================='
# print 'Testing implementation of loadSubjects'
# subjects = loadSubjects(SHORT_SUBJECT_FILENAME)
# printSubjects(subjects)
# print '==========================================='
# print 'Testing implementation of cmpWork(): '
# print 'Should return -1: ',cmpWork(subject2, subject1)
# print '==========================================='
# print 'Testing implementation of cmpValue(): '
# print 'Should return 1: ',cmpValue(subject1, subject2)
# print '==========================================='
# print 'Testing implementation of cmpValue(): '
# print 'Should return 1: ',cmpRatio(subject1, subject2)
# print '==========================================='
# print 'Testing implementation of greedyAdvisor(): '
# print 'Using cmpWork: '
# final_subjects1 = greedyAdvisor(subjects, maxWork=40, comparator=cmpWork)
# printSubjects(final_subjects1)
# print 'Using cmpValue: '
# final_subjects2 = greedyAdvisor(subjects, maxWork=20, comparator=cmpValue)
# printSubjects(final_subjects2)
# print 'Using cmpRatio: '
# final_subjects3 = greedyAdvisor(subjects, maxWork=30, comparator=cmpRatio)
# printSubjects(final_subjects3)
# print '==========================================='
# print 'Testing implementation of bruteForceAdvisor(): '
# brute_answer = bruteForceAdvisor(subjects, maxWork=40)
# printSubjects(brute_answer)
# print '==========================================='
# print 'Testing implementation of timeGreedy():'
# subjects_long = loadSubjects(SUBJECT_FILENAME) 
# print timeGreedy(subjects_long, 40, cmpRatio)
print '==========================================='
print 'Testing implementation of plotTimes(): '
print plotTimes(SUBJECT_FILENAME, maxWork=50, subjectSizes=[1, 2, 5, 10, 20, 35], numRuns=10)


# The time taken by the Brute Force advisor grows exponentially
# as the number of subjects increases, while the other grows roughly
# linearly. This makes sense since the greedy algorithm
# is roughly O(n log n) where n is the length of the subject list,
# brute force is exponential with O(2^n)