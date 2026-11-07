def doStringPreValidation(userInput: str) -> bool:
    # Check the input string has matching braces
    # with a stack and index location
    inputStack: list = list()

    for i in range(0, len(userInput)):
        if userInput[i] == "{" or userInput[i] == "(":
            inputStack.append((userInput[i], i))
        elif userInput[i] == "}":
            if inputStack:
                if inputStack[-1][0] == "{":
                    inputStack.pop()
                else:
                    print(f"ERROR: expected ) closure at {i}")
                    printError(userInput, i)
                    return False
            else:
                print(f"ERROR: Unexpected }} closure")
                printError(userInput, i)
                return False
        elif userInput[i] == ")":
            if inputStack:
                if inputStack[-1][0] == "(":
                    inputStack.pop()
                else:
                    print(f"ERROR: expected }} closure at {i}")
                    printError(userInput, i)
                    return False
            else:
                print(f"ERROR: Unexpected ) closure")
                printError(userInput, i)
                return False

    if len(inputStack) > 0:
        print(f"ERROR: unclosed {inputStack[-1][0]} at {i}")
        printError(userInput, i + 1)
        return False

    return True

def printError(orgStr: str, failPoint: int):
    print(orgStr)
    failStr: str = ""
    for i in range(0, failPoint):
        failStr += " "
    failStr += "^"
    print(failStr)
