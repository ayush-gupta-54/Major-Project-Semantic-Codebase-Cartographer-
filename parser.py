import ast

def parse_file(filepath):
    # Read file safely (binary)
    with open(filepath, "rb") as f:
        raw = f.read()

    source = raw.decode("utf-8", errors="ignore")

    tree = ast.parse(source)

    functions = []
    calls = []

    class Visitor(ast.NodeVisitor):
        def __init__(self):
            self.current_function = None

        def visit_FunctionDef(self, node):
            self.current_function = node.name
            functions.append(node.name)
            self.generic_visit(node)

        def visit_Call(self, node):
            if isinstance(node.func, ast.Name):
                calls.append((self.current_function, node.func.id))
            elif isinstance(node.func, ast.Attribute):
                calls.append((self.current_function, node.func.attr))
            self.generic_visit(node)

    Visitor().visit(tree)

    return {
        "functions": functions,
        "calls": calls
    }