def test_part_1():
    assert part_1(['ULL', 'RRDDD', 'LURDL', 'UUUUD', ]) == '1985'
    # Check we can reach the corners / bounding is OK
    assert part_1(
        ['LLLLLL', 'UUUUU', 'RRRRRR', 'DDDDD', 'LLLLL']
    ) == '41397'


def part_1(data):
    """Follow instructions to calculate the bathroom key code."""
    keypad = (
        ('1', '2', '3', ),
        ('4', '5', '6', ),
        ('7', '8', '9', ),
    )
    return build_code(data, keypad, [1, 1])


def test_part_2():
    assert part_2(['ULL', 'RRDDD', 'LURDL', 'UUUUD', ]) == '5DB3'


def part_2(data):
    """Follow instructions, just on a differently shaped keypad."""
    keypad = (
        (None, None, '1', None, None, ),
        (None, '2', '3', '4', None, ),
        ('5', '6', '7', '8', '9', ),
        (None, 'A', 'B', 'C', None, ),
        (None, None, 'D', None, None, ),
    )
    starting_index = [2, 0]
    return build_code(data, keypad, starting_index)


def build_code(data, keypad, starting_index):
    current_index = starting_index
    code = ''
    for chunk in data:
        for movement in chunk:
            effect = -1 if movement in ('U', 'L', ) else 1
            new_location = current_index[:]
            if movement in ('U', 'D', ):
                new_location[0] += effect
            else:
                new_location[1] += effect

            if new_location[0] < 0 or new_location[1] < 0:
                continue

            try:
                res = keypad[new_location[0]][new_location[1]]
            except IndexError:
                # Not a valid location on the keypad
                continue
            else:
                if res is not None:
                    current_index = new_location

        code += keypad[current_index[0]][current_index[1]]

    return code


if __name__ == '__main__':
    with open('02.txt') as fin:
        data = fin.read()
    chunks = data.split()

    test_part_1()
    answer = part_1(chunks)
    print 'The bathroom code is %s.' % answer

    test_part_2()
    answer = part_2(chunks)
    print 'The second bathroom code is %s.' % answer
