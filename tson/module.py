from typing import List, Set
from .ast import AssignmentNode
from .evaluate import evaluate_tson
from .typecheck import TypeChecker


class TSONModule:
    def __init__(self, assignments: List[AssignmentNode]):
        self.assignments = assignments
        self.typechecker = TypeChecker()
        self.values = {}
        self.exports: Set[str] = set()
        self.default_export: str = ""

    def get(self, label: str):
        return self.values.get(label, None)

    def get_default_export(self):
        return self.get(self.default_export)

    def evaluate(self):
        for assignment in self.assignments:
            self.evaluate_assignment(assignment)

    def evaluate_assignment(self, assignment: AssignmentNode):
        if assignment.stype == "let":
            value = evaluate_tson(assignment.value, self.values)
            ttype = self.typechecker.check(value)
            self.typechecker.declare(assignment.label.value, ttype)
            self.values[assignment.label.value] = value

        elif assignment.stype == "type":
            pass

        else:
            raise ValueError
