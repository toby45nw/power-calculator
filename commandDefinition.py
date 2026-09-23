class CommandDefinition:
    def __init__(self, name, validator):
        self.name = name
        self.validator = validator
        # self.operation = operation

    def validate(self, args, assignment, state):
        return self.validator(args, assignment, state)

    def execute(self, args, assignment, state):
        return self.operation(args, assignment, state)

def validate_arithmetic(args, assignment, state):
    if state.has_ans() and len(args) >= 1:
        return True

    if not state.has_ans() and len(args) >= 2:
        return True

    return False

def validate_only_command(args, assignment, state):
    if args or assignment:
        return False

    return True

def validate_set(args, assignment, state):
    if len(args) == 1 and assignment:
        return True


add = CommandDefinition("add", validate_arithmetic)
subtract = CommandDefinition("subtract", validate_arithmetic)
multiply = CommandDefinition("multiply", validate_arithmetic)
divide = CommandDefinition("divide", validate_arithmetic)

clear = CommandDefinition("clear", validate_only_command)
vars = CommandDefinition("vars", validate_only_command)
set = CommandDefinition("set", validate_set)


