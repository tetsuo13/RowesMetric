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

import json 
import math
import sys

from RoweMetric import grid
from RoweMetric import noticeability

k1 = 0.5
k2 = 0.5

database = []

def calculate_speed(position_1, position_2):
    """
    Distance in meters per second.
    TODO: Distance will need to be measured in whatever Kinect uses.
    """
    x1, y1 = position_1[0], position_1[1]
    x2, y2 = position_2[0], position_2[1]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def calculate_heading(position_1, position_2):
    x1, y1 = position_1[0], position_1[1]
    x2, y2 = position_2[0], position_2[1]

    delta_x = x2 - x1
    delta_y = y2 - y1

    return math.degrees(math.atan2(delta_y, delta_x))

def get_second_operand(i, list):
    """
    TODO: What is the heading if it's the last position?
    """

    # Grab the next item in the list.
    j = i + 1

    # If the next item is past the last, get the previous item instead.
    if i == len(list) - 1:
        j = i - 1

    return [list[j][0], list[j][1]]

def setup_database(data_file_path):
    data_file = open(data_file_path).read()
    return json.loads(data_file)

# q(s,h)
def probability_speed_and_heading(i):
    position_2 = get_second_operand(i, position)

    heading = calculate_heading(position[i], position_2)
    distance = calculate_speed(position[i], position_2)

# s(t)
def suspiciousness(t):
    x, y = t[0], t[1]
    return k1 / (k1 + probability_in_region(x, y) * probability_speed_and_heading(t))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Requires path to data file'
        sys.exit()

    # Only process regions in this list. Leave empty to process all regions.
    restrict_to_regions = [38]

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
                                                 regions[region_num][0],
                                                 regions[region_num][1])
    else:
        for i, region in enumerate(regions):
            print 'Region', str(i),
            print noticeability.do_noticeability(database, region[0],
                                                 region[1])