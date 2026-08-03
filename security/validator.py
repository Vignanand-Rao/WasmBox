import ast
from security.blocked import BLOCKED_MODULES, BLOCKED_FUNCTIONS

class SecurityVisitor(ast.NodeVisitor):
    def __init__(self):
        self.errors = []

    def visit_Import(self, node):
        for module in node.names:
            if module.name in BLOCKED_MODULES:
                self.errors.append(
                    f"Blocked Module : {module.name}"
                )
        self.generic_visit(node)
    def visit_ImportFrom(self, node):
        if node.module in BLOCKED_MODULES:
            self.errors.append(
                f"Blocked Module : {node.module}"
            )
        self.generic_visit(node)
    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            if node.func.id in BLOCKED_FUNCTIONS:
                self.errors.append(
                    f"Blocked Function : {node.func.id}"
                )
        self.generic_visit(node)
def validate(code):
    tree = ast.parse(code)
    visitor = SecurityVisitor()
    visitor.visit(tree)
    return visitor.errors