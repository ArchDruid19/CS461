from machine_parser import MachineParserSyntaxException
from nfa_validator import InvalidNFAException
from nfa import NFA
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
        nfa: NFA = NFA(args.nfa)
        print("VALID")
        nfa.printNFA()
    except MachineParserSyntaxException as me:
        print(me)
        print("INVALID")
    except InvalidNFAException as ie:
        print(ie)
        print("INVALID")


if __name__ == "__main__":
    main()
