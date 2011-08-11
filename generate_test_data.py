from __future__ import division
from polygon import Polygon
import tables as tab

def sigma_format(sigma):
    return 'sigma_'+str(sigma)

def sides_format(sides):
    return 'sides_'+str(sides)

class Point2D(tab.IsDescription):
    x = tab.Float64Col()
    y = tab.Float64Col()

with tab.openFile('./testData.h5', mode = 'a', title = 'Polygon Identification Test') as h5file:
    for sigma in [0, .05, .1]:
        if not h5file.root.__contains__(sigma_format(sigma)):
            sigma_group = h5file.createGroup(h5file.root, sigma_format(sigma))
        else:
            sigma_group = h5file.root._v_children[sigma_format(sigma)]
        for sides in range(3, 8):
            if not sigma_group.__contains__(sides_format(sides)):
                sides_group = h5file.createGroup(sigma_group, sides_format(sides))
            else:
                sides_group = sigma_group._v_children[sides_format(sides)]
            table = h5file.createTable(sides_group,'sensor_data',Point2D)
            p = Polygon(num_sides = sides, regular = False)
            data = p.sample(400, sigma = sigma)
            row = table.row
            for point in data:
                row['x'] = point[0]
                row['y'] = point[1]
                row.append()
            table.flush()
            corners_table = h5file.createTable(sides_group,'real_corners',Point2D)
            row = corners_table.row
            for point in p.corners:
                row['x'] = point[0]
                row['y'] = point[1]
                row.append()
            corners_table.flush()




