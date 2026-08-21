"""Testes das métricas."""

from __future__ import annotations

import pandas as pd

from diagnostico_retrabalho.metrics import compute_summary, rank_by
from diagnostico_retrabalho.models import RetrabalhoPolicy


def test_compute_summary(
    sample_ordens: pd.DataFrame, policy: RetrabalhoPolicy
) -> None:
    s = compute_summary(sample_ordens, policy)
    assert s["ordens_com_retrabalho"] == 1
    assert s["custo_direto_rs"] == 100.0
    assert s["custo_oportunidade_rs"] == 160.0
    assert s["custo_total_nao_qualidade_rs"] == 260.0


def test_rank_by_processo(sample_ordens: pd.DataFrame) -> None:
    ranking = rank_by(sample_ordens, "processo")
    assert len(ranking) == 1
    assert ranking.iloc[0]["custo_total_rs"] == 260.0
