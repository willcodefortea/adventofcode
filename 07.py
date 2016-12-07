
# This whole process could be sped up by parsing each IP into
# distinct blocks, this works but is inefficient.


def within_hyernet_sequence(ip, index):
    # First check left for [
    for i in xrange(index, 0, -1):
        if ip[i] == ']':
            return False
        if ip[i] == '[':
            break
    else:
        return False
    # Then check right for ]
    for i in xrange(index, len(ip)):
        if ip[i] == '[':
            return False
        if ip[i] == ']':
            break
    else:
        return False
    return True


def supports_tls(ip):
    has_abba = False

    for i in xrange(len(ip) - 3):
        diffreent_chars = ip[i] != ip[i+1]
        mirrored = ip[i:i+2] == ip[i+3:i+1:-1]
        if diffreent_chars and mirrored:
            if within_hyernet_sequence(ip, i):
                return False
            has_abba = True
    return has_abba


def supports_ssl(ip):
    bab_codes = []
    expected_bab_codes = []

    def is_aba(code):
        different_chars = code[0] == code[2] and code[0] != code[1]
        return different_chars and not within_hyernet_sequence(ip, i)

    def is_bab(code):
        different_chars = code[0] == code[2] and code[0] != code[1]
        return different_chars and within_hyernet_sequence(ip, i)

    for i in xrange(len(ip) - 2):
        code = ip[i:i+3]
        if is_aba(code):
            expected_bab_code = '{0}{1}{0}'.format(code[1], code[0])
            expected_bab_codes.append(expected_bab_code)
            continue
        if is_bab(code):
            bab_codes.append(code)
            continue

    return sum(expected in bab_codes for expected in expected_bab_codes) > 0


def test_part_1():
    assert supports_tls('abba[mnop]qrst')
    assert not supports_tls('abcd[bddb]xyyx')
    assert not supports_tls('aaaa[qwer]tyui')
    assert supports_tls('abba[mnop]qrst')


def part_1(codes):
    return sum(supports_tls(code) for code in codes)


def test_part_2():
    assert supports_ssl('aba[bab]xyz')
    assert not supports_ssl('xyx[xyx]xyx')
    assert supports_ssl('aaa[kek]eke')
    assert supports_ssl('zazbz[bzb]cdb')


def part_2(codes):
    return sum(supports_ssl(code) for code in codes)


if __name__ == '__main__':
    with open('07.txt') as fin:
        data = fin.read().split()

    test_part_1()
    answer = part_1(data)
    print 'The total number of IPs that support TLS is %s.' % answer

    test_part_2()
    answer = part_2(data)
    print 'The total number of IPs that support SSL is %s.' % answer
