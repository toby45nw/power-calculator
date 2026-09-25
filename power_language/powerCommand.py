from result import Result

# Holds the power command and the logic to execute the command
class PowerCommand:

    def __init__(self, command, arguments, assignmentTarget):
        self.command = command
        self.arguments = arguments
        self.assignmentTarget = assignmentTarget

    def __repr__(self):
        return f"{self.command.name} {self.arguments} {self.assignmentTarget}"

    # Resolve the arguments in the command
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

    # Run the command
    def execute(self, state):

        # Special vars case
        if self.command.name == "vars":
            return Result(message=str(state.get_variables()))

        # Get the resolved arguments
        resolved_args = self.resolve_args(state)
        # execute the command
        result = self.command.execute(resolved_args)

        # Deal with the clear and ans case
        if self.command.name == "clear":
            state.set_ans(result)
            return Result(message="ans cleared")

        if self.assignmentTarget == "ans":
            state.set_ans(result)
            return Result(value=result, target="ans")

        # update state, return the result
        state.set_variable(name=self.assignmentTarget, value=result)
        return Result(value=result, target=self.assignmentTarget)
        

