def parse_input(data):
    return [
        char == '^' for char in data
    ]


def to_str(rows):
    res = []
    for row in rows:
        res.append(''.join([
            '^' if tile else '.'
            for tile in row
        ]))
    return '\n'.join(res)


def is_trap(index, prev_row):
    """Check if the tile at this index is a trap."""
    start = index - 1 if index > 0 else 0
    end = index + 2
    tiles = prev_row[start:end]
    if index == 0:
        # insert a safe tile
        tiles.insert(0, False)
    elif index == len(prev_row) - 1:
        # Insert a safe to tile to the right
        tiles.append(False)

    rules = [
        tiles[0] and tiles[1],  # rule 1
        tiles[1] and tiles[2],  # rule 2
        tiles[0] and not (tiles[1] or tiles[2]),  # rule 3
        tiles[2] and not (tiles[0 or tiles[1]]),  # rule 4
    ]

    # Abuse the fact that Truth == 1 and False == 0
    return sum(rules) == 1

    return (
        (tiles[1] and (tiles[0] or tiles[1])) or  # rules 1 and 2
        tiles[0] or  # rule 3
        tiles[1]  # rule 4
    )


def build_rows(start, num_rows):
    rows = [
        start
    ]
    while len(rows) < num_rows:
        prev_row = rows[-1]
        new_row = []
        for i in xrange(len(start)):
            new_row.append(
                is_trap(i, prev_row)
            )
        rows.append(new_row)

    return rows


def count_safe_tiles(rows):
    total = 0
    for row in rows:
        total += len(row) - sum(row)
    return total


def test():
    data = parse_input('..^^.')
    rows = build_rows(data, 3)
    assert to_str(rows) == """..^^.
.^^^^
^^..^"""

    data = parse_input('.^^.^.^^^^')
    rows = build_rows(data, 10)
    assert to_str(rows) == """.^^.^.^^^^
^^^...^..^
^.^^.^.^^.
..^^...^^^
.^^^^.^^.^
^^..^.^^..
^^^^..^^^.
^..^^^^.^^
.^^^..^.^^
^^.^^^..^^"""


def main():
    test()

    with open('18.txt') as fin:
        data = parse_input(fin.read())
    rows = build_rows(data, 40)
    print 'The number of safe tiles is %s.' % count_safe_tiles(rows)

    rows = build_rows(data, 400000)
    print 'The number of safe tiles is %s.' % count_safe_tiles(rows)


if __name__ == '__main__':
    main()
