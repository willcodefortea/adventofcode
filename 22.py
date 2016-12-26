from collections import namedtuple
from copy import deepcopy


class Node(object):
    def __init__(self, pos, size, used, source=False):
        self.pos = pos
        self.size = size
        self.used = used
        self.source = source

    def __repr__(self):
        return 'Node<(%s,%s) %sT %sT>' % (self.pos[0], self.pos[1], self.size, self.used)

    @property
    def avail(self):
        return self.size - self.used


def parse_filesize(size):
    return int(size[:-1])


def parse_position(filename):
    name = filename.split('/')[-1]
    x, y = (int(part[1:]) for part in name.split('-')[1:])
    return x, y


def get_grid_size(nodes):
    max_x, max_y = 0, 0
    for node in nodes:
        if node.pos[0] > max_x:
            max_x = node.pos[0]
        elif node.pos[1] > max_y:
            max_y = node.pos[1]
    return max_x, max_y


def parse_input(data):
    lines = data.split('\n')
    nodes = []
    for line in lines[2:]:  # First two line can be ignored
        chunks = line.split()
        pos = parse_position(chunks[0])
        size, used = (
            parse_filesize(chunk) for chunk in chunks[1:3]
        )
        nodes.append(Node(pos, size, used))

    size = get_grid_size(nodes)
    nodes = sorted(nodes, key=lambda node: (node.pos[1], node.pos[0] + size[1] * node.pos[1]))

    return nodes


def viable_pairs(nodes):
    for node_a in nodes:
        for node_b in nodes:
            if node_a.used > 0 and node_a.used <= node_b.avail:
                yield node_a, node_b


def get_node(data, x, y, grid_width):
    return data[x + (grid_width + 1) * y]


def available_moves(data, size):
    """Find all the available moves on the data set."""
    neighbours = ((1, 0), (0, 1), (-1, 0), (0, -1), )
    for x in range(size[0]):
        for y in range(size[1]):
            node = get_node(data, x, y, size[0])

            for deltas in neighbours:
                new_x, new_y = x + deltas[0], y + deltas[1]

                if new_x < 0 or new_x > size[0] or new_y < 0 or new_y > size[1]:
                    continue
                dest = get_node(data, new_x, new_y, size[0])

                if dest.avail >= node.used:
                    print x,y,new_x,new_y
                    yield (x, y), (new_x, new_y)


def cost(data, grid_width):
    for index, node in enumerate(data):
        if node.source:
            break
    x, y = index % grid_width, index // grid_width
    print 'cost %s, %s' % (x, y)
    return x + y


def shortest_path(data):
    """Find the shortest path for moving data from (X, 0) to (0, 0).

    This isn't as simple as it appears as we may have to perform other
    moves in order to clear the path for us to move into. Thus we
    perform a breadth first search minimising our cost (distance from
    target) and then optimize based on that.
    """
    size = get_grid_size(data)
    grid_x = size[0]

    # Mark our destination node so we can follow it around.
    data[grid_x].source = True
    paths = [
        [data, 0, ],
    ]
    shortest_path_length = None

    print paths[0][0]

    while True:
        new_paths = []
        for path in paths:
            data, steps = path

            for move in available_moves(data, size):
                new_data = deepcopy(data)
                steps += 1

                origin_node = get_node(new_data, move[0][0], move[0][1], grid_x)
                dest_node = get_node(new_data, move[1][0], move[1][1], grid_x)

                print move, origin_node, dest_node, grid_x

                dest_node.used += origin_node.used
                origin_node.used = 0

                if cost(new_data, grid_x) == 0:
                    if not shortest_path_length or shortest_path_length > steps:
                        shortest_path_length = steps
                    continue

                if shortest_path_length and steps > shortest_path_length:
                    continue

                new_paths.append((new_data, steps))
            break

        paths = new_paths
        # sorted(paths, key=lambda path: cost(path[0], grid_x))

        for path in paths:
            print path[0]

        if paths[0][1] > 10:
            raise Exception('failed to solve.')
        if not paths:
            break

    return shortest_path_length




    return shortest_path_length


def test():
    test_input = """
    Filesystem            Size  Used  Avail  Use%
/dev/grid/node-x0-y0   10T    8T     2T   80%
/dev/grid/node-x0-y1   11T    6T     5T   54%
/dev/grid/node-x0-y2   32T   28T     4T   87%
/dev/grid/node-x1-y0    9T    7T     2T   77%
/dev/grid/node-x1-y1    8T    0T     8T    0%
/dev/grid/node-x1-y2   11T    7T     4T   63%
/dev/grid/node-x2-y0   10T    6T     4T   60%
/dev/grid/node-x2-y1    9T    8T     1T   88%
/dev/grid/node-x2-y2    9T    6T     3T   66%"""
    data = parse_input(test_input)
    assert get_grid_size(data) == (2, 2)
    assert shortest_path(data) == 7


def main():
    test()

    with open('22.txt') as fin:
        data = parse_input(fin.read())

    print 'The number of viable pairs is %s.' % len(list(viable_pairs(data)))
    # 958 is incorrect, too high
    # 815 is incorrect, too low

if __name__ == '__main__':
    main()
