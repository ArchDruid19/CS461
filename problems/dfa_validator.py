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
    parseDFAStringToPieces(userDFA)


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
                    print(f"ERROR: expected ( at {inputStack[-1][1]} {i}")
                    return False
            else:
                print(f"ERROR: Unexpected ) closure")
                printError(userInput, i)
                return False
    #print()
    print(inputStack)
    return True

def printError(orgStr: str, failPoint: int):
    print(orgStr)
    failStr: str = ""
    if failPoint == 0:
        failStr = "^"
    else:
        for i in range(0, failPoint):
            failStr += " "
        failStr += "^"
    print(failStr)


def validateDFA() -> bool:
    pass


def parseDFAStringToPieces(dfa: str) -> None:
    # Remove outer braces, if they are present
    dfa: str = dfa[1 : len(dfa) - 1]

    dfaPieces: list = splitDFAInput(dfa)


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
