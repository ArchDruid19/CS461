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
    if not doStringPreValidation(userDFA):
        return
    # Remove outer braces, if they are present
    stripDFA: str = checkOpenCharAndStrip(userDFA, "(", ")")
    if stripDFA is None:
        print("Run the program with -h for proper input format")
        return

    dfaPieces: list = splitInput(stripDFA)
    if len(dfaPieces) != 5:
        print("The DFA tuple must only have 5 pieces")
        print("Run the program with -h for proper input format")
        return

    dfaStates: set = parseSet(dfaPieces[0], "t")
    print(dfaStates)


def parseSet(piece: str, name: str) -> set | None:
    stripPiece = checkOpenCharAndStrip(piece, "{", "}")
    if stripPiece is None:
        return
    elif stripPiece == "".strip():
        return set()

    rtnSet = set()
    listPieces = splitInput(stripPiece)
    print(listPieces)


def checkOpenCharAndStrip(piece: str, opener: str, closer: str):
    stripStr: str = ""
    if len(piece) >= 2 and piece[0] == opener and piece[-1] == closer:
        stripStr = piece[1:-1]
    else:
        return None
    print(stripStr)
    return stripStr


def splitInput(dfa: str) -> list:
    dfaPieces: list = list()
    startCount = 0
    depthCount = 0
    for k in range(0, len(dfa)):
        if dfa[k] == "{" or dfa[k] == "(":
            depthCount += 1
        elif dfa[k] == "}" or dfa[k] == ")":
            depthCount -= 1

        if depthCount == 0 and dfa[k] == ",":
            # print(startCount, k, dfa[startCount:k].strip())
            dfaPieces.append(dfa[startCount:k].strip())
            startCount = k + 1

    # print(dfa[startCount:].strip())
    dfaPieces.append(dfa[startCount:].strip())

    return dfaPieces


def doStringPreValidation(userInput: str) -> bool:
    # Check the input string has matching braces
    # with a stack and index location
    inputStack: list = list()

    for i in range(0, len(userInput)):
        if userInput[i] == "{" or userInput[i] == "(":
            inputStack.append((userInput[i], i))
        elif userInput[i] == "}":
            if inputStack:
                if inputStack[-1][0] == "{":
                    inputStack.pop()
                else:
                    print(f"ERROR: expected ) closure at {i}")
                    printError(userInput, i)
                    return False
            else:
                print(f"ERROR: Unexpected }} closure")
                printError(userInput, i)
                return False
        elif userInput[i] == ")":
            if inputStack:
                if inputStack[-1][0] == "(":
                    inputStack.pop()
                else:
                    print(f"ERROR: expected }} closure at {i}")
                    printError(userInput, i)
                    return False
            else:
                print(f"ERROR: Unexpected ) closure")
                printError(userInput, i)
                return False

    if len(inputStack) > 0:
        print(f"ERROR: unclosed {inputStack[-1][0]} at {i}")
        printError(userInput, i + 1)
        return False

    return True


def printError(orgStr: str, failPoint: int):
    print(orgStr)
    failStr: str = ""
    for i in range(0, failPoint):
        failStr += " "
    failStr += "^"
    print(failStr)


if __name__ == "__main__":
    main()
