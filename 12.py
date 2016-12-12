def build_registry():
    return {
        'a': 0,
        'b': 0,
        'c': 0,
        'd': 0,
        'instruction': 0,
    }


def _int_or_registry_value(registry, key):
    """Check if the key is an integer or a registry value."""
    try:
        value = int(key)
    except ValueError:
        value = registry[key]
    return value


def copy(registry, source, destintion):
    value = _int_or_registry_value(registry, source)
    registry[destintion] = value


def increase(registry, destintion):
    registry[destintion] += 1


def decrease(registry, destintion):
    registry[destintion] -= 1


def jump(registry, key, amount):
    value = _int_or_registry_value(registry, key)
    amount = int(amount)
    if value != 0:
        registry['instruction'] += amount


def execute_instruction(instruction, registry):
    chunks = instruction.split(' ')
    name = chunks[0]

    if name == 'cpy':
        method = copy
    elif name == 'inc':
        method = increase
    elif name == 'dec':
        method = decrease
    elif name == 'jnz':
        method = jump
    else:
        raise Exception('Unknown instruction "%s".' % instruction)

    prev_instruction_index = registry['instruction']
    method(registry, *chunks[1:])

    if prev_instruction_index == registry['instruction']:
        # The instruction did NOT jump to a different location, advance
        # ourselves
        registry['instruction'] += 1


def execute_instructions(instructions, registry):
    while True:
        try:
            instruction = instructions[registry['instruction']]
        except IndexError:
            break
        execute_instruction(instruction, registry)


def test_part_1():
    instructions = [
        'cpy 41 a',
        'inc a',
        'inc a',
        'dec a',
        'jnz a 2',
        'dec a',
    ]
    registry = build_registry()
    execute_instructions(instructions, registry)
    assert registry['a'] == 42


def main():
    with open('12.txt') as fin:
        instructions = fin.read().split('\n')
    test_part_1()

    registry = build_registry()
    execute_instructions(instructions, registry)
    answer = registry['a']
    print 'The value in register a is %s.' % answer

    registry = build_registry()
    registry['c'] = 1
    execute_instructions(instructions, registry)
    answer = registry['a']
    print 'The value in register a is %s.' % answer


if __name__ == '__main__':
    main()
