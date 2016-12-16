from collections import namedtuple


Disc = namedtuple('Disc', 'count,start')


def can_fall_through(time, discs):
    """Can a ball through through the maze at this time."""
    for index, disc in enumerate(discs, 1):
        position_at_time = (disc.start + index + time) % disc.count
        if position_at_time != 0:
            return False
    return True


def parse_input(lines):
    """Translate input into a friendly Disc tuple.

    Input is of the form:

        Disc #1 has 17 positions; at time=0, it is at position 15.

    """
    discs = []
    for line in lines:
        chunks = line.split()
        count = int(chunks[3])
        starting_position = int(chunks[-1].rstrip('.'))
        discs.append(
            Disc(count, starting_position)
        )
    return discs


def test_part_1():
    assert not can_fall_through(0, [Disc(5, 4), Disc(2, 1), ])
    assert can_fall_through(5, [Disc(5, 4), Disc(2, 1), ])


def part_1(discs):
    """Deterimine the lowest time at which we can fall through.

    This is super naive and just tests all available times.
    """
    time = 0
    while True:
        if can_fall_through(time, discs):
            return time
        time += 1


def main():
    with open('15.txt') as fin:
        data = fin.read().split('\n')
    discs = parse_input(data)
    test_part_1()

    print 'The first time a ball can fall through is at %s.' % part_1(discs)

    discs.append(Disc(11, 0))
    print 'The first time a ball can fall through is at %s.' % part_1(discs)


if __name__ == '__main__':
    main()
