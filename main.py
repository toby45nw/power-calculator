from calculatorState import CalculatorState
from powerParser import PowerParser
from powerCommand import PowerCommand
from tokeniser import Tokeniser

def run_calculator():
    run = True

    tokeniser = Tokeniser()
    state = CalculatorState()


    state.set_variable("x", 5)
    print(state.get_variables())


    parser = PowerParser(state)

    while run == True:
        line = input("What would you like to enter? ")

        # Empty line
        if not line.strip():
            continue

        # Exit condition
        if line == "exit":
            break

        #Tokenise the line
        tokens = tokeniser.tokenise(line)

        try:
            command = parser.parse(tokens)

        except ValueError:
            print("Your Command is invalid")
            continue

        command.printCommand()

if __name__ == "__main__":
    run_calculator()