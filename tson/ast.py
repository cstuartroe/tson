from typing import List, Dict
from .token import Token


class Node:
    def __init__(self, token: Token):
        self.token = token


class ExpressionNode(Node):
    pass


class SimpleNode(ExpressionNode):
    def __init__(self, token: Token):
        super().__init__(token)

    def __hash__(self):
        return hash(self.token.value)


class ArrayNode(ExpressionNode):
    def __init__(self, openbr: Token, elements: List[ExpressionNode]):
        super().__init__(openbr)
        self.elements = elements


class ObjectNode(ExpressionNode):
    def __init__(self, openbr: Token, items: Dict[Token, ExpressionNode]):
        super().__init__(openbr)
        self.items = items


class StatementNode(Node):
    pass


class AssignmentNode(StatementNode):
    def __init__(self, declarer: Token, label: Token, value: ExpressionNode):
        super().__init__(declarer)
        self.stype = declarer.value
        self.label = label
        self.value = value
