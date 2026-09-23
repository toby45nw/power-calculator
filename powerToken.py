from dataclasses import dataclass
from enum import Enum, auto

class TokenType(Enum):
    NUMBER = auto()
    NAME = auto()
    ANS = auto()
    WORD = auto()
    OPERATOR = auto()

@dataclass
class Token:
    type: TokenType
    value: str