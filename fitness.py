from __future__ import division

import numpy as np
import Image

image = Image.open('sample_med.png')
(width,height) = image.size
image = image.convert('RGB')
image_data = np.resize(image.getdata(),(height,width,3))
print image_data

def line_distance(x0,y0,x1,y1,x2,y2):
    return np.abs((x2-x1)*(y1-y0)-(x1-x0)*(y2-y1))/\
        np.sqrt(np.square(x2-x1)+np.square(y2-y1))

def check_points(line_data):
    error = 0
    points = np.reshape(np.array(line_data),(-1,2))
    for (i,point) in enumerate(points):
        for j in range(i+1,len(points)):
            if all(point == points[j]):
                return 1e308
    for x in range(width):
        for y in range(height):
            # print "Value at x:",x,"y:",y,"is",image_data[y][x][0]
            min_dist = min([line_distance(x,y,
                points[i][0],
                points[i][1],
                points[(i+1)%len(points)][0],
                points[(i+1)%len(points)][1]) for i in range(len(points))])
            error += min_dist*image_data[y][x][0]
    return error

