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
import sys

from RoweMetric import exposure, globals, noticeability, point

class Suspiciousness():
    def __init__(self, database, regions):
        # Dictionary to hold speed to heading values. Each element index
        # corresponds to the region number.
        self.speed_and_heading = {}
        self._process_regions(database, regions)

    def _process_regions(self, database, regions):
        for region_id, region in enumerate(regions):
            #print region_id
            agents = self._find_all_points_in_region(database['agents'],
                                                     region)

            if len(agents) == 0:
                continue

            print 'There are', str(len(agents)), 'agents in region', str(region_id)
            for agent_id, points_in_region in agents.iteritems():
                speed, heading = self._find_velocity_vector(self._agent(database,
                                                                        agent_id),
                                                            region,
                                                            points_in_region)

                print agent_id, len(points_in_region)
                #print self._sort_points(points_in_region)
                print speed, heading
                #sys.exit()

            if region_id == 3:
                sys.exit()

    def _agent(self, database, agent_id):
        """Return agent object for a given agent ID.
        """
        for agent in database['agents']:
            if agent['agentid'] == agent_id:
                return agent

        # Should never get this far.
        raise Exception('Invalid agent ID needle, ' + str(agent_id))

    def _find_velocity_vector(self, agent, region, points):
        absolute_points = self._find_absolute_points_in_region(agent, region,
                                                               points)

        speed = None

        heading = (absolute_points[-1].y - absolute_points[0].y /
                   absolute_points[-1].x - absolute_points[0].x)

        return speed, heading

    def _find_absolute_points_in_region(self, agent, region, points):
        """Finds absolute min and max points in region.

        Since the set of points will most likely lie just inside the region
        boundary, we need to find the point that starts on the region boundary
        that is part of the total points segment. Return value is the points
        argument with two additional points, one each at the beginning and end
        which lies on the region boundary.
        """
        # Represents first and last points in region.
        first_point_in_region, last_point_in_region = points[0], points[-1]

        # One point before the first in the region; first point outside region
        # for the first point inside. Same thing for last point.
        point_before_first = self._get_adjacent_point(agent['positions'],
                                                      first_point_in_region,
                                                      True)
        point_after_last = self._get_adjacent_point(agent['positions'],
                                                    last_point_in_region,
                                                    False)

        # Find points which are on the region boundary.
        first_point = self._region_line_segment_intersect(region,
                                                          [first_point_in_region,
                                                           point_before_first])
        last_point = self._region_line_segment_intersect(region,
                                                         [last_point_in_region,
                                                          point_after_last])

        if first_point is not None:
            points = first_point + points
        if last_point is not None:
            points += last_point

        return points

    def _intersection(self, line_a, line_b):
        """Find point of intersection between two lines.

        Implementation of algorithm described by Paul Bourke, "Intersection
        point of two lines in 2 dimensions". See
        http://paulbourke.net/geometry/pointlineplane/
        """
        d = (line_b[1].y - line_b[0].y) * (line_a[1].x - line_a[0].x) - \
            (line_b[1].x - line_b[0].x) * (line_a[1].y - line_a[0].y)

        n_a = (line_b[1].x - line_b[0].x) * (line_a[0].y - line_b[0].y) - \
              (line_b[1].y - line_b[0].y) * (line_a[0].x - line_b[0].x)

        n_b = (line_a[1].x - line_a[0].x) * (line_a[0].y - line_b[0].y) - \
              (line_a[1].y - line_a[0].y) * (line_a[0].x - line_b[0].x)

        if d == 0:
            return None

        ua = n_a / d
        ub = n_b / d

        if ua >= 0.0 and ua <= 1.0 and ub >= 0.0 and ub <= 1.0:
            return point.Point(line_a[0].x + (ua * (line_a[1].x - line_a[0].x)),
                               line_a[0].y + (ua * (line_a[1].y - line_a[0].y)))
        return None

    def _region_line_segment_intersect(self, region, segment):
        """Point of intersection between line segment and region boundary.

        Given a line segment, find which of the four line segments that makes
        up a region it intersects with. Returns that intersection point.
        """
        # Line segments that comprise region bounary. Lines drawn from left to
        # right, top to bottom.
        boundary = [[point.Point(region[0].x, region[0].y),
                     point.Point(region[1].x, region[0].y)], # Top
                    [point.Point(region[0].x, region[1].y),
                     point.Point(region[1].x, region[1].y)], # Bottom
                    [point.Point(region[0].x, region[0].y),
                     point.Point(region[0].x, region[1].y)], # Left
                    [point.Point(region[1].x, region[0].y),
                     point.Point(region[1].x, region[1].y)]] # Right

        for piece in boundary:
            result = self._intersection(piece, segment)
            if result is not None:
                return result

        # Segment doesn't intersect region boundary.
        return None

    def _get_adjacent_point(self, points, needle, get_previous_point):
        """Retrieves the previous or next point from needle.
        """
        for i, point in enumerate(points):
            if point == needle:
                if get_previous_point:
                    if i == 0:
                        return point
                    return points[i + 1]
                else:
                    if i == len(points):
                        return point
                    return points[i - 1]

        # Should never get this far.
        raise Exception('Invalid needle requested')

    def _find_all_points_in_region(self, agents, region):
        agents_in_region = {}

        for agent in agents:
            #print 'Processing agent', str(agent['agentid'])
            points_in_region = []

            for position in agent['positions']:
                if (position.x >= region[0].x and position.x <= region[1].x and
                    position.y <= region[0].y and position.y >= region[1].y):
                    points_in_region.append(position)

            if len(points_in_region) > 0:
                #print '\t', str(len(points_in_region)), 'points'
                agents_in_region[agent['agentid']] = points_in_region

        #print str(len(agents_in_region)), 'agents were found'
        return agents_in_region

    def _sort_points(self, points):
        """Sort a list of 2D points from smallest to largest.

        Represent points in polar coordinates with respect to the center point
        and use the angle as the sorting key.
        """
        x, y = zip(*((p.x, p.y) for p in points))
        avg_x = sum(x) / len(x)
        avg_y = sum(y) / len(y)
        return sorted(points,
                      key=lambda p: math.atan2(p.x - avg_x, p.y - avg_y))

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