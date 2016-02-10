# Problem Set 7: Simulating the Spread of Disease and Virus Population Dynamics 
# Name:
# Collaborators:
# Time:

import numpy
import random
import pylab


class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. No further code changes needed.
    """

#
# PROBLEM 1
#
class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):

        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.   
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).
        """

        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

    def __str__(self):
        '''String representation of a SimpleVirus'''
        return 'SimpleVirus object with maxBirthProb: %s, clearProb: %s' % (self.maxBirthProb, self.clearProb)
    
    def doesClear(self):

        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step. 
        returns: True with probability self.clearProb and otherwise returns
        False.
        """
        # Returns true self.clearProb times
        
        choice = random.random()
        return choice < self.clearProb
    
    def reproduce(self, popDensity):

        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the SimplePatient and
        Patient classes. 
        The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """

        # Determines whether virus particle reproduces at a time step, with probability self.maxBirthProb * (1 - popDensity)
        # var = random.random()
        choice = random.random()
        if choice < self.maxBirthProb * (1 - popDensity):
            childVirus = SimpleVirus(self.maxBirthProb, self.clearProb)
            return childVirus
        else:
            raise NoChildException

class SimplePatient(object):

    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """    

    def __init__(self, viruses, maxPop):

        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the  maximum virus population for this patient (an integer)
        """

        self.viruses = viruses
        self.maxPop = maxPop

    def __str__(self):
        '''String representation of SimplePatient class object'''
        return 'Patient with %d virus instance(s) with a maxPop of %d' % (len(self.viruses), self.maxPop)
    
    def getTotalPop(self):

        """
        Gets the current total virus population. 
        returns: The total virus population (an integer)
        """

        return len(self.viruses)

    def update(self):

        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:
        
        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.   
        - The current population density is calculated. This population density
          value is used until the next call to update() 
        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient.                    

        returns: The total virus population at the end of the update (an
        integer)
        """

        # Create copies of the viruses to maintain
        surviving_viruses = []
        child_viruses = []
        
        # Determine whether each virus particle survives and updates the list of virus particles accordingly.
        
        for virus in self.viruses:
            if not virus.doesClear():
                surviving_viruses.append(virus)
        
        # Current pop density calculated. This density value is used until next call to update() 
        current_pop_density = float(len(surviving_viruses)) / self.maxPop
        
        # Reassign the current virus list to only the surviving viruses
        self.viruses = surviving_viruses
        
        # Determine whether each surviving virus particle should reproduce and add child virus particles to the list of viruses in this patient.
        for virus in self.viruses:
            # Add parent viruses to list
            child_viruses.append(virus)
            try:
                childVirus = virus.reproduce(current_pop_density)
                child_viruses.append(childVirus)
            # if the virus does not reproduce, skip this step
            except:
                pass
                
        # Reassign parents + children as the current virus list, and return
        self.viruses = child_viruses
        return self.getTotalPop()
        
#
# PROBLEM 2
#
def simulationWithoutDrug():

    """
    Run the simulation and plot the graph for problem 2 (no drugs are used,
    viruses do not have any drug resistance).    
    Instantiates a patient, runs a simulation for 300 timesteps, and plots the
    total virus population as a function of time.    
    """
    
    # Initialize variables
    time_step = 0
    virus_list = []
    x_time = []
    y_pop = []
    
    # Create a virus list of 100 simpleVirus instances
    for i in range(100):
        new_virus = SimpleVirus(0.1, 0.05)
        virus_list.append(new_virus)
    
    # Instantiate a simple patient from the virus list with 1000 max virus pop
    sim_patient = SimplePatient(virus_list, 1000)
    
    # Loop through time steps and populate x and y axes based on simulation
    for i in range(300):
        x_time.append(time_step)
        y_pop.append(sim_patient.update())
        time_step += 1
        
    pylab.title('Total virus population in a single patient by time step')
    pylab.xlabel('Number of time steps')
    pylab.ylabel('Number of virus particles')
    pylab.plot(x_time, y_pop)
    
    
    
    
# #### TESTS
# print '============================================'
# print 'Testing SimpleVirus class implementation:'
# virus1 = SimpleVirus(.99, .01)
# print virus1
# print type(virus1)
# print type(virus1) == SimpleVirus
# print '============================================'
# print 'Testing SimpleVirus doesClear method:'
# if virus1.doesClear():
    # print 'Cleared,',virus1
# else:
    # print 'Not cleared,',virus1
# if virus1.doesClear():
    # print 'Cleared,',virus1
# else:
    # print 'Not cleared,',virus1
# if virus1.doesClear():
    # print 'Cleared,',virus1
# else:
    # print 'Not cleared,',virus1
# print '============================================'
# print 'Testing SimpleVirus reproduce method:'
# new_child1 = virus1.reproduce(.001)
# print new_child1
# new_child2 = virus1.reproduce(.001)
# print new_child2
# new_child3 = virus1.reproduce(.001)
# print new_child3
# print '============================================'
# print 'Testing SimplePatient class implementation:'
# virus_list = []
# for i in range(100):
    # new_virus = SimpleVirus(0.99, 0.01)
    # virus_list.append(new_virus)
# patient = SimplePatient(virus_list, 100)
# print patient
# print 'Patient getTotalPop is: ',patient.getTotalPop()
# print '============================================'
# print 'Testing SimplePatient.update(): '
# for i in range(0, 10):
    # print patient.update()
# print '============================================'
# print 'Testing simulation: '
# simulationWithoutDrug()
# pylab.show()
# print 'Completed simulation.'
# print '============================================'