from .token import Tokenizer
from .parse import Parser
from .types import (
    TSONNull,
    TSONUndefined,
    TSONBoolean,
    TSONString,
    TSONNumber,
    TSONAny,
    TSONUnknown,
    TSONArrayType,
    TSONObjectType,
    TSONUnionType,
    cleverUnion,
)
from .evaluate import null, undefined
from .typecheck import TypeChecker
from .module import TSONModule


def loads_as_module(s):
    lines = s.split("\n")
    tokens = list(Tokenizer(lines).tokens())
    p = Parser(tokens)
    p.parse()
    m = TSONModule(p.assignments)
    m.evaluate()
    return m


def loads(s):
    return loads_as_module(s).get_default_export()


def load_as_module(fp):
    return loads_as_module(fp.read())


def load(fp):
    return load_as_module(fp).get_default_export()


__version__ = "0.0.0"
