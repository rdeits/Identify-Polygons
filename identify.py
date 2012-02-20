from __future__ import division

import numpy as np
import random
from ga.ga import GA as BaseGA
from ga.ga import Individual as BaseIndividual
import sys
# import matplotlib.pyplot as plt

class GA(BaseGA):
    def create_population(self,size):
        """Initialize the population with new individuals.
        The generation of a new (presumably random) individual is handled by the
        Individual class."""
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
    def report(self,plot=False):
        self.sort()
        print "Best fitness:", self.individuals[0].fitness
        print "Best genotype:", self.individuals[0].genotype
        corners = self.fitness_function.generate_polygon(self.individuals[0].genotype)
        if plot:
            self.fitness_function.plot_estimate(self.individuals[0].genotype)
        return [self.individuals[0].fitness, self.individuals[0].genotype, corners]
        # plt.figure()
        # plt.plot(self.best_fitnesses)
        # plt.show()


class Individual(BaseIndividual):
    """each individual in the population is an instance of Individual, which
    contains two public fields: self.genotype is a numpy array of the continuous
    values which that individual passes to the objective function self.fitness
    is the numerical fitness score for that individual as returned by the
    objective function"""
    def __init__(self, fitness_function, genotype=None):
        if genotype is None:
            self.genotype = [int(round(random.random()*(fitness_function.ub[i]-
                fitness_function.lb[i]) + fitness_function.lb[i]))\
                        for i in range(fitness_function.num_vars)]
        else:
            self.genotype = genotype
        self.genotype.sort()
        self.fitness_function = fitness_function

    @property
    def genotype(self):
        return self._genotype

    @genotype.setter
    def genotype(self,value):
        value.sort()
        self._genotype = value
        self._dirty = True
        self._fitness = 1e308


if __name__ == "__main__":
    # import ga.newFitness as fitness
    import ga.fitness as fitness
    best_fitness = 1e308
    num_sides = 3
    ga_list = []
    while True:
        tester = fitness.PolygonTester(sys.argv[1],
                num_sides)
        ga = GA(tester,stall_generations = 20)
        new_fitness = ga.run()[0]
        ga_list.append(ga)
        if new_fitness > 0.9 * best_fitness:
            print "Number of sides was", num_sides - 1
            break
        best_fitness = new_fitness
        num_sides += 1
    ga_list[-2].report(True)
