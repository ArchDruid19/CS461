# Read a 5-tuple (Q, Sigma, delta, q0, F).
# Check that Q is nonempty,
# q0 belongs to Q,
# and F is a subset of Q.
# Transition sources and destinations must be declared states,
# and labels must be input symbols or epsilon.
# Zero, one, or multiple destinations are allowed for each state/label pair.
# Document how omitted transitions represent an empty destination set.


# Small class that inherits Exception because
# using just Exception in a try except block
# for DFA errors might catch errors we don't want to
# catch
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

        self.validateStates(states)
        self.validateInputAlphabet(inputAlphabet)
        self.validateStartState(startState, states)
        self.validateFinalStates(finalStates, states)

        transitionDict: dict = self.buildTransitionDictionary(transitionList)
        self.validateTransitionMembership(transitionDict, inputAlphabet, states)

        self.states = states
        self.inputAlphabet = inputAlphabet
        self.transitionFunc = transitionDict
        self.startState = startState
        self.finalState = finalStates

    def validateStates(self, states: set):
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

    def validateStartState(self, startState: str, states: set):
        # There must be a start state
        if startState == "":
            raise InvalidNFAException("The start state must be non-empty.")
        # The start state must be in Q
        elif startState not in states:
            raise InvalidNFAException("The start state is not in the set of states")

    def validateInputAlphabet(self, inputAlphabet: set):
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
    def validateFinalStates(self, finalStates: set, states: set):
        # Take set difference; any values that arnt in the states
        # but appear in the final states will be left, which 
        # indicates that some state(s)
        badStates: set = finalStates - states
        if len(badStates) > 0:
            sortedBadStates: list = sorted(badStates)
            excStr: str = ", ".join(sortedBadStates)
            raise InvalidNFAException("Found final states not in Q: {" + excStr + "}")

    # Build the dictionary from the list of tuples
    def buildTransitionDictionary(self, transitions: list) -> dict:
        transitionsDict: dict = dict()
        for source, symbol, dest in transitions:
            tmpKey: tuple = (source, symbol)
            if tmpKey in transitionsDict:
                transitionsDict[tmpKey].add(dest)
            else:
                transitionsDict[tmpKey] = set(dest)
        return transitionsDict

    def validateTransitionMembership(
        self, transitionDict: dict, inputAlphabet: set, states: set
    ):
        for (source, symbol), dest in transitionDict.items():
            tmpTransitionStr: str = f"({source}, {symbol}, {"".join(dest)})"
            # If the transition symbol is not in the input alphabet, then we
            # reject
            if symbol not in inputAlphabet and symbol != self.emptyString:
                raise InvalidNFAException(
                    f"Symbol '{symbol}' not in input alphabet, but found in transition"
                    + f" {tmpTransitionStr}"
                )
            # If the source state for a transition is not in Q, then we must reject
            if source not in states:
                raise InvalidNFAException(
                    f"State {source} not in Q, but found in transition"
                    + f" {tmpTransitionStr}"
                )
            # If the destination state for a transitions is not in Q, then we must reject
            potentialBadStates: set = dest - states
            if len(potentialBadStates) > 0:
                raise InvalidNFAException(
                    f"State {"".join(potentialBadStates)} not in Q, but found in transition"
                    + f" {tmpTransitionStr}"
                )

    def printNFA(self):
        print(f"Q = {self.states}")
        print(f"Sigma = {self.inputAlphabet}")
        print(f"Delta = {self.transitionFunc}")
        print(f"Q0 = {self.startState}")
        print(f"F = {self.finalState}")
