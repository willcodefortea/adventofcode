class Interpreter(object):
    def __init__(self, instructions):
        self.instructions = instructions
        self.index = 0
        self.registry = {
            'a': 0,
            'b': 0,
            'c': 0,
            'd': 0,
        }

    def execute(self):
        """Perform all instructions."""
        while True:
            try:
                instruction = self.instructions[self.index]
            except IndexError:
                break
            self.execute_instruction(instruction)

    def _int_or_registry_value(self, key):
        """Check if the key is an integer or a registry value."""
        try:
            value = int(key)
        except ValueError:
            value = self.registry[key]
        return value

    def copy(self, source, destintion):
        """Copy either a value or a registry value to another registry."""
        value = self._int_or_registry_value(source)
        self.registry[destintion] = value

    def increase(self, destintion):
        """Increase a registry value."""
        self.registry[destintion] += 1

    def decrease(self, destintion):
        """Decrease a registry value."""
        self.registry[destintion] -= 1

    def jump(self, key, amount):
        """Jump to a previous instruction if the flag is set."""
        value = self._int_or_registry_value(key)
        amount = int(amount)
        if value != 0:
            self.index += amount

    @property
    def operations_map(self):
        """Dumb instruction key to method mapping."""
        return {
            'cpy': self.copy,
            'inc': self.increase,
            'dec': self.decrease,
            'jnz': self.jump,
        }

    def execute_instruction(self, instruction):
        """Parse the instruction and perform the required operation."""
        chunks = instruction.split(' ')
        name = chunks[0]
        arguments = chunks[1:]

        try:
            operation = self.operations_map[name]
        except KeyError:
            raise Exception('Unknown instruction "%s".' % name)

        # Keep track of the previous instruction index in case the operation
        # changes it.
        prev_instruction_index = self.index

        # Perform the operation with any remaining arguments from the
        # instruction
        operation(*arguments)

        if prev_instruction_index == self.index:
            # The instruction did NOT jump to a different location, advance it
            # ourselves
            self.index += 1


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
