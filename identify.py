from __future__ import division

import numpy as np
import random
from ga import GA as BaseGA
from ga import Individual as BaseIndividual
# import matplotlib.pyplot as plt

class GA(BaseGA):
    def create_population(self,size):
        individuals = [Individual(self.fitness_function,None)\
                for i in range(size)]
        self.individuals = np.array(individuals)

    def mutate_all(self):
        """perform mutation on all individuals in the population except the top 
        self.elite_count by randomly replacing values in those individuals with 
        new values within the allowable range"""
        for indiv in self.individuals[self.elite_count:]:
            self.update_mutation_factor()
            new_genotype = indiv.genotype
            for j in range(self.num_vars):
                if random.random() < self.mut_rate:
                    offset = (2*(random.random()-0.5)
                            *self.mutation_factor
                            *(self.ub[j]-self.lb[j]))
                    # print "offset:",offset
                    # if offset > 0 and offset < 1:
                        # offset = 1
                    # elif offset < 0 and offset > -1:
                        # offset = -1
                    # else:
                        # offset = int(offset)
                    new_genotype[j] = int(round(new_genotype[j]+offset))
                    new_genotype[j] %= (self.fitness_function.ub[j])
                    if new_genotype[j] > self.ub[j]:
                        new_genotype[j] = self.ub[j]
                    elif new_genotype[j] < self.lb[j]:
                        new_genotype[j] = self.lb[j]
            indiv.genotype = new_genotype
        for i in range(len(self.individuals)):
            for j in range(i):
                if self.individuals[i].genotype == self.individuals[j].genotype:
                    self.individuals[i] = Individual(self.fitness_function)
                    break
    def report(self):
        print "Best fitness:", self.individuals[0].fitness
        print "Best genotype:", self.individuals[0].genotype
        # self.fitness_function.plot_estimate(self.individuals[0].genotype)
        # plt.figure()
        # plt.plot(self.best_fitnesses)
        # plt.show()
        

class Individual(BaseIndividual):
    def __init__(self, fitness_function, genotype=None):
        if genotype is None:
            self.genotype = [int(round(random.random()*(fitness_function.ub[i]-
                fitness_function.lb[i]) + fitness_function.lb[i]))\
                        for i in range(fitness_function.num_vars)]
        else:
            self.genotype = genotype
        self.fitness_function = fitness_function

    @property
    def genotype(self):
        return self._genotype

    @genotype.setter
    def genotype(self,value):
        value.sort()
        self._genotype = value
        self.dirty = True
        self._fitness = 1e308



# def find_polygon(

if __name__ == "__main__":
    import newFitness
    num_sides = 4
    tester = newFitness.PolygonTester('sample2.png',
            num_sides,)
    ga = GA(tester,stall_generations = 20)
    ga.run()
