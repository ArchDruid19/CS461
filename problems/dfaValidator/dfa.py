# Small class that inherits Exception because
# using just Exception in a try except block
# for DFA errors might catch errors we don't want to
# catch
class InvalidDFAException(Exception):
    pass


class DFA:
    def __init__(
        self,
        states: set,
        inputAlphabet: set,
        transitionFunc: dict,
        startState: str,
        finalState: set,
    ):
        self.validateStates(states)

        self.validateStartState(startState, states)

        self.states = states
        self.inputAlphabet = inputAlphabet
        self.transitionFunc = transitionFunc
        self.startState = startState
        self.finalState = finalState

    def validateStates(self, states: set):
        if len(states) == 0:
            raise InvalidDFAException("INVALID: The set of states (Q) cannot be empty")
        elif len(states) > 26:
            raise InvalidDFAException("INVALID: A maximum of 26 states are allowed")

    def validateStartState(self, startState: str, states: set):
        if startState == "":
            raise InvalidDFAException("INVALID: The start state must be non-empty.")
        elif startState not in states:
            raise InvalidDFAException(
                "INVALID: The start state is not in the set of states"
            )

    def validateInputAlphabet(self, inputAlphabet: set):
        pass

    def parseAndValidateTransitions(self, transitions: list):
        pass

    def printDFA(self):
        print(f"Q = {self.states}")
        print(f"Sigma = {self.inputAlphabet}")
        print(f"Delta = {self.transitionFunc}")
        print(f"Q0 = {self.startState}")
        print(f"F = {self.finalState}")
