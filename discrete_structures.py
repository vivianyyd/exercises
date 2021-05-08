from itertools import chain, combinations


def powerset(iterable):
    """Returns the powerset of an iterable as a set."""
    s = list(iterable)
    return set(chain.from_iterable(combinations(s, r) for r in range(len(s) + 1)))


class Automaton:
    def __init__(self, states, alphabet, transitions, initial, final, typ):
        self.states = states  # set of states
        self.alphabet = alphabet  # set of possible chars
        self.transitions = transitions  # dfa {(s_i,a): s_f}, nfa {(s_i,a): {S_f}}
        self.initial = initial  # int
        self.final = final
        self.type = typ  # 'dfa' or 'nfa'

    def convert(self, new_type):
        """Converts from one type of automaton to the other."""
        new_type = new_type.lower()
        if self.type == new_type:
            print('This automaton is already a', new_type, '!')
            return None
        elif new_type == 'nfa':
            new_f = {}
            for inp in self.transitions.keys():
                new_f[inp] = {self.transitions[inp]}
            return Automaton(self.states, self.alphabet, new_f, self.initial, self.final, new_type)
        elif new_type == 'dfa':
            states = powerset(self.states)
            new_f = {}
            final = set()
            for S in states:
                for a in self.alphabet:
                    next_S = set()
                    for s in S:
                        if (s, a) in self.transitions.keys():
                            next_S = next_S.union(self.transitions[s, a])
                        if s in self.final:
                            final.add(S)
                    new_f[(S, a)] = next_S
            return Automaton(states, self.alphabet, new_f, {self.initial}, final, new_type)
        else:
            print('Not a valid automaton type')

    def print(self):
        print('Type', self.type.upper())
        print('S:\t', self.states)
        print('∑:\t', self.alphabet)
        print('s0:\t', self.initial)
        print('F:\t', self.final)
        print('transition function:')
        s_col, a_col, S_col = 0, 0, 0
        for x, a in self.transitions.keys():
            s_col = max(s_col, len(str(x)))
            a_col = max(a_col, len(str(a)))
            S_col = max(S_col, len(str(self.transitions[x, a])))
        a_col += 6
        print(str.format("{:>" + str(s_col) + "}{:^" + str(a_col) + "}{:<" + str(S_col) + "}", 's', 'a', 'S\''))
        for x, a in self.transitions.keys():
            if self.type == 'dfa':
                if type(x) is int:
                    print(str.format("{:>" + str(s_col) + "}{:^" + str(a_col) + "}{:<" + str(S_col) + "}",
                                     x, a, self.transitions[x, a]))
                else:
                    print(str.format("{:>" + str(s_col) + "}{:^" + str(a_col) + "}{:<" + str(S_col) + "}",
                                     str(set(x) if len(x) != 0 else '{}'), str(a),
                                     str(self.transitions[x, a] if len(self.transitions[x, a]) != 0 else '{}')))
            elif self.type == 'nfa':
                print(str.format("{:>" + str(s_col) + "}{:^" + str(a_col) + "}{:<" + str(S_col) + "}",
                                 x, a, str(self.transitions[x, a] if len(self.transitions[x, a]) != 0 else '{}')))
        print('-----')


if __name__ == "__main__":
    print('Example DFA:')
    dfa_f = {(0, 0): 0, (0, 1): 1, (1, 0): 0, (1, 1): 2, (2, 0): 2, (2, 1): 2}
    dfa = Automaton({0, 1, 2}, {0, 1}, dfa_f, 0, {0.1}, 'dfa')
    dfa.print()
    print('Example NFA:')
    nfa_f = {(0, 0): {0, 1}, (1, 1): {1}}
    nfa = Automaton({0, 1}, {0, 1}, nfa_f, 0, {1}, 'nfa')
    nfa.print()
    print('Converting NFA to DFA:')
    nfa.convert('dfa').print()

