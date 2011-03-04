from __future__ import division

import numpy as np
import random

class FitnessFunction:
    def __init__(self,function,num_vars,lb=None,ub=None):
        # function should take a vector of length num_vars
        self.function = function
        self.num_vars = num_vars
        if lb is None:
            self.lb = [0 for i in range(num_vars)]
        else:
            self.lb = lb
        if ub is None:
            self.ub = [1 for i in range(num_vars)]
        else:
            self.ub = ub
    def __call__(self,x):
        assert len(x) == self.num_vars, "len(x) != num_vars"
        assert [x[i] > self.lb[i] for i in range(self.num_vars)], "x below lb"
        assert [x[i] < self.ub[i] for i in range(self.num_vars)], "x above ub"
        return self.function(x)

# def pack_fitness_function(function,num_vars,lb=None,ub=None):
    # packed_function = function
    # packed_function.num_vars = num_vars
    # packed_function.lb = lb

class GA:
    def __init__(self,fitness_function,pop_size = 12,
            keep_fraction = .5,
            mut_rate = 0.1,
            elite_count = 1,
            max_generations = 10000,
            fitness_tol = 0.1,
            min_fitness = 0,
            stall_generations = 1000):
        self.fitness_function = fitness_function
        self.pop_size = pop_size
        self.keep_fraction = keep_fraction
        self.mut_rate = mut_rate
        self.elite_count = elite_count
        self.max_generations = max_generations
        self.fitness_tol = 0.1
        self.min_fitness = min_fitness
        self.stall_generations = stall_generations
        self.generation = 0
        self.best_fitnesses = []
        self.keep_num = int((self.keep_fraction * pop_size) / 2 * 2)

        self.lb = self.fitness_function.lb
        self.ub = self.fitness_function.ub
        self.num_vars = self.fitness_function.num_vars

        self.individuals = self.create_population(self.pop_size)

    def create_population(self,size):
        individuals = [Individual(self.fitness_function,None)\
                for i in range(size)]
        return np.array(individuals)

    def sort(self):
        self.individuals = self.individuals[np.argsort(
            [ind.fitness for ind in self.individuals])]

    def evaluate(self):
        for indiv in self.individuals:
            indiv.evaluate()

    def step(self):
        '''Run an entire generation'''
        print "stepping"
        self.evaluate()
        self.sort() # This causes the fitness function to be called as needed
        self.best_fitnesses.append(self.individuals[0].fitness)
        self.print_status()
        if self.done():
            self.report()
            return True
        self.cull()
        self.reproduce()
        self.mutate_all()
        self.generation += 1
        return False

    def print_status(self):
        print "=================================="
        print "Generation",self.generation,"run. Sorted individuals:"
        for indiv in self.individuals:
            print "Genotype:", indiv.genotype
            print "Fitness:", indiv.fitness,"\n"

    def run(self):
        while not self.step():
            pass

    def done(self):
        return (self.generation >= self.max_generations or
                (self.generation > self.stall_generations and 
                    (self.best_fitnesses[-self.stall_generations] - 
                        self.best_fitnesses[-1] == 0)) or 
                    (self.best_fitnesses[-1] <= self.min_fitness))

    def report(self):
        print "Best fitness:", self.individuals[0].fitness
        print "Best genotype:", self.individuals[0].genotype

    def reproduce(self):
        new_children = []
        assert (self.pop_size-len(self.individuals)) % 2 == 0
        for i in range((self.pop_size-len(self.individuals))//2):
            [parent0, parent1] = self.select_parents()
            [child0, child1] = self.combine(parent0, parent1)
            new_children.append(child0)
            new_children.append(child1)
            # print "combined genotypes:"
            # print parent0.genotype
            # print parent1.genotype
            # print "got genotypes:"
            # print child0.genotype
            # print child1.genotype
            # print "\n\n"
        self.individuals = np.concatenate((self.individuals,
            np.array(new_children)))

    def select_parents(self):
        """This function chooses two parents from the population to be 
        parents for two children by selecting the best two out of three
        random individuals from the population."""

        # Choose three different individuals at random
        available = range(len(self.individuals))
        chosen = np.array([0 for i in range(3)])
        for i in range(3):
            chosen[i] = available[random.randrange(0,
                len(self.individuals)-i)]
            available.remove(chosen[i])
        candidates = self.individuals[chosen]

        # sort the three candidates by fitness
        candidates = candidates[np.argsort([ind.fitness for ind in candidates])]

        # choose the best two candidates to be parents and return 
        # those individuals
        return [candidates[0],candidates[1]]

    def combine(self,parent0,parent1):
        crossover_point = random.randint(0,self.num_vars-1)
        genotype0 = (parent0.genotype[:crossover_point] +
                parent1.genotype[crossover_point:])
        genotype1 = (parent1.genotype[:crossover_point] +
                parent1.genotype[crossover_point:])
        return [Individual(self.fitness_function, genotype0),
                Individual(self.fitness_function, genotype1)]

    def cull(self):
        """self.cull() removes the least-fit members of the population, keeping 
        self.keep_num individuals"""
        # remove the individuals at the end of the list 
        # (those with the highest (worst) fitness values)
        self.individuals = np.resize(self.individuals,self.keep_num)

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
                    new_genotype[j] = new_genotype[j]+offset
                    if new_genotype[j] > self.ub[j]:
                        new_genotype[j] = self.ub[j]
                    elif new_genotype[j] < self.lb[j]:
                        new_genotype[j] = self.lb[j]
            indiv.genotype = new_genotype

    def update_mutation_factor(self):
        if self.generation > 10:
            self.mutation_factor = 2.5/self.generation
        else:
            self.mutation_factor = 0.25

class PolygonGA(GA):
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
                    new_genotype[j] = new_genotype[j]+offset
                    new_genotype[j] %= (2*np.pi)
                    if new_genotype[j] > self.ub[j]:
                        new_genotype[j] = self.ub[j]
                    elif new_genotype[j] < self.lb[j]:
                        new_genotype[j] = self.lb[j]
            indiv.genotype = new_genotype
    def report(self):
        print "Best fitness:", self.individuals[0].fitness
        print "Best genotype:", self.individuals[0].genotype
        newFitness.plot_estimate(self.individuals[0].genotype)


class Individual(object):
    """each individual in the population is an instance of Individual, 
    which contains three fields:
    self._genotype is a numpy array of the continuous values which that 
        individual passes to the objective function
    self.fitness is the numerical fitness score for that individual as 
        returned by the objective function
    self.dirty specifies whether that individual has been mutated (or created) 
        since it was last evaluated, and thus determines whether the individual
        needs to be evaluated by the objective function."""
    def __init__(self, fitness_function, genotype=None):
        if genotype is None:
            self.genotype = [(random.random()*(fitness_function.ub[i]-
                fitness_function.lb[i]) + fitness_function.lb[i])\
                        for i in range(fitness_function.num_vars)]
        else:
            self.genotype = genotype
        self.fitness_function = fitness_function

    @property
    def genotype(self):
        return self._genotype

    @genotype.setter
    def genotype(self,value):
        self._genotype = value
        self.dirty = True
        self._fitness = 1e308
    
    @property
    def fitness(self):
        self.evaluate()
        return self._fitness

    def evaluate(self):
        if self.dirty:
            self._fitness = self.fitness_function(self.genotype)
            self.dirty = False

if __name__ == "__main__":
    def myfunc1(x):
        return sum([i**2 for i in x])
    # fitness_func = FitnessFunction(myfunc1,4,[-10]*12,[10]*12)

    # import fitness
    # fitness_func = FitnessFunction(fitness.check_points,4,[0]*4,[2*np.pi]*4)
    import newFitness
    fitness_func = FitnessFunction(newFitness.calculate_error,4,[0]*4,[2*np.pi]*4)

    ga = PolygonGA(fitness_func,min_fitness = 5400)
    ga.run()



