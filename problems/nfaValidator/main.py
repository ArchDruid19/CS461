from machine_parser import MachineParser, MachineParserSyntaxException
from nfa_validator import NfaValidator, InvalidNFAException

import argparse

parser = argparse.ArgumentParser(
    description="Input: the formal definition of a NFA. Output: Either VALID or INVALID to indicate if it is a NFA or not."
)

parser.add_argument(
    "nfa",
    help="The inputted string must be of the form ({Q}, {Sigma}, {delta}, q0, {F})"
    + "\n To represent the empty set, use {} with no values inside. For the empty string,"
    + " use 'eps'.",
)

args = parser.parse_args()


def main():
    try:
        nfaParser = MachineParser(["S", "S", "ST", "N", "S"], args.nfa)
        nfa = NfaValidator(nfaParser.machinePieces)
        print("VALID")
        nfa.printDFA()
    except MachineParserSyntaxException as me:
        print(me)
        print("INVALID")
    except InvalidNFAException as ie:
        print(ie)
        print("INVALID")


if __name__ == "__main__":
    main()
