from collections import defaultdict


TEST_DATA = [
    'eedadn',
    'drvtee',
    'eandsr',
    'raavrd',
    'atevrs',
    'tsrnev',
    'sdttsa',
    'rasrtv',
    'nssdts',
    'ntnada',
    'svetve',
    'tesnvt',
    'vntsnd',
    'vrdear',
    'dvrsen',
    'enarar',
]


def error_correct_message(data, reverse=True):
    positions = defaultdict(lambda: defaultdict(int))

    for line in data:
        for index, char in enumerate(line):
            positions[index][char] += 1

    extracted = [
        sorted(item.iteritems(), key=lambda x: x[1], reverse=reverse)[0]
        for item in positions.values()
    ]

    return ''.join(val[0] for val in extracted)


def test_part_1():
    assert part_1(TEST_DATA) == 'easter'


def part_1(data):
    return error_correct_message(data, reverse=True)


def test_part_2():
    assert part_2(TEST_DATA) == 'advent'


def part_2(data):
    return error_correct_message(data, reverse=False)


if __name__ == '__main__':
    with open('06.txt') as fin:
        data = fin.read().split()

    test_part_1()
    answer = part_1(data)
    print 'The error corrected message is %s.' % answer

    test_part_2()
    answer = part_2(data)
    print 'The second error corrected password is %s.' % answer
