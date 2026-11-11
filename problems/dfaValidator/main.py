import argparse
from dfa_validator import DFAValidator, InvalidDFAException
from dfa import DFA
from machine_parser import MachineParser, MachineParserSyntaxException

# Example DFA string: ({A,B}, {0,1}, {(A,0,A), (A,1,B), (B,0,A), (B,1,B)}, A, {B})


parser = argparse.ArgumentParser(
    description="Input: the formal definition of a DFA. Output: Either VALID or INVALID to indicate if it is a DFA or not."
)

parser.add_argument(
    "dfa",
    help="The inputted string must be of the form ({Q}, {Sigma}, {delta}, q0, {F})"
    + "\n To represent the empty set, use {} with no values inside. For the empty string,"
    + " use 'eps'.",
)

args = parser.parse_args()


def main():
    try:
        dfaParse = MachineParser(["S", "S", "ST3", "N", "S"], args.dfa)
        validDFA = DFAValidator(dfaParse.machinePieces)
        dfa = DFA(validDFA)
        dfa.printDFA()
        print("VALID")
    except MachineParserSyntaxException as me:
        print(me)
        print("INVALID")
    except InvalidDFAException as ie:
        print(ie)
        print("INVALID")


if __name__ == "__main__":
    main()
