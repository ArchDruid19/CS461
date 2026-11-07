# Small class that inherits Exception because
# using just Exception in a try except block
# for DFA errors might catch errors we don't want to
# catch
class InvalidDFAException(Exception):
    pass


class DFA:
    emptyString: str = "eps"

    def __init__(
        self,
        states: set,
        inputAlphabet: set,
        transitionFunc: dict,
        startState: str,
        finalState: set,
    ):
        self.validateStates(states)
        self.validateInputAlphabet(inputAlphabet)
        self.validateStartState(startState, states)
        self.validateFinalStates(finalState, states)

        transitionDict: dict = self.buildTransitionDictionary(transitionFunc)
        print(transitionDict)

        self.states = states
        self.inputAlphabet = inputAlphabet
        self.transitionFunc = transitionDict
        self.startState = startState
        self.finalState = finalState

    def validateStates(self, states: set):
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

    def validateStartState(self, startState: str, states: set):
        # There must be a start state
        if startState == "":
            raise InvalidDFAException("The start state must be non-empty.")
        # The start state must be in Q
        elif startState not in states:
            raise InvalidDFAException("The start state is not in the set of states")

    def validateInputAlphabet(self, inputAlphabet: set):
        for i in inputAlphabet:
            # If the empty string is present in the alphabet, then we reject
            # as that is not allowed in a DFA
            if i == self.emptyString:
                raise InvalidDFAException(
                    "The empty string is not allowed as an input symbol"
                )
            # Each input symbol must be 1 character, in the range 0 to 9
            elif len(i) > 1:
                raise InvalidDFAException("Input symbol must be only 1 character")
            elif ord(i) < 48 or ord(i) > 57:
                raise InvalidDFAException(
                    f"Input symbols must be between 0 and 9, found {i}"
                )

    # The set of final states must be a subset of Q, and the empty
    # set is allowed for DFA's that accept just the empty string
    def validateFinalStates(self, finalStates: set, states: set):
        badStates: set = finalStates - states
        if len(badStates) > 0:
            sortedBadStates: list = sorted(badStates)
            excStr: str = ", ".join(sortedBadStates)
            raise InvalidDFAException("Found states not in Q: {" + excStr + "}")

    # The transition function from the parser is passed in as a list of
    # tuples.
    # This function builds a dictionary from those tuples, in the form
    # (start_state, symbol): destination_state.
    # Every start state and symbol pair must be unique: if we have 2
    # pairs that contain the same start state, symbol, and destination, then
    # this is a duplicate transition which cannot exist in a DFA.
    # If we find the same duplicate pairs but they go to differant destinations,
    # then this implies nondeterminism which cannot exist in a DFA
    def buildTransitionDictionary(self, transitions: list) -> dict:
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

    def printDFA(self):
        print(f"Q = {self.states}")
        print(f"Sigma = {self.inputAlphabet}")
        print(f"Delta = {self.transitionFunc}")
        print(f"Q0 = {self.startState}")
        print(f"F = {self.finalState}")
