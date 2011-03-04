from __future__ import division

import numpy as np
from scipy import stats
import Image
import matplotlib.pyplot as plt

image = Image.open('sample_med_rot.png')
(width,height) = image.size
image = image.convert('RGB')
image_data = np.resize(image.getdata(),(height,width,3))
# print image_data
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

def regression(x,y):
    A = np.vstack([x,np.ones(len(x))]).T
    [[m,b], residues,rank,s] = np.linalg.lstsq(A,y)
    # print "slope:",m
    # print "intercept:",c
    # print "residues",residues
    # x = np.array(x)
    # plt.plot(x,m*x+b)
    if len(residues) == 0:
        return 0, 0, 0
    else:
        return m, b, residues[0]

# plt.figure()
# plt.hold(True)

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
    # plt.clf()
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
                angle %= (2*np.pi)
                # print "(",x,",",y,") at angle",angle
                if ((t0 < t1) and (angle > t0 and angle < t1)
                        or ((t0 >= t1) and (angle > t0 or angle < t1))):
                    if image_data[y][x][0] > 0:
                        x_bin.append(x)
                        y_bin.append(y)
        if len(x_bin) > 1:
            error += regression(x_bin,y_bin)[2]
        # else:
            # print "no points between",t0,'and',t1
    # print "error =",error
    # plt.show()
    return error

def plot_estimate(thetas):
    plt.figure()
    plt.hold(True)
    x = range(width)
    y = range(height)
    X, Y = np.meshgrid(x,y)
    plt.contourf(X,Y,image_data[:,:,0])
    error = 0
    slopes = []
    intercepts = []
    corners = []
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
                angle %= (2*np.pi)
                # print "(",x,",",y,") at angle",angle
                if ((t0 < t1) and (angle > t0 and angle < t1)
                        or ((t0 >= t1) and (angle > t0 or angle < t1))):
                    if image_data[y][x][0] > 0:
                        x_bin.append(x)
                        y_bin.append(y)
        if len(x_bin) > 0:
            m, b, residues = regression(x_bin,y_bin)
            error += residues
            slopes.append(m)
            intercepts.append(b)
        else:
            m = b = 0
        plt.plot([0,width],[b, width*m+b])
            # print "no points between",t0,'and',t1
    # print "error =",error

    for i in range(len(slopes)):
        m0 = slopes[i]
        b0 = intercepts[i]
        m1 = slopes[(i+1)%len(slopes)]
        b1 = intercepts[(i+1)%len(slopes)]
        x = (b1-b0)/(m0-m1)
        corners.append([x, m0*x+b0])
    for [x,y] in corners:
        plt.plot(x,y,'ro')
    plt.xlim([0,width])
    plt.ylim([0,height])
    plt.show()
    return error


if __name__ == "__main__":
    # calculate_error([np.pi/4,np.pi*3/4,np.pi*5/4,np.pi*7/4])
    print calculate_error([0,np.pi/2,np.pi,np.pi*3/2])
    plot_estimate([0,np.pi/2,np.pi,np.pi*3/2])
