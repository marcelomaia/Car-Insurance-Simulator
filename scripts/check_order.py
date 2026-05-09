import ast
import glob
import sys


def count_class_method_order_violations(filepath, tree):
    errors = 0
    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue
        names = [stmt.name for stmt in node.body if isinstance(stmt, (ast.AsyncFunctionDef, ast.FunctionDef))]
        if names != sorted(names):
            print(f"❌ Invalid method order in class '{node.name}' in file {filepath}")
            print(f"   Current order: {names}")
            print(f"   Expected order: {sorted(names)}\n")
            errors += 1
    return errors


def count_module_class_order_violations(filepath, tree):
    if not isinstance(tree, ast.Module):
        return 0
    names = [stmt.name for stmt in tree.body if isinstance(stmt, ast.ClassDef)]
    if names != sorted(names):
        print(f"❌ Invalid class order at module scope in file {filepath}")
        print(f"   Current order: {names}")
        print(f"   Expected order: {sorted(names)}\n")
        return 1
    return 0


def count_module_function_order_violations(filepath, tree):
    if not isinstance(tree, ast.Module):
        return 0
    names = [stmt.name for stmt in tree.body if isinstance(stmt, (ast.AsyncFunctionDef, ast.FunctionDef))]
    if names != sorted(names):
        print(f"❌ Invalid function order at module scope in file {filepath}")
        print(f"   Current order: {names}")
        print(f"   Expected order: {sorted(names)}\n")
        return 1
    return 0


def count_parameter_order_violations(filepath, tree):
    errors = 0
    for node in ast.walk(tree):
        if not isinstance(node, (ast.AsyncFunctionDef, ast.FunctionDef)):
            continue
        args = [arg.arg for arg in node.args.args if arg.arg not in ("cls", "self")]
        if args != sorted(args):
            print(f"❌ Invalid parameter order in function/method '{node.name}' in file {filepath}")
            print(f"   Current order: {args}")
            print(f"   Expected order: {sorted(args)}\n")
            errors += 1
    return errors


def verify_file(filepath):
    with open(filepath, encoding="utf-8") as file:
        content = file.read()
    return verify_source(content, filepath)


def verify_source(content, filepath):
    try:
        tree = ast.parse(content)
    except SyntaxError:
        return 0

    errors = 0
    errors += count_class_method_order_violations(filepath, tree)
    errors += count_module_class_order_violations(filepath, tree)
    errors += count_module_function_order_violations(filepath, tree)
    errors += count_parameter_order_violations(filepath, tree)
    return errors


if __name__ == "__main__":
    print("🔍 Running alphabetical-order linter...\n")

    python_files = glob.glob("**/*.py", recursive=True)
    total_errors = 0

    for filepath in python_files:
        if ".venv" not in filepath and "venv" not in filepath:
            total_errors += verify_file(filepath)

    if total_errors == 0:
        print("✅ OK: functions, classes, methods, and parameters are in alphabetical order.")
    else:
        print(f"🚨 Found {total_errors} alphabetical-order violation(s). Fix them before submitting.")

    sys.exit(1 if total_errors else 0)
