# 6.00 Problem Set 8
#
# Name:
# Collaborators:
# Time:


import numpy
import random
import pylab
from ps7 import *

#
# PROBLEM 1
#
class ResistantVirus(SimpleVirus):

    """
    Representation of a virus which can have drug resistance.
    """      
    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):

        """
        Initialize a ResistantVirus instance, saves all parameters as attributes of the instance.

        maxBirthProb: Maximum reproduction probability (float b/w 0-1)        
        clearProb: Maximum clearance probability (float b/w 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'grimpex',False}, means that this virus
        particle is resistant to neither guttagonol nor grimpex.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.        

        """
        # Can use super(Subclass, self) or Superclass.__init__
        super(ResistantVirus, self).__init__(maxBirthProb, clearProb)
        self.resistances = resistances
        self.mutProb = mutProb

    def __str__(self):
        ''' String representation of ResistantVirus class'''
        return 'ResistantVirus object with maxBirthProb: %.2f, clearProb %.2f, resistances %s, mutProb %.2f' % (self.maxBirthProb, self.clearProb, self.resistances, self.mutProb)
    
    def isResistantTo(self, drug):

        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in Patient to determine how many virus
        particles have resistance to a drug.    

        drug: The drug (a string)
        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """

        try:
            return self.resistances[drug]
        except:
            return False
            
    def isResistantToAll (self, drugList):
        """ Helper function that checks if virus is resistant to all the drugs
            in drugList """
        for drug in drugList:
            if not self.isResistantTo(drug):
                return False
        return True

    def reproduce(self, popDensity, activeDrugs):

        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient class.

        If the virus particle is not resistant to any drug in activeDrugs,
        then it does not reproduce. 
        Otherwise, the virus particle reproduces with probability:   self.maxBirthProb * (1 - popDensity). 
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). 

        For each drug resistance trait of the virus ( i.e. each key of
        self.resistances ), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.  

        For example, if a virus particle is resistant to guttagonol but not
        grimpex, and `self.mutProb` is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90% 
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        grimpex and a 90% chance that the offspring will not be resistant to
        grimpex.

        popDensity: population density (a float), defined as the current
        virus population divided by the maximum population        

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings). 
        
        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.         
        """
        # If virus particle is not resistant to any drug in activeDrugs, does not reproduce.
        for drug in activeDrugs:
            if not self.isResistantTo(drug):
                raise NoChildException()
        
        choice = random.random()
        if choice < self.maxBirthProb * (1 - popDensity):
            child_resistances = {}
            for drug in self.resistances:
                prob = random.random()
                if prob < self.mutProb:    # 1 - mutProb that child inherits resistance
                    child_resistances[drug] = not self.resistances[drug]
                else:
                    child_resistances[drug] = self.resistances[drug]
                    
            # Return childVirus with same attributes as aprent except for resistances
            childVirus = ResistantVirus(self.maxBirthProb, self.clearProb, child_resistances, self.mutProb)
            return childVirus
        else:
        # If popDensity is high enough, no reproduction 
            raise NoChildException()

class Patient(SimplePatient):

    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).               

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)
        
        maxPop: the  maximum virus population for this patient (an integer)
        """
        
        SimplePatient.__init__(self, viruses, maxPop)
        self.activeDrugs = []
    
    def __str__(self):
        '''String representation of a Patient (adds activeDrugs to string'''
        return 'Patient with %d virus instance(s) with a maxPop of %d and %d active Drugs (%s)' % (len(self.viruses), self.maxPop, len(self.activeDrugs), self.activeDrugs)
        
    def addPrescription(self, newDrug):

        """
        Administer a drug to this patient. After a prescription is added, the 
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: list of drugs being administered to a patient is updated
        """
        
        if newDrug not in self.activeDrugs:
            self.activeDrugs.append(newDrug)

    def getPrescriptions(self):

        """
        Returns the drugs that are being administered to this patient.
        returns: The list of drug names (strings) being administered to this
        patient.
        """

        return self.activeDrugs

    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in 
        drugResist. Uses the isResistantTo(drug) method of ResistantVirus.

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'grimpex'])

        returns: the population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        num_resistant_viruses = 0
        for virus in self.viruses:
            if virus.isResistantToAll(drugResist):
                num_resistant_viruses += 1
        return num_resistant_viruses

    def update(self):

        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:
        
        - Determine whether each virus particle survives and update the list of 
          virus particles accordingly          
        - The current population density is calculated. This population density
          value is used until the next call to update().
        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient. 
          The listof drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces. 

        returns: the total virus population at the end of the update (an
        integer)
        
        """
        surviving_viruses = []
        
        # Determine whether each virus particle survives and update virus list
        for virus in self.viruses:
            if not virus.doesClear():
                surviving_viruses.append(virus)
        
        current_pop_density = float(len(surviving_viruses)) / self.maxPop
        self.viruses = surviving_viruses
        
        # Determine whether each virus particle should reproduce and add offspring virus particles to the list of viruses in this patient. 
        # The listof drugs being administered should be accounted for in the determination of whether each virus particle reproduces. 
        # Drugs taken keep virus particles from reproducing if they are not resistant.
        
        child_viruses = []
        for virus in self.viruses:
            child_viruses.append(virus)
            try:
                childVirus = virus.reproduce(current_pop_density, self.activeDrugs)
                child_viruses.append(childVirus)
            except NoChildException:
                pass
        self.viruses = child_viruses
        return self.getTotalPop()

#
# PROBLEM 2
#

#############################################
# Helper function that runs a single simulation 
def runDrugSimulation(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                       mutProb, numStepsBeforeDrugApplied, totalNumSteps):
    '''Helper function that runs a single simulation. '''
    
    assert numStepsBeforeDrugApplied <= totalNumSteps
    
    viruses = []
    for i in xrange(0, numViruses):
        viruses.append(ResistantVirus(maxBirthProb, clearProb, resistances, mutProb))
    
    patient = Patient(viruses, maxPop)
    
    # Run the simulation with or without a drug for numStepsBeforeDrugApplied times
    numVirusesPerStep = []
    numResistantVirusesEachStep = []
    for i in xrange(0, totalNumSteps):
        if i == numStepsBeforeDrugApplied:
            patient.addPrescription('guttagonol')
        numVirusesPerStep.append(patient.update())  # # viruses in patient after timestep
        numResistantVirusesEachStep.append(patient.getResistPop(['guttagonol']))
        
    return (numVirusesPerStep, numResistantVirusesEachStep)
###############################################

def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                       mutProb, numTrials):

    """

    Runs simulations and plots graphs for problem 4.
    Instantiates a patient, runs a simulation for 150 timesteps, adds
    guttagonol, and runs the simulation for an additional 150 timesteps.
    total virus population vs. time and guttagonol-resistant virus population
    vs. time are plotted
    """
    # Initialize variables
    totalViruses = None
    resistantViruses = None
    
    for i in range(0,num_trials):
        (total, resistant) = runDrugSimulation(numViruses, maxPop, maxBirthProb, clearProb, resistances, mutProb, 150, 300)
    if totalViruses == None:
        totalViruses = total
        resistantViruses = resistant
    else:
        for j in xrange(0, len(total)):
            totalViruses[j] += total[j]
            resistantViruses[j] += resistant[j]
            
    for i in xrange(0, len(totalViruses)):
        totalViruses[i] /= float(numTrials)
        resistantViruses[i] /= float(numTrials)

    pylab.plot(xrange(0, len(totalViruses)), totalViruses, label = "Total")
    pylab.plot(xrange(0, len(totalViruses)), resistantViruses,
               label = "ResistantVirus")
    pylab.title("ResistantVirus simulation")
    pylab.xlabel("time step")
    pylab.ylabel("# viruses")
    pylab.legend(loc = "best")
    pylab.show()
        

#
# PROBLEM 3
#        

    
def simulationDelayedTreatment(numViruses, maxPop, maxBirthProb,
                                      clearProb, resistances, mutProb, numTrials):

    """
    Runs simulations and make histograms for problem 5.
    Runs multiple simulations to show the relationship between delayed treatment
    and patient outcome.
    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).    
    """
    
    # Outcome = a list of virus population to be plotting as a histogram 
    
    delays = [300,150,75,0]
    finalResults = {}
    
    for delay in delays:
        finalNumViruses = []
        for i in xrange(0, numTrials):
            total = runDrugSimulation(numViruses, maxPop, maxBirthProb,
                                      clearProb, resistances, mutProb, delay, delay+150)
            finalNumViruses.append(total[-1])
            finalResults[delay] = finalNumViruses
        
    
    plotNum = 1
    for n in delays:
        pylab.subplot(2, 2, plotNum)
        pylab.title("delay: " + str(n))
        pylab.xlabel("final virus counts")
        pylab.ylabel("# trials")
        pylab.hist(finalResults[n], bins=12, range=(0, 600)) # each bin of size 50
        plotNum += 1

    pylab.show()
    

#
# PROBLEM 4
#

def simulationTwoDrugsDelayedTreatment():

    """
    Runs simulations and make histograms for problem 6.
    Runs multiple simulations to show the relationship between administration
    of multiple drugs and patient outcome.
   
    Histograms of final total virus populations are displayed for lag times of
    150, 75, 0 timesteps between adding drugs (followed by an additional 150
    timesteps of simulation).
    """

    delays = [300,150,75,0]
    finalNumViruses = []
    finalResults = {}
    
    for delay in delays:
        total = runDrugSimulation(1000, 1000, .9, .1, ['guttagonol', 'grimpex'], .05, delay, delay+150)
        finalNumViruses.append(total)
        finalResults[delay] = finalNumViruses
        
    plotNum = 1
    for n in delays:
        pylab.subplot(2, 2, plotNum)
        pylab.title("delay: " + str(n))
        pylab.xlabel("final virus counts")
        pylab.ylabel("# trials")
        pylab.hist(finalResults[n], bins=12, range=(0, 600)) # each bin of size 50
        plotNum += 1

    pylab.show()



# # ### TESTS
# # VIRUS
# print '=========================================='
# print 'Testing implementation of ResistantVirus class: '
# resVirus = ResistantVirus(.9, .05,{'guttagonol':False, 'grimpex':True, 'gutsalol': True}, .2)
# print resVirus
# print '=========================================='
# print 'Testing implementation of isResistantTo method: '
# print 'Below should return True: '
# print resVirus.isResistantTo('gutsalol')
# print 'Below should return False: '
# print resVirus.isResistantTo('Prozac')
# print '=========================================='
# print 'Testing implementation of reproduce method: '
# print resVirus.reproduce(.01, ['grimpex'])
# num_reproductions = 0
# num_trials = 100
# for i in range(num_trials):
    # try:
        # resChild = resVirus.reproduce(popDensity = .01, activeDrugs = ['grimpex'])
        # num_reproductions += 1
    # except:
        # pass
# print '%d reproductions out of %d trials' % (num_reproductions, num_trials)
# print '=========================================='
# print '=========================================='

# # # PATIENT
# print 'Testing implementation of Patient class with 2 viruses and max pop of 10: '
# resVirus2 = ResistantVirus(.8, .1,{'grimpex':True, 'gutsalol': True}, .4)
# virus_list = [resVirus, resVirus2]
# patient = Patient(virus_list, 10)
# print patient
# print '=========================================='
# # print 'Testing implementation of addPrescription method: '
# new_drug = patient.addPrescription('grimpex')
# # new_drug = patient.addPrescription('gutsalol')
# # print patient
# print '=========================================='
# print 'Testing implementation of getPrescriptions method: '
# print patient.getPrescriptions()
# print '=========================================='
# print 'Testing implementation of getResistPop method: '
# print patient.getResistPop(['grimpex', 'gutsalol'])
# print patient.getResistPop(['grimpex'])
# print '=========================================='
# print 'Testing implementation of update method: '
# print 'patient is: ',patient
# print 'Updating.....'
# patient.update()
# patient.update()
# patient.update()
# print 'updated patient is: ',patient
# print '=========================================='
# print 'Testing runDrugSimulation: '
# (numViruses, maxPop, maxBirthProb, clearProb, resistances, mutProb, numStepsBeforeDrugApplied, totalNumSteps)
# print runDrugSimulation(100, 1000, .95, .05, {'guttagonol':False}, .05, 50, 100)
# print '=========================================='
# print 'Testing simulation'
# simulationWithDrug(100, 1000, .95, .05, {'guttagonol':False}, .05, 100)
# pylab.show()
print '=========================================='
print '=========================================='
print 'Testing simulationDelayedTreatment: '
#numViruses, maxPop, maxBirthProb,clearProb, resistances, mutProb, numTrials
print simulationDelayedTreatment(100, 1000, .95, .05, {'guttagonol':False}, .05, 100)
print '=========================================='
# print 'Testing simulationTwoDrugsDelayedTreatment: '
# print simulationTwoDrugsDelayedTreatment()