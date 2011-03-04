from __future__ import division

import numpy as np
from scipy import stats
import Image
import matplotlib.pyplot as plt
import csv

image = Image.open('sample.png')
(width,height) = image.size
image = image.convert('RGB')
image_data = np.resize(image.getdata(),(height,width,3))
# print image_data
total_value = 0
x_weight = 0
y_weight = 0
# for x in range(width):
    # for y in range(height):
        # x_weight += x * image_data[y][x][0]
        # y_weight += y * image_data[y][x][0]
        # total_value += image_data[y][x][0]

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
# print data
x_list = [el[0] for el in data]
y_list = [el[1] for el in data]
# print x_list
centroid = (sum(x_list)/len(x_list), sum(y_list)/len(y_list))
print "centroid:",centroid

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
    # plt.hold(True)
    # x = range(width)
    # y = range(height)
    # X, Y = np.meshgrid(x,y)
    # plt.contourf(X,Y,image_data[:,:,0])
    error = 0
    # slopes = []
    # intercepts = []
    # corners = []
    for i, t0 in enumerate(thetas):
        t1 = thetas[(i+1)%len(thetas)]
        x_bin = []
        y_bin = []
        for x,y in data:
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
                x_bin.append(x)
                y_bin.append(y)
        if len(x_bin) > 0:
            m, b, residues = regression(x_bin,y_bin)
            error += residues
            # slopes.append(m)
            # intercepts.append(b)
        # else:
            # m = b = 0
            # print "no points between",t0,'and',t1
        # plt.plot([0,width],[b, width*m+b])
    # print "error =",error

    # for i in range(len(slopes)):
        # m0 = slopes[i]
        # b0 = intercepts[i]
        # m1 = slopes[(i+1)%len(slopes)]
        # b1 = intercepts[(i+1)%len(slopes)]
        # x = (b1-b0)/(m0-m1)
        # corners.append([x, m0*x+b0])
    # for [x,y] in corners:
        # plt.plot(x,y,'ro')
    # plt.xlim([0,width])
    # plt.ylim([0,height])
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
        for x,y in data:
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
                x_bin.append(x)
                y_bin.append(y)
        if len(x_bin) > 0:
            m, b, residues = regression(x_bin,y_bin)
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
    print plot_estimate([0,np.pi/2,np.pi,np.pi*3/2])
