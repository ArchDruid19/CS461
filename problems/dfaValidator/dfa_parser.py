import argparse
from dfa import DFA, InvalidDFAException

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

args = parser.parse_args()


def main():
    rawUserDFAInput: str = args.dfa
    rawUserDFAInput = rawUserDFAInput.strip()
    if not inputStringPreValidation(rawUserDFAInput):
        return

    # Remove outer braces from original user inputted
    # 5-tuple
    rawStrippedUserDFA: str = checkOpenCharAndStrip(rawUserDFAInput, "(", ")")
    if rawStrippedUserDFA is None:
        print("Run the program with -h for proper input format")
        print("INVALID")
        return

    # Split the input into 5 seperate strings
    rawDFAPieces: list = splitInput(rawStrippedUserDFA)
    if len(rawDFAPieces) != 5:
        print("The DFA tuple must only have 5 pieces")
        print("Run the program with -h for proper input format")
        print("INVALID")
        return

    # Parse the states of the DFA and put them in a set. The states MUST be the first
    # item in the 5-tuple
    dfaStates: set = parseSet(rawDFAPieces[0], "states")
    if dfaStates is None:
        return

    # Parse the alphabet of the DFA and put it into a set
    dfaAlphabet: set = parseSet(rawDFAPieces[1], "alphabet")
    if dfaAlphabet is None:
        return

    # Parse the final states of the DFA into a set
    dfaFinalStates: set = parseSet(rawDFAPieces[4], "final states")
    if dfaFinalStates is None:
        return

    # Start state doesnt need stripping or splitting, so take it
    # directly
    dfaStartState: str = rawDFAPieces[3]

    dfaTransitions: list = parseTransitions(rawDFAPieces[2])
    if dfaTransitions is None:
        return

    try:
        userDFA = DFA(
            dfaStates, dfaAlphabet, dfaTransitions, dfaStartState, dfaFinalStates
        )
        print("VALID")
        userDFA.printDFA()
    except InvalidDFAException as e:
        print(e)
        print("INVALID")


def parseSet(piece: str, name: str) -> set | None:
    stripPiece = checkOpenCharAndStrip(piece, "{", "}")
    if stripPiece is None:
        print("ERROR: Please use {} for sets")
        print("INVALID")
        return
    # If we remove the outer brackets/parenthesis and
    # there is nothing, then it is an empty set
    elif stripPiece.strip() == "":
        return set()

    rtnSet = set()
    listPieces = splitInput(stripPiece)

    for i in listPieces:
        if i == "":
            print(f"ERROR: Malformed input for {name}")
            print("INVALID")
            return
        if i in rtnSet:
            print(f"ERROR: Duplicate value '{i}' in {name}")
            print("INVALID")
            return
        rtnSet.add(i)

    return rtnSet


# We will parse the transitions as a list of 3-tuples,
# and then validate them in the DFA class in the constructor
def parseTransitions(transitions: str) -> list | None:
    transitionTuplesList: list = list()
    setStrip = checkOpenCharAndStrip(transitions, "{", "}")
    if setStrip is None:
        print("ERROR: Please use {} for sets")
        print("INVALID")
        return

    splitTransitions = splitInput(setStrip)
    for ch in splitTransitions:
        tmpStrip: str = checkOpenCharAndStrip(ch, "(", ")")
        tmpSplit: list = splitInput(tmpStrip)
        if len(tmpSplit) == 3:
            transitionTuple: tuple = (tmpSplit[0], tmpSplit[1], tmpSplit[2])
            transitionTuplesList.append(transitionTuple)
        else:
            print(f"ERROR: Transition {ch} must have three items")
            print("INVALID")
            return
    return transitionTuplesList


def checkOpenCharAndStrip(piece: str, opener: str, closer: str) -> str | None:
    stripStr: str = ""
    # Each piece we strip must start and end with the supplied opener
    # and closer, and therefore must also have a length of at least 2.

    if len(piece) >= 2 and piece[0] == opener and piece[-1] == closer:
        stripStr = piece[1:-1]
    else:
        return
    return stripStr


def splitInput(input: str) -> list:
    pieces: list = list()
    startCount = 0
    depthCount = 0
    for k in range(0, len(input)):
        if input[k] == "{" or input[k] == "(":
            depthCount += 1
        elif input[k] == "}" or input[k] == ")":
            depthCount -= 1

        if depthCount == 0 and input[k] == ",":
            pieces.append(input[startCount:k].strip())
            startCount = k + 1

    pieces.append(input[startCount:].strip())

    return pieces


def inputStringPreValidation(input: str) -> bool:
    inputStack: list = list()
    charClosureMap: dict = {"}": "{", ")": "("}
    revCharClosureMap: dict = {"{": "}", "(": ")"}

    count: int = 0
    for ch in input:
        if ch in charClosureMap.values():
            inputStack.append((ch, count))
        elif ch in charClosureMap:
            # Extra closure symbol somewhere
            if len(inputStack) == 0:
                print(f"ERROR: Extra {ch} closure at {count}")
                print("INVALID")
                return False
            # Mismatched opener/closure pair
            elif inputStack[-1][0] != charClosureMap[ch]:
                print(
                    f"ERROR: Expected {revCharClosureMap[inputStack[-1][0]]} to close {inputStack[-1][0]} at"
                    + f" position {inputStack[-1][1]}, but found {ch} at position {count}"
                )
                print("INVALID")
                return False
            else:
                inputStack.pop()
        count += 1

    # Extra opener symbol somewhere
    if len(inputStack) > 0:
        print(f"ERROR: Unexpected {inputStack[-1][0]} opener at {inputStack[-1][1]}")
        print("INVALID")
        return False
    return True


if __name__ == "__main__":
    main()
