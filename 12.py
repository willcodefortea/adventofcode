from interpreter import Interpreter


def test_part_1():
    instructions = [
        'cpy 41 a',
        'inc a',
        'inc a',
        'dec a',
        'jnz a 2',
        'dec a',
    ]
    interpreter = Interpreter(instructions)
    interpreter.execute()
    assert interpreter.registry['a'] == 42


def main():
    with open('12.txt') as fin:
        instructions = fin.read().split('\n')
    test_part_1()

    interpreter = Interpreter(instructions)
    interpreter.execute()
    answer = interpreter.registry['a']
    print 'The value in register a is %s.' % answer

    interpreter = Interpreter(instructions)
    interpreter.registry['c'] = 1
    interpreter.execute()
    answer = interpreter.registry['a']
    print 'The value in register a is %s.' % answer


if __name__ == '__main__':
    main()
