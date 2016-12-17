from collections import namedtuple
from hashlib import md5
import operator


Location = namedtuple('Location', 'up,down,left,right')

UP = 'U'
DOWN = 'D'
LEFT = 'L'
RIGHT = 'R'

MAP = (UP, DOWN, LEFT, RIGHT)


def abs_x_y(path):
    x, y = 0, 0
    for char in path:
        if char in (UP, DOWN):
            x += 1 if char == DOWN else -1
        else:
            y += 1 if char == RIGHT else -1
    return x, y


def is_within_bounds(path):
    x, y = abs_x_y(path)
    return x >= 0 and y >= 0 and x < 4 and y < 4


def valid_movements(seed, path):
    hash = md5('%s%s' % (seed, path)).hexdigest()
    open_chars = 'bcdef'

    for index, char in enumerate(hash[:4]):
        if char in open_chars:
            new_path = path + MAP[index]
            if is_within_bounds(new_path):
                yield new_path


def cost(path):
    """How far from the end location are we?"""
    x, y = abs_x_y(path)
    dest = (3, 3)
    return abs(dest[0] - x) + abs(dest[0] - y)


def find_path(seed, shortest=True):
    """Find a valid path from the top-left to bottom-right of a 4x4 grid."""
    paths = [
        '',  # We start having not moved anywhere.
    ]
    winning_path = None

    op = operator.lt if shortest else operator.gt

    while True:
        new_paths = []
        for path in paths:
            for new_path in valid_movements(seed, path):
                valid_winner = winning_path is not None
                winning_test = valid_winner and op(len(new_path), len(winning_path))
                if cost(new_path) == 0:
                    # We've arrived.
                    if winning_path is None or winning_test:
                        winning_path = new_path
                        continue
                    else:
                        # We failed our check, and cannot continue on
                        # this path
                        continue

                if valid_winner and shortest and not winning_test:
                    # We can short-circuit as we don't have a winner.
                    # For longest path we need to keep searching.
                    continue

                new_paths.append(new_path)
        paths = new_paths

        if len(paths) == 0:
            break
    return winning_path


def test():
    assert list(valid_movements('hijkl', '')) == ['D', ]
    assert find_path('ihgpwlah') == 'DDRRRD'
    assert find_path('kglvqrro') == 'DDUDRLRRUDRD'
    assert find_path('ulqzkmiv') == 'DRURDRUDDLLDLUURRDULRLDUUDDDRR'

    assert len(find_path('ihgpwlah', False)) == 370
    assert len(find_path('kglvqrro', False)) == 492
    assert len(find_path('ulqzkmiv', False)) == 830


def main():
    test()

    print 'The shortest path is %s.' % find_path('pxxbnzuo')
    print 'The longest path length is %s.' % len(find_path('pxxbnzuo', False))

if __name__ == '__main__':
    main()
