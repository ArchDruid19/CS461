import argparse
import dfa

# When our Lord entered the temple and found it polluted by money-changers
# and beasts, did he ask them to leave? Did he cry? Did he simply walk away?

# Example DFA string: ({A,B}, {0,1}, {(A,0,A), (A,1,B), (B,0,A), (B,1,B)}, A, {B})

# TODO: Fix inputs like (A,B), (C,D), (E,F), (H,I), (J,K) in pre-validation
# TODO: Make better and more accurate error messages

parser = argparse.ArgumentParser(
    description="Input: a DFA. Output: Either True or False to indicate if it is a DFA or not."
)

parser.add_argument(
    "dfa",
    help="The inputted string must be of the form ({Q}, {Sigma}, {delta}, q0, {F})",
)

args = parser.parse_args()


def main():
    userDFA: str = args.dfa
    userDFA = userDFA.strip()
    if not inputStringPreValidation(userDFA):
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

    dfaStates: set = parseSet(dfaPieces[0], "states")
    if dfaStates is None:
        return
    print(dfaStates)

    dfaAlphabet: set = parseSet(dfaPieces[1], "alphabet")
    if dfaAlphabet is None:
        return
    print(dfaAlphabet)

    dfaFinalStates: set = parseSet(dfaPieces[4], "final states")
    if dfaFinalStates is None:
        return
    print(dfaFinalStates)

    startState: str = dfaPieces[3]
    print(startState)

    transitions: dict = parseTransitions(dfaPieces[2])


def parseSet(piece: str, name: str) -> set | None:
    stripPiece = checkOpenCharAndStrip(piece, "{", "}")
    if stripPiece is None:
        return
    elif stripPiece.strip() == "":
        return set()

    rtnSet = set()
    listPieces = splitInput(stripPiece)

    for i in listPieces:
        if i == "":
            print(f"Malformed input for {name}")
            return
        if i in rtnSet:
            print(f"Duplicate value '{i}' in {name}")
            return
        rtnSet.add(i)

    return rtnSet

# We will parse the transitions as a list of 3-tuples,
# and then validate them in the DFA class in the constructor
def parseTransitions(transitions: str) -> dict:
    setStrip = checkOpenCharAndStrip(transitions, "{", "}")
    splitTransitions = splitInput(setStrip)
    
    for ch in splitTransitions:
        tmpStrip: str = checkOpenCharAndStrip(ch, "(", ")")
        tmpSplit: list = splitInput(tmpStrip)
        for tmpCh in tmpSplit:
            print(tmpCh, end=" ")
        print()


def checkOpenCharAndStrip(piece: str, opener: str, closer: str) -> str | None:
    stripStr: str = ""
    if len(piece) >= 2 and piece[0] == opener and piece[-1] == closer:
        stripStr = piece[1:-1]
    else:
        return
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
            dfaPieces.append(dfa[startCount:k].strip())
            startCount = k + 1

    dfaPieces.append(dfa[startCount:].strip())

    return dfaPieces


def inputStringPreValidation(userInput: str) -> bool:
    inputStack: list = list()
    charClosureMap: dict = {"}": "{", ")": "("}
    revCharClosureMap: dict = {"{": "}", "(": ")"}

    count: int = 0
    for ch in userInput:
        if ch in charClosureMap.values():
            # print(ch, end="")
            inputStack.append((ch, count))
        elif ch in charClosureMap:
            # print(ch, end="")
            # Extra closure symbol somewhere
            if len(inputStack) == 0:
                print(f"ERROR: Extra {ch} closure at {count}")
                return False
            # Mismatched opener/closure pair
            elif inputStack[-1][0] != charClosureMap[ch]:
                print(
                    f"ERROR: Expected {revCharClosureMap[inputStack[-1][0]]} to close {inputStack[-1][0]} at"
                    + f" position {inputStack[-1][1]}, but found {ch} at position {count}"
                )
                return False
            else:
                inputStack.pop()
        count += 1

    # Extra opener symbol somewhere
    if len(inputStack) > 0:
        print(f"ERROR: Unexpected {inputStack[-1][0]} opener at {inputStack[-1][1]}")
        return False
    return True


if __name__ == "__main__":
    main()
