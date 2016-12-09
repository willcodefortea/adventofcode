from cStringIO import StringIO


def extract_marker(stream):
    marker_char = stream.read(1)
    marker = ''
    while marker_char != ')':
        marker += marker_char
        marker_char = stream.read(1)
    return map(int, marker.split('x'))


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
            length, multiple = extract_marker(compressed)
            clear = compressed.read(length)
            # Expand any child compression if there is any
            if '(' in clear and use_sub_markers:
                clear = decompress(clear, use_sub_markers)
            clear = clear * multiple
        decompressed += clear
    return decompressed


def decompressed_length(compressed, use_sub_markers=False):
    """Don't bother keeping track of the decompression, just the resulting size.

    This takes execution time of part2 from ~40s to ~0.01s.
    """
    size = 0
    compressed = StringIO(compressed)

    while True:
        char = compressed.read(1)
        if not char:
            break
        length = 1

        if char == '(':
            chunk_length, multiple = extract_marker(compressed)
            chunk = compressed.read(chunk_length)
            # Expand any child compression if there is any
            if '(' in chunk and use_sub_markers:
                chunk_length = decompressed_length(chunk, use_sub_markers)
            length = chunk_length * multiple
        size += length
    return size


def test_part_1():
    assert decompress('ADVENT') == 'ADVENT'
    assert decompress('A(1x5)BC') == 'ABBBBBC'
    assert decompress('(3x3)XYZ') == 'XYZXYZXYZ'
    assert decompress('A(2x2)BCD(2x2)EFG') == 'ABCBCDEFEFG'
    assert decompress('(6x1)(1x3)A') == '(1x3)A'
    assert decompress('X(8x2)(3x3)ABCY') == 'X(3x3)ABC(3x3)ABCY'


def part_1(compressed):
    return decompressed_length(compressed)


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
    return decompressed_length(compressed, True)


def main():
    with open('09.txt') as fin:
        data = fin.read().strip()

    test_part_1()
    answer = part_1(data)
    print 'Decompressed length of the file is %s.' % answer

    test_part_2()
    answer = part_2(data)
    print 'Decompressed length of the file (improved format) is %s.' % answer

if __name__ == '__main__':
    main()
