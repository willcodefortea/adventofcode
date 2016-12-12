from collections import namedtuple


Move = namedtuple('Move', 'old_floor,new_floor,items')


class State(object):
    def __init__(self, state, elevator=0, depth=0, moves=None):
        self.state = state
        self.depth = depth
        self.elevator = elevator
        self.moves = moves or []

    def __str__(self):
        output = []
        for index, floor in enumerate(self.state):
            output.append(
                'F{} {} {}'.format(
                    index,
                    'E ' if index == self.elevator else '. ',
                    ' '.join(floor)
                )
            )
        return '\n'.join(output[::-1])

    @property
    def key(self):
        chunks = [
            '%d%s' % (index, '-'.join(sorted(floor)))
            for index, floor in enumerate(self.state)
        ]

        chunks.insert(0, str(self.elevator))
        return ','.join(chunks)

    def clone(self):
        return State(
            [f[:] for f in self.state],
            depth=self.depth,
            elevator=self.elevator,
            moves=self.moves[:]
        )

    @property
    def cost(self):
        """A cost function for our state. Lower is better.

        We're seeking to get all components on the top floor, so describe
        the cost as the number of sum(no. items * distance) for each
        possible distance.

        The result is clamped between 0 and 1.
        """
        if self._cost is None:
            max_cost = sum(len(f) for f in self.state) * (len(self.state) - 1)
            total = 0
            for index, floor in enumerate(self.state[::-1]):
                total += index * len(floor)
            self._cost = 1.0 * total / max_cost
        return self._cost
    _cost = None

    @property
    def is_valid(self):
        """Does anything end up frying in this state?"""
        for floor in self.state:
            required_generators = set()
            generators = set()
            for item in floor:
                if item[1] == 'M':
                    required_generators.add('%sG' % item[0])
                else:
                    generators.add(item)

            # If we have a chip and *any* generators without each chip's
            # corresponding generator, we'll fry the chip
            if generators:
                missing_generators = required_generators - generators
                if missing_generators:
                    return False
        return True

    @property
    def available_moves(self):
        """Find any and all valid moves that can be made from this state."""
        floor = self.state[self.elevator]

        for new_floor in (self.elevator - 1, self.elevator + 1):
            if new_floor < 0 or new_floor >= len(self.state):
                continue

            # First grab each item, then any grouping of two
            for index, item in enumerate(floor):
                yield Move(
                    self.elevator, new_floor, [item, ]
                )

                for second_item in floor[index + 1:]:
                    yield Move(
                        self.elevator, new_floor, [item, second_item, ]
                    )

    def apply_move(self, move):
        """Update our state."""
        self.state[move.new_floor].extend(move.items)
        for item in move.items:
            self.state[move.old_floor].remove(item)

        self.depth += 1
        self.elevator = move.new_floor
        self.moves.append(move)


def test_part_1():
    state = State(
        [
            ['HM', 'LM'],
            ['HG', ],
            ['LG', ],
            [],
        ]
    )

    result = part_1(state)
    assert result == 11


def find_lowest_path(state):
    """
    Find the shortest allowed route to move items to the 4th floor.

    We explore routes that are most likely to be correct based on the
    state's cost and the number of steps taken (as that's what we're
    seeking to minimize).
    """
    visited = set()
    states = [state, ]
    shortest_depth = None
    while True:
        new_states = []
        lowest_cost = states[0].cost
        for state in states:
            if state.cost > lowest_cost:
                # No point looking at this or any following states just
                # yet.
                break

            for move in state.available_moves:
                new_state = state.clone()
                new_state.apply_move(move)

                if new_state.key in visited:
                    # We've travelled this path before, skip it.
                    continue
                visited.add(new_state.key)

                if new_state.is_valid:
                    # We've found a valid state, either explore it next
                    # time or throw it away
                    if new_state.cost == 0:
                        if shortest_depth is None or new_state.depth < shortest_depth:
                            shortest_depth = new_state.depth
                        # We've found a solution and don't need to continue
                        # exploring this state
                        continue

                    if shortest_depth and new_state.depth >= shortest_depth:
                        # Ignore this state, we don't need it
                        continue

                    # This state needs further exploration, add it for
                    # next time.
                    new_states.append(new_state)

        # Update our states for checking.
        # Sort by the cost of the state and the number of steps so we evaluate
        # states most likely to be correct first.
        states = sorted(
            new_states,
            key=lambda state: (state.cost, state.depth)
        )
        if not states:
            # We have no more states to explore
            break
    return shortest_depth


def part_1(state):
    return find_lowest_path(state)


def main():
    state = State(
        [
            ['PG', 'TG', 'TM', 'PRG', 'RG', 'RM', 'CG', 'CM', ],
            ['PM', 'PRM', ],
            [],
            [],
        ]
    )
    test_part_1()
    answer = part_1(state)
    print 'The minimum number of moves is %s.' % answer

    state2 = State(
        [
            [
                'PG', 'TG', 'TM', 'PRG', 'RG', 'RM', 'CG', 'CM', 'EG', 'EM',
                'DG', 'DM'
            ],
            ['PM', 'PRM', ],
            [],
            [],
        ]
    )
    answer = part_1(state2)
    print 'The minimum number of moves is %s.' % answer

if __name__ == '__main__':
    main()
