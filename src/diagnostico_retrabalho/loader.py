"""Carregamento e validação dos dados de entrada."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

REQUIRED_COLS = [
    "id",
    "data",
    "processo",
    "produto",
    "operador",
    "turno",
    "unidades",
    "unidades_retrabalho",
    "horas_retrabalho",
    "custo_hora",
    "custo_material",
    "causa",
    "ticket_hora",
]


def load_ordens(path: Path) -> pd.DataFrame:
    """Lê e valida o arquivo de ordens."""
    if not path.exists():
        raise FileNotFoundError(f"Arquivo de ordens não encontrado: {path}")

    df = pd.read_csv(path)
    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"Colunas obrigatórias ausentes em ordens: {missing}")

    df = df.copy()
    df["id"] = df["id"].astype(str).str.strip()
    df["data"] = pd.to_datetime(df["data"], errors="coerce")
    if df["data"].isna().any():
        raise ValueError("Existem datas inválidas em ordens")

    for col in ["processo", "produto", "operador", "turno"]:
        df[col] = df[col].astype(str).str.strip()

    df["causa"] = df["causa"].fillna("").astype(str).str.strip()

    numeric_cols = [
        "unidades",
        "unidades_retrabalho",
        "horas_retrabalho",
        "custo_hora",
        "custo_material",
        "ticket_hora",
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        if df[col].isna().any():
            raise ValueError(f"{col} deve ser numérico")
        if (df[col] < 0).any():
            raise ValueError(f"{col} deve ser >= 0")

    if (df["unidades_retrabalho"] > df["unidades"]).any():
        raise ValueError("unidades_retrabalho não pode ser maior que unidades")

    # Flags e custos por linha
    df["tem_retrabalho"] = (df["unidades_retrabalho"] > 0) | (df["horas_retrabalho"] > 0)
    df["custo_mao_obra_rs"] = df["horas_retrabalho"] * df["custo_hora"]
    df["custo_direto_rs"] = df["custo_mao_obra_rs"] + df["custo_material"]
    df["custo_oportunidade_rs"] = df["horas_retrabalho"] * df["ticket_hora"]
    df["custo_total_rs"] = df["custo_direto_rs"] + df["custo_oportunidade_rs"]

    # FPY por ordem (1.0 se unidades == 0 e sem retrabalho)
    df["fpy"] = df.apply(
        lambda r: 1.0
        if r["unidades"] == 0
        else max(0.0, (r["unidades"] - r["unidades_retrabalho"]) / r["unidades"]),
        axis=1,
    )

    return df.reset_index(drop=True)
