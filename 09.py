from cStringIO import StringIO


def decompress(compressed, use_sub_markers=False):
    # Convert the string to a file like object
    compressed = StringIO(compressed)
    decompressed = ''

    while True:
        char = compressed.read(1)
        if not char:
            break

        clear = char

        if char == '(':
            # Extract the marker
            marker_char = compressed.read(1)
            marker = ''
            while marker_char != ')':
                marker += marker_char
                marker_char = compressed.read(1)
            length, multiple = map(int, marker.split('x'))

            clear = compressed.read(length)
            # Expand any child compression if there is any
            if '(' in clear and use_sub_markers:
                clear = decompress(clear, use_sub_markers)
            clear = clear * multiple
        decompressed += clear
    return decompressed


def test_part_1():
    assert decompress('ADVENT') == 'ADVENT'
    assert decompress('A(1x5)BC') == 'ABBBBBC'
    assert decompress('(3x3)XYZ') == 'XYZXYZXYZ'
    assert decompress('A(2x2)BCD(2x2)EFG') == 'ABCBCDEFEFG'
    assert decompress('(6x1)(1x3)A') == '(1x3)A'
    assert decompress('X(8x2)(3x3)ABCY') == 'X(3x3)ABC(3x3)ABCY'


def part_1(compressed):
    return len(decompress(compressed))


def test_part_2():
    assert decompress('(3x3)XYZ', True) == 'XYZXYZXYZ'
    assert decompress('X(8x2)(3x3)ABCY', True) == 'XABCABCABCABCABCABCY'
    assert decompress(
        '(27x12)(20x12)(13x14)(7x10)(1x12)A', True
    ) == 'A' * 241920
    assert len(decompress(
        '(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN', True
    )) == 445


def part_2(compressed):
    return len(decompress(compressed, True))


def main():
    with open('09.txt') as fin:
        data = fin.read().strip()

    test_part_1()
    answer = part_1(data)
    print 'The decompressed length of the file is %s.' % answer

    test_part_2()
    answer = part_2(data)
    print 'The decompressed length of the file using the improved format is:\n%s' % answer

if __name__ == '__main__':
    main()
