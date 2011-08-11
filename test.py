import numpy as np
import matplotlib.pyplot as plt
from polygon import Polygon
from identify import *
import ga.newFitness as fitness
import os.path
p = Polygon(num_sides = 5, regular = False)
data = p.sample(400, sigma = 0.05)
tester = fitness.PolygonTester(data, 5)
ga = GA(tester, stall_generations = 20)
new_fitness = ga.run()[0]

[fitness, genotype, corners] = ga.report(False)

plt.figure()
plt.hold(True)
plt.plot([corners[i][0] for i in range(-1,len(corners))], 
         [corners[i][1] for i in range(-1,len(corners))],'k-') 
plt.plot([p.corners[i][0] for i in range(-1,len(p.corners))], 
         [p.corners[i][1] for i in range(-1,len(p.corners))],'r-') 
plt.plot([p[0] for p in data], [p[1] for p in data], 'bo')
n = 0
base_path = 'doc/files/2011-08-11'
while True:
    fname = 'test-5-side%03d.png' %n
    if os.path.exists(os.path.join(base_path, fname)):
        n += 1
    else:
        plt.savefig(os.path.join(base_path, fname))
        break



