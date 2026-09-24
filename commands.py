class Command:
    def __init__(self, name, default_assignment="ans"):
        self.name = name
        self.default_assignment = default_assignment
        self.uses_ans = False

    def validate(self, args, assignment, state):
        raise NotImplementedError

    def execute(self, args):
        raise NotImplementedError

class ArithmeticCommand(Command):
    def __init__(self, name, default_assignment="ans"):
        super().__init__(name, default_assignment)
        self.uses_ans = True

    def validate(self, args, assignment, state):
        return ((state.has_ans() and len(args) >= 1) or (not state.has_ans() and len(args) >= 2))

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


class Clear(Command):
    def __init__(self):
        super().__init__("clear")

    def validate(self, args, assignment, state):
        return not args and assignment == "ans"

    def execute(self, args):
        return None

class Set(Command):
    def __init__(self):
        super().__init__("set")

    def validate(self, args, assignment, state):
        return len(args) == 1 and assignment == "ans"

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

