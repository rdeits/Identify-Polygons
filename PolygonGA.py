from __future__ import division

import numpy as np
import random

from ga import FitnessFunction,GA
from ga import Individual as OldIndividual

class Individual(OldIndividual):
    def __init__(self, fitness_function, genotype=None):
        self.dirty = True
        if genotype is None:
            self.genotype = [(random.random()*(fitness_function.ub[i]-
                fitness_function.lb[i]) + fitness_function.lb[i])\
                        for i in range(fitness_function.num_vars)]
        else:
            self.genotype = genotype
        self.dirty = True
        self._fitness = 1e308
        self.fitness_function = fitness_function
        self.sort_genotype()

    def sort_genotype(self):
        self.genotype = np.reshape(self.genotype,(-1,2))
        self.genotype = self.genotype[np.argsort([i[1] for i in self.genotype])]
        self.genotype = np.reshape(self.genotype,(-1))

    def evaluate(self):
        if self.dirty:
            cartesian_genotype = (
                    [5 + self.genotype[0]*np.cos(self.genotype[1]),
                        5 + self.genotype[0]*np.sin(self.genotype[1]),
                    5 + self.genotype[2]*np.cos(self.genotype[3]),
                        5 + self.genotype[2]*np.sin(self.genotype[3]),
                    5 + self.genotype[4]*np.cos(self.genotype[5]),
                        5 + self.genotype[4]*np.sin(self.genotype[5]),
                    5 + self.genotype[6]*np.cos(self.genotype[7]),
                        5 + self.genotype[6]*np.sin(self.genotype[7])])
            self._fitness = self.fitness_function(cartesian_genotype)
            self.dirty = False


class PolyGA(GA):
    def combine(self,parent0,parent1):
        mask0 = np.array([random.random() for i in range(self.num_vars)])
        mask1 = np.array([random.random() for i in range(self.num_vars)])
        genotype0 = (parent0.genotype * mask0 + 
                parent0.genotype * (1-mask0))
        genotype1 = (parent1.genotype * mask1 +
                parent1.genotype * (1-mask1))
        return [Individual(self.fitness_function, genotype0),
                Individual(self.fitness_function, genotype1)]
    def mutate_all(self):
        """perform mutation on all individuals in the population except the top 
        self.elite_count by randomly replacing values in those individuals with 
        new values within the allowable range"""
        for i in range(self.elite_count, len(self.individuals)):
            for j in range(self.num_vars):
                if random.random() < self.mut_rate:
                    self.individuals[i].genotype[j] = (random.random()*
                            (self.ub[j]-self.lb[j])+self.lb[j])
                    self.individuals[i].sort_genotype()

if __name__ == "__main__":
    # def myfunc1(x):
        # return sum([i**2 for i in x])
    # fitness_func = FitnessFunction(myfunc1,4,[-10]*12,[10]*12)

    import fitness
    fitness_func = FitnessFunction(fitness.check_points,8,[0,0]*4,[7,2*np.pi]*4)

    ga = PolyGA(fitness_func)
    ga.run()
