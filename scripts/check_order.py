import ast
import glob
import sys


def count_class_method_order_violations(filepath, tree):
    erros = 0
    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue
        names = [stmt.name for stmt in node.body if isinstance(stmt, (ast.AsyncFunctionDef, ast.FunctionDef))]
        if names != sorted(names):
            print(f"❌ ERRO na ordem dos métodos da classe '{node.name}' no arquivo {filepath}")
            print(f"   Ordem atual:  {names}")
            print(f"   Deveria ser:  {sorted(names)}\n")
            erros += 1
    return erros


def count_module_class_order_violations(filepath, tree):
    if not isinstance(tree, ast.Module):
        return 0
    names = [stmt.name for stmt in tree.body if isinstance(stmt, ast.ClassDef)]
    if names != sorted(names):
        print(f"❌ ERRO na ordem das classes no módulo no arquivo {filepath}")
        print(f"   Ordem atual:  {names}")
        print(f"   Deveria ser:  {sorted(names)}\n")
        return 1
    return 0


def count_module_function_order_violations(filepath, tree):
    if not isinstance(tree, ast.Module):
        return 0
    names = [stmt.name for stmt in tree.body if isinstance(stmt, (ast.AsyncFunctionDef, ast.FunctionDef))]
    if names != sorted(names):
        print(f"❌ ERRO na ordem das funções no módulo no arquivo {filepath}")
        print(f"   Ordem atual:  {names}")
        print(f"   Deveria ser:  {sorted(names)}\n")
        return 1
    return 0


def count_parameter_order_violations(filepath, tree):
    erros = 0
    for node in ast.walk(tree):
        if not isinstance(node, (ast.AsyncFunctionDef, ast.FunctionDef)):
            continue
        args = [arg.arg for arg in node.args.args if arg.arg not in ("cls", "self")]
        if args != sorted(args):
            print(f"❌ ERRO na função/método '{node.name}' no arquivo {filepath}")
            print(f"   Ordem atual:  {args}")
            print(f"   Deveria ser:  {sorted(args)}\n")
            erros += 1
    return erros


def verify_file(filepath):
    with open(filepath, encoding="utf-8") as file:
        content = file.read()
    return verify_source(content, filepath)


def verify_source(content, filepath):
    try:
        tree = ast.parse(content)
    except SyntaxError:
        return 0

    erros = 0
    erros += count_class_method_order_violations(filepath, tree)
    erros += count_module_class_order_violations(filepath, tree)
    erros += count_module_function_order_violations(filepath, tree)
    erros += count_parameter_order_violations(filepath, tree)
    return erros


if __name__ == "__main__":
    print("🔍 Iniciando Linter Anti-Honeypot (Ordem Alfabética)...\n")

    arquivos_python = glob.glob("**/*.py", recursive=True)
    total_erros = 0

    for arquivo in arquivos_python:
        if ".venv" not in arquivo and "venv" not in arquivo:
            total_erros += verify_file(arquivo)

    if total_erros == 0:
        print("✅ Tudo limpo! Funções, classes, métodos e parâmetros em ordem alfabética.")
    else:
        print(f"🚨 Encontrados {total_erros} erros de ordem alfabética. Arrume antes de enviar.")

    sys.exit(1 if total_erros else 0)
