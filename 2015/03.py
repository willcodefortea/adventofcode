def count_visted_locations(instructions, num_paths=1):
    paths = [
        [(0, 0), ] for _ in xrange(num_paths)
    ]

    mapping = {
        '>': (1, 0),
        '<': (-1, 0),
        '^': (0, 1),
        'v': (0, -1),
    }

    locations = set([(0, 0)])

    for index, char in enumerate(instructions):
        path = paths[index % num_paths]
        delta = mapping[char]
        last_location = path[-1][:]
        new_location = (
            last_location[0] + delta[0], last_location[1] + delta[1]
        )
        path.append(new_location)
        locations.add(new_location)
    return len(locations)


def test():
    assert count_visted_locations('>') == 2
    assert count_visted_locations('^>v<') == 4
    assert count_visted_locations('v^v^v^v^v') == 2

    assert count_visted_locations('v^', 2) == 3
    assert count_visted_locations('^>v<', 2) == 3
    assert count_visted_locations('^v^v^v^v^v', 2) == 11


def main():
    with open('03.txt') as fin:
        data = fin.read()
    test()
    print 'Number of houses visited is %s.' % count_visted_locations(data)
    print 'Number of houses visited with 2 santas is %s.' % count_visted_locations(data, 2)


if __name__ == '__main__':
    main()
