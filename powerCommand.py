class PowerCommand:

    def __init__(self, command, arguments, assignmentTarget = "ans"):
        self.command = command
        self.arguments = arguments
        self.assignmentTarget = assignmentTarget

    def printCommand(self):
        print(self.command.name, self.arguments, self.assignmentTarget)