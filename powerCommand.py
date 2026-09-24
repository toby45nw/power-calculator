from powerResult import Result

class PowerCommand:

    def __init__(self, command, arguments, assignmentTarget):
        self.command = command
        self.arguments = arguments
        self.assignmentTarget = assignmentTarget

    def __repr__(self):
        return f"{self.command.name} {self.arguments} {self.assignmentTarget}"

    def resolve_args(self, state):
        resolved_args = []

        if self.command.uses_ans and state.has_ans():
            resolved_args.append(state.get_ans())

        for arg in self.arguments:
            if state.has_variable(arg):
                resolved_args.append(state.get_variable(arg))
            else:
                resolved_args.append(float(arg))

        return resolved_args

    def execute(self, state):

        if self.command.name == "vars":
            return Result(message=str(state.get_variables()))

        resolved_args = self.resolve_args(state)
        result = self.command.execute(resolved_args)

        if self.command.name == "clear":
            state.set_ans(result)
            return Result(message="ans cleared")

        if self.assignmentTarget == "ans":
            state.set_ans(result)
            return Result(value=result, target="ans")

        state.set_variable(name=self.assignmentTarget, value=result)
        return Result(value=result, target=self.assignmentTarget)
        

