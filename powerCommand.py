class PowerCommand:

    def __init__(self, command, arguments, assignmentTarget):
        self.command = command
        self.arguments = arguments
        self.assignmentTarget = assignmentTarget

    def resolve_args(self, state):
        resolved_args = []

        if state.has_ans():
            resolved_args.append(state.get_ans())

        for arg in self.arguments:
            if state.has_variable(arg):
                resolved_args.append(state.get_variable(arg))

            else:
                resolved_args.append(float(arg))

        return resolved_args
    
    def printCommand(self):
        print(self.command.name, self.arguments, self.assignmentTarget)

    def execute(self, state):
        resolved_args = self.resolve_args(state)
        print(self.arguments)
        print(resolved_args)
        

