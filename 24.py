from collections import defaultdict, deque

WALL = '#'
EMPTY = '.'


def build_graph(maze):
    """Convert string maze to an adjacency list.

    The list takes the form of

        {
            node: [node1, node2, ...]
            ...
        }

    Where each node is of the form ((x, y), value)
    """
    deltas = [
        (0, 1), (0, -1), (1, 0), (-1, 0)
    ]
    rows = maze.split('\n')
    width = len(rows[0])
    height = len(rows)
    graph = defaultdict(set)
    for y, row in enumerate(rows):
        for x, cell in enumerate(row):
            # Check viable neighbours
            node = ((x, y), rows[y][x])
            for delta in deltas:
                new_x, new_y = x + delta[0], y + delta[1]
                if new_x < 0 or new_x >= width or new_y < 0 or new_y >= height:
                    continue
                new_cell = rows[new_y][new_x]
                if new_cell != WALL:
                    # We don't have a wall. Valid movement.
                    new_node = ((new_x, new_y), new_cell)
                    graph[node].add(new_node)
    return graph


def find_interesting_locations(maze):
    """Extract any location that isn't a wall or empty."""
    locations = []
    rows = maze.split('\n')
    for y, row in enumerate(rows):
        for x, cell in enumerate(row):
            if cell not in (WALL, EMPTY, ):
                locations.append(
                    ((x, y), cell)
                )
    return locations


def all_paths(graph, start, goal):
    """Find all paths from our start node to the goal.

    If we meet a non empty node as we attempt to reach our destination
    skip this path.
    """
    queue = deque([(start, [start]), ])
    visited = set()
    while queue:
        vertex, path = queue.popleft()
        for next in graph[vertex] - set(path):
            if next in visited:
                # We've been here before, so by definition we were here
                # on a shorter path.
                continue
            visited.add(next)
            if next == goal:
                yield path + [next, ]
            if next[1] != EMPTY:
                continue
            else:
                queue.append((next, path + [next, ]))


def shortest_path(graph, start, goal):
    """Find the shortest path between two nodes.

    As all paths is a BFS of our graph, the first result is (by
    definition) ths shortest path. If no valid paths exist then the
    generate will throw an exception.
    """
    try:
        return next(all_paths(graph, start, goal))
    except StopIteration:
        return None


def find_minimum_distances(maze, graph, locations):
    """Find the shortest distance between every interesting lcoation.

    This is essentially a sub graph of the interesting nodes. Here the
    nodes take the form

        {
            value: [(value, distance), ...],
            ...
        }

    """
    results = defaultdict(set)
    for start in locations:
        for goal in locations:
            if start == goal:
                continue
            path = shortest_path(graph, start, goal)
            if path:
                results[start[1]].add((goal[1], len(path) - 1))
    return results


def shortest_path_all_locations(maze, return_to_0=False):
    """Find the shortest path that visits all the intesting locations."""
    graph = build_graph(maze)
    locations = find_interesting_locations(maze)
    min_distances = find_minimum_distances(maze, graph, locations)

    all_locations = set(min_distances.keys())
    start = '0'
    queue = deque([(start, [(start, 0), ])])

    shortest_distance = None

    while queue:
        vertex, path = queue.popleft()
        for node in min_distances[vertex]:
            # Check for completion
            new_path = path + [node, ]
            visited_locations = set([n[0] for n in new_path])
            distance = reduce(lambda accum, n: accum + n[1], new_path, 0)
            winning = len(all_locations - visited_locations) == 0
            if winning and return_to_0:
                winning = new_path[-1] == '0'
            if winning:
                # We've met everything record the distance.
                if shortest_distance is None or distance < shortest_distance:
                    shortest_distance = distance
                continue

            if shortest_distance is not None and distance > shortest_distance:
                continue
            queue.append(
                (node[0], new_path)
            )
    return shortest_distance


def test():
    maze = """###########
#0.1.....2#
#.#######.#
#4.......3#
###########"""

    assert shortest_path_all_locations(maze) == 14


def main():
    test()

    with open('24.txt') as fin:
        maze = fin.read()
    print 'Shortest path is %s.' % shortest_path_all_locations(maze)
    print 'Shortest path that returns to 0 is %s.' % shortest_path_all_locations(maze, True)


if __name__ == '__main__':
    main()
