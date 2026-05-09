"""Unit tests for presentation dependency wiring."""

from unittest.mock import MagicMock

from presentation.deps import get_current_year


def test_get_current_year_reads_datetime_now_year(monkeypatch):
    fixed = MagicMock()
    fixed.year = 2033
    dt_mod = MagicMock()
    dt_mod.now.return_value = fixed
    monkeypatch.setattr("presentation.deps.datetime", dt_mod)
    assert get_current_year() == 2033
