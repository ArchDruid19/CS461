# Small class that inherits Exception because
# using just Exception in a try except block
# for DFA errors might catch errors we don't want to
# catch
class InvalidDFAException(Exception):
    pass


class DFAValidator:
    emptyString: str = "eps"

    def __init__(
        self,
        machinePieces: list,
    ):
        states = machinePieces[0]
        inputAlphabet = machinePieces[1]
        transitionFunc = machinePieces[2]
        startState = machinePieces[3]
        finalState = machinePieces[4]

        self._validateStates(states)
        self._validateInputAlphabet(inputAlphabet)
        self._validateStartState(startState, states)
        self._validateFinalStates(finalState, states)

        transitionDict: dict = self._buildTransitionDictionary(transitionFunc)
        self._validateTransitionMembership(transitionDict, inputAlphabet, states)
        self._validateTransitionCompleteness(transitionDict, inputAlphabet, states)

        self.states = states
        self.inputAlphabet = inputAlphabet
        self.transitionFunc = transitionDict
        self.startState = startState
        self.finalState = finalState

    def _validateStates(self, states: set):
        # We must have at least one state in Q
        if len(states) == 0:
            raise InvalidDFAException("The set of states (Q) cannot be empty")
        # As per the instructions, we can only have a max of 26 states
        elif len(states) > 26:
            raise InvalidDFAException(
                f"A maximum of 26 states are allowed, {len(states)} was found"
            )
        for i in states:
            # Each state symbol must be 1 character
            if len(i) != 1:
                raise InvalidDFAException(
                    f"State symbols must be 1 character long, found {i} of length {len(i)}"
                )
            # Each state symbol must be a character between A and Z
            elif ord(i) < 65 or ord(i) > 90:
                raise InvalidDFAException(
                    f"States symbols must be between A and Z, found {i}"
                )

    def _validateStartState(self, startState: str, states: set):
        # There must be a start state
        if startState == "":
            raise InvalidDFAException("The start state must be non-empty.")
        # The start state must be in Q
        elif startState not in states:
            raise InvalidDFAException("The start state is not in the set of states")

    def _validateInputAlphabet(self, inputAlphabet: set):
        for i in inputAlphabet:
            # If the empty string is present in the alphabet, then we reject
            # as that is not allowed in a DFA
            if i == self.emptyString:
                raise InvalidDFAException(
                    "The empty string is not allowed as an input symbol"
                )
            # Each input symbol must be 1 character, in the range 0 to 9
            elif len(i) != 1:
                raise InvalidDFAException("Input symbol must be only 1 character")
            elif ord(i) < 48 or ord(i) > 57:
                raise InvalidDFAException(
                    f"Input symbols must be between 0 and 9, found {i}"
                )

    # The set of final states must be a subset of Q, and the empty
    # set is allowed for DFA's that accept nothing
    def _validateFinalStates(self, finalStates: set, states: set):
        badStates: set = finalStates - states
        if len(badStates) > 0:
            sortedBadStates: list = sorted(badStates)
            excStr: str = ", ".join(sortedBadStates)
            raise InvalidDFAException("Found final states not in Q: {" + excStr + "}")

    # The transition function from the parser is passed in as a list of
    # tuples.
    # This function builds a dictionary from those tuples, in the form
    # (start_state, symbol): destination_state.
    # Every start state and symbol pair must be unique: if we have 2
    # pairs that contain the same start state, symbol, and destination, then
    # this is a duplicate transition which cannot exist in a DFA.
    # If we find the same duplicate pairs but they go to different destinations,
    # then this implies nondeterminism which cannot exist in a DFA
    def _buildTransitionDictionary(self, transitions: list) -> dict:
        transitionsDict: dict = dict()
        for source, symbol, dest in transitions:
            tmpKey: tuple = (source, symbol)
            if tmpKey in transitionsDict:
                if transitionsDict[tmpKey] == dest:
                    raise InvalidDFAException(
                        f"Duplicate transition ({source}, {symbol}, {dest}) found"
                    )
                else:
                    raise InvalidDFAException(
                        f"Nondeterministic transition ({source}, {symbol}, {dest}) found;"
                        + f" already have ({source}, {symbol}, {transitionsDict[tmpKey]})"
                    )
            transitionsDict[(source, symbol)] = dest
        return transitionsDict

    def _validateTransitionMembership(
        self, transitionDict: dict, inputAlphabet: set, states: set
    ):
        for (source, symbol), dest in transitionDict.items():
            tmpTransitionStr: str = f"({source}, {symbol}, {dest})"
            # If the symbol is the empty string, we must reject as that is not
            # allowed in a transition
            if symbol == self.emptyString:
                raise InvalidDFAException(
                    f"Empty string found in transition {tmpTransitionStr}"
                )
            # If the transition symbol is not in the input alphabet, then we
            # reject
            if symbol not in inputAlphabet:
                raise InvalidDFAException(
                    f"Symbol '{symbol}' not in input alphabet, but found in transition"
                    + f" {tmpTransitionStr}"
                )
            # If the source state for a transition is not in Q, then we must reject
            if source not in states:
                raise InvalidDFAException(
                    f"State {source} not in Q, but found in transition"
                    + f" {tmpTransitionStr}"
                )
            # If the destination state for a transitions is not in Q, then we must reject
            if dest not in states:
                raise InvalidDFAException(
                    f"State {dest} not in Q, but found in transition"
                    + f" {tmpTransitionStr}"
                )

    def _validateTransitionCompleteness(
        self, transitionDict: dict, inputAlphabet: set, states: set
    ):
        # The number of transitions for a DFA is |Q| * |sigma|.
        # Each state must be paired with each input symbol
        for state in states:
            for symbol in inputAlphabet:
                tmpTuple: tuple = (state, symbol)
                if tmpTuple not in transitionDict:
                    raise InvalidDFAException(
                        f"Source state {state} must have a transition for symbol {symbol}, "
                        + "but none was found"
                    )
