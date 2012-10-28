# UNC Greensboro, CSC 593, Fall 2012
#
# By Andrei Nicholson
# Mentored by Dr. Shan Suthaharan

class Grid:
    """Class to manage the bounding box grid over all agent positions
    """

    # TODO: Calculating this number is another project in itself. Should be
    # another class within this submodule.
    num_divisions = 7

    def __init__(self, database):
        self._find_bounding_box(database)
        self._find_division_points()

    def _find_bounding_box(self, database):
        top_left = [min([position[0] for agent in database['agents'] for position in agent['positions']]),
                    max([position[1] for agent in database['agents'] for position in agent['positions']])]
        bottom_right = [max([position[0] for agent in database['agents'] for position in agent['positions']]),
                        min([position[1] for agent in database['agents'] for position in agent['positions']])]
        self.bounding_box = [top_left, bottom_right]

    def _find_division_points(self):
        self.divide = [abs(self.bounding_box[1][0] - self.bounding_box[0][0]) / self.num_divisions,
                       abs(self.bounding_box[1][1] - self.bounding_box[0][1]) / self.num_divisions]

    def calculate_regions(self, database):
        """Calculate top-left and bottom-right coordinates for each region.

        Start at top-left-most region and work down rows, start at the top for
        each new column.

        """
        regions = []
        for x in range(0, self.num_divisions):
            for y in range(0, self.num_divisions):
                top_left = [self.bounding_box[0][0] + (x * self.divide[0]),
                            self.bounding_box[0][1] - (y * self.divide[1])]
                bottom_right = [self.bounding_box[0][0] + ((x + 1) * self.divide[0]),
                                self.bounding_box[0][1] - ((y + 1) * self.divide[1])]
                regions.append([top_left, bottom_right])
        return regions