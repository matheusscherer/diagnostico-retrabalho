"""Testes de integração."""

from __future__ import annotations

from pathlib import Path

from diagnostico_retrabalho.analyzer import run_diagnosis
from diagnostico_retrabalho.report import build_markdown_report


def test_end_to_end(data_dir: Path) -> None:
    result = run_diagnosis(ordens_path=data_dir / "ordens.csv")
    assert result.summary["ordens_com_retrabalho"] == 1
    assert result.custo_total_nao_qualidade == 260.0
    md = build_markdown_report(result)
    assert "Retrabalho" in md
    assert "não-qualidade" in md or "nao-qualidade" in md or "Custo total" in md
