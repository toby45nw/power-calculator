from dataclasses import dataclass

# Result class to hold the calculator result
@dataclass
class Result:
    value: float = None     # the number, if there is one
    target: str = None      # where it was stored: "ans" or a variable name
    message: str = None     # plain info text ("ans cleared", the vars listing)
    error: str = None       # set when something went wrong