from __future__ import division
import numpy as np
import random
import matplotlib.pyplot as plt

"""
This program is meant to provide a framework for generating random polygons to
be used as inputs to the polygon identification system. We will produce sample
data by first generating a Polygon object and then taking sample points which
lie on that polygon. The points will then be offset in a random direction to
simulate sensor noise and error.
"""

class Polygon:
    def __init__(self, num_sides = 3, regular = True):
        self.num_sides = num_sides
        if regular:
            self.angles = np.ones(num_sides) * 2*np.pi/num_sides
        else:
            self.angles = np.zeros(num_sides)
            for i in range(num_sides-1):
                min_angle = max(0, 
                                2*np.pi - (num_sides - i - 1)*np.pi - sum(self.angles[0:i]))
                max_angle = min(np.pi,
                                2*np.pi - sum(self.angles[0:i]))
                # print min_angle, max_angle
                self.angles[i] = random.random() * (max_angle - min_angle) + min_angle
            self.angles[-1] = 2*np.pi - sum(self.angles[0:num_sides-1])
        cum_angles = [sum(self.angles[0:i+1]) for i in range(num_sides)]
        self.corners = [(np.cos(cum_angles[i]), np.sin(cum_angles[i]))
                        for i in range(num_sides)]
        self.sides = [np.sqrt((self.corners[i][0] - self.corners[i-1][0])**2
                              + (self.corners[i][1] - self.corners[i-1][1])**2)
                      for i in range(num_sides)]
        self.cum_sides = [sum(self.sides[0:i+1]) for i in range(num_sides)]
        self.perimeter = self.cum_sides[-1]
        # print self.angles
        # print cum_angles
        # print self.corners
        print self.sides
        print self.cum_sides
        # plt.plot([self.corners[i][0] for i in range(-1,len(self.corners))],
                 # [self.corners[i][1] for i in range(-1,len(self.corners))])
        # plt.hold(True)
        # plt.plot([0], [0])
        # plt.show()
    def sample(self, n, sigma = 0):
        """
        Return a list of n points which lie on the polygon, each point having
        been shifted in a random direction by a random distance whose standard
        deviation is zero.
        """
        points = []
        for i in range(n):
            rand_pos = random.random() * self.perimeter
            for j in range(self.num_sides):
                if rand_pos <= self.cum_sides[j]:
                    current_side = j
                    break
            offset = self.cum_sides[current_side] - rand_pos
            side_fraction = offset/self.sides[current_side]
            point = ((side_fraction*(self.corners[current_side-1][0]
                                     - self.corners[current_side][0])
                      + self.corners[current_side][0]),
                     (side_fraction*(self.corners[current_side-1][1]
                                     - self.corners[current_side][1])
                      + self.corners[current_side][1]))
            points.append(point)        
        plt.plot([self.corners[i][0] for i in range(-1,len(self.corners))], 
                 [self.corners[i][1] for i in range(-1,len(self.corners))]) 
        plt.hold(True) 
        plt.plot([p[0] for p in points], [p[1] for p in points], 'ro')
        plt.show()
        return points

if __name__ == "__main__":
    p = Polygon(num_sides = 3, regular = False)
    p.sample(100)
        
