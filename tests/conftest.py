"""Fixtures compartilhadas."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from diagnostico_retrabalho.models import RetrabalhoPolicy


@pytest.fixture
def sample_ordens() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "id": "O1",
                "data": pd.Timestamp("2026-08-01"),
                "processo": "Montagem",
                "produto": "A",
                "operador": "João",
                "turno": "manhã",
                "unidades": 100,
                "unidades_retrabalho": 0,
                "horas_retrabalho": 0.0,
                "custo_hora": 30.0,
                "custo_material": 0.0,
                "causa": "",
                "ticket_hora": 80.0,
                "tem_retrabalho": False,
                "custo_mao_obra_rs": 0.0,
                "custo_direto_rs": 0.0,
                "custo_oportunidade_rs": 0.0,
                "custo_total_rs": 0.0,
                "fpy": 1.0,
            },
            {
                "id": "O2",
                "data": pd.Timestamp("2026-08-01"),
                "processo": "Montagem",
                "produto": "A",
                "operador": "João",
                "turno": "manhã",
                "unidades": 80,
                "unidades_retrabalho": 10,
                "horas_retrabalho": 2.0,
                "custo_hora": 30.0,
                "custo_material": 40.0,
                "causa": "Ajuste",
                "ticket_hora": 80.0,
                "tem_retrabalho": True,
                "custo_mao_obra_rs": 60.0,
                "custo_direto_rs": 100.0,
                "custo_oportunidade_rs": 160.0,
                "custo_total_rs": 260.0,
                "fpy": 0.875,
            },
        ]
    )


@pytest.fixture
def policy() -> RetrabalhoPolicy:
    return RetrabalhoPolicy(fpy_target=0.95)


@pytest.fixture
def data_dir(tmp_path: Path) -> Path:
    raw = tmp_path / "raw"
    raw.mkdir()
    pd.DataFrame(
        [
            {
                "id": "O1",
                "data": "2026-08-01",
                "processo": "Montagem",
                "produto": "A",
                "operador": "João",
                "turno": "manhã",
                "unidades": 100,
                "unidades_retrabalho": 0,
                "horas_retrabalho": 0,
                "custo_hora": 30,
                "custo_material": 0,
                "causa": "",
                "ticket_hora": 80,
            },
            {
                "id": "O2",
                "data": "2026-08-01",
                "processo": "Montagem",
                "produto": "A",
                "operador": "João",
                "turno": "manhã",
                "unidades": 80,
                "unidades_retrabalho": 10,
                "horas_retrabalho": 2,
                "custo_hora": 30,
                "custo_material": 40,
                "causa": "Ajuste",
                "ticket_hora": 80,
            },
        ]
    ).to_csv(raw / "ordens.csv", index=False)
    return raw
