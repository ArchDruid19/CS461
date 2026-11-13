import argparse
from dfa_validator import InvalidDFAException
from dfa import DFA, DFAInputException
from machine_parser import MachineParserSyntaxException

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

argGroup = parser.add_mutually_exclusive_group(required=True)

argGroup.add_argument(
    "-i",
    "--input",
    help="An input to run on the DFA",
)

argGroup.add_argument(
    "-v",
    "--validate",
    help="Validate the DFA without running input",
    action="store_true",
)

args = parser.parse_args()


def main():
    try:
        dfa = DFA(args.dfa)
        # Need to check if None because an empty input
        # is still valid
        if args.input is not None:
            if dfa.simulateDFA(args.input):
                print("ACCEPTED")
            else:
                print("REJECTED")
        if args.validate:
            print("VALID")
    except MachineParserSyntaxException as me:
        print(me)
        if args.validate:
            print("INVALID")
    except InvalidDFAException as ie:
        print(ie)
        if args.validate:
            print("INVALID")
    except DFAInputException as de:
        print(de)


if __name__ == "__main__":
    main()
