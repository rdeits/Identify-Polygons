import numpy as np
import matplotlib.pyplot as plt
from polygon import Polygon
from identify import *
import ga.fitness as fit
import os.path
import random
import tables as tab

# num_data_points = 400
# sigma = 0.05
fitness_improvement_factor = 0.95

"""
Read the images stored in the testData.h5 HDF5 database, try the polygon identification on them, and save the results in TiddlyWiki markup format.
"""

result_file = open('results.txt','w')
print >>result_file, "| Image | Real N | Calculated N | Sensor sigma |"

total_errors = {}

source_file = tab.openFile('testData.h5', 'r')


for group in source_file.walkGroups():
    if not 'sensor_data' in group._v_children:
        continue
    real_corners = group.real_corners.read()
    real_num_sides = len(real_corners)
    sigma = group._v_attrs['sigma']
    data = group.sensor_data.read()
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
    plt.plot([real_corners[i][0] for i in range(-1,len(real_corners))],
             [real_corners[i][1] for i in range(-1,len(real_corners))],'r-')
    plt.plot([corners[i][0] for i in range(-1,len(corners))],
             [corners[i][1] for i in range(-1,len(corners))],'k-')
    plt.plot([point[0] for point in data], [point[1] for point in data], 'b.')
    plt.legend(["Real Polygon, # sides: %i" %real_num_sides, "Calculated Polygon, # sides: %i" %len(corners), "Sensor Points"])
    n = 0
    base_path = 'files/2011-08-15/h5'
    rel_path = os.path.join('doc', base_path)
    if not os.path.isdir(rel_path):
        os.mkdir(rel_path)
    while True:
        fname = 'test%03d.png' %n
        if os.path.exists(os.path.join(rel_path, fname)):
            n += 1
        else:
            plt.savefig(os.path.join(rel_path, fname))
            plt.close()
            break
    print >>result_file,  "|{{thumb{[img[foo|"+base_path+"/test%03d.png][" %n +base_path+"/test%03d.png]]}}}" %n + " | " + str(real_num_sides) + " | " + str(len(corners)) + " | " + str(sigma) + " |"
    side_error = len(corners) - real_num_sides
    if side_error in total_errors:
        total_errors[side_error] += 1
    else:
        total_errors[side_error] = 1

result_file.close()
print total_errors



