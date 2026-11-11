class MachineParserSyntaxException(Exception):
    pass


# S for set, ST for set of tuples, N for neither
# parseList will also give us how many items should be included
class MachineParser:
    def __init__(self, parseList: list, rawInput: str):
        self.parseList = parseList
        self.rawInput = rawInput.strip()
        numItems = len(parseList)

        self._inputStringPreValidation()

        strippedInput: str = self._checkOpenCharAndStrip(self.rawInput, "(", ")")
        rawPieces: list = self._splitInput(strippedInput)

        if len(rawPieces) != numItems:
            raise MachineParserSyntaxException(f"The tuple must have {numItems} pieces")

        machinePieces: list = self._parseMachinePartsIntoList(rawPieces)
        print(machinePieces)
        self.machinePieces = machinePieces

    def _parseMachinePartsIntoList(self, rawPieces: list) -> list:
        tupleList: list = list()
        countIDX: int = 0
        for item in self.parseList:
            if item == "S":
                tupleList.append(self._parseSet(rawPieces[countIDX]))
            elif "ST" in item:
                if len(item) == 3:
                    self.tupleNum = int(item[2])
                    print(self.tupleNum)
                    tupleList.append(self._parseTransitions(rawPieces[countIDX]))
                else:
                    raise MachineParserSyntaxException(
                        "If using ST, please enter a tuple size (i.e ST3 for a 3 tuple)"
                    )
            elif item == "N":
                tupleList.append(rawPieces[countIDX])
            else:
                raise MachineParserSyntaxException(
                    f"Expected S, ST, or N but got {item}"
                )
            countIDX += 1
        return tupleList

    def _parseSet(self, piece: str) -> set:
        stripPiece = self._checkOpenCharAndStrip(piece, "{", "}")
        if stripPiece is None:
            raise MachineParserSyntaxException("ERROR: Please use {} for sets")
        # If we remove the outer brackets/parenthesis and
        # there is nothing, then it is an empty set
        elif stripPiece.strip() == "":
            return set()

        rtnSet = set()
        listPieces = self._splitInput(stripPiece)

        for i in listPieces:
            if i == "":
                raise MachineParserSyntaxException("ERROR: Malformed input")
            if i in rtnSet:
                raise MachineParserSyntaxException(f"ERROR: Duplicate value '{i}'")
            rtnSet.add(i)

        return rtnSet

    # Parse the transitions as a list of 3-tuples
    def _parseTransitions(self, transitions: str) -> list | None:
        transitionTuplesList: list = list()
        setStrip = self._checkOpenCharAndStrip(transitions, "{", "}")
        if setStrip is None:
            raise MachineParserSyntaxException("ERROR: Please use {} for sets")

        splitTransitions = self._splitInput(setStrip)
        for ch in splitTransitions:
            tmpStrip: str = self._checkOpenCharAndStrip(ch, "(", ")")
            tmpSplit: list = self._splitInput(tmpStrip)
            if len(tmpSplit) == self.tupleNum:
                transitionTuple: tuple = (tmpSplit[0], tmpSplit[1], tmpSplit[2])
                transitionTuplesList.append(transitionTuple)
            else:
                raise MachineParserSyntaxException(
                    f"ERROR: Transition {ch} must have {self.tupleNum} items"
                )
        return transitionTuplesList

    # Each piece we strip must start and end with the supplied opener
    def _checkOpenCharAndStrip(
        self, piece: str, opener: str, closer: str
    ) -> str | None:

        stripStr: str = ""
        if len(piece) >= 2 and piece[0] == opener and piece[-1] == closer:
            stripStr = piece[1:-1]
        else:
            return None
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

    def _inputStringPreValidation(self):
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
                    raise MachineParserSyntaxException(
                        f"ERROR: Extra {ch} closure at {count}"
                    )
                # Mismatched opener/closure pair
                elif inputStack[-1][0] != charClosureMap[ch]:
                    raise MachineParserSyntaxException(
                        (
                            f"ERROR: Expected {charOpenerMap[inputStack[-1][0]]} to close {inputStack[-1][0]} at"
                            + f" position {inputStack[-1][1]}, but found {ch} at position {count}"
                        )
                    )
                else:
                    inputStack.pop()
            count += 1

        # Extra opener symbol somewhere
        if len(inputStack) > 0:
            raise MachineParserSyntaxException(
                f"ERROR: Unexpected {inputStack[-1][0]} opener at {inputStack[-1][1]}"
            )
        return True
