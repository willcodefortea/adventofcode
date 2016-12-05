from tools import grouper


def is_valid_triangle(x, y, z):
    """Two sides must always add up to more the than third."""
    return x + y > z and x + z > y and y + z > x


def test_part_1():
    assert part_1(((5, 10, 25,), )) == 0


def part_1(data):
    """Count the number of valid triangles in data."""
    valid = 0

    for tri in data:
        if is_valid_triangle(*tri):
            valid += 1
    return valid


def test_part_2():
    data = [
        [101, 301, 501, ],
        [102, 302, 502, ],
        [103, 303, 503, ],
        [201, 401, 601, ],
        [202, 402, 602, ],
        [203, 403, 603, ],
    ]
    assert part_2(data) == 6


def part_2(data):
    """Look at the colums, not the rows for triangles."""
    valid = 0
    cols = zip(*data)
    for col in cols:
        # Group the col into iterables of 3
        for tri in grouper(col, 3):
            if is_valid_triangle(*tri):
                valid += 1
    return valid


if __name__ == '__main__':
    data = []
    with open('03.txt') as fin:
        for line in fin.readlines():
            if not line:
                break
            data.append([int(x) for x in line.split()])

    test_part_1()
    answer = part_1(data)
    print 'There are %s valid triangles.' % answer

    test_part_2()
    answer = part_2(data)
    print 'There are %s vertical triangles.' % answer
