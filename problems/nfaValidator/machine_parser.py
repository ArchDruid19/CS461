class MachineParserSyntaxException(Exception):
    pass


# S for set, ST for set of tuples, N for neither
# parseList will also give us how many items should be included
class MachineParser:
    def __init__(self, parseList: list, rawInput: str):
        self.parseList = parseList
        self.rawInput = rawInput.strip()
        numItems = len(parseList)

        if not self._inputStringPreValidation():
            return

        rawPieces: list = self._splitInput(rawInput)

        if len(rawPieces) != numItems:
            print(f"The tuple must have {numItems} pieces")
            print("INVALID")
            return

    def _parseMachinePartsIntoList(self) -> list | None:
        tupleList: list = list()
        for item in self.parseList:
            if item == "S":
                self._pars
            elif item == "ST":
                pass
            elif item == "N":
                pass
            else:
                print(f"Expected S, ST, or N, but got {item}")
                return
        return tupleList

    def _parseSet(self, piece: str, name: str) -> set | None:
        stripPiece = self._checkOpenCharAndStrip(piece, "{", "}")
        if stripPiece is None:
            print("ERROR: Please use {} for sets")
            print("INVALID")
            return
        # If we remove the outer brackets/parenthesis and
        # there is nothing, then it is an empty set
        elif stripPiece.strip() == "":
            return set()

        rtnSet = set()
        listPieces = self._splitInput(stripPiece)

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
    def _parseTransitions(self, transitions: str) -> list | None:
        transitionTuplesList: list = list()
        setStrip = self._checkOpenCharAndStrip(transitions, "{", "}")
        if setStrip is None:
            print("ERROR: Please use {} for sets")
            print("INVALID")
            return

        splitTransitions = self._splitInput(setStrip)
        for ch in splitTransitions:
            tmpStrip: str = self._checkOpenCharAndStrip(ch, "(", ")")
            tmpSplit: list = self._splitInput(tmpStrip)
            if len(tmpSplit) == 3:
                transitionTuple: tuple = (tmpSplit[0], tmpSplit[1], tmpSplit[2])
                transitionTuplesList.append(transitionTuple)
            else:
                print(f"ERROR: Transition {ch} must have three items")
                print("INVALID")
                return
        return transitionTuplesList

    def _checkOpenCharAndStrip(
        self, piece: str, opener: str, closer: str
    ) -> str | None:
        stripStr: str = ""
        # Each piece we strip must start and end with the supplied opener
        # and closer, and therefore must also have a length of at least 2.

        if len(piece) >= 2 and piece[0] == opener and piece[-1] == closer:
            stripStr = piece[1:-1]
        else:
            return
        return stripStr

    def _splitInput(self, input: str) -> list:
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

    def _inputStringPreValidation(self) -> bool:
        inputStack: list = list()
        charClosureMap: dict = {"}": "{", ")": "("}
        charOpenerMap: dict = {"{": "}", "(": ")"}

        count: int = 0
        for ch in self.rawInput:
            if ch in charOpenerMap:
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
                        f"ERROR: Expected {charOpenerMap[inputStack[-1][0]]} to close {inputStack[-1][0]} at"
                        + f" position {inputStack[-1][1]}, but found {ch} at position {count}"
                    )
                    print("INVALID")
                    return False
                else:
                    inputStack.pop()
            count += 1

        # Extra opener symbol somewhere
        if len(inputStack) > 0:
            print(
                f"ERROR: Unexpected {inputStack[-1][0]} opener at {inputStack[-1][1]}"
            )
            print("INVALID")
            return False
        return True
