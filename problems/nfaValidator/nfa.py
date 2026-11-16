from nfa_validator import NfaValidator
from machine_parser import MachineParser


class NFA:
    def __init__(self, inputMachine: str):
        nfaParser = MachineParser(["S", "S", "ST3", "N", "S"], inputMachine)
        validNFA = NfaValidator(nfaParser.machinePieces)
        self.nfa = validNFA

    def printNFA(self):
        print(f"Q = {", ".join(self.nfa.states)}")
        print(f"Sigma = {", ".join(self.nfa.inputAlphabet)}")
        print(f"Delta = {self.nfa.transitionFunc}")
        print(f"Q0 = {self.nfa.startState}")
        print(f"F = {", ".join(self.nfa.finalState)}")
