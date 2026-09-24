class PowerCommand:

    def __init__(self, command, arguments, assignmentTarget):
        self.command = command
        self.arguments = arguments
        self.assignmentTarget = assignmentTarget

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
    
    def print_command(self):
        print(self.command.name, self.arguments, self.assignmentTarget)

    def execute(self, state):

        if self.command.name == "vars":
            print(state.get_variables())
            return

        resolved_args = self.resolve_args(state)
        result = self.command.execute(resolved_args)

        if self.command.name == "clear":
            state.set_ans(result)
            print("ans cleared")
            return

        if self.assignmentTarget == "ans":
            state.set_ans(result)
            print(state.get_ans())
            return

        state.set_variable(name=self.assignmentTarget, value=result)
        

