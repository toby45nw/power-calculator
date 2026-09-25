class CalculatorState:
    def __init__(self):
        self.variables = {}
        self.ans = None

    def set_variable(self, name, value):
        self.variables[name] = value 

    def remove_variable(self, name):
        if name in self.variables:
            del self.variables[name]

    def clear_variables(self):
        self.variables = {}

    def has_variable(self, name):
        return name in self.variables

    def get_variable(self, name):
        return self.variables.get(name)

    def get_variables(self):
        return self.variables.copy()

    def set_ans(self, value):
        self.ans = value

    def has_ans(self):
        return self.ans is not None

    def get_ans(self):
        return self.ans

    def clear_ans(self):
        self.ans = None