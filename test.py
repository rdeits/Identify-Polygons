import numpy as np
import matplotlib.pyplot as plt
from polygon import Polygon
from identify import *
import ga.fitness as fit
import os.path
import random

num_data_points = 400
sigma = 0.05
fitness_improvement_factor = 0.95

result_file = open('results.txt','w')
print >>result_file, "| Image | Real N | Calculated N | Sensor sigma |"

total_errors = {}

for j in range(40):
    real_num_sides = random.randint(3, 6)
    p = Polygon(num_sides = real_num_sides, regular = False)
    data = p.sample(num_data_points, sigma = sigma)
    best_fitness = 1e308
    old_result = None
    new_result = None
    num_sides = 3
    while True:
        old_result = new_result
        tester = fit.PolygonTester(data, num_sides, residue_method = 'line')
        ga = GA(tester, stall_generations = 20)
        new_fitness = ga.run()[0]
        new_result = ga.report(False)
        if new_fitness > fitness_improvement_factor * best_fitness:
            print "Number of sides was", num_sides - 1
            break
        best_fitness = new_fitness
        num_sides += 1
    
    [fitness, genotype, corners] = old_result 
    print num_sides - 1, len(corners), corners
    plt.figure()
    plt.hold(True)
    plt.plot([p.corners[i][0] for i in range(-1,len(p.corners))], 
             [p.corners[i][1] for i in range(-1,len(p.corners))],'r-') 
    plt.plot([corners[i][0] for i in range(-1,len(corners))], 
             [corners[i][1] for i in range(-1,len(corners))],'k-')
    plt.plot([point[0] for point in data], [point[1] for point in data], 'b.')
    plt.legend(["Real Polygon, # sides: %i" %real_num_sides, "Calculated Polygon, # sides: %i" %len(corners), "Sensor Points"])
    n = 0
    base_path = 'files/2011-08-15/segment'
    rel_path = os.path.join('doc', base_path)
    if not os.path.isdir(rel_path):
        os.mkdir(rel_path)
    while True:
        fname = 'test%03d.png' %n
        if os.path.exists(os.path.join(rel_path, fname)):
            n += 1
        else:
            plt.savefig(os.path.join(rel_path, fname))
            break
    print >>result_file,  "|{{thumb{[img[foo|"+base_path+"/test%03d.png][" %n +base_path+"/test%03d.png]]}}}" %n + " | " + str(real_num_sides) + " | " + str(len(corners)) + " | " + str(sigma) + " |"
    side_error = len(corners) - real_num_sides
    if side_error in total_errors:
        total_errors[side_error] += 1
    else:
        total_errors[side_error] = 1

result_file.close()
print total_errors



