
def parse_input(str_data):
    """Read and sort the rules."""
    lines = str_data.split('\n')
    data = []
    for line in lines:
        chunk = line.split('-')
        data.append(
            (int(chunk[0]), int(chunk[1]))
        )
    data = sorted(data, key=lambda x: x[0])
    return data


def find_ips(rules):
    """Find all IPs that fall between the rules."""
    lower_bound = 0
    for rule in rules:
        for ip in xrange(lower_bound, rule[0]):
            yield ip
        # Move our lower bound if this rule is higher. If it isn't, then
        # this rule is a subset of the previous one.
        new_lower_bound = rule[1] + 1
        if new_lower_bound > lower_bound:
            lower_bound = new_lower_bound


def test():
    str_data = """5-8
0-2
4-7"""
    data = parse_input(str_data)
    assert find_ips(data).next() == 3


def main():
    test()

    with open('20.txt') as fin:
        str_data = fin.read()

    data = parse_input(str_data)
    ips = list(find_ips(data))

    print 'Lowest ip is %s' % ips[0]
    print 'Total number of ips is %s' % len(ips)


if __name__ == '__main__':
    main()
