def is_nice_string(string):
    bad_strings = [
        'ab', 'cd', 'pq', 'xy',
    ]
    vowels = 'aeiou'
    vowel_count = 0
    has_pair = False

    for index, char in enumerate(string):
        if char in vowels:
            vowel_count += 1

        pair = string[index: index+2]
        if not has_pair and len(pair) == 2 and pair[0] == pair[1]:
            has_pair = True

        if pair in bad_strings:
            # No need to continue
            return False

    return vowel_count >= 3 and has_pair


def is_nice_string_v2(string):
    pairs = []
    has_duplicate_pair = False


def test():
    assert is_nice_string('ugknbfddgicrmopn')
    assert is_nice_string('aaa')
    assert not is_nice_string('jchzalrnumimnmhp')
    assert not is_nice_string('haegwjzuvuyypxyu')
    assert not is_nice_string('dvszwmarrgswjxmb')


def main():
    with open('05.txt') as fin:
        data = fin.read().split()

    test()
    nice_strings_count = sum(is_nice_string(string) for string in data)
    print 'The number of nice strings is %s.' % nice_strings_count

if __name__ == '__main__':
    main()
