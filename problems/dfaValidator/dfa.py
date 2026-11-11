from dfa_validator import DFAValidator


class DFAInputException(Exception):
    pass


class DFA:
    def __init__(self, validDFA: DFAValidator):
        self.dfa = validDFA

    def _validateInput(self, input: str):
        potentialBadSymbols: set = set(input) - self.dfa.inputAlphabet

        if len(potentialBadSymbols) > 0:
            badSymbols: str = ", ".join(sorted(potentialBadSymbols))
            raise DFAInputException(
                f"INPUT ERROR: Symbols found that are not in the alphabet: {badSymbols}"
            )

    def simulateDFA(self, input: str) -> bool:
        self._validateInput(input)
        # We always start at the dfa's start state
        currentState: str = self.dfa.startState

        for ch in input:
            if (currentState, ch) in self.dfa.transitionFunc:
                currentState = self.dfa.transitionFunc[(currentState, ch)]
                print(currentState)
        if currentState in self.dfa.finalState:
            return True
        else:
            return False

    def printDFA(self):
        print(f"Q = {self.dfa.states}")
        print(f"Sigma = {self.dfa.inputAlphabet}")
        print(f"Delta = {self.dfa.transitionFunc}")
        print(f"Q0 = {self.dfa.startState}")
        print(f"F = {self.dfa.finalState}")
