from __future__ import division

import numpy as np
from scipy import stats
import Image
import matplotlib.pyplot as plt
import csv

image = Image.open('sample_tri2.png')
(width,height) = image.size
image = image.convert('RGB')
image_data = np.resize(image.getdata(),(height,width,3))
total_value = 0
x_weight = 0
y_weight = 0

f = open('data.csv','wb')
csv_writer = csv.writer(f)
for x in range(width):
    for y in range(height):
        if image_data[y][x][0] > 0:
            csv_writer.writerow([x,y])
f.close()
f = open('data.csv','rb')
csv_reader = csv.reader(open('data.csv','rb'))
data = [[float(row[0]),float(row[1])] for row in csv_reader] 
x_list = [el[0] for el in data]
y_list = [el[1] for el in data]
centroid = (sum(x_list)/len(x_list), sum(y_list)/len(y_list))
print "centroid:",centroid

angles = np.zeros(len(data))
for i,[x,y] in enumerate(data):
    if x == centroid[0]:
        if y > centroid[1]:
            angles[i] = np.pi/2
        else:
            angles[i] = np.pi*3/2
    else:
        angles[i] = np.arctan((y-centroid[1])/(x-centroid[0]))
    if x < centroid[0]:
        angles[i] += np.pi
    angles[i] %= (2*np.pi)
    


def regression(x,y):
    A = np.vstack([x,np.ones(len(x))]).T
    [[m,b], residues,rank,s] = np.linalg.lstsq(A,y)
    # print "slope:",m
    # print "intercept:",c
    # print "residues",residues
    # x = np.array(x)
    # plt.plot(x,m*x+b)
    # plt.figure()
    # plt.plot(x,y,'ro')
    if len(residues) == 0:
        return 0, 0, 0
    else:
        return m, b, residues[0]

def orthogonal_regression(x,y):
    x = np.array(x)
    y = np.array(y)
    n = len(x)
    x_bar = np.mean(x)
    y_bar = np.mean(y)
    s_xx = 1/(n-1) * np.sum(np.power(x-x_bar,2))
    s_xy = 1/(n-1) * np.sum(np.multiply((x-x_bar),(y-y_bar)))
    s_yy = 1/(n-1) * np.sum(np.power(y-y_bar,2))
    beta1 = ((s_yy - s_xx + np.sqrt(np.power(s_yy-s_xx,2)+4*np.power(s_xy,2)))/
            (2*s_xy))
    beta0 = y_bar - beta1*x_bar
    a = -beta1
    b = 1
    c = -beta0
    residue = np.sum(np.divide(np.abs(a*x + b*y + c),np.sqrt(a**2 + b**2)))
    # print "slope:", beta1
    # print "intercept:", beta0
    # print "residue:",residue
    return beta1, beta0, residue

def calculate_error(thetas):
    error = 0
    for i, t0 in enumerate(thetas):
        t1 = thetas[(i+1)%len(thetas)]
        x_bin = []
        y_bin = []
        for i, [x,y] in enumerate(data):
            # print "(",x,",",y,") at angle",angle
            if ((t0 < t1) and (angles[i] > t0 and angles[i] < t1)
                    or ((t0 >= t1) and (angles[i] > t0 or angles[i] < t1))):
                x_bin.append(x)
                y_bin.append(y)
        if len(x_bin) > 1:
            m, b, residues = orthogonal_regression(x_bin,y_bin)
            error += residues
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
        for i, [x,y] in enumerate(data):
            # print "(",x,",",y,") at angle",angle
            if ((t0 < t1) and (angles[i] > t0 and angles[i] < t1)
                    or ((t0 >= t1) and (angles[i] > t0 or angles[i] < t1))):
                x_bin.append(x)
                y_bin.append(y)
        if len(x_bin) > 1:
            m, b, residues = orthogonal_regression(x_bin,y_bin)
            error += residues
            slopes.append(m)
            intercepts.append(b)
        else:
            m = b = 0
            # print "no points between",t0,'and',t1
        plt.plot([0,width],[b, width*m+b])
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
    # print calculate_error([0,np.pi/2,np.pi,np.pi*3/2])
    from timeit import Timer
    t = Timer('print calculate_error([0,np.pi/2,np.pi,np.pi*3/2])','from newFitness import calculate_error;import numpy as np')
    print t.timeit(1)

