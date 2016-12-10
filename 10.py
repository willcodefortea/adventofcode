from collections import defaultdict


def give_value(config, bot, value):
    """Give a bot in the config a value to hold."""
    if len(config[bot]) == 2:
        return False

    config[bot].append(value)
    return True


def compare(config, bot, low, high):
    """Have a bot compare and assign it's values."""
    if len(config[bot]) != 2:
        return False

    config[low].append(min(config[bot]))
    config[high].append(max(config[bot]))
    # Clear the list
    config[bot] = []
    return True


def parse_instruction(instruction):
    """Return the method + arguments to be performed."""
    chunks = instruction.split(' ')

    if chunks[0] == 'value':
        # We're giving a vlaue to a bot
        value = int(chunks[1])
        bot = chunks[-1]
        args = (bot, value, )
        func = give_value
    else:
        # We're swapping values
        bot = chunks[1]
        low = chunks[6]
        if chunks[5] == 'output':
            low = 'output %s' % low
        high = chunks[-1]
        if chunks[-2] == 'output':
            high = 'output %s' % high
        args = (bot, low, high, )
        func = compare

    return func, args


def perform_instructions(instructions, before_op=None):
    """Apply all instructions to the config, updating config by ref.

    The supplied order of the instructions does not mean they will be
    executed in that order. Each bot can only perform the action if it
    is in a specific state, otherwise we skip it until the next state
    update.
    """
    config = defaultdict(list)

    parsed_instructions = [
        parse_instruction(instruction)
        for instruction in instructions
    ]

    to_be_performed = parsed_instructions

    while True:
        performed = []

        for parsed in to_be_performed:
            func, args = parsed

            if before_op:
                # Let any listeners know that an op is about to be
                # performed
                before_op(config, func, args)

            if func(config, *args):
                performed.append(parsed)

        to_be_performed = [
            parsed for parsed in to_be_performed if parsed not in performed
        ]

        if len(performed) == 0:
            # Nothing has changed, nothing will change next time
            break
    return config


def test_part_1():
    instructions = [
        'value 5 goes to bot 2',
        'bot 2 gives low to bot 1 and high to bot 0',
        'value 3 goes to bot 1',
        'bot 1 gives low to output 1 and high to bot 0',
        'bot 0 gives low to output 2 and high to output 0',
        'value 2 goes to bot 2',
    ]

    config = part_1(instructions, [2, 5, ])
    assert config['output 0'] == [5, ]
    assert config['output 1'] == [2, ]
    assert config['output 2'] == [3, ]
    assert config['bot_responsible_for_comparision'] == '2'


def part_1(instructions, watch):
    def watch_for_comparision(config, func, args):
        if func == compare:
            bot = args[0]
            if sorted(config[bot]) == watch:
                config['bot_responsible_for_comparision'] = bot

    config = perform_instructions(instructions, watch_for_comparision)
    return config


def part_2(instructions):
    config = perform_instructions(instructions)
    return (
        config['output 0'][0] * config['output 1'][0] * config['output 2'][0]
    )


def main():
    with open('10.txt') as fin:
        data = fin.read().split('\n')
    test_part_1()

    config = part_1(data, [17, 61])
    print 'The bot number is %s.' % config['bot_responsible_for_comparision']

    answer = part_2(data)
    print 'Muliplying the outputs gives %s.' % answer

if __name__ == '__main__':
    main()
