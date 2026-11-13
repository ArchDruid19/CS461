from dfa_validator import DFAValidator
from machine_parser import MachineParser


class DFAInputException(Exception):
    pass


class DFA:
    def __init__(self, machineStr: str):
        dfaParse = MachineParser(["S", "S", "ST3", "N", "S"], machineStr)
        self.dfa = DFAValidator(dfaParse.machinePieces)

    def _validateInput(self, input: str):
        potentialBadSymbols: set = set(input) - self.dfa.inputAlphabet

        if len(potentialBadSymbols) > 0:
            badSymbols: str = ", ".join(sorted(potentialBadSymbols))
            raise DFAInputException(
                f"INPUT ERROR: Symbols found that are not in the alphabet: {badSymbols}"
            )

    def simulateDFA(self, inputString: str) -> bool:
        self._validateInput(inputString)
        # We always start at the dfa's start state
        currentState: str = self.dfa.startState
        stateSequence: list = list(currentState)

        for ch in inputString:
            if (currentState, ch) in self.dfa.transitionFunc:
                currentState = self.dfa.transitionFunc[(currentState, ch)]
                stateSequence.append(currentState)

        print("->".join(stateSequence))
        return currentState in self.dfa.finalState

    def printDFA(self):
        print(f"Q = {self.dfa.states}")
        print(f"Sigma = {self.dfa.inputAlphabet}")
        print(f"Delta = {self.dfa.transitionFunc}")
        print(f"Q0 = {self.dfa.startState}")
        print(f"F = {self.dfa.finalState}")
