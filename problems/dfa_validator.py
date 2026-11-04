import argparse

# When our Lord entered the temple and found it polluted by money-changers
# and beasts, did he ask them to leave? Did he cry? Did he simply walk away?

# Example DFA string: ({A,B}, {0,1}, {(A,0,A), (A,1,B), (B,0,A), (B,1,B)}, A, {B})

parser = argparse.ArgumentParser(
    description="Input: a DFA. Output: Either True or False to indicate if it is a DFA or not."
)

parser.add_argument(
    "dfa",
    help="The inputted string must be of the form ({Q}, {Sigma}, {delta}, q0, {F})",
)

args = parser.parse_args()


def main():
    userDFA = args.dfa
    parseValid: bool = True
    # This is true for ALL inputs, they must be enclosed
    # within braces
    if userDFA[0] != "(":
        print("Missing opening (")
        parseValid = False
    elif userDFA[len(userDFA) - 1] != ")":
        print("Missing closing )")
        parseValid = False

    parseRawDFAString(userDFA)

    if not parseValid:
        return


def validateDFA(dfa: str) -> bool:
    parsedDFA: list = list()
    isDFA: bool = True
    test = dfa.split(", ")
    for i in test:
        print(i.split(","))
    return isDFA


def parseRawDFAString(dfa: str) -> None:
    testList: list = list()
    testStr: str = ""
    depthCount = 0
    for k in range(0, len(dfa)):
        if dfa[k] == "{" or dfa[k] == "(":
            depthCount += 1
        elif dfa[k] == "}" or dfa[k] == ")":
            depthCount -= 1

        if depthCount > 0:
            print(dfa[k], end="")
            testStr += dfa[k]
    print()
    print(testStr.split("{")[1:])
    # validateDFA(args.dfa)


if __name__ == "__main__":
    main()
