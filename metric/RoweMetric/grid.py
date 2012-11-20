# UNC Greensboro, CSC 593, Fall 2012
#
# By Andrei Nicholson
# Mentored by Dr. Shan Suthaharan

# Make all divisions result in a float.
from __future__ import division

from RoweMetric import point

class Grid:
    """Class to manage the bounding box grid over all agent positions.
    """

    # TODO: Calculating this number is another project in itself. Should be
    # another class within this submodule.
    num_divisions = 7

    def __init__(self, database):
        self._find_bounding_box(database)
        self._find_division_points()

    def _find_bounding_box(self, database):
        all_x = [position.x for agent in database['agents'] for position in agent['positions']]
        all_y = [position.y for agent in database['agents'] for position in agent['positions']]
        top_left = point.Point(min(all_x), max(all_y))
        bottom_right = point.Point(max(all_x), min(all_y))
        self.bounding_box = [top_left, bottom_right]

    def _find_division_points(self):
        self.divide = point.Point(abs(self.bounding_box[1].x - self.bounding_box[0].x) / self.num_divisions,
                                  abs(self.bounding_box[1].y - self.bounding_box[0].y) / self.num_divisions)

    def calculate_regions(self, database):
        """Calculate top-left and bottom-right coordinates for each region.

        Start at top-left-most region and work down rows, start at the top for
        each new column.
        """
        regions = []
        for x in range(0, self.num_divisions):
            for y in range(0, self.num_divisions):
                top_left = point.Point(self.bounding_box[0].x + (x * self.divide.x),
                                       self.bounding_box[0].y - (y * self.divide.y))
                bottom_right = point.Point(self.bounding_box[0].x + ((x + 1) * self.divide.x),
                                           self.bounding_box[0].y - ((y + 1) * self.divide.y))
                regions.append([top_left, bottom_right])
        return regions

    def area_of_region(self):
        """Calculate the area of a region.
        """
        length = abs(self.bounding_box[0].x + self.divide.x - self.bounding_box[0].x)
        return length * length
