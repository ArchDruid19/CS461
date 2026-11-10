from machine_parser import MachineParser
from nfa_validator import NfaValidator

import argparse

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
    nfaParser = MachineParser(["S", "S", "ST", "N", "S"], args.dfa)


if __name__ == "__main__":
    main()
