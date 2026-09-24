from powerToken import TokenType, Token
import re

NUMBER_PATTERN = re.compile(r"-?(\d+\.?\d*|\.\d+)")

class Tokeniser:

    def tokenise(self, line):
        tokens = []
        elements = line.split()

        for element in elements:
            tokens.append(Token(self.classify(element), element))

        return tokens
        

    def classify(self, element):
        if NUMBER_PATTERN.fullmatch(element):
            return TokenType.NUMBER

        if element == "ans":
            return TokenType.ANS

        if len(element) == 1 and element.isalpha():
            return TokenType.NAME

        if element in {"+", "-", "*", "/"}:
            return TokenType.OPERATOR

        return TokenType.WORD
            