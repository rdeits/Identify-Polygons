from __future__ import division

import numpy as np
# from scipy import stats, weave
import Image
import matplotlib.pyplot as plt
import csv
import time
import os
from matplotlib.nxutils import pnpoly

def orthogonal_regression(x,y):
    """Given two arrays, x and y, perform orthogonal regression on them, as
    described in http://en.wikipedia.org/wiki/Deming_regression. Returns
    [slope, intercept, total residue]"""
    # x = np.array(x)
    # y = np.array(y)
    # print "x:"
    # print x
    # print "y:"
    # print y
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
    """A class based on the FitnessFunction class from ga.py to be used for
    polygon fitting. It takes a filename and a number of sides and tests
    polygon fits against the data in the file. The file can either be a CSV
    file of (x, y) pairs of points approximately defining the edges of the
    polygon or a PNG image, in which any point with non-zero red value is
    considered a candidate for part of the edge of the polygon. 

    When doing optimization, the PolygonTester's __call__ expects a list of
    length num_vars specifiying the indices of four points in its data set,
    sorted by their angle relative to their centroid. It returns the total
    orthogonal distance of all points from the polygon calculated using those
    four indices for orthogonal regression."""
    def __init__(self, input_data, num_vars):
        self.num_vars = num_vars
        self.load_data(input_data)
        self.calculate_angles()
        self.lb = [0]*num_vars
        self.ub = [len(self.data)]*num_vars
        self.sort_data()

    def load_data(self,input_data):
        if isinstance(input_data, str):
            extension = input_data.split(os.path.extsep)[-1]
            assert extension == 'png' or extension == 'csv', "Data must be png or csv"
            if  extension == 'png':
                self.data_type = "image"
                self.image = Image.open(input_data)
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
            else:
                self.data_type = "csv"
                csv_reader = csv.reader(open(input_data,'rb'))
                self.data = [[float(row[0]),float(row[1])] for row in csv_reader] 
        else:
            self.data_type = "array"
            self.data = input_data
        self.x_list = np.array([el[0] for el in self.data])
        self.y_list = np.array([el[1] for el in self.data]) 
        self.x_range = [min(self.x_list),max(self.x_list)]
        self.y_range = [min(self.y_list),max(self.y_list)]
        if self.data_type == "csv":
            self.width = self.x_range[1]-self.x_range[0] 
            self.height = self.y_range[1] - self.y_range[0]
        self.centroid = (sum(self.x_list)/len(self.x_list), 
                sum(self.y_list)/len(self.y_list))
        # print "centroid:",self.centroid


    def calculate_angles(self):
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

    
    def sort_data(self):
        # print np.argsort(self.angles)
        # self.data = self.data[np.argsort(self.angles)]
        # self.x_list = np.array([el[0] for el in self.data])
        # self.y_list = np.array([el[1] for el in self.data])
        self.x_list = self.x_list[np.argsort(self.angles)]
        self.y_list = self.y_list[np.argsort(self.angles)]

    def __call__(self,indices):
        """Divide the data points up into num_vars bins at the points specified
        in indices. Then perform orthogonal regression on all the points in
        each bin and return the total error. Thus, each bin of points is
        considered to be a candidate for the collection of all the points along
        a given side of the polygon."""
        # self.error = 0
        # for i, t0 in enumerate(indices):
            # t1 = indices[(i+1)%len(indices)]
            # if t0 < t1:
                # self.x_bin = self.x_list[t0:t1]
                # self.y_bin = self.y_list[t0:t1]
            # else:
                # self.x_bin = np.hstack((self.x_list[t0:],self.x_list[:t1]))
                # self.y_bin = np.hstack((self.y_list[t0:],self.y_list[:t1]))
            # if len(self.x_bin) > 1:
                # self.error +=  orthogonal_regression(self.x_bin,self.y_bin)[2]
        # return self.error
        self.generate_polygon(indices)
        return self.error

    def generate_polygon(self, indices):
        slopes = []
        intercepts = []
        self.corners = []
        self.error = 0
        for i, t0 in enumerate(indices):
            t1 = indices[(i+1)%len(indices)]
            if t0 < t1:
                self.x_bin = self.x_list[t0:t1]
                self.y_bin = self.y_list[t0:t1]
            else:
                self.x_bin = np.hstack((self.x_list[t0:],self.x_list[:t1]))
                self.y_bin = np.hstack((self.y_list[t0:],self.y_list[:t1]))
            if len(self.x_bin) > 1:
                m, b, residue =  orthogonal_regression(self.x_bin,self.y_bin)
                self.error += residue
                slopes.append(m)
                intercepts.append(b)
            else:
                m = b = 0
                # print "no points between",t0,'and',t1

        for i in range(len(slopes)):
            m0 = slopes[i]
            b0 = intercepts[i]
            m1 = slopes[(i+1)%len(slopes)]
            b1 = intercepts[(i+1)%len(slopes)]
            x = (b1-b0)/(m0-m1)
            self.corners.append([x, m0*x+b0])
        corner_index = 0
        for i in range(len(self.corners)):
            [x0,y0] = self.corners[i]
            [x1,y1] = self.corners[(i+1)%len(self.corners)]
            # print "Corner at", x0, ",", y0
        return self.corners

    def plot_estimate(self, indices):
        # plt.figure()
        plt.hold(True)
        if self.data_type == "image":
            x = range(self.width)
            y = range(self.height)
            X, Y = np.meshgrid(x,y)
            plt.contourf(X,Y,self.image_data[:,:,0])
        else:
            plt.plot(self.x_list,self.y_list,'bo')

        self.generate_polygon(indices)
        plt.plot([self.corners[i][0] for i in range(-1,len(self.corners))], 
                 [self.corners[i][1] for i in range(-1,len(self.corners))], 'r-') 

        plt.xlim(self.x_range)
        plt.ylim(self.y_range)
        plt.show()
        if self.data_type == "csv":
            f = open("corners.csv",'wb')
            csv_writer = csv.writer(f)
            for point in self.corners:
                csv_writer.writerow(point)
            f.close()


if __name__ == "__main__":
    tester = PolygonTester('sonar_data.csv',4)
    print tester([0,4,8,12])
   
