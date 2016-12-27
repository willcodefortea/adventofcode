from interpreter import Interpreter2


def test():
    instructions = [
        'cpy 2 a',
        'tgl a',
        'tgl a',
        'tgl a',
        'cpy 1 a',
        'dec a',
        'dec a',
    ]

    interpreter = Interpreter2(instructions)
    interpreter.execute()
    assert interpreter.registry['a'] == 3


def main():
    with open('23.txt') as fin:
        instructions = fin.read().split('\n')

    interpreter = Interpreter2(instructions[:])
    interpreter.registry['a'] = 7
    interpreter.execute()
    print 'The value to send is %s.' % interpreter.registry['a']

    interpreter = Interpreter2(instructions[:])
    interpreter.registry['a'] = 12
    interpreter.execute()
    print 'The value to send is %s.' % interpreter.registry['a']


if __name__ == '__main__':
    main()
