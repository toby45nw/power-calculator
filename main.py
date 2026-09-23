from calculatorState import CalculatorState
from powerParser import PowerParser
from powerCommand import PowerCommand
from tokeniser import Tokeniser

def run_calculator():
    run = True

    tokeniser = Tokeniser()
    state = CalculatorState()
    parser = PowerParser(state)

    state.set_variable("x", float(5))
    print(state.get_variables())

    while run == True:
        line = input("What would you like to enter? ")

        # Empty line
        if not line.strip():
            continue

        # Exit condition
        if line == "exit":
            break

        # Tokenise the line
        tokens = tokeniser.tokenise(line)

        # Try to parse the line
        try:
            command = parser.parse(tokens)

        # Except a value error
        except ValueError:
            print("Your Command is invalid")
            continue

        command.execute(state=state)

        # Execute

if __name__ == "__main__":
    run_calculator()