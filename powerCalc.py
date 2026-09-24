from calculatorState import CalculatorState
from powerParser import PowerParser
from tokeniser import Tokeniser
from powerResult import Result

class PowerCalc:
    def __init__(self):
        self.state = CalculatorState()
        self.tokeniser = Tokeniser()
        self.parser = PowerParser(self.state)

    def execute(self, line):
        if not line.strip():
            return Result()

        tokens = self.tokeniser.tokenise(line)
        try:
            command = self.parser.parse(tokens)
            return command.execute(self.state)
        except ValueError:
            return Result(error="Your Command is invalid")
        except ZeroDivisionError:
            return Result(error="Cannot divide by zero")