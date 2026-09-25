from power_language.powerToken import TokenType
from power_language.powerCommand import PowerCommand
from power_language.commands import Add, Subtract, Multiply, Divide, Set, Clear, Vars, Assign

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

    # Validate the arguments in a command; if the args is a number or a variable (NAME) its valid
    def is_valid_argument(self, token):
        if token.type == TokenType.NUMBER:
            return True

        if token.type == TokenType.NAME:
            return self.state.has_variable(token.value)

        return False

    # Validate the command; Calls the validate function of the command object
    # The command object holds its own validation logic
    def validate_command(self, command, args, assignment):
        if not command.validate(args, assignment, self.state):
            raise ValueError("Invalid command")

    # Parse the tokens
    def parse(self, tokens):

        # print(tokens)
        command = self.valid_commands[tokens[0].value]
        args, assignment = command.resolve_shape(tokens[1:], self.state)

        print("args:", args, "assignment:", assignment)

        return PowerCommand(command, args, assignment)


        # # Shorthand method to set the state
        # if (len(tokens) == 2) and (tokens[0].type == TokenType.NUMBER) and (tokens[1].type == TokenType.NAME):
        #     return PowerCommand(self.valid_commands["assign"], [tokens[0].value], tokens[1].value)

        # # Valid command and an assgined variable (variable doesnt have a saved value)
        # # Return the power comman with the command, args, and assginment
        # if (tokens[0].type == TokenType.WORD and tokens[0].value in self.valid_commands) and (tokens[-1].type == TokenType.NAME and not self.state.has_variable(tokens[-1].value)):
        #     for token in tokens[1:-1]:
        #         if not self.is_valid_argument(token):
        #             raise ValueError("Invalid arguments")

        #     command = self.valid_commands[tokens[0].value]
        #     args = [token.value for token in tokens[1:-1]]
        #     assignment = tokens[-1].value

        #     self.validate_command(command, args, assignment)

        #     return PowerCommand(command, args, assignment)

        # # Valid command but no assignemnt targer (the assignemnt targer is dealt with in the previous if so only need to check for valid command word and valid args now)
        # # Return the command with the command, args, and default loaction for that command
        # if (tokens[0].type == TokenType.WORD and tokens[0].value in self.valid_commands):
        #     for token in tokens[1:]:
        #         if not self.is_valid_argument(token):
        #             raise ValueError("Invalid argument")

        #     command = self.valid_commands[tokens[0].value]
        #     args = [token.value for token in tokens[1:]]
        #     assignment = command.default_assignment

        #     self.validate_command(command, args, assignment)

        #     return PowerCommand(command, args, assignment)

        # raise ValueError("Invalid power command")
        



