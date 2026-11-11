from nfa_validator import NfaValidator


class NFA:
    def __init__(self, validNFA: NfaValidator):
        self.nfa = validNFA

    def printNFA(self):
        print(f"Q = {", ".join(self.nfa.states)}")
        print(f"Sigma = {", ".join(self.nfa.inputAlphabet)}")
        print(f"Delta = {self.nfa.transitionFunc}")
        print(f"Q0 = {self.nfa.startState}")
        print(f"F = {", ".join(self.nfa.finalState)}")
