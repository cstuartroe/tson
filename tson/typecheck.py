from typing import Dict
from .token import Token
from .types import (
    TSONType,
    TSONNumber,
    TSONString,
    TSONBoolean,
    TSONNull,
    TSONUndefined,
    TSONArrayType,
    TSONObjectType,
    cleverUnion,
)
from .evaluate import evaluate_tson, null, undefined

STANDARD_TYPES = {
    "number": TSONNumber,
    "string": TSONString,
    "boolean": TSONBoolean,
    "null": TSONNull,
    "undefined": TSONUndefined,
}

TOKEN_TYPES = {
    Token.NUMBER: TSONNumber,
    Token.STRING: TSONString,
    Token.BOOL: TSONBoolean,
    "null": TSONNull,
    "undefined": TSONUndefined,
}


class TypeChecker:
    def __init__(self):
        self.type_names = {**STANDARD_TYPES}
        self.symbol_table: Dict[str, TSONType] = {}

    def declare(self, label: str, ttype: TSONType):
        self.symbol_table[label] = ttype

    def check(self, value) -> TSONType:
        if value is null:
            return TSONNull

        elif value is undefined:
            return TSONUndefined

        elif type(value) in {int, float}:
            return TSONNumber

        elif type(value) is str:
            return TSONString

        elif type(value) is bool:
            return TSONBoolean

        elif type(value) is list:
            return TSONArrayType(etype=cleverUnion(*[self.check(e) for e in value]))

        elif type(value) is dict:
            items: Dict[str, TSONType] = {}
            for k, v in value.items():
                items[k] = self.check(v)

            return TSONObjectType(items=items)

        else:
            raise ValueError(f"Invalid TSON expression: {value}")
