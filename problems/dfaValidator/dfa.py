from dfa_validator import DFAValidator


class DFA:
    def __init__(self, validDFA: DFAValidator):
        self.dfa = validDFA
        pass

    def simulateDFA(self, input: str):
        pass

    def printDFA(self):
        print(f"Q = {self.dfa.states}")
        print(f"Sigma = {self.dfa.inputAlphabet}")
        print(f"Delta = {self.dfa.transitionFunc}")
        print(f"Q0 = {self.dfa.startState}")
        print(f"F = {self.dfa.finalState}")
