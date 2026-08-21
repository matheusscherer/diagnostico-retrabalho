"""Testes do loader."""

from __future__ import annotations

from pathlib import Path

import pytest

from diagnostico_retrabalho.loader import load_ordens


def test_load_ordens_ok(data_dir: Path) -> None:
    df = load_ordens(data_dir / "ordens.csv")
    assert len(df) == 2
    assert "custo_direto_rs" in df.columns
    assert df.loc[df["id"] == "O2", "custo_direto_rs"].iloc[0] == 100.0


def test_load_missing_file(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_ordens(tmp_path / "x.csv")
