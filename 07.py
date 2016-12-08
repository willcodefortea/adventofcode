import re


def supports_tls(ip):
    has_abba = False
    standard, hypernet = parse_ip(ip)

    def test_abba(chunk):
        for i in xrange(len(chunk) - 3):
            diffreent_chars = chunk[i] != chunk[i+1]
            mirrored = chunk[i:i+2] == chunk[i+3:i+1:-1]
            if diffreent_chars and mirrored:
                return True
        return False

    within_hyernet = sum(test_abba(chunk) for chunk in hypernet) > 0
    if within_hyernet:
        return False

    has_abba = sum(test_abba(chunk) for chunk in standard) > 0
    return has_abba


def supports_ssl(ip):
    expected_bab_codes = []
    standard, hypernet = parse_ip(ip)

    for chunk in standard:
        for i in xrange(len(chunk) - 2):
            if chunk[i] != chunk[i + 1] and chunk[i] == chunk[i + 2]:
                expected_bab_code = '{0}{1}{0}'.format(chunk[i + 1], chunk[i])
                expected_bab_codes.append(expected_bab_code)

    for bab in expected_bab_codes:
        for chunk in hypernet:
            if bab in chunk:
                return True
    return False


hypernet_re = re.compile(r'\[([a-zA-Z]+)\]')
standard_re = re.compile(r'(?:^|\])([a-zA-Z]+)(?:$|\[)')


def parse_ip(ip):
    """Split an IP into hypernet sequences."""
    return standard_re.findall(ip), hypernet_re.findall(ip)


def test_part_1():
    assert parse_ip('abba[mnop]qrst') == (['abba', 'qrst'], ['mnop', ], )
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
