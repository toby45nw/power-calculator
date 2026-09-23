from powerToken import TokenType
from powerCommand import PowerCommand
from commands import Add, Subtract, Multiply, Divide, Set, Clear, Vars, Assign

class PowerParser:

    valid_commands = {
        "add": Add(),
        "subtract": Subtract(),
        "multiply": Multiply(),
        "divide": Divide(),
        "set": Set(),
        "clear": Clear(),
        "vars": Vars(),
        "assign": Assign()
    }

    def __init__(self, state):
        self.state = state

    def is_valid_argument(self, token):
        if token.type == TokenType.NUMBER:
            return True

        if token.type == TokenType.ANS:
            return self.state.has_ans()

        if token.type == TokenType.NAME:
            return self.state.has_variable(token.value)

        return False

    def validate_command(self, command, args, assignment):
        if not command.validate(args, assignment, self.state):
            raise ValueError("Invalid command")


    def parse(self, tokens):

        if (len(tokens) == 2) and (tokens[0].type == TokenType.NUMBER) and (tokens[1].type == TokenType.NAME):
            return PowerCommand(self.valid_commands["assign"], tokens[0].value, tokens[1].value)

        if (tokens[0].type == TokenType.WORD and tokens[0].value in self.valid_commands) and (tokens[-1].type == TokenType.NAME and not self.state.has_variable(tokens[-1].value)):
            for token in tokens[1:-1]:
                if not self.is_valid_argument(token):
                    raise ValueError("Invalid arguments")

            command = self.valid_commands[tokens[0].value]
            args = [token.value for token in tokens[1:-1]]
            assignment = tokens[-1].value

            self.validate_command(command, args, assignment)
            
            return PowerCommand(command, args, assignment)

        if (tokens[0].type == TokenType.WORD and tokens[0].value in self.valid_commands):
            for token in tokens[1:]:
                if not self.is_valid_argument(token):
                    raise ValueError("Invalid argument")

            command = self.valid_commands[tokens[0].value]
            args = [token.value for token in tokens[1:]]
            assignment = None

            self.validate_command(command, args, assignment)
      
            return PowerCommand(command, args)

        raise ValueError("Invalid power command")
        



