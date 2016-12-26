import inspect

from interpreter import Interpreter


class Interpreter2(Interpreter):

    def __init__(self, *args, **kwargs):
        super(Interpreter2, self).__init__(*args, **kwargs)
        self.optimize_instructions()

    def get_argument_count(self, method):
        argspec = inspect.getargspec(method)
        return len(argspec.args) - 1  # Ignore the self arg.

    @property
    def operations_map(self):
        op_map = super(Interpreter2, self).operations_map
        op_map['tgl'] = self.toggle
        op_map['nop'] = self.noop
        op_map['mul'] = self.multiply
        op_map['add'] = self.add
        return op_map

    def noop(self):
        """A null operation. Does nothing."""
        pass

    def add(self, a, b):
        """Add a to b and store in b."""
        amount_a = self._int_or_registry_value(a)
        amount_b = self._int_or_registry_value(b)
        self.registry[b] = amount_a + amount_b

    def multiply(self, a, b):
        """Multiply a by b and store in b."""
        amount_a = self._int_or_registry_value(a)
        amount_b = self._int_or_registry_value(b)
        self.registry[b] = amount_a * amount_b

    def toggle(self, amount):
        amount = self._int_or_registry_value(amount)

        modify_index = self.index + amount
        try:
            instruction_to_toggle = self.instructions[modify_index]
        except IndexError:
            # Outside program, do nothing
            return

        chunks = instruction_to_toggle.split()
        instruction_name = chunks[0]
        method = self.operations_map[instruction_name]
        arg_count = self.get_argument_count(method)

        if arg_count == 1:
            if instruction_name == 'inc':
                # The instruction is swapped to dec
                new_instruction = 'dec'
            else:
                new_instruction = 'inc'
        elif arg_count == 2:
            if instruction_name == 'jnz':
                new_instruction = 'cpy'
            else:
                new_instruction = 'jnz'

        chunks[0] = new_instruction
        self.instructions[modify_index] = ' '.join(chunks)
        # We've modified the code, update any optimizations
        # print 'TGL', modify_index, instruction_to_toggle
        # self.optimize_instructions()

    def optimize_instructions(self):
        """Are there any instructions that we can reduce?.

        By inspecting and this type of instruction modification is known
        as a peephole optimization.

        The question strongly hints at multiplcation so search for that,
        this is a type of strength reduction.

        https://en.wikipedia.org/wiki/Peephole_optimization
        """
        for index, instruction in enumerate(self.instructions):
            chunks = instruction.split(' ')
            if chunks[0] == 'jnz':
                amount = self._int_or_registry_value(chunks[-1])
                if amount < 0:
                    # We're going back. Are we performing a multiplication?
                    # A multiplication is simply an addition done several
                    # times.
                    # To increase a reg by N, we need to to N jumps. To
                    # multiply N by M, we need to repeat M additions.
                    instructions = self.instructions[index + amount: index]
                    reg = chunks[1]
                    if reg not in self.registry:
                        # This is not a variable jump, skip it
                        continue

                    inc_reg = None
                    decr_counter = False
                    multiplier = '1'
                    clear = None
                    for i_index, inner_instruction in enumerate(instructions):
                        inner_chunks = inner_instruction.split()
                        if inner_chunks[0] == 'inc':
                            inc_reg = inner_chunks[1]
                        elif inner_instruction == 'dec %s' % reg:
                            decr_counter = True
                            clear = reg
                        elif inner_chunks[0] == 'mul':
                            # Check if this multiplcation can be further
                            # improved.
                            a, b = inner_chunks[1:]
                            if a == '1':
                                # Look for a copy instruction to the
                                # mult reg
                                for ins in instructions:
                                    ins_chunks = ins.split()
                                    if ins_chunks[0] != 'cpy':
                                        continue
                                    if ins_chunks[2] == b:
                                        multiplier = ins_chunks[1]
                                        clear = b
                                        break
                        elif inner_chunks[0] == 'add':
                            if clear:
                                # We've got a previos mul, set the target
                                # reg
                                inc_reg = inner_chunks[-1]

                        elif inner_chunks[-1] == reg:
                            # Something another type of instruction is
                            # being performed on the counter reg, this
                            # isn't multiplication
                            decr_counter = False
                            break

                    if inc_reg and decr_counter:
                        # Replace these instructions with an add N
                        ins = 'mul %s %s' % (multiplier, reg)
                        self.instructions[index + amount] = ins
                        clear_ins = 'cpy 0 %s' % clear

                        ins = 'add %s %s' % (reg, inc_reg)
                        self.instructions[index + amount + 1] = ins
                        for n in range(index + amount + 2, index + 1):
                            if self.instructions[n].startswith('cpy 0'):
                                # Clearing, no need to replace with a noop
                                continue
                            elif clear:
                                self.instructions[n] = clear_ins
                                clear = None
                            else:
                                self.instructions[n] = 'nop'

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
