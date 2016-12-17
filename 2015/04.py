from hashlib import md5


def mine_adventcoins(seed, num_zeros=5):
    index = 0
    while True:
        hash = md5('%s%s' % (seed, index)).hexdigest()
        if hash[:num_zeros] == '0' * num_zeros:
            yield index
        index += 1


def test():
    assert mine_adventcoins('abcdef').next() == 609043
    assert mine_adventcoins('pqrstuv').next() == 1048970


def main():
    test()
    print 'First index to produce a coin is %s.' % mine_adventcoins('yzbqklnj').next()
    print 'First index to produce a coin with 6 zeros is %s.' % mine_adventcoins('yzbqklnj', 6).next()


if __name__ == '__main__':
    main()
