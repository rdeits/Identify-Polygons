import numpy as np
import matplotlib.pyplot as plt
from polygon import Polygon
from identify import *
import ga.newFitness as fit
import os.path
import random

num_data_points = 400
sigma = 0.05

result_file = open('results.txt','w')
print >>result_file, "| Image | Real N | Calculated N | Sensor sigma |"

for j in range(40):
    real_num_sides = random.randint(3, 6)
    p = Polygon(num_sides = real_num_sides, regular = False)
    data = p.sample(num_data_points, sigma = sigma)
    best_fitness = 1e308
    num_sides = 3
    ga_list = []
    while True:
        tester = fit.PolygonTester(data, num_sides)
        ga = GA(tester, stall_generations = 20)
        new_fitness = ga.run()[0]
        ga_list.append(ga)
        if new_fitness > .9 * best_fitness:
            print "Number of sides was", num_sides - 1
            break
        best_fitness = new_fitness
        num_sides += 1

    [fitness, genotype, corners] = ga_list[-2].report(False)
    plt.figure()
    plt.hold(True)
    plt.plot([p.corners[i][0] for i in range(-1,len(p.corners))], 
             [p.corners[i][1] for i in range(-1,len(p.corners))],'r-') 
    plt.plot([corners[i][0] for i in range(-1,len(corners))], 
             [corners[i][1] for i in range(-1,len(corners))],'k-') 
    plt.plot([point[0] for point in data], [point[1] for point in data], 'b.')
    plt.legend(["Real Polygon, # sides: %i" %real_num_sides, "Calculated Polygon, # sides: %i" %len(corners), "Sensor Points"])
    n = 0
    base_path = 'doc/files/2011-08-11/n-side'
    while True:
        fname = 'test%03d.png' %n
        if os.path.exists(os.path.join(base_path, fname)):
            n += 1
        else:
            plt.savefig(os.path.join(base_path, fname))
            break
    print >>result_file,  "|{{thumb{[img[foo|files/2011-08-11/n-side/test%03d.png][files/2011-08-11/n-side/test%03d.png]]}}}" %(n,n) + " | " + str(real_num_sides)\
            + " | " + str(len(corners)) + " | " + str(sigma) + " |"

result_file.close()



