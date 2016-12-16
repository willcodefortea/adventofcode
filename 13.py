from collections import defaultdict
from functools import partial


def cost(position, destination):
    """Cost function of our current position vs the destination.

    Use the Manhatten distance to determin our cost, we're using a
    square grid and can't move diagonally, so this seems appropriate.
    """
    delta_x = position[0] - destination[0]
    delta_y = position[1] - destination[1]

    return abs(delta_x) + abs(delta_y)


def is_wall(magic_number, x, y):
    """Determine if a location is a wall using the provided equation."""
    res = (x * x + 3 * x + 2 * x * y + y + y * y) + magic_number
    as_binary = '{0:b}'.format(res)
    ones_only = [i for i in as_binary if i == '1']
    return len(ones_only) % 2 == 1


def available_locations(magic_number, position):
    """Yield all possible movements from this position."""
    deltas = (
        (-1, 0),
        (0, -1),
        (1, 0),
        (0, 1),
    )
    for delta in deltas:
        new_x = position[0] + delta[0]
        new_y = position[1] + delta[1]
        if new_x >= 0 and new_y >= 0:
            if not is_wall(magic_number, new_x, new_y):
                yield (new_x, new_y)


def find_shortest_path(magic_number, destination):
    """Determine the shortest path to the destination."""
    paths = [
        [(1, 1), ],  # We have a single path, starting at (1, 1)
    ]
    shortest_path = None

    while True:
        path = paths.pop(0)  # Take the lowest cost path to explore first
        for next_location in available_locations(magic_number, path[-1]):
            if next_location in path:
                # Already visited on this path, ignore it.
                continue
            new_path = path[:]
            if cost(next_location, destination) == 0:
                # We've arrived at the end
                if shortest_path is None or len(new_path) < shortest_path:
                    shortest_path = len(new_path)
                else:
                    # No need to continue exploring
                    continue
            new_path.append(next_location)

            if shortest_path and len(new_path) > shortest_path:
                # We've used too many steps, ignore
                continue

            # Add this path onto the set to be explored next time
            paths.append(new_path)
        paths = sorted(
            paths,
            key=lambda path: cost(path[-1], destination)
        )

        if not paths:
            break

    return shortest_path


def distinct_locations(magic_number, steps):
    """How many distinct locations can we reach in n steps."""
    positions = set((1, 1))  # Include the starting locatio
    paths = [
        [(1, 1), ]
    ]
    while True:
        path = paths.pop(0)
        for next_location in available_locations(magic_number, path[-1]):
            if next_location in path:
                # We're revisting a location on the same path, no need
                # to continue exlporing it
                continue
            if next_location in positions:
                # We've been here before, meaning we've explored all
                # points from here too, so we can ignore it
                continue
            positions.add(next_location)
            new_path = path[:]
            new_path.append(next_location)
            if len(new_path) <= steps:
                paths.append(new_path)

        if not paths:
            break

    return len(positions)


def test_part_1():
    for point in ((0, 0), (0, 1), (1, 1), (1, 2)):
        assert not is_wall(10, *point)
    for point in ((1, 0), (2, 1), (3, 0), (0, 2)):
        assert is_wall(10, *point)

    assert list(available_locations(10, (1, 1))) == [(0, 1), (1, 2)]
    assert part_1(magic_number=10, destination=(7, 4)) == 11


def part_1(magic_number, destination):
    return find_shortest_path(magic_number, destination)


def part_2(magic_number):
    return distinct_locations(magic_number, 50)


def main():
    test_part_1()
    print 'Minimum number of steps is %s.' % part_1(1352, (31, 39))
    print 'Total number of positions is %s.' % part_2(1352)


if __name__ == '__main__':
    main()
