from calculatorState import CalculatorState
from powerParser import PowerParser
from tokeniser import Tokeniser
from powerResult import Result


# Assembled all the power calculator parts into the calculator
# Holds: state, tokeniser, parser and the history
class PowerCalc:
    def __init__(self):
        self.state = CalculatorState()
        self.tokeniser = Tokeniser()
        self.parser = PowerParser(self.state)
        self.history = []

    def execute(self, line):
        # If the line is empty return an empty result object and the calculator will just move to the next line
        if not line.strip():
            return Result()

        # tokenise the line
        # Try to parse the command line; return a powercommand object with the command loaded in
        # Try to execute the command; execute on the object with the loaded command
        # Except errors
        # Append the result to history
        # Resturn the result for the for the wrapper to display
        tokens = self.tokeniser.tokenise(line)
        try:
            command = self.parser.parse(tokens)
            result = command.execute(self.state)
        except ValueError:
            result = Result(error="Your Command is invalid")
        except ZeroDivisionError:
            result = Result(error="Cannot divide by zero")

        self.history.append((line.strip(), result))
        return result