from collections import namedtuple
from copy import deepcopy
from hashlib import md5


class Node(object):
    def __init__(self, pos, size, used, source=False):
        self.pos = pos
        self.size = size
        self.used = used
        self.source = source

    def __repr__(self):
        contains_data = 'X' if self.source else '0'
        return '<(%s,%s) %2sT %2sT %s>' % (
            self.pos[0], self.pos[1], self.used, self.size, contains_data
        )

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
    """Find all the available moves on the data set.

    Any viable data swaps that can be performed between two neighbours
    is a valid move.
    """
    neighbours = ((1, 0), (0, 1), (-1, 0), (0, -1), )
    for x in range(size[0] + 1):
        for y in range(size[1] + 1):
            node = get_node(data, x, y, size[0])

            if node.used == 0:
                # No data to move, skip it.
                continue

            for deltas in neighbours:
                new_x, new_y = x + deltas[0], y + deltas[1]

                if new_x < 0 or new_x > size[0] or new_y < 0 or new_y > size[1]:
                    # We're out of bounds, skip it.
                    continue
                dest = get_node(data, new_x, new_y, size[0])

                if dest.avail >= node.used:
                    yield (x, y), (new_x, new_y)


def cost(data, grid_width):
    for index, node in enumerate(data):
        if node.source:
            break
    x, y = index % (grid_width + 1), index // (grid_width + 1)
    # print x, y, index, grid_width, x + y
    return x + y


def build_key(data):
    """Build a unique key for a state."""
    hasher = md5()
    for node in data:
        hasher.update(str(node))
    return hasher.hexdigest()


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
        [data, 0, cost(data, grid_x)],
    ]
    shortest_path_length = None

    seen = set()

    while True:
        new_paths = []
        lowest_cost = paths[0][-1]
        print '###', len(paths), lowest_cost
        for path in paths:
            data, steps, data_cost = path
            if data_cost > lowest_cost:
                # Don't follow just yet. Explore lowest cost items
                # first
                new_paths.append(path)
                continue

            for move in available_moves(data, size):
                new_data = [deepcopy(n) for n in data]

                origin_node = get_node(new_data, move[0][0], move[0][1], grid_x)
                dest_node = get_node(new_data, move[1][0], move[1][1], grid_x)

                dest_node.used += origin_node.used
                origin_node.used = 0

                key = build_key(new_data)
                if key in seen:
                    continue
                seen.add(key)

                if origin_node.source:
                    dest_node.source = True
                    origin_node.source = False

                if cost(new_data, grid_x) == 0:
                    print 'FOUND THE SHORTEST PATH', steps
                    if not shortest_path_length or shortest_path_length > steps:
                        shortest_path_length = steps
                    continue

                if shortest_path_length and steps >= shortest_path_length:
                    continue

                new_paths.append((new_data, steps + 1, cost(new_data, grid_x)))

        paths = new_paths
        sorted(paths, key=lambda path: path[-1])

        if not paths:
            # We've extinguished all possible viable paths, we're done!
            break

    return shortest_path_length + 1


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
    print 'The shortest path is %s.' % shortest_path(data)

if __name__ == '__main__':
    main()
