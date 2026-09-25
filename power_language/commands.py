from power_language.powerToken import TokenType

# Define the commands and logic to validate and execute, and where to save the result
class Command:
    def __init__(self, name, default_assignment="ans"):
        self.name = name
        self.default_assignment = default_assignment
        self.uses_ans = False

    def resolve_shape(self, tokens, state):

        if (tokens[-1].type == TokenType.NAME and not state.has_variable(tokens[-1].value)):
            assignment = tokens[-1].value
            token_arguments = [token for token in tokens[:-1]]

        else:
            assignment = self.default_assignment
            token_arguments = [token for token in tokens[:]]

        return token_arguments, assignment


    # def validate(self, args, assignment, state):
    #     raise NotImplementedError

    def execute(self, args):
        raise NotImplementedError

class ArithmeticCommand(Command):
    def __init__(self, name, default_assignment="ans"):
        super().__init__(name, default_assignment)
        self.uses_ans = True

    def is_valid_argument(self, token, state):
        if token.type == TokenType.NUMBER:
            return True

        if token.type == TokenType.NAME:
            return state.has_variable(token.value)

        return False

    def resolve_shape(self, tokens, state):
        token_arguments, assignment = super().resolve_shape(tokens, state)

        if state.has_ans():
            minimum = 1
        else:
            minimum = 2

        if len(token_arguments) < minimum:
            raise ValueError("Invalid number of arguments")

        for token in token_arguments:
            if not self.is_valid_argument(token, state):
                raise ValueError("Invalid argument")

        arguments = [token.value for token in token_arguments]

        return arguments, assignment



    # def validate(self, args, assignment, state):
    #     return ((state.has_ans() and len(args) >= 1) or (not state.has_ans() and len(args) >= 2))

    

class Add(ArithmeticCommand):
    def __init__(self):
        super().__init__("add")

    def execute(self, args):
        result = args[0]

        for arg in args[1:]:
            result += arg

        return result

class Subtract(ArithmeticCommand):
    def __init__(self):
        super().__init__("subtract")

    def execute(self, args):
        result = args[0]

        for arg in args[1:]:
            result -= arg

        return result

class Multiply(ArithmeticCommand):
    def __init__(self):
        super().__init__("multiply")

    def execute(self, args):
        result = args[0]

        for arg in args[1:]:
            result *= arg

        return result

class Divide(ArithmeticCommand):
    def __init__(self):
        super().__init__("divide")

    def execute(self, args):
        result = args[0]

        for arg in args[1:]:
            result /= arg

        return result




####### Work here next!!!!
####### Update clear to validate shape and then vars and then how they execute and how powercommand handles them.
####### Power command doesnt need to valdiate arguments anymore as its done in shape validaation!!!!

class Clear(Command):
    def __init__(self):
        super().__init__("clear")

    def validate(self, args, assignment, state):
        print(args, assignment)
        return not args and assignment == "ans"

    def execute(self, args):
        return None

class Set(Command):
    def __init__(self):
        super().__init__("set")

    def resolve_shape(self, tokens, state):

        if len(tokens) > 1 or not tokens[0].type == TokenType.NUMBER:
            raise ValueError("Invalid argument")

        argument = [token.value for token in tokens]
        return(argument, self.default_assignment)

    # def validate(self, args, assignment, state):
    #     return len(args) == 1 and assignment == "ans"

    def execute(self, args):
        return args[0]

class Vars(Command):
    def __init__(self):
        super().__init__("vars", None)

    def validate(self, args, assignment, state):
        return not args and not assignment

class Assign(Command):
    def __init__(self):
            super().__init__("assign")

    def execute(self, args):
        return args[0]

