from collections import defaultdict
from hashlib import md5


mem_cache = defaultdict(list)


def find_valid_hashes(base):
    n = 0

    # Check out local store of hash for this base first
    for digest, n in mem_cache[base]:
        yield digest

    while True:
        digest = md5('%s%s' % (base, n)).hexdigest()
        if digest[:5] == '00000':
            mem_cache[base].append((digest, n))
            yield digest
        n += 1


def test_part_1():
    assert part_1('abc') == '18f47a30'


def part_1(door_id):
    res = ''
    for digest in find_valid_hashes(door_id):
        res += digest[5]
        if len(res) == 8:
            break
    return res


def test_part_2():
    assert part_2('abc') == '05ace8e3'


def part_2(door_id):
    res = ['_', ] * 8
    for digest in find_valid_hashes(door_id):
        if '_' not in res:
            break
        try:
            index = int(digest[5])
        except ValueError:
            continue
        else:
            if index > 7 or res[index] != '_':
                continue
            res[index] = digest[6]
    return ''.join(res)


if __name__ == '__main__':
    test_part_1()
    answer = part_1('wtnhxymk')
    print 'The password is %s.' % answer

    test_part_2()
    answer = part_2('wtnhxymk')
    print 'The second password is %s.' % answer
