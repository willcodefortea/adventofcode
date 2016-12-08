class Screen(object):
    """A simple object to keep track of a screen's state."""

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

        # Create our screen, being careful to ensure we instantiate new
        # lists, otherwise we'll end up mutating various rows
        # simultaneously.
        self.screen = [
            [0, ] * cols
            for _ in xrange(rows)
        ]

    def __str__(self):
        """Transform our array into a friendly output."""
        return '\n'.join(
            ''.join(['#' if value else '.' for value in row])
            for row in self.screen
        )

    def perform_instruction(self, instruction):
        """Inspect an instruction and pass to the appropriate handler."""
        if instruction.startswith('rect'):
            self.rect(instruction)
        elif instruction.startswith('rotate row'):
            self.rotate_row(instruction)
        elif instruction.startswith('rotate column'):
            self.rotate_column(instruction)
        else:
            raise Exception(u'Unknown instruction %s' % instruction)

    def rect(self, instruction):
        """Turn ON all pixels in a rectangle at the topleft of the screen.

        Instruction is of the form: rect AxB
        """
        _, grid = instruction.split(' ')
        x, y = [int(s) for s in grid.split('x')]

        for row in xrange(y):
            for col in xrange(x):
                self.screen[row][col] = 1

    def rotate_column(self, instruction):
        """Rotate a column's values down by B pixels.

        Instruction is of the form: rotate column x=A by B
        """
        chunks = instruction.split(' ')
        col = int(chunks[2].split('=')[1])
        amount = int(chunks[4])

        new_cols = []

        for index, row in enumerate(self.screen):
            new_value = self.screen[(index - amount) % self.rows][col]
            new_cols.append(new_value)

        for index, row in enumerate(self.screen):
            row[col] = new_cols[index]

    def rotate_row(self, instruction):
        """Rotate a row's values right by B pixels.

        Instruction is of the form: rotate row y=A by B
        """
        chunks = instruction.split(' ')
        row = int(chunks[2].split('=')[1])
        amount = int(chunks[4])

        new_row = []

        for index, col in enumerate(self.screen[row]):
            new_value = self.screen[row][index - amount % self.cols]
            new_row.append(new_value)
        self.screen[row] = new_row

    @property
    def lit_pixels(self):
        """Return the number of currently lit pixels."""
        return sum(
            sum(row) for row in self.screen
        )


def test_part_1():
    s = Screen(3, 7)
    s.perform_instruction('rect 3x2')
    assert str(s) == '\n'.join((
        "###....",
        "###....",
        ".......",
    ))

    s.perform_instruction('rotate column x=1 by 1')
    assert str(s) == '\n'.join((
        "#.#....",
        "###....",
        ".#.....",
    ))

    s.perform_instruction('rotate row y=0 by 4')
    assert str(s) == '\n'.join((
        "....#.#",
        "###....",
        ".#.....",
    ))

    s.perform_instruction('rotate column x=1 by 1')
    assert str(s) == '\n'.join((
        ".#..#.#",
        "#.#....",
        ".#.....",

    ))


def part_1(instructions):
    screen = Screen(6, 50)
    for instruction in instructions:
        screen.perform_instruction(instruction)
    return screen.lit_pixels


def part_2(instructions):
    screen = Screen(6, 50)
    for instruction in instructions:
        screen.perform_instruction(instruction)
    return str(screen)


def main():
    with open('08.txt') as fin:
        data = fin.read().split('\n')

    test_part_1()
    answer = part_1(data)
    print 'The number of lit pixels is %s.' % answer

    answer = part_2(data)
    print 'The screen is displaying:\n%s' % answer

if __name__ == '__main__':
    main()
