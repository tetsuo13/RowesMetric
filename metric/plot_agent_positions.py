# UNC Greensboro, CSC 593, Fall 2012
#
# By Andrei Nicholson
# Mentored by Dr. Shan Suthaharan

"""
Notes:

http://matplotlib.org/users/pyplot_tutorial.html
http://matplotlib.org/examples/pylab_examples/hexbin_demo.html
"""

import matplotlib.cm as cm
import matplotlib.pyplot as pyplot
import sys

from RoweMetric.database import setup_database
from RoweMetric import globals
from RoweMetric import grid
from RoweMetric import noticeability

class OutputType:
    AGENT_POSITIONS = 1
    GRID_OVERLAY = 2
    GRID_WITH_RESULTS = 3
    HEATMAP = 4

def draw_grid_overlay(grid, show_noticeability):
    grid_alpha = 0.5

    left_most = grid.bounding_box[0][0]
    right_most = grid.bounding_box[0][0] + (grid.num_divisions * grid.divide[0])
    top_most = grid.bounding_box[0][1]
    bottom_most = grid.bounding_box[0][1] - (grid.num_divisions * grid.divide[1])

    for i in range(0, grid.num_divisions + 1):
        pyplot.plot([left_most, right_most],
                    [grid.bounding_box[0][1] - (i * grid.divide[1]),
                     grid.bounding_box[0][1] - (i * grid.divide[1])],
                    'r--', alpha=grid_alpha)
        pyplot.plot([grid.bounding_box[0][0] + (i * grid.divide[0]),
                     grid.bounding_box[0][0] + (i * grid.divide[0])],
                    [top_most, bottom_most],
                    'r--', alpha=grid_alpha)

    if show_noticeability:
        draw_noticeability_in_grid(database, grid)

def noticeability_for_regions(grid, database):
    area_of_region = grid.area_of_region()
    regions = grid.calculate_regions(database)
    n = []
    for region in regions:
        n.append(noticeability.do_noticeability(database, area_of_region,
                                                region[0], region[1]))
    return n

def draw_noticeability_in_grid(database, grid):
    n = noticeability_for_regions(grid, database)
    n_i = 0

    for x in range(0, grid.num_divisions):
        for y in range(0, grid.num_divisions):
            if (n[i][0] == globals.NOT_APPLICABLE and
                n[i][1] == globals.NOT_APPLICABLE):
                n_i += 1
                continue

            pyplot.text(grid.bounding_box[0][0] + (x * grid.divide[0]) + 0.025,
                        grid.bounding_box[0][1] - (y * grid.divide[1]) - 0.35,
                        str(n[i][0]) + '\n' + str(n[i][1]))
            n_i += 1

def plot_agent_positions(database, restrict_to_agents, output_type):
    if output_type == OutputType.GRID_OVERLAY:
        agent_alpha = 0.3
    else:
        agent_alpha = 1.0

    for agent in database['agents']:
        if (len(restrict_to_agents) > 0 and
            not agent['agentid'] in restrict_to_agents):
            continue
        pyplot.plot([position[0] for position in agent['positions']],
                    [position[1] for position in agent['positions']],
                    label=str(agent['agentid']),
                    alpha=agent_alpha)

def draw_plot(database, grid):
    # Agent IDs to plot. Left blank all agents will be plotted.
    restrict_to_agents = []

    if (output_type == OutputType.AGENT_POSITIONS or
        output_type == OutputType.GRID_OVERLAY):
        plot_agent_positions(database, restrict_to_agents, output_type)

    if output_type != OutputType.AGENT_POSITIONS:
        draw_grid_overlay(grid, (output_type == OutputType.GRID_WITH_RESULTS))
    else:
        pyplot.legend()

    pyplot.ylabel('y')
    pyplot.xlabel('x')
    pyplot.title('Agent positions')
    pyplot.show()

def draw_heatmap(database, grid):
    n = noticeability_for_regions(grid, database)

    # Replace all NOT_APPLICABLE with zero.
    # TODO: There's GOT to be a cleaner way!
    for i,x in enumerate(n):
        if n[i][0] == globals.NOT_APPLICABLE:
            n[i][0] = 0
        if n[i][1] == globals.NOT_APPLICABLE:
            n[i][1] = 0

    # Create a two-dimensional array to hold values for non-deceptive agent's
    # noticeability. Rearrange for a {(0,0),(0,1),(0,2)...} layout instead of
    # the region (top-to-bottom, left-to-right).
    #
    # TODO: This is upside down.
    data = []
    area_of_region = grid.area_of_region()

    for y in range(0, grid.num_divisions):
        row = []
        for x in range(0, grid.num_divisions):
            top_left = [grid.bounding_box[0][0] + (x * grid.divide[0]),
                        grid.bounding_box[0][1] - (y * grid.divide[1])]
            bottom_right = [grid.bounding_box[0][0] + ((x + 1) * grid.divide[0]),
                            grid.bounding_box[0][1] - ((y + 1) * grid.divide[1])]
            n = noticeability.do_noticeability(database, area_of_region,
                                               top_left, bottom_right)
            if n[0] == globals.NOT_APPLICABLE:
                n[0] = 0
            if n[1] == globals.NOT_APPLICABLE:
                n[1] = 0

            row.append(n[1])
        data.append(row)

    # BuGn, OrRd
    fig = pyplot.figure()
    ax1 = fig.add_subplot(111)
    cmap = cm.get_cmap('OrRd', 10)
    ax1.imshow(data, interpolation='nearest', cmap=cmap)
    pyplot.show()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Requires path to data file'
        sys.exit()

    output_type = OutputType.GRID_OVERLAY

    database = setup_database(sys.argv[1])
    grid = grid.Grid(database)

    if output_type == OutputType.HEATMAP:
        draw_heatmap(database, grid)
    else:
        draw_plot(database, grid)