from typing import Dict, Set, List


class TSONType:
    def __init__(self, name=None):
        self.name = name

    def __eq__(self, other):
        return self.name is other.name

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(repr(self))


TSONString = TSONType("string")
TSONNumber = TSONType("number")
TSONBoolean = TSONType("boolean")
TSONNull = TSONType("null")
TSONUndefined = TSONType("undefined")
TSONAny = TSONType("any")
TSONUnknown = TSONType("unknown")


class TSONObjectType(TSONType):
    def __init__(self, items: Dict[str, TSONType]):
        super().__init__()
        self.items = items

    def __eq__(self, other):
        if not isinstance(other, TSONObjectType):
            return False

        if set(self.items.keys()) != set(other.items.keys()):
            return False

        for k, v in self.items:
            if v != other.items[k]:
                return False

        return True

    def __repr__(self):
        s = '{'
        for k, v in sorted(list(self.items.items())):
            s += k + ": " + repr(v) + ", "
        if self.items:
            s = s[:-2]
        s += '}'

        return s

    def __hash__(self):
        return hash(repr(self))


class TSONArrayType(TSONType):
    def __init__(self, etype: TSONType):
        super().__init__()
        self.etype = etype

    def __eq__(self, other):
        if not isinstance(other, TSONArrayType):
            return False

        return self.etype == other.etype

    def __repr__(self):
        return repr(self.etype) + "[]"

    def __hash__(self):
        return hash(repr(self))


class TSONUnionType(TSONType):
    def __init__(self, types: Set[TSONType]):
        super().__init__()
        self.types = types

    def __repr__(self):
        return "(" + " | ".join(sorted(map(repr, self.types))) + ")"


def cleverUnionObjects(otype1: TSONObjectType, otype2: TSONObjectType):
    items = {}
    for key in set(otype1.items.keys()) | set(otype2.items.keys()):
        items[key] = cleverUnion(
            otype1.items.get(key, TSONUndefined),
            otype2.items.get(key, TSONUndefined),
        )
    return TSONObjectType(items)


def levelTypes(*tson_types: TSONType):
    for ttype in tson_types:
        if type(ttype) is TSONUnionType:
            yield from ttype.types
        else:
            yield ttype


def cleverUnion(*tson_types: TSONType) -> TSONType:
    array_type: TSONArrayType = None
    object_type: TSONObjectType = None
    simple_types: Set[TSONType] = set()

    tson_types = list(levelTypes(*tson_types))

    for ttype in tson_types:
        if type(ttype) is TSONObjectType:
            object_type = ttype if object_type is None else cleverUnionObjects(ttype, object_type)
        elif type(ttype) is TSONArrayType:
            array_type = ttype if array_type is None else TSONArrayType(cleverUnion(ttype.etype, array_type.etype))
        elif ttype is TSONUnknown:
            pass
        elif ttype is TSONAny:
            return ttype
        else:
            simple_types.add(ttype)

    all_types = {*simple_types}
    if array_type is not None:
        all_types.add(array_type)
    if object_type is not None:
        all_types.add(object_type)

    if len(all_types) == 0:
        return TSONUnknown
    elif len(all_types) == 1:
        return list(all_types)[0]
    else:
        return TSONUnionType(all_types)
