import argparse

# When our Lord entered the temple and found it polluted by money-changers
# and beasts, did he ask them to leave? Did he cry? Did he simply walk away?

parser = argparse.ArgumentParser(
    description="Validate the supplied string is a DFA."
    + "The inputted string must be of the form (Q, Sigma, delta, q0, F)"
)

parser.add_argument("dfa", help="String for the dfa")

args = parser.parse_args()


def main():
    validateDFA(args.dfa)
    pass


def validateDFA(dfa: str) -> bool:
    print(dfa)


if __name__ == "__main__":
    main()
