def required_paper(w, l, h):
    surface_area = 2 * (l * w + l * h + w * h)
    ordered = sorted([w, l, h])
    slack = ordered[0] * ordered[1]
    return surface_area + slack


def requried_ribbon(w, l, h):
    ordered = sorted([w, l, h])
    smallest_paramiter = 2 * (ordered[0] + ordered[1])
    bow = w * l * h
    return smallest_paramiter + bow


def test():
    assert required_paper(2, 3, 4) == 58
    assert required_paper(1, 1, 10) == 43

    assert requried_ribbon(2, 3, 4) == 34
    assert requried_ribbon(1, 1, 10) == 14


def main():
    with open('02.txt') as fin:
        data = [
            [int(n) for n in line.split('x')]
            for line in
            fin.read().split()
        ]
    test()
    total = sum(required_paper(*args) for args in data)
    print 'The total wrapping paper required is %s.' % total

    total_ribbon = sum(requried_ribbon(*args) for args in data)
    print 'The total ribbon required is %s.' % total_ribbon


if __name__ == '__main__':
    main()
