import ast
import glob
import sys


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
    functions = [node for node in ast.walk(tree) if isinstance(node, (ast.AsyncFunctionDef, ast.FunctionDef))]
    for node in functions:
        args = [arg.arg for arg in node.args.args if arg.arg not in ("cls", "self")]
        if args != sorted(args):
            print(f"❌ ERRO na função/método '{node.name}' no arquivo {filepath}")
            print(f"   Ordem atual:  {args}")
            print(f"   Deveria ser:  {sorted(args)}\n")
            erros += 1

    return erros


if __name__ == "__main__":
    print("🔍 Iniciando Linter Anti-Honeypot (Ordem Alfabética)...\n")

    arquivos_python = glob.glob("**/*.py", recursive=True)
    total_erros = 0

    for arquivo in arquivos_python:
        if ".venv" not in arquivo and "venv" not in arquivo:
            total_erros += verify_file(arquivo)

    if total_erros == 0:
        print("✅ Tudo limpo! Parâmetros em ordem alfabética. Pode enviar o teste!")
    else:
        print(f"🚨 Encontrados {total_erros} erros de ordem alfabética. Arrume antes de enviar.")

    sys.exit(1 if total_erros else 0)
