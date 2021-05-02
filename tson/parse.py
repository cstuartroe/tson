from .ast import *

SIMPLE_TTYPES = {
    Token.LABEL,
    Token.NUMBER,
    Token.BOOL,
    Token.STRING,
    "null",
    "undefined",
}


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.assignments: List[AssignmentNode] = []

    def eof(self):
        return self.i == len(self.tokens)

    def next(self):
        return self.tokens[self.i]

    def expect(self, ttype):
        t = self.next()
        if t.ttype is not ttype:
            t.raise_error(f"Expected {ttype}")
        self.i += 1
        return t

    def parse(self):
        self.i = 0
        while not self.eof():
            self.assignments.append(self.grab_assignment())

    def grab_assignment(self):
        declarer = self.expect(Token.DECLARER)
        label = self.expect(Token.LABEL)
        self.expect('=')
        value = self.grab_expression()
        self.expect(';')

        return AssignmentNode(
            declarer=declarer,
            label=label,
            value=value,
        )

    def grab_expression(self):
        t = self.next()

        if t.ttype in SIMPLE_TTYPES:
            self.i += 1
            return SimpleNode(t)

        elif t.ttype == '{':
            return self.grab_object()

        elif t.ttype == '[':
            return self.grab_array()

        else:
            t.raise_error("Invalid start to expression")

    def grab_sequence(self, grabber, terminator):
        while True:
            yield grabber()

            if self.next().ttype == ',':
                self.i += 1
                if self.next().ttype == terminator:
                    break
            else:
                break

    def grab_array(self):
        openbr = self.expect('[')

        elements = list(self.grab_sequence(self.grab_expression, ']'))

        self.expect(']')

        return ArrayNode(
            openbr=openbr,
            elements=list(elements),
        )

    def grab_object(self):
        openbr = self.expect('{')

        items: Dict[Token, ExpressionNode] = {}

        for key, value in self.grab_sequence(self.grab_kv, '}'):
            if key in items:
                key.raise_error("Key already set")
            else:
                items[key.token] = value

        self.expect('}')

        return ObjectNode(
            openbr=openbr,
            items=items,
        )

    def grab_kv(self) -> (SimpleNode, ExpressionNode):
        key = self.grab_expression()
        if not isinstance(key, SimpleNode) or key.token.ttype not in {Token.LABEL, Token.STRING}:
            key.token.raise_error("Invalid object key")

        self.expect(':')

        value = self.grab_expression()

        return key, value
