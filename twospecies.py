import random

class Model:

    def __init__(self, gensize = 20, herbivoremutationsize = 3, herbmutationsize = 3, herbivoremutationchance = 1.0, herbmutationchance = 1.0, herbivoreselection = True, herbselection = True, seed = None):
        """
        Initializes a Model object containing a set of herbivores and a set of herbs (all integers from 1 to 100), along with various inputs controlling the behavior of the model over time.
        gensize: Positive int, number of members per generation
        herbivoremutationsize: int or float, standard deviation of herbivore children's int values relative to parent values
        herbmutationsize: as herbivoremutationsize, but for herbs
        herbivoremutationchance: float, probability from 0 to 1 that a herbivore's child's int value will vary from its parent's value as defined by herbivoremutationsize
        herbmutationchance: as herbivoremutationchance, but for herbs
        herbivoreselection: bool, if True herbivores have better reproductive odds when closer to herbs
        herbselection: bool, if True herbs have better reproductive odds when further from herbivores
        seed: int, string, bytes, or bytearray; seed for randomization of model; useful when you want to precisely reproduce behavior
        """
        random.seed(seed)
        self.gensize = gensize
        self.herbivores = []
        self.herbs = []
        for i in range(gensize):
            self.herbivores.append(random.randint(1, 100))
            self.herbs.append(random.randint(1, 100))
        self.herbivoremutationsize = herbivoremutationsize
        self.herbmutationsize = herbmutationsize
        self.herbivoremutationchance = herbivoremutationchance
        self.herbmutationchance = herbmutationchance
        self.herbivoreselection = herbivoreselection
        self.herbselection = herbselection

    def nextgeneration(self):
        """
        Pick self.gensize herbivores as parents of the new generation of herbivores, and self.gensize herbs as parents of the new generation of herbs, weighted by closeness-to-environment if selection is enabled or with equal probability otherwise; with probability of the relevant mutation chance, create one new member for each parent, with an int value in a bell curve centered around the parent's int value, and set the list of those as the new member list; insofar as that probability isn't met, create a child with value identical to the parent's value
        """
        if self.herbivoreselection:
            herbivorefitness = []
            for i in range(self.gensize):
                ithherbivorefitness = 50 - abs(self.avgdist(self.herbivores[i], self.herbs))
                if ithherbivorefitness < 1:  # Necessary to avoid bugs wherein all fitnesses are 0 and the weighting breaks down
                    ithherbivorefitness = 1
                herbivorefitness.append(ithherbivorefitness)
            herbivoreparents = random.choices(self.herbivores, weights = herbivorefitness, k = self.gensize)
        else:
            herbivoreparents = random.choices(self.herbivores, k = self.gensize)
        if self.herbselection:
            herbfitness = []
            for i in range(self.gensize):
                ithherbfitness = abs(self.avgdist(self.herbs[i], self.herbivores))
                if ithherbfitness < 1:
                    ithherbfitness = 1
                herbfitness.append(ithherbfitness)
            herbparents = random.choices(self.herbs, weights = herbfitness, k = self.gensize)
        else:
            herbparents = random.choices(self.herbs, k = self.gensize)
        newherbivores = []
        newherbs = []
        for parent in herbivoreparents:
            if random.random() < self.herbivoremutationchance:
                child = ((round((random.normalvariate(parent, self.herbivoremutationsize))) - 1) % 100) + 1
            else:
                child = parent
            newherbivores.append(child)
        for parent in herbparents:
            if random.random() < self.herbmutationchance:
                child = ((round((random.normalvariate(parent, self.herbmutationsize))) - 1) % 100) + 1
            else:
                child = parent
            newherbs.append(child)
        self.herbivores = newherbivores
        self.herbs = newherbs

    def display(self, gennum = None):
        """
        Prints a visual display of the generation, with * symbols representing herbivores and % symbols representing herbs, at width 100 (one column for each possible integer value of members and environment)
        """
        genstring = ""
        if gennum:
            genstring += "Generation {}:\n".format(gennum)
        herbivorevals = {}
        herbvals = {}
        combinedvals = {}
        for i in range(100):
            herbivorevals[i + 1] = 0
            herbvals[i + 1] = 0
            combinedvals[i + 1] = []
        highestval = 0
        for herbivore in self.herbivores:
            herbivorevals[herbivore] += 1
            if herbivorevals[herbivore] > highestval:
                highestval = herbivorevals[herbivore]
        for herb in self.herbs:
            herbvals[herb] += 1
            if herbvals[herb] + herbivorevals[herb] > highestval:
                highestval = herbvals[herb] + herbivorevals[herb]
        for key in combinedvals:
            for i in range(herbvals[key]):
                combinedvals[key].append("%")
            for i in range(herbivorevals[key]):
                combinedvals[key].append("*")
        while highestval > 0:
            genstring += "\n"
            for i in range(100):
                if len(combinedvals[i + 1]) >= highestval:
                    genstring += combinedvals[i + 1].pop()
                else:
                    genstring += " "
            highestval -= 1
        print(genstring)

    def distancefromenv(self, mem):
        return Model.distance(self.environment, mem)

    @staticmethod
    def distance(center, offset):
      # Gets the distance of an int from 1 to 100 to another int, given a ring shape such that 1 is adjacent to 100
        if offset > center:
            leftward = (100 - offset) + center
            rightward = offset - center
        else:
            rightward = (100 - center) + offset
            leftward = center - offset
        if leftward < rightward:
            return (leftward, False)
        else:
            return (rightward, True)
        #Returns True to go right, False to go left

    def avgdist(self, number, population):
        """
        Gets and returns the average distance (according to the distance staticmethod) of an input number to all members of a population of ints in the correct range
        number: int from 1 to 100
        population: list of ints from 1 to 100
        """
        total = 0
        for member in population:
            mempull = Model.distance(number, member)[0]
            total += abs(mempull)
        return total // self.gensize

def runmodel(gencount, gensize = 20, herbivoremutationsize = 3, herbmutationsize = 3, herbivoremutationchance = 1.0, herbmutationchance = 1.0, herbivoreselection = True, herbselection = True, seed = None):
    # Creates a model with input properties (see Model comment for details), then runs it for input number of generations and prints each generation
    m = Model(gensize, herbivoremutationsize, herbmutationsize, herbivoremutationchance, herbivoremutationchance, herbivoreselection, herbselection, seed)
    gennum = 1
    while gencount > 0:
        m.display(gennum)
        m.nextgeneration()
        gennum += 1
        gencount -= 1

# Specific behaviors

def drift(gencount):  # Both species randomly drifting
    runmodel(gencount, herbivoreselection = False, herbselection = False)

def herbivoredrift(gencount):  # Herbivores randomly drifting
    runmodel(gencount, herbivoreselection = False)

def herbdrift(gencount):  # Herbs randomly drifting
    runmodel(gencount, herbselection = False)

def staticchase(gencount):  # Herbs not mutating
    runmodel(gencount, herbmutationsize = 0)

def staticescape(gencount):  # Herbivores not mutating
    runmodel(gencount, herbivoremutationsize = 0)

def chase(gencount):  # Equal mutation rates
    runmodel(gencount)

def chasewin(gencount):  # Herbivores mutating faster than herbs
    runmodel(gencount, herbivoremutationsize = 5)

def chaseloss(gencount):  #Herbs mutating faster than herbivores
    runmodel(gencount, herbmutationsize = 5)
