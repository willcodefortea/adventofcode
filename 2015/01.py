def calculate_floor(data, interesting_floor=None):
    floor = 0
    for position, char in enumerate(data, 1):
        floor += -1 if char == ')' else 1
        if interesting_floor is not None and floor == interesting_floor:
            return position
    return floor


def test():
    assert calculate_floor('(())') == 0
    assert calculate_floor('(((') == 3


def main():
    with open('01.txt') as fin:
        data = fin.read()
    test()
    print 'Santa ends up on floor %s.' % calculate_floor(data)
    print 'First position that takes Satan to -1 is %s.' % calculate_floor(data, -1)

if __name__ == '__main__':
    main()
