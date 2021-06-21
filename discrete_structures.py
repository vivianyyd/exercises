from itertools import chain, combinations


def powerset(iterable):
    """Returns the powerset of an iterable as a set."""
    s = list(iterable)
    return set(chain.from_iterable(combinations(s, r) for r in range(len(s) + 1)))


class Automaton:
    def __init__(self, states, alphabet, transitions, initial, final, typ):
        self.states = states  # set of states
        x = None  # in case states is empty
        for x in states:
            break
        self.state_type = type(x)  # a really sad way of getting the type of a state.
        self.alphabet = alphabet  # set of possible chars
        self.transitions = transitions  # dfa {(s_i,a): s_f}, nfa {(s_i,a): {S_f}}
        self.initial = initial  # int
        self.final = final  # set of states
        self.type = typ  # 'dfa' or 'nfa' - make this an enum?

    def accept(self, x):
        """Returns true if string x is accepted by the automaton; false otherwise."""
        curr = {self.initial}
        for a in x:
            a = int(a)
            new_curr = set()
            for state in curr:
                if self.type == 'dfa' and self.state_type is int:
                    new_curr.add(self.transitions[state, a])
                elif self.type == 'nfa':
                    if (state, a) in self.transitions.keys():
                        new_curr = new_curr.union(self.transitions[state, a])
                else:
                    print('i made an oopsie')
            curr = new_curr
        return True if len(curr.intersection(self.final)) > 0 else False

    def convert(self, new_type):
        """Converts from one type of automaton to the other."""
        new_type = new_type.lower().strip()
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
            for state_set in states:
                for a in self.alphabet:
                    next_S = set()
                    for state in state_set:
                        if (state, a) in self.transitions.keys():
                            next_S = next_S.union(self.transitions[state, a])
                        if state in self.final:
                            final.add(state_set)
                    new_f[(state_set, a)] = next_S
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
                if self.state_type is int:
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
    # more examples
    mf = {(0, 0): {1, 2}, (1, 0): {1}, (1, 1): {2}, (2, 1): {2}}
    m = Automaton({0, 1, 2}, {0, 1}, mf, 0, {0, 2}, 'nfa')
    tm = m.convert('dfa')
    tm.print()
    tmpf = tm.states.difference(tm.final)
    tmp = Automaton(tm.states, tm.alphabet, tm.transitions, 0, tmpf, 'dfa')
    tmp.print()
    mp = tmp.convert('nfa')
    print(mp)
    print('Converting NFA to DFA:')
    nfa.convert('dfa').print()
    print(nfa.accept('000001'))  # True
    print(nfa.accept('000001111'))  # True
    print(nfa.accept('0'))  # True
    print(nfa.accept('00'))  # True
    print(nfa.accept('1'))  # False
    print(nfa.accept('11111'))  # False
    print('Discussion section exercise:')
    nfa_f_2 = {(0, 0): {1}, (0, 1): {1, 2}, (1, 0): {1}, (1, 1): {1},
               (2, 0): {3}, (2, 1): {2}, (3, 0): {3}, (3, 1): {3}}
    nfa_2 = Automaton({0, 1, 2, 3}, {0, 1}, nfa_f_2, 0, {1, 2, 3}, 'nfa')
    dfa_2 = nfa_2.convert('dfa')
    dfa_2.print()
    print(len(dfa_2.final))
