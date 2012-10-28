#http://matplotlib.org/users/pyplot_tutorial.html

import json
import matplotlib.pyplot as pyplot
import sys

class Grid:
    num_divisions = 7

    def __init__(self, database):
        self.find_bounding_box(database)
        self.find_division_points()

    def find_bounding_box(self, database):
        top_left = [min([position[0] for agent in database['agents'] for position in agent['positions']]),
                    max([position[1] for agent in database['agents'] for position in agent['positions']])]
        bottom_right = [max([position[0] for agent in database['agents'] for position in agent['positions']]),
                        min([position[1] for agent in database['agents'] for position in agent['positions']])]
        self.bounding_box = [top_left, bottom_right]

    def find_division_points(self):
        self.divide = [abs(self.bounding_box[1][0] - self.bounding_box[0][0]) / self.num_divisions,
                       abs(self.bounding_box[1][1] - self.bounding_box[0][1]) / self.num_divisions]

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Requires path to data file'
        sys.exit()

    # Agent IDs to plot. Left blank all agents will be plotted.
    restrict_to_agents = []

    data_file = open(sys.argv[1]).read()
    database = json.loads(data_file)

    grid = Grid(database)

    for agent in database['agents']:
        if len(restrict_to_agents) > 0 and not agent['agentid'] in restrict_to_agents:
            continue
        pyplot.plot([position[0] for position in agent['positions']],
                    [position[1] for position in agent['positions']], label=str(agent['agentid']))

    left_most = grid.bounding_box[0][0]
    right_most = grid.bounding_box[0][0] + (grid.num_divisions * grid.divide[0])
    top_most = grid.bounding_box[0][1]
    bottom_most = grid.bounding_box[0][1] - (grid.num_divisions * grid.divide[1])

    # Draw grid overlay.
    for i in range(0, grid.num_divisions + 1):
        pyplot.plot([left_most, right_most],
                    [grid.bounding_box[0][1] - (i * grid.divide[1]), grid.bounding_box[0][1] - (i * grid.divide[1])],
                    'r--', alpha=0.3)
        pyplot.plot([grid.bounding_box[0][0] + (i * grid.divide[0]), grid.bounding_box[0][0] + (i * grid.divide[0])],
                    [top_most, bottom_most],
                    'r--', alpha=0.3)

    # Label the regions.
    region = 0
    for x in range(0, grid.num_divisions):
        for y in range(0, grid.num_divisions):
            pyplot.text(grid.bounding_box[0][0] + (x * grid.divide[0]) + 0.065,
                        grid.bounding_box[0][1] - (y * grid.divide[1]) - 0.3,
                        str(region))
            region += 1

    pyplot.ylabel('y')
    pyplot.xlabel('x')
    pyplot.title('Agent positions')
    pyplot.legend()
    pyplot.show()