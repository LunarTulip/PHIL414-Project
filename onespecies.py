import random

class Model:

    def __init__(self, gensize = 20, memmutation = 3, envchangechance = 0.2, envchangebeneficial = 1.0, environment = None, selection = True):
        """
        Initializes a Model object containing a set of members (integers from 1 to 100), an environment (also an integer from 1 to 100), and various inputs controlling the behavior of the model over time.
        gensize: Positive int, number of members per generation
        memmutation: int or float, standard deviation of children's int values relative to parent values
        envchangechance: float, probability from 0 to 1 that the environment will change each generation
        envchangebeneficial: float from -1 to 1, shifts probability that the environment will move towards the center of population; -1 always shifts away, 1 alaways shifts towards, 0 gives 50/50 odds
        environment: Int from 1 to 100, optionally set environment to initialize at a specific value
        selection: bool, if True creatures with int values nearer the environment have better reproductive odds than those further away
        """
        self.gensize = gensize
        self.members = []
        for i in range(gensize):  # Fill Members list with random ints in the correct range
            self.members.append(random.randint(1, 100))
        self.memmutation = memmutation
        self.envchangechance = envchangechance
        self.envchangebeneficial = envchangebeneficial
        if environment:  # If an environment value was input, set environment to that; else set it to a random int in the correct range
            self.environment = environment
        else:
            self.environment = random.randint(1, 100)
        self.selection = selection

    def nextgeneration(self):
        """
        Pick self.gensize members as parents of the new generation, weighted by closeness-to-environment if selection is enabled or with equal probability otherwise; then create one new member for each parent, with an int value in a bell curve centered around the parent's int value, and set the list of those as the new member list
        """
        if self.selection:
            fitness = []
            for i in range(self.gensize):
                ithfitness = 50 - self.distancefromenv(self.members[i])[0]
                fitness.append(ithfitness)
            parents = random.choices(self.members, fitness, k = self.gensize)
        else:
            parents = random.choices(self.members, k = self.gensize)
        newgen = []
        for parent in parents:
            child = ((round((random.normalvariate(parent, self.memmutation))) - 1) % 100) + 1
            newgen.append(child)
        self.members = newgen

    def shiftenvironment(self):
        """
        Calculates the direction in which the environment needs to move to approach the center of the current population; with probability abs(self.envchangebeneficial), shifts in that direction if self.envchangebeneficial is positive or the other direction if it's negative, with larger shifts when center of population is further away; else shifts in a random direction with same distance rule
        """
        if random.random() < self.envchangechance:
            avgpull = 0
            for member in self.members:
                mempull, memdir = self.distancefromenv(member)
                if memdir:
                    avgpull += mempull
                else:
                    avgpull -= mempull
            avgpull = avgpull // self.gensize
            if random.random() < abs(self.envchangebeneficial) and avgpull != 0:
                if self.envchangebeneficial > 0:
                    if avgpull < 0:
                        self.environment = (((self.environment - abs(round(random.normalvariate(0, avgpull // 2)))) - 1) % 100) + 1
                    elif avgpull > 0:
                        self.environment = (((self.environment + abs(round(random.normalvariate(0, avgpull // 2)))) - 1) % 100) + 1
                else:
                    if avgpull < 0:
                        self.environment = (((self.environment + abs(round(random.normalvariate(0, avgpull // 2)))) - 1) % 100) + 1
                    elif avgpull > 0:
                        self.environment = (((self.environment - abs(round(random.normalvariate(0, avgpull // 2)))) - 1) % 100) + 1
            else:
                self.environment = (round((random.normalvariate(self.environment, avgpull // 2))) % 100) + 1

    def displayverbose(self, gennum = None):
        """
        Prints a visual display of the generation, with v representing the environment and # signs representing each member, at width 100 (one column for each possible integer value of members and environment)
        """
        genstring = ""
        if gennum:
            genstring += "Generation {}:\n".format(gennum)
        vals = {}
        for i in range(100):
            vals[i + 1] = 0
        highestval = 0
        for member in self.members:
            vals[member] += 1
            if vals[member] > highestval:
                highestval = vals[member]
        for i in range(100):
            if i + 1 == self.environment:
                genstring += "v"
            else:
                genstring += " "
        while highestval > 0:
            genstring += "\n"
            for i in range(100):
                if vals[i + 1] >= highestval:
                    genstring += "#"
                else:
                    genstring += " "
            highestval -= 1
        print(genstring)

    def displayconcise(self, gennum = None):
        # Prints the value of the environment
        genstring = ""
        if gennum:
            genstring += "Generation {}: ".format(gennum)
        genstring += str(self.environment)
        print(genstring)

    def distancefromenv(self, mem):
        """
        Gets the shortest distance of a given member of the population from the environment, as well as whether that distance is from traveling down ('left') or up ('right') along the line of integers (keeping in mind that the values form a ring, such that 1 and 100 have distance 1, not distance 99); returns the distance plus a boolean representing direction
        """
        if mem > self.environment:
            leftward = (100 - mem) + self.environment
            rightward = mem - self.environment
        else:
            rightward = (100 - self.environment) + mem
            leftward = self.environment - mem
        if leftward < rightward:
            return (leftward, False)
        else:
            return (rightward, True)
        #Returns True to go right, False to go left

def runmodel(gencount, gensize = 20, memmutation = 3, envchangechance = 0.2, envchangebeneficial = 1.0, environment = None, selection = True, verbose = True):
    # Creates a model with input properties (see Model comment for details), then runs it for input number of generations and prints each generation
    m = Model(gensize, memmutation, envchangechance, envchangebeneficial, environment, selection)
    gennum = 1
    while gencount > 0:
        if verbose:
            m.displayverbose(gennum)
        else:
            m.displayconcise(gennum)
        m.shiftenvironment()
        m.nextgeneration()
        gennum += 1
        gencount -= 1

# For demo

def drift(gencount, environment = None):  # Random drift
    runmodel(gencount, envchangechance = 0, environment = environment, selection = False)

def staticenv(gencount, environment = None):  # Environment doesn't move
    runmodel(gencount, envchangechance = 0, environment = environment)

def edriftslow(gencount, environment = None):  # Environment shifts in random direction 20% of the time
    runmodel(gencount, envchangebeneficial = 0.0, environment = environment)

def edriftfast(gencount, environment = None):  # Environment shifts in random direction 50% of the time
    runmodel(gencount, envchangechance = 0.5, envchangebeneficial = 0.0, environment = environment)

def pullslow(gencount, environment = None):  # Environment shifts towards center of population 20% of the time
    runmodel(gencount, environment = environment)

def pullfast(gencount, environment = None):  # Environment shifts towards center of population 50% of the time
    runmodel(gencount, envchangechance = 0.5, environment = environment)

def pushslow(gencount, environment = None):  # Environment shifts away from center of population 20% of the time
    runmodel(gencount, envchangebeneficial = -1.0, environment = environment)

def pushfast(gencount, environment = None):  # Environment shifts away from center of population 50% of the time
    runmodel(gencount, envchangechance = 0.5, envchangebeneficial = -1.0, environment = environment)
