import ast

def extract_code(file_path):
    with open(file_path) as file:
        code = file.read()

    tree = ast.parse(code)
    result = {"imports": [], "variables": [], "functions": [], "classes": []}

    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                result["imports"].append(f"import {alias.name.strip()}")

        elif isinstance(node, ast.ImportFrom):
            if node.module is not None:
                for alias in node.names:
                    result["imports"].append(f"from {node.module.strip()} import {alias.name.strip()}")

        elif isinstance(node, ast.FunctionDef):
            body = ast.unparse(node).strip()
            result["functions"].append(f"{body}\n")

        elif isinstance(node, ast.ClassDef):
            body = ast.unparse(node).strip()
            result["classes"].append(f"{body}\n")

        elif isinstance(node, ast.Assign):
            body = ast.unparse(node).strip()
            result["variables"].append(f"{body}\n")

    return result