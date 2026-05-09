import ast
import glob
import io
import runpy
from contextlib import redirect_stdout
from pathlib import Path

import pytest

from scripts.check_order import (
    count_module_class_order_violations,
    count_module_function_order_violations,
    verify_file,
    verify_source,
)

_CHECK_ORDER_SCRIPT = Path(__file__).resolve().parents[1] / "check_order.py"


def test_async_invalid_parameter_order():
    source = "async def alpha(zeta, alpha):\n    pass\n"
    assert verify_source(source, "async_invalid.py") == 1


def test_async_valid_parameter_order():
    source = "async def alpha(alpha, zeta):\n    pass\n"
    assert verify_source(source, "async_valid.py") == 0


def test_class_attributes_invalid_order():
    source = "class C:\n    z: int\n    a: int\n"
    assert verify_source(source, "attrs_bad.py") == 1


def test_class_attributes_valid_order():
    source = "class C:\n    a: int\n    z: int\n"
    assert verify_source(source, "attrs_ok.py") == 0


def test_class_methods_invalid_order():
    source = "class C:\n    def b(self):\n        pass\n    def a(self):\n        pass\n"
    assert verify_source(source, "methods_bad.py") == 1


def test_class_methods_valid_order():
    source = "class C:\n    def a(self):\n        pass\n    def b(self):\n        pass\n"
    assert verify_source(source, "methods_ok.py") == 0


def test_cls_first_parameter_ignored():
    source = "class Beta:\n    @classmethod\n    def gamma(cls, apple, banana):\n        pass\n"
    assert verify_source(source, "cls_ok.py") == 0


def test_invalid_parameter_order_increments_errors(capsys):
    source = "def foo(banana, apple):\n    pass\n"
    assert verify_source(source, "bad.py") == 1
    captured = capsys.readouterr()
    assert "bad.py" in captured.out
    assert "foo" in captured.out
    assert "banana" in captured.out
    assert "apple" in captured.out


def test_main_exits_nonzero_when_parameters_unsorted(monkeypatch, tmp_path):
    arquivo = tmp_path / "bad.py"
    arquivo.write_text("def x(z, a):\n    pass\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    def fake_glob(pattern, recursive=True):
        return [str(arquivo.name)]

    monkeypatch.setattr(glob, "glob", fake_glob)

    buffer = io.StringIO()
    with redirect_stdout(buffer), pytest.raises(SystemExit) as exc_info:
        runpy.run_path(str(_CHECK_ORDER_SCRIPT), run_name="__main__")
    assert exc_info.value.code == 1


def test_main_exits_zero_when_all_parameters_sorted(monkeypatch, tmp_path):
    arquivo = tmp_path / "good.py"
    arquivo.write_text("def x(a, z):\n    pass\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    def fake_glob(pattern, recursive=True):
        return [str(arquivo.name)]

    monkeypatch.setattr(glob, "glob", fake_glob)

    buffer = io.StringIO()
    with redirect_stdout(buffer), pytest.raises(SystemExit) as exc_info:
        runpy.run_path(str(_CHECK_ORDER_SCRIPT), run_name="__main__")
    assert exc_info.value.code == 0


def test_module_classes_invalid_order():
    source = "class Z:\n    pass\nclass A:\n    pass\n"
    assert verify_source(source, "classes_bad.py") == 1


def test_module_classes_valid_order():
    source = "class A:\n    pass\nclass Z:\n    pass\n"
    assert verify_source(source, "classes_ok.py") == 0


def test_module_functions_and_parameters_both_invalid():
    source = "def foo(banana, apple):\n    pass\ndef bar():\n    pass\n"
    assert verify_source(source, "both_bad.py") == 2


def test_module_functions_invalid_order():
    source = "def z():\n    pass\ndef a():\n    pass\n"
    assert verify_source(source, "funcs_bad.py") == 1


def test_module_functions_valid_order():
    source = "def a():\n    pass\ndef z():\n    pass\n"
    assert verify_source(source, "funcs_ok.py") == 0


def test_module_order_helpers_return_zero_for_eval_expression_tree():
    tree = ast.parse("1 + 2", mode="eval")
    assert count_module_class_order_violations("expr.py", tree) == 0
    assert count_module_function_order_violations("expr.py", tree) == 0


def test_multiple_functions_counts_all_violations():
    source = "def first(z, a):\n    pass\n\ndef second(b, a):\n    pass\n"
    assert verify_source(source, "multi.py") == 2


def test_nested_function_invalid_order():
    source = "def outer():\n    def inner(z, a):\n        pass\n    return inner\n"
    assert verify_source(source, "nested.py") == 1


def test_self_first_parameter_ignored():
    source = "class Delta:\n    def method(self, apple, banana):\n        pass\n"
    assert verify_source(source, "self_ok.py") == 0


def test_syntax_error_returns_zero():
    assert verify_source("def broken(\n", "syntax.py") == 0


def test_valid_parameter_order_returns_zero():
    source = "def bar(apple, banana, cherry):\n    pass\n"
    assert verify_source(source, "good.py") == 0


def test_verify_file_reads_and_checks(tmp_path):
    arquivo = tmp_path / "sample.py"
    arquivo.write_text("def x(z, a):\n    pass\n", encoding="utf-8")

    assert verify_file(str(arquivo)) == 1
