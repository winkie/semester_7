LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGITS = "0123456789"
OTHERS = "!\"#$%&'()*+,-./:;<=>?@[\] ^_`{|}~"

class DFA(object):
    def __init__(self):
        self.states = []
        self.transitions = dict()
        self.final = []
        self.state = None
        
    def feed(self, char):
        assert self.state in self.states

        transition = filter(lambda x: char in x[0],
                            self.transitions[self.state])
        if len(transition) > 1:
            raise RuntimeError("Some non-deterministic shit is here! " + str(transition))
        elif len(transition) == 0:
            self.state = "error"
            return

        transition = transition[0]
        if not transition:
            self.state = "error"
        else:
            self.state = transition[1]

    def reset(self):
        self.state = self.states[0]

    def isFinal(self):
        return self.state in self.final

    def isError(self):
        return self.state == "error"

    def match(self, string, startpos = 0):
        slen, end = len(string), startpos
        while end < slen:
            good, state = self.isFinal(), self.state
            self.feed(string[end])

            if self.isError():
                if good:
                    return end
                else:
                    return 0

            end += 1

        if self.isFinal():
            return end
        else:
            return 0

    def addState(self, state, final = False):
        self.states.append(state)
        if final:
            self.final.append(state)
        self.transitions[state] = []

    def addStates(self, states):
        for s in states:
            if not s in self.states:
                self.addState(s)

    def setFinal(self, state):
        assert state in self.states
        if not state in self.final:
            self.final.append(state)

    def addTransition(self, s1, s2, chars):
        assert s1 in self.states and s2 in self.states

        if not s1 in self.transitions:
            self.transitions[s1] = [[chars, s2]]
            return

        transition = filter(lambda x: x[1] == s2, self.transitions[s1])
        if len(transition) == 0:
            self.transitions[s1].append([chars, s2])
        elif len(transition) == 1:
            transition = transition[0]
            transition[0] = "".join(set(transition[0] + chars))
        else:
            raise RuntimeError("Many transitions from %s to %s" % (s1, s2))
        
    @staticmethod
    def createString(string):
        dfa = DFA()
        dfa.addState(string + "_0")
        pstate = dfa.state = dfa.states[0]
        for i, c in enumerate(string[:-1]):
            nstate = string + "_" + str(i + 1)
            dfa.addState(nstate)
            dfa.addTransition(pstate, nstate, c)
            pstate = nstate
        dfa.addState(string.upper(), True)
        dfa.addTransition(pstate, dfa.states[-1], string[-1])
        return dfa


class RegExMatcher(object):
    #Keep regex version of lexer?
    def match(self, string, startpos = 0):
        pass

class ParallelTokenMatcher(object):
    def __init__(self, dfas):
        pass
    
    def match(self, string, startpos = 0):
        pass

class SequentialTokenMatcher(object):
    def __init__(self):
        pass

    def match(self, tokens, string, startpos = 0):
        for _, dfa in tokens: dfa.reset()
        res = map(lambda (type, dfa): (type, dfa.match(string, startpos)), tokens)
        m = max(res, key = lambda k: k[1])
        return m

