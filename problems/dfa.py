class DFA:
    def __init__(
            self, 
            states: set, 
            inputAlphabet: set,
            transitionFunc: set,
            startState: str,
            finalState: set
            ):
        self.states = states
        self.inputAlphabet = inputAlphabet
        self.transitionFunc = transitionFunc
        self.startState = startState
        self.finalState = finalState
        pass
