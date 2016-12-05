from collections import defaultdict
from itertools import chain
import string


def split_code(code):
    checksum = code[-6: -1]
    name, sector = code[:-7].rsplit('-', 1)
    return name, int(sector), checksum


def is_real_room(name, checksum):
    letters = defaultdict(lambda: 0)

    for letter in chain(*name.split('-')):
        letters[letter] += 1

    top_5 = sorted(letters.items(), key=lambda x: (-1 * x[1], x[0]))[:5]
    generated_code = ''.join(x[0] for x in top_5)
    return generated_code == checksum


def decrypt(code, sector):
    alphabet = string.ascii_lowercase
    start = sector % len(alphabet)
    shift = string.maketrans(alphabet, alphabet[start:] + alphabet[:start])
    shifted = string.translate(code, shift)
    return shifted.replace('-', ' ')


def test_part_1():
    def split_and_check(code):
        name, _, checksum = split_code(code)
        return is_real_room(name, checksum)

    assert split_and_check('aaaaa-bbb-z-y-x-123[abxyz]')
    assert split_and_check('a-b-c-d-e-f-g-h-987[abcde]')
    assert split_and_check('not-a-real-room-404[oarel]')
    assert not split_and_check('totally-real-room-200[decoy]')


def part_1(data):
    res = 0
    for code in data:
        name, sector, checksum = split_code(code)
        if is_real_room(name, checksum):
            res += sector
    return res


def test_part_2():
    assert decrypt('qzmt-zixmtkozy-ivhz', 343) == 'very encrypted name'


def part_2(data):
    for code in data:
        name, sector, _ = split_code(code)
        decrypted = decrypt(name, sector)
        if 'north' in decrypted:
            return sector


if __name__ == '__main__':
    with open('04.txt') as fin:
        data = fin.read()
    codes = data.split()

    test_part_1()
    answer = part_1(codes)
    print 'The sum of real sector IDs is %s.' % answer

    test_part_2()
    answer = part_2(codes)
    print 'The room sector for "northpole object sotrage is" %s.' % answer
