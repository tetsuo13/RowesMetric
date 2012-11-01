#!/usr/bin/env python
#
# UNC Greensboro, CSC 593, Fall 2012
#
# By Andrei Nicholson
# Mentored by Dr. Shan Suthaharan

"""
Notes:

Exposure of deceptive agent D is E = (1 / T) \sum_{t = 0}^{T - 1} s(t) \sum_{i = 0}^{N} v(i,t)n(i,t) (eq. 2)

v(i,t) = visibility at time t from non-deceptive agent i
p(x,y) = probability, agent at the location (x,y)
q(s,h) = probability, speed and heading
p(x,y)q(s,h) = joint probability, particular location with a particular velocity vector
s(t) = k_1 / (k_1 + p(x,y)q(s,h)) (eq. 3) (scale of 0 to 1)
n(i,t) = noticeability at time t by agent i (scale of 0 to 1)
n(i,t) = k_3 / (k_3 + p(x,y))

numpy.random.normal(0, 0.01, 10)

Look through positions_seen for other (x,y) locations (with buffer?). The
return value of the proabability functions is

   (how many times this (x,y) has been observed before) / (total positions)


If n(x,y) is 1, p(x,y) = 0
"""

# Make all divisions result in a float.
from __future__ import division

import sys

from RoweMetric.database import setup_database
from RoweMetric import grid
from RoweMetric import noticeability

database = []

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Requires path to data file'
        sys.exit()

    # Only process regions in this list. Leave empty to process all regions.
    restrict_to_regions = []

    # Read in database of agents from Kinect.
    database = setup_database(sys.argv[1])

    # Set up bounding box around agent positions.
    grid = grid.Grid(database)

    # Prepare all regions within bounding box.
    regions = grid.calculate_regions(database)

    print 'n(region) = [non-deceptive, deceptive]'
    print

    if len(restrict_to_regions) > 0:
        for region_num in restrict_to_regions:
            print 'Region', str(region_num),
            print noticeability.do_noticeability(database,
                                                 grid.area_of_region(),
                                                 regions[region_num][0],
                                                 regions[region_num][1])
    else:
        for i, region in enumerate(regions):
            print 'Region', str(i),
            print noticeability.do_noticeability(database,
                                                 grid.area_of_region(),
                                                 region[0], region[1])