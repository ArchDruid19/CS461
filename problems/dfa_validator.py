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
    if doStringPreValidation(userDFA):
        print("Good!")
    # parseRawDFAString(userDFA)


def doStringPreValidation(userInput: str) -> bool:
    # Check the input string has matching braces
    # with a stack and index location (very similar to)
    # the PDA we use for matching braces)
    inputStack: list = list()

    for i in range(0, len(userInput)):
        if userInput[i] == "{" or userInput[i] == "(":
            inputStack.append((userInput[i], i))
        elif userInput[i] == "}":
            # !Add same logic for if symbol is ) but for }
            if inputStack[-1][0] == "{":
                inputStack.pop()
        elif userInput[i] == ")":
            if inputStack:
                if inputStack[-1][0] == "(":
                    inputStack.pop()
                else:
                    print(f"ERROR: expected }} at {inputStack[-1][1]} {i}")
            else:
                print(f"ERROR: Unexpected ) closure at {i}")
    #print()
    print(inputStack)


def validateDFA() -> bool:
    pass


def parseRawDFAString(dfa: str) -> None:
    parseValid: bool = True
    # This is true for ALL inputs, they must be enclosed
    # within braces
    if dfa[0] != "(":
        print("Missing opening (")
        parseValid = False
    elif dfa[len(dfa) - 1] != ")":
        print("Missing closing )")
        parseValid = False

    if not parseValid:
        return

    # Remove outer braces, if they are present
    dfa: str = dfa[1 : len(dfa) - 1]

    dfaPieces: list = splitDFAInput(dfa)

    print(dfaPieces, len(dfaPieces))

    mere = dfaPieces[2]
    testy: list = splitDFAInput(mere[1 : len(mere) - 1])


def checkOpenCharAndStrip(dfa: str):
    pass


def splitDFAInput(dfa: str) -> list:
    dfaPieces: list = list()
    startCount = 0
    depthCount = 0
    for k in range(0, len(dfa)):
        if dfa[k] == "{" or dfa[k] == "(":
            depthCount += 1
        elif dfa[k] == "}" or dfa[k] == ")":
            depthCount -= 1

        if depthCount == 0 and dfa[k] == ",":
            #print(startCount, k, dfa[startCount:k].strip())
            dfaPieces.append(dfa[startCount:k].strip())
            startCount = k + 1

    #print(dfa[startCount:].strip())
    dfaPieces.append(dfa[startCount:].strip())

    return dfaPieces


if __name__ == "__main__":
    main()
