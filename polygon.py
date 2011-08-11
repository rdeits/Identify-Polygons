from __future__ import division
import numpy as np
import random
import matplotlib.pyplot as plt

class Polygon:
    def __init__(self, num_sides = 3, regular = True):
        if regular:
            self.angles = np.ones(num_sides) * 2*np.pi/num_sides
        else:
            self.angles = np.zeros(num_sides)
            for i in range(num_sides-1):
                min_angle = max(0, 
                                2*np.pi - (num_sides - i - 1)*np.pi - sum(self.angles[0:i]))
                max_angle = min(np.pi,
                                2*np.pi - sum(self.angles[0:i]))
                print min_angle, max_angle
                self.angles[i] = random.random() * (max_angle - min_angle) + min_angle
            self.angles[-1] = 2*np.pi - sum(self.angles[0:num_sides-1])
        cum_angles = [sum(self.angles[0:i+1]) for i in range(num_sides)]
        self.corners = [(np.cos(cum_angles[i]), np.sin(cum_angles[i]))
                        for i in range(num_sides)]
        self.sides = [np.sqrt((self.corners[i][0] - self.corners[i-1][0])**2
                              + (self.corners[i][1] - self.corners[i-1][1])**2)
                      for i in range(num_sides)]
        print self.angles
        print cum_angles
        print self.corners
        print self.sides
        plt.plot([self.corners[i][0] for i in range(-1,len(self.corners))],
                 [self.corners[i][1] for i in range(-1,len(self.corners))])
        plt.hold(True)
        plt.plot([0], [0])
        plt.show()



if __name__ == "__main__":
    p = Polygon(num_sides = 3, regular = False)
        
