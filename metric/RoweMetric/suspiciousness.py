# UNC Greensboro, CSC 593, Fall 2012
#
# By Andrei Nicholson
# Mentored by Dr. Shan Suthaharan

# Make all divisions result in a float.
from __future__ import division

NOT_APPLICABLE = '--'

# q(s,h)
def probability_speed_and_heading(i):
    position_2 = get_second_operand(i, position)

    heading = calculate_heading(position[i], position_2)
    distance = calculate_speed(position[i], position_2)

# s(t)
def suspiciousness(t):
    x, y = t[0], t[1]
    return k1 / (k1 + probability_in_region(x, y) * probability_speed_and_heading(t))

def calculate_speed(position_1, position_2):
    """Distance in meters per second.

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