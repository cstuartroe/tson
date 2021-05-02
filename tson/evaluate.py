from .token import Token
from .ast import (
    ExpressionNode,
    SimpleNode,
    ArrayNode,
    ObjectNode,
)


class _Null:
    def __repr__(self):
        return "tson.null"


null = _Null()


class _Undefined:
    def __repr__(self):
        return "tson.undefined"


undefined = _Undefined


def evaluate_tson(expression: ExpressionNode, symbol_table):
    if isinstance(expression, SimpleNode):
        if expression.token.ttype == Token.LABEL:
            if expression.token.value not in symbol_table:
                expression.token.raise_error("Label unassigned")

            return symbol_table[expression.token.value]

        elif expression.token.ttype == "null":
            return null
        elif expression.token.ttype == "undefined":
            return undefined

        else:
            return expression.token.value

    elif isinstance(expression, ArrayNode):
        return [evaluate_tson(e, symbol_table) for e in expression.elements]

    elif isinstance(expression, ObjectNode):
        obj = {}
        for k, v in expression.items.items():
            obj[k.value] = evaluate_tson(v, symbol_table)
        return obj

    else:
        raise ValueError(f"Unknown expression type: {type(expression)}")
