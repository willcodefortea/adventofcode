from collections import deque


def white_elephant(n):
    """Solution to part 1."""
    res = 1
    for i in xrange(2, n + 1):
        nxt = (res + 2)
        if nxt != i:
            nxt = nxt % i
        res = nxt
    return res


def white_elephant_2(n):
    """Solution to part 2.

    Each elf selects another elf half way away from their current
    location, flooring the index when it's even.

    Rather than popping from the middle of a list, keep track of two
    lists, the left and the right, and efficiently pop and rotate from
    either end.
    """
    # Sorted first half of elements
    left = deque(i for i in xrange(1, (n / 2) + 1))
    # Second half of elements
    right = deque(i for i in xrange((n / 2) + 1, n + 1))

    while left and right:
        if len(left) > len(right):
            # Uneven remaining elves, take one from the left of the
            # center
            left.pop()
        else:
            right.popleft()

        # Now move the elves around.
        # Wrap around by pushing the lowest value onto the right
        right.append(left.popleft())
        # Center shifts to the left
        left.append(right.popleft())
    return left[0]


def test():
    assert white_elephant(5) == 3
    assert white_elephant_2(5) == 2
    assert white_elephant_2(5) == 2


def main():
    test()

    print 'The %s elf gets all the presents.' % white_elephant(3004953)
    print 'The %s elf gets all the presents.' % white_elephant_2(3004953)

if __name__ == '__main__':
    main()

