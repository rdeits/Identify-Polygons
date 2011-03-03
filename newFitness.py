from __future__ import division

import numpy as np
from scipy import stats
import Image
import matplotlib.pyplot as plt

image = Image.open('sample_med_rot.png')
(width,height) = image.size
image = image.convert('RGB')
image_data = np.resize(image.getdata(),(height,width,3))
print image_data
total_value = 0
x_weight = 0
y_weight = 0
for x in range(width):
    for y in range(height):
        x_weight += x * image_data[y][x][0]
        y_weight += y * image_data[y][x][0]
        total_value += image_data[y][x][0]

centroid = (x_weight/total_value, y_weight/total_value)
print "centroid:",centroid

def find_residues(x,y):
    A = np.vstack([x,np.ones(len(x))]).T
    [[m,c], residues,rank,s] = np.linalg.lstsq(A,y)
    # print "slope:",m
    # print "intercept:",c
    # print "residues",residues
    if len(residues) == 0:
        return 0
    else:
        return residues[0]

# def find_residues(x,y):
    # slope,intercept,r,p,stderr = stats.linregress(x,y)
    # # print "slope:",slope
    # # print "intercept:",intercept
    # # print "residues",stderr
    # x = np.array(x)
    # # plt.plot(x,slope*x+intercept)
    # return stderr

def calculate_error(thetas):
    # plt.figure()
    # plt.hold(True)
    error = 0
    for i, t0 in enumerate(thetas):
        t1 = thetas[(i+1)%len(thetas)]
        x_bin = []
        y_bin = []
        for x in range(width):
            for y in range(height):
                if x == centroid[0]:
                    if y > centroid[1]:
                        angle = np.pi/2
                    else:
                        angle = np.pi*3/2
                else:
                    angle = np.arctan((y-centroid[1])/(x-centroid[0]))
                if x < centroid[0]:
                    angle += np.pi
                angle = (angle+2*np.pi)%(2*np.pi)
                # print "(",x,",",y,") at angle",angle
                if ((t0 < t1) and (angle > t0 and angle < t1)
                        or ((t0 >= t1) and (angle > t0 or angle < t1))):
                    for i in range(image_data[y][x][0]):
                        x_bin.append(x)
                        y_bin.append(y)
        if len(x_bin) > 0:
            error += find_residues(x_bin,y_bin)
        # else:
            # print "no points between",t0,'and',t1
    # print "error =",error
    return error
    # plt.show()

if __name__ == "__main__":
    # calculate_error([np.pi/4,np.pi*3/4,np.pi*5/4,np.pi*7/4])
    print calculate_error([0,np.pi/2,np.pi,np.pi*3/2])
