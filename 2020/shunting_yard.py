from collections import deque

class Calculator:
    ops = {
        "+":lambda x, y:x + y,
        "*":lambda x, y:x * y,
    }

    precedence = (
        ("+", "*"),
    )

    def _prec(self, op, _cache={}):
        if op in _cache:
            return _cache[op]

        for i, level in enumerate(self.precedence, start=1):
            if op in level:
                _cache[op] = i
                return i

        _cache[op] = 0
        return 0

    def evaluate(self, my_string):
            ops = self.ops
            # Add spaces around parens
            my_string = "".join(f' {i} ' if i in "()" else i for i in my_string)
            # tokenize
            tokens = deque(i if (i in ops or i in "()") else int(i) for i in my_string.split())
            stack = self._shunt(tokens)
            return self._eval(stack)

    def _shunt(self, tokens):
        prec, ops, stack, op_stack = self._prec, self.ops, [], []

        while tokens:
            token = tokens.popleft()
            if token in ops:
                while op_stack and prec(op_stack[-1]) >= prec(token):
                    stack.append(op_stack.pop())
                op_stack.append(token)
            elif token == "(":
                op_stack.append(token)
            elif token == ")":
                while op_stack and op_stack[-1] != "(":
                    stack.append(op_stack.pop())
                if op_stack[-1] == "(":
                    op_stack.pop()
                if op_stack and op_stack[-1] != "(":
                    stack.append(op_stack.pop())
            else:
                stack.append(token)

        stack.extend(reversed(op_stack))
        return stack

    def _eval(self, stack):
        ops = self.ops
        token = stack.pop()
        if token in ops:
            y, x = self._eval(stack), self._eval(stack)
            return ops[token](x, y)
        return token