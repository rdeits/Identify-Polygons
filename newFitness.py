from __future__ import division

import numpy as np
from scipy import stats, weave
import Image
import matplotlib.pyplot as plt
import csv
import time

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

class PolygonTester:
    def __init__(self,filename,num_vars,lb=None,ub=None):
        self.num_vars = num_vars
        if lb is None:
            self.lb = [0 for i in range(num_vars)]
        else:
            self.lb = lb
        if ub is None:
            self.ub = [1 for i in range(num_vars)]
        else:
            self.ub = ub        
        self.image = Image.open(filename)
        (self.width,self.height) = self.image.size
        self.image = self.image.convert('RGB')
        self.image_data = np.resize(self.image.getdata(),(self.height,self.width,3))

        self.data = []
        # f = open('data.csv','wb')
        # csv_writer = csv.writer(f)
        for x in range(self.width):
            for y in range(self.height):
                if self.image_data[y][x][0] > 0:
                    # csv_writer.writerow([x,y])
                    self.data.append([x,y])
        # f.close()
        # f = open('data.csv','rb')
        # csv_reader = csv.reader(open('data.csv','rb'))
        # data = [[float(row[0]),float(row[1])] for row in csv_reader] 
        self.x_list = np.array([el[0] for el in self.data])
        self.y_list = np.array([el[1] for el in self.data])
        self.centroid = (sum(self.x_list)/len(self.x_list), 
                sum(self.y_list)/len(self.y_list))
        print "centroid:",self.centroid

        self.angles = np.zeros(len(self.data))
        for i,[x,y] in enumerate(self.data):
            if x == self.centroid[0]:
                if y > self.centroid[1]:
                    self.angles[i] = np.pi/2
                else:
                    self.angles[i] = np.pi*3/2
            else:
                self.angles[i] = np.arctan((y-self.centroid[1])/(x-self.centroid[0]))
            if x < self.centroid[0]:
                self.angles[i] += np.pi
            self.angles[i] %= (2*np.pi)
    

    def __call__(self,thetas):
        self.error = 0
        for i, t0 in enumerate(thetas):
            t1 = thetas[(i+1)%len(thetas)]
            slices = []
            for i in range(len(self.data)):
                if ((t0 < t1) and (self.angles[i] > t0 and self.angles[i] < t1)
                        or ((t0 >= t1) and (self.angles[i] > t0 
                            or self.angles[i] < t1))):
                    slices.append(i) # This seems to be the fastest way 
                                        # to grow the list
                    # slices[0:0] = i
            self.x_bin = self.x_list[slices]
            self.y_bin = self.y_list[slices]
            if len(self.x_bin) > 1:
                self.error +=  orthogonal_regression(self.x_bin,self.y_bin)[2]
        return self.error

    def plot_estimate(self,thetas):
        plt.figure()
        plt.hold(True)
        x = range(self.width)
        y = range(self.height)
        X, Y = np.meshgrid(x,y)
        plt.contourf(X,Y,self.image_data[:,:,0])
        error = 0
        slopes = []
        intercepts = []
        corners = []
        self.error = 0
        for i, t0 in enumerate(thetas):
            t1 = thetas[(i+1)%len(thetas)]
            slices = []
            for i in range(len(self.data)):
                if ((t0 < t1) and (self.angles[i] > t0 and self.angles[i] < t1)
                        or ((t0 >= t1) and (self.angles[i] > t0 
                            or self.angles[i] < t1))):
                    slices.append(i) # This seems to be the fastest way 
                                        # to grow the list
                    # slices[0:0] = i
            self.x_bin = self.x_list[slices]
            self.y_bin = self.y_list[slices]
            if len(self.x_bin) > 1:
                m, b, residue =  orthogonal_regression(self.x_bin,self.y_bin)
                self.error += residue
                slopes.append(m)
                intercepts.append(b)
            else:
                m = b = 0
                # print "no points between",t0,'and',t1
            plt.plot([0,self.width],[b, self.width*m+b])
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
        plt.xlim([0,self.width])
        plt.ylim([0,self.height])
        plt.show()
        return error


# if __name__ == "__main__":
    # calculate_error([np.pi/4,np.pi*3/4,np.pi*5/4,np.pi*7/4])
    # print calculate_error([0,np.pi/2,np.pi,np.pi*3/2])
    # from timeit import Timer
    # t = Timer('t.calculate_error([0,np.pi/2,np.pi,np.pi*3/2])','from newFitness import PolygonTester;import numpy as np;t=PolygonTester()')
    # print t.timeit(100)/100

