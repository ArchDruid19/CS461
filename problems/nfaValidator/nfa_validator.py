# Raise this exception for any errors found
class InvalidNFAException(Exception):
    pass


class NfaValidator:
    emptyString: str = "eps"
    machinePartsMap: dict = {
        "states": 0,
        "input": 1,
        "transitions": 2,
        "start": 3,
        "final": 4,
    }

    def __init__(self, machineParts: list):
        states = machineParts[self.machinePartsMap["states"]]
        inputAlphabet = machineParts[self.machinePartsMap["input"]]
        transitionList = machineParts[self.machinePartsMap["transitions"]]
        startState = machineParts[self.machinePartsMap["start"]]
        finalStates = machineParts[self.machinePartsMap["final"]]

        self._validateStates(states)
        self._validateInputAlphabet(inputAlphabet)
        self._validateStartState(startState, states)
        self._validateFinalStates(finalStates, states)

        transitionDict: dict = self._buildTransitionDictionary(transitionList)
        self._validateTransitionMembership(transitionDict, inputAlphabet, states)

        self.states = states
        self.inputAlphabet = inputAlphabet
        self.transitionFunc = transitionDict
        self.startState = startState
        self.finalState = finalStates

    def _validateStates(self, states: set):
        # We must have at least one state in Q
        if len(states) == 0:
            raise InvalidNFAException("The set of states (Q) cannot be empty")
        # As per the instructions, we can only have a max of 26 states
        elif len(states) > 26:
            raise InvalidNFAException(
                f"A maximum of 26 states are allowed, {len(states)} was found"
            )
        for i in states:
            # Each state symbol must be 1 character
            if len(i) != 1:
                raise InvalidNFAException(
                    f"State symbols must be 1 character long, found {i} of length {len(i)}"
                )
            # Each state symbol must be a character between A and Z
            elif ord(i) < 65 or ord(i) > 90:
                raise InvalidNFAException(
                    f"States symbols must be between A and Z, found {i}"
                )

    def _validateStartState(self, startState: str, states: set):
        # There must be a start state
        if startState == "":
            raise InvalidNFAException("The start state must be non-empty.")
        # The start state must be in Q
        elif startState not in states:
            raise InvalidNFAException("The start state is not in the set of states")

    def _validateInputAlphabet(self, inputAlphabet: set):
        for i in inputAlphabet:
            # The empty string isnt allowed in an NFA's alphabet
            if i == self.emptyString:
                raise InvalidNFAException(
                    "The empty string is not allowed as an input symbol"
                )
            # Each input symbol must be 1 character, in the range 0 to 9
            elif len(i) != 1:
                raise InvalidNFAException("Input symbol must be only 1 character")
            elif ord(i) < 48 or ord(i) > 57:
                raise InvalidNFAException(
                    f"Input symbols must be between 0 and 9, found {i}"
                )

    # The set of final states must be a subset of Q
    def _validateFinalStates(self, finalStates: set, states: set):
        # Take set difference; any values that arnt in the states
        # but appear in the final states will be left, which
        # indicates that some state(s)
        badStates: set = finalStates - states
        if len(badStates) > 0:
            sortedBadStates: list = sorted(badStates)
            excStr: str = ", ".join(sortedBadStates)
            raise InvalidNFAException("Found final states not in Q: {" + excStr + "}")

    # Build the dictionary from the list of tuples
    def _buildTransitionDictionary(self, transitions: list) -> dict:
        transitionsDict: dict = dict()
        for source, symbol, dest in transitions:
            tmpKey: tuple = (source, symbol)
            if tmpKey in transitionsDict:
                transitionsDict[tmpKey].add(dest)
            else:
                transitionsDict[tmpKey] = {dest}
        return transitionsDict

    def _validateTransitionMembership(
        self, transitionDict: dict, inputAlphabet: set, states: set
    ):
        for (source, symbol), dest in transitionDict.items():
            # If the transition symbol is not in the input alphabet, then we
            # reject
            if symbol not in inputAlphabet and symbol != self.emptyString:
                raise InvalidNFAException(
                    f"Symbol '{symbol}' not in input alphabet, but found in transition"
                    + f" from {source} on {symbol}"
                )
            # If the source state for a transition is not in Q, then we must reject
            if source not in states:
                raise InvalidNFAException(
                    f"State {source} not in Q, but found in transition"
                    + f" from {source} on {symbol}"
                )
            # If the set of destination states for a transition is not in Q, then we must reject
            potentialBadStates: set = dest - states
            if len(potentialBadStates) > 0:
                badStatesStr: str = ", ".join(potentialBadStates)
                raise InvalidNFAException(
                    f"State {badStatesStr} not in Q, but found in transition"
                    + f" from {source} on {symbol}"
                )
