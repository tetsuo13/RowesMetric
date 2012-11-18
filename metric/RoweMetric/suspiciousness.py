# UNC Greensboro, CSC 593, Fall 2012
#
# By Andrei Nicholson
# Mentored by Dr. Shan Suthaharan
#
# For a given region for all agents in region:
#
#   1. Find distance between min and max points in region.
#   2. Use distance to compute speed. If Kinect records one point per second,
#      speed is distance / num_seconds.
#   3. Take slope of min and max points. This is the heading.
#
# For all regions, after they've been calculated:
#
#   1. Set up x number of bins. 
#   2. Create array with speed to heading slots.
#   3. Record how many agents fit into each slot. How many were traveling at
#      speed x and heading y.
#   4. The q value is for a given region is  number of agents in slot over
#      slot1 + slot2 + ... + slotn
#
# Three different types of scenarios that can occur in a region for time t:
#
#   1. Only one point in the region.
#   2. No points in the region.
#   3. Two points but their slope not representative of that region.
#
# Kinect records at 30 fps. Take entire position list and divide by 30 to find
# out how many seconds were recorded.
#

# Make all divisions result in a float.
from __future__ import division

import math

from RoweMetric import exposure
from RoweMetric import globals
from RoweMetric import noticeability

class Suspiciousness():
    def __init__(self, database, regions):
        # Dictionary to hold speed to heading values. Each element index
        # corresponds to the region number.
        self.speed_and_heading = {}
        self._process_regions(database, regions)

    def _process_regions(self, database, regions):
        import sys
        for region_id, region in enumerate(regions):
            agents = self._find_all_points_in_region(database['agents'],
                                                     region)

            if len(agents) == 0:
                continue

            for agent_id, points_in_region in agents.iteritems():
                print points_in_region
                print self._sort_points(points_in_region)
                sys.exit()

            if region_id == 3:
                sys.exit()

    def _find_all_points_in_region(self, agents, region):
        agents_in_region = {}

        for agent in agents:
            points_in_region = []

            for position in agent['positions']:
                if (position[0] >= region[0][0] and
                    position[0] <= region[1][0] and
                    position[1] <= region[0][1] and
                    position[1] >= region[1][1]):
                    points_in_region.append(position)

            if len(points_in_region) > 0:
                agents_in_region[agent['agentid']] = points_in_region

        return agents_in_region

    def _sort_points(self, points):
        """Sort a list of 2D points from smallest to largest.

        Represent points in polar coordinates with respect to the center point
        and use the angle as the sorting key.
        """
        x, y = zip(*((p[0], p[1]) for p in points))
        avg_x = sum(x) / len(x)
        avg_y = sum(y) / len(y)
        return sorted(points,
                      key=lambda p: math.atan2(p[0] - avg_x, p[1] - avg_y))

def probability_speed_and_heading(database, top_left, bottom_left):
    position_2 = get_second_operand(i, position)

    heading = average_heading(position[i], position_2)
    distance = calculate_speed(position[i], position_2)

def do_suspiciousness(database, top_left, bottom_right):
    p_nondeceptive, p_deceptive = exposure.probability_in_region(database,
                                                                 top_left,
                                                                 bottom_right)
    s_nondeceptive, s_deceptive = probability_speed_and_heading(database,
                                                                top_left,
                                                                bottom_right)

    x, y = t[0], t[1]
    return k1 / (k1 + probability_in_region(x, y) * probability_speed_and_heading(t))

def calculate_speed(position_1, position_2):
    """Distance in meters per second.

    TODO: Distance will need to be measured in whatever Kinect uses.

    """
    x1, y1 = position_1[0], position_1[1]
    x2, y2 = position_2[0], position_2[1]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def average_heading(position_1, position_2):
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