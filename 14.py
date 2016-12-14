from collections import defaultdict, namedtuple
from hashlib import md5


Item = namedtuple('Item', 'hash,index')


def simple_hash(base, index):
    """MD5 a base and the current index."""
    return md5('%s%d' % (base, index)).hexdigest()


def stretched_hash(salt, index):
    """Perform the same hash 2016 + 1 times."""
    hash = simple_hash(salt, index)
    for _ in xrange(2016):
        hash = simple_hash(hash, index)
    return hash


def generate_keys(salt, hasher=simple_hash):
    """Search for valid keys, infinitely yeilding them as we go."""
    index = 0
    potentials = defaultdict(list)

    while True:
        hash = hasher(salt, index)
        for char_index, char in enumerate(hash):
            if char * 3 == hash[char_index:char_index + 3]:
                # We have a triple
                if char * 5 == hash[char_index:char_index + 5]:
                    # We have a quint! Now yield any valid matches that
                    # are within range.
                    matches = [
                        item for item in potentials[char]
                        if (item.index + 1000) > index
                    ]
                    # We have at least one valid
                    for match in matches:
                        yield match
                    # We have either used *all* the matches, or anything
                    # remaining is invalid. Either way, reset the list.
                    potentials[char] = []
                # Store hash for later (a quint is a valid start for the
                # next key).
                potentials[char].append(Item(hash, index))

                # Only consider the first triplet in a hash, move to the
                # next index
                break
        index += 1


def build_keys(salt, hasher=simple_hash):
    """Continually build keys until we reach our required number."""
    keys = []
    for key in generate_keys(salt, hasher):
        keys.append(key)
        if len(keys) == 64:
            break
    return keys


def test_part_1():
    assert part_1('abc') == 22728


def test_part_2():
    assert part_2('abc') == 22551


def part_1(salt):
    keys = build_keys(salt)
    return max(k[1] for k in keys)


def part_2(salt):
    keys = build_keys(salt, hasher=stretched_hash)
    return max(k[1] for k in keys)


def main():
    salt = 'ngcjuoqr'

    test_part_1()
    print 'The index that produces the 64th key is %s.' % part_1(salt)

    test_part_2()
    print 'The index that produces the 64th key is %s.' % part_2(salt)


if __name__ == '__main__':
    main()
