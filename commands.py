class Command:
    def __init__(self, name):
        self.name = name

    def validate(self, args, assignment, state):
        raise NotImplementedError


class ArithmeticCommand(Command):
    def validate(self, args, assignment, state):
        return ((state.has_ans() and len(args) >= 1) or (not state.has_ans() and len(args) >= 2))

class Add(ArithmeticCommand):
    def __init__(self):
        super().__init__("add")

class Subtract(ArithmeticCommand):
    def __init__(self):
        super().__init__("subtract")

class Multiply(ArithmeticCommand):
    def __init__(self):
        super().__init__("multiply")

class Divide(ArithmeticCommand):
    def __init__(self):
        super().__init__("divide")


class Clear(Command):
    def __init__(self):
        super().__init__("clear")

    def validate(self, args, assignment, state):
        return not args and not assignment

class Vars(Command):
    def __init__(self):
        super().__init__("vars")

    def validate(self, args, assignment, state):
        return not args and not assignment

class Set(Command):
    def __init__(self):
        super().__init__("set")

    def validate(self, args, assignment, state):
        return len(args) == 1 and assignment


class Assign(Command):
    def __init__(self):
            super().__init__("assign")

