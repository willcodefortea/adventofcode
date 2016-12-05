NORTH, EAST, SOUTH, WEST = range(4)


def rotation(facing, direction):
    """Change our rotation.

    Args:
        facing int The direction 0,1,2,3 that we're currently facing.
        direction str The direction of rotation.
    """
    rotation = 1 if direction == 'R' else -1
    new_facing = facing + rotation

    # Clip our direction be a valid index
    new_facing %= 4
    if new_facing < 0:
        new_facing = WEST

    return new_facing


def test_part_1():
    assert part_1(['R2', 'L3']) == 5
    assert part_1(['R2', 'R2', 'R2']) == 2
    assert part_1(['R5', 'L5', 'R5', 'R3']) == 12


def part_1(data):
    """Follow instructions and see how many blocks away we are."""
    steps = [0, 0, 0, 0, ]  # North, East, South, West
    facing = 0  # Start facing north

    for step in data:
        facing = rotation(facing, step[0])
        num_steps = int(step[1:])
        steps[facing] += num_steps

    total_north = steps[0] - steps[2]
    total_east = steps[1] - steps[3]
    return abs(total_north) + abs(total_east)


def test_part_2():
    assert part_2(['R8', 'R4', 'R4', 'R8', ]) == 4


def part_2(data):
    """Search for the first location visited twice."""
    visited = [[0, 0], ]  # Start at the center
    facing = 0  # Start facing north

    for step in data:
        facing = rotation(facing, step[0])

        # Change y if moving N, S, else x
        changing_index = 1 if facing in (NORTH, SOUTH) else 0

        effect = 1 if facing in (NORTH, EAST) else -1
        num_steps = int(step[1:])

        for n in xrange(num_steps):
            next_location = visited[-1][:]
            next_location[changing_index] += effect

            if next_location in visited:
                return abs(next_location[0]) + abs(next_location[1])

            visited.append(next_location)
    raise Exception("No positions revisted.")

if __name__ == '__main__':
    with open('01.txt') as fin:
        data = fin.read()
    chunks = data.split(', ')

    test_part_1()
    answer = part_1(chunks)
    print 'Easter Bunny HQ is %s blocks away.' % answer

    test_part_2()
    answer = part_2(chunks)
    print 'The first location visited twich is %s blocks away.' % answer
