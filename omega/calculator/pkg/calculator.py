import re

class Calculator:
    def __init__(self):
        self.output = []
        self.operators = []
        self.precedence = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
            "(": 0,
        }

    def _shunt_operators(self, operator):
        while (self.operators and
               self.operators[-1] != "(" and
               self.precedence.get(operator, 0) <= self.precedence.get(self.operators[-1], 0)):
            self.output.append(self.operators.pop())
        self.operators.append(operator)

    def evaluate(self, expression):
        self.output = []
        self.operators = []
        
        # Add spaces around operators and parentheses for easier tokenization
        expression = re.sub(r'([+\-*/()])', r' \1 ', expression)
        tokens = expression.split()

        for token in tokens:
            if re.match(r'^-?\d+(\.\d+)?$', token):  # Handle numbers (integers and floats, including negative)
                self.output.append(float(token))
            elif token == "(":
                self.operators.append(token)
            elif token == ")":
                while self.operators and self.operators[-1] != "(":
                    self.output.append(self.operators.pop())
                if self.operators and self.operators[-1] == "(":
                    self.operators.pop() # Pop the "("
                else:
                    return "Error: Mismatched parentheses"
            elif token in self.precedence:
                self._shunt_operators(token)
            else:
                return "Error: Invalid token"

        while self.operators:
            if self.operators[-1] == "(":
                return "Error: Mismatched parentheses"
            self.output.append(self.operators.pop())
        
        return self._evaluate_rpn()

    def _evaluate_rpn(self):
        stack = []
        for token in self.output:
            if isinstance(token, float):
                stack.append(token)
            else:
                operator = token
                if len(stack) < 2:
                    return "Error: Invalid RPN expression"
                b = stack.pop()
                a = stack.pop()
                if operator == "+":
                    stack.append(a + b)
                elif operator == "-":
                    stack.append(a - b)
                elif operator == "*":
                    stack.append(a * b)
                elif operator == "/":
                    if b == 0:
                        return "Error: Division by zero"
                    stack.append(a / b)
        if len(stack) != 1:
            return "Error: Invalid RPN expression"
        return stack[0]
