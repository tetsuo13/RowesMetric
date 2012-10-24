#http://matplotlib.org/users/pyplot_tutorial.html

import json
import matplotlib.pyplot as pyplot
import sys

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Requires path to data file'
        sys.exit()

    data_file = open(sys.argv[1]).read()
    database = json.loads(data_file)

    for agent in database['agents']:
        pyplot.plot([position[0] for position in agent['positions']],
                    [position[1] for position in agent['positions']])

    pyplot.ylabel('y')
    pyplot.xlabel('x')
    pyplot.title('Agent positions')
    pyplot.show()