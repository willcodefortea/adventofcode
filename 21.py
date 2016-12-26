

def swap_position(chars, x, y):
    chars[x], chars[y] = chars[y], chars[x]


def swap_letters(chars, a, b):
    for index, char in enumerate(chars):
        if char == a:
            x = index
        elif char == b:
            y = index
    swap_position(chars, x, y)


def rotate(chars, direction, amount, reverse=False):
    if direction == 'left' and not reverse or direction == 'right' and reverse:
        for _ in range(amount):
            char = chars.pop(0)
            chars.append(char)

    else:
        for _ in range(amount):
            char = chars.pop()
            chars.insert(0, char)


def rotate_position(chars, a, reverse=False):
    for index, char in enumerate(chars):
        if char == a:
            break

    amount = 1 + index
    if index >= 4:
        amount += 1

    if reverse:
        # rotate and test.
        for amount in range(len(chars)):
            tmp = chars[:]
            rotate(tmp, 'left', amount)
            # Now that tmp has been rotated by N, attempt to rotate back
            # by position by the same character and test for a match.
            tmp1 = tmp[:]
            rotate_position(tmp, a)
            if tmp == chars:
                rotate(chars, 'left', amount)
                return
                final_amount = amount
                # we've found the correct rotation, apply it to our
                # original chars set and quit.
                # rotate(chars, 'left', amount)
                # return


    rotate(chars, 'right', amount)


def reverse(chars, x, y):
    replace = chars[x:y+1][::-1]
    for index, char in enumerate(replace):
        chars[x + index] = char


def move(chars, x, y):
    char = chars.pop(x)
    chars.insert(y, char)


def test():
    # chars = list('abc')
    # swap_position(chars, 0, 2)
    # assert ''.join(chars) == 'cba'

    # chars = list('abc')
    # swap_letters(chars, 'a', 'b')
    # assert ''.join(chars) == 'bac'

    # chars = list('abc')
    # rotate(chars, 'left', 1)
    # assert ''.join(chars) == 'bca'

    # chars = list('abc')
    # rotate(chars, 'left', 1)
    # assert ''.join(chars) == 'bca'

    # chars = list('abcd')
    # rotate_position(chars, 'b')
    # assert ''.join(chars) == 'cdab'

    # chars = list('abcd')
    # reverse(chars, 1, 3)
    # assert ''.join(chars) == 'adcb'

    # chars = list('abcd')
    # move(chars, 1, 3)
    # assert ''.join(chars) == 'acdb'

    # chars = list('abcd')
    # move(chars, 0, 1)
    # assert ''.join(chars) == 'bacd'

    # chars = list('abcde')
    # reverse(chars, 0, 4)
    # assert ''.join(chars) == 'edcba'

    # Test various states of rotation
    chars = 'abcdef'
    for char in chars:
        tmp = list(chars)
        instruction = 'rotate based on position of letter %s' % char
        follow_instructions(tmp, [instruction, ])
        # Now rotate back
        follow_instructions(tmp, [instruction, ], True)
        print instruction, chars, ''.join(tmp), ''.join(chars)
        # We should be back where we started
        assert ''.join(tmp) == ''.join(chars)

    chars = list('decab')
    follow_instructions(chars, ['rotate based on position of letter d'], True)
    assert ''.join(chars) == 'ecabd'

    chars = list('ecabd')
    follow_instructions(chars, ['rotate based on position of letter b'], True)
    assert ''.join(chars) == 'abdec'

    chars = list('bcdea')
    follow_instructions(chars, ['rotate left 1 step'], True)
    assert ''.join(chars) == 'abcde'

    chars = list('abdec')
    follow_instructions(chars, ['move position 3 to position 0'], True)
    assert ''.join(chars) == 'bdeac'


def follow_instructions(chars, instructions, reverse_method=False):
    step = -1 if reverse_method else 1
    for instruction in instructions[::step]:
        method, args = get_method(instruction, reverse_method)
        method(chars, *args)


def get_method(instruction, reverse_method):
    chunks = instruction.split()
    if instruction.startswith('swap position'):
        method = swap_position
        args = (int(chunks[2]), int(chunks[5]))
    elif instruction.startswith('swap letter'):
        method = swap_letters
        args = (chunks[2], chunks[5])
    elif instruction.startswith('move position'):
        method = move
        args = (int(chunks[2]), int(chunks[5]), )
        if reverse_method:
            args = args[::-1]
    elif instruction.startswith('rotate based on position of letter'):
        method = rotate_position
        args = (chunks[6], reverse_method, )
    elif instruction.startswith('reverse'):
        method = reverse
        args = (int(chunks[2]), int(chunks[4]))
    elif instruction.startswith('rotate'):
        method = rotate
        args = (chunks[1], int(chunks[2]), reverse_method)
    else:
        raise Exception('Unknown instruction %s' % instruction)

    return method, args


def main():
    # test()

    chars = list('abcde')
    follow_instructions(chars, [
        'swap position 4 with position 0',
        'swap letter d with letter b',
        'reverse positions 0 through 4',
        'rotate left 1 step',
        'move position 1 to position 4',
        'move position 3 to position 0',
        'rotate based on position of letter b',
        'rotate based on position of letter d',
    ])
    assert ''.join(chars) == 'decab'

    chars = list('decab')
    follow_instructions(chars, [
        'swap position 4 with position 0',
        'swap letter d with letter b',
        'reverse positions 0 through 4',
        'rotate left 1 step',
        'move position 1 to position 4',
        'move position 3 to position 0',
        'rotate based on position of letter b',
        'rotate based on position of letter d',
    ], reverse_method=True)
    assert ''.join(chars) == 'abcde'

    with open('21.txt') as fin:
        instructions = fin.read().split('\n')
    chars = list('abcdefgh')
    follow_instructions(chars, instructions)
    print 'The scrambled password is %s.' % ''.join(chars)

    chars = list('fbgdceah')
    # Follow the instructions in reverse order to unscramble
    follow_instructions(chars, instructions, reverse_method=True)
    res = ''.join(chars)
    incorrect = ['bafgdhec', 'dfhbecag', ]
    assert res not in incorrect
    print 'The unscrambled password is %s.' % ''.join(chars)
    # dfhbecag. is incorrect
    # bafgdhec is incorrect


if __name__ == '__main__':
    main()
