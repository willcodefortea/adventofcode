import string

from tools import grouper


def dragon(data):
    """Perform our modified dragon mutation to the data."""
    # First reverse
    next_section = data[::-1]
    # Now translate, 1 -> 0 and 0 -> 1
    shift = string.maketrans('01', '10')
    shifted = string.translate(next_section, shift)
    return '%s0%s' % (data, shifted)


def checksum(data):
    """Calculate the paired recursive checksum."""
    res = ''
    for pair in grouper(data, n=2):
        char = '1' if pair[0] == pair[1] else '0'
        res += char

    if len(res) % 2 == 0:
        # It's even, call again.
        return checksum(res)
    return res


def fill_disk(initial_state, length):
    """Create 'random' data to populate the disk."""
    state = initial_state
    while len(state) < length:
        state = dragon(state)
    return checksum(state[:length])


def test():
    assert dragon('1') == '100'
    assert dragon('0') == '001'
    assert dragon('11111') == '11111000000'
    assert dragon('111100001010') == '1111000010100101011110000'

    assert checksum('110010110100') == '100'

    assert fill_disk('10000', 20) == '01100'


def main():
    test()
    seed = '10001001100000001'
    print 'The correct checksum is %s.' % fill_disk(seed, 272)
    print 'The second disk checksum is %s.' % fill_disk(seed, 35651584)


if __name__ == '__main__':
    main()
