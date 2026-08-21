"""Cálculo das métricas de impacto financeiro do retrabalho."""

from __future__ import annotations

import pandas as pd

from diagnostico_retrabalho.models import RetrabalhoPolicy


def _pct(part: float, whole: float) -> float:
    if whole == 0:
        return 0.0
    return round(100.0 * part / whole, 1)


def compute_summary(ordens: pd.DataFrame, policy: RetrabalhoPolicy) -> dict:
    """Resumo executivo com os números principais de dinheiro."""
    total = len(ordens)
    com_rt = ordens[ordens["tem_retrabalho"]]
    n_rt = len(com_rt)

    unidades_total = float(ordens["unidades"].sum())
    unidades_rt = float(ordens["unidades_retrabalho"].sum())
    horas_rt = float(ordens["horas_retrabalho"].sum())

    custo_direto = float(ordens["custo_direto_rs"].sum())
    custo_oportunidade = float(ordens["custo_oportunidade_rs"].sum())
    custo_material = float(ordens["custo_material"].sum())
    custo_mao_obra = float(ordens["custo_mao_obra_rs"].sum())

    fpy = (
        1.0
        if unidades_total == 0
        else max(0.0, (unidades_total - unidades_rt) / unidades_total)
    )

    return {
        "periodo_inicio": ordens["data"].min().strftime("%Y-%m-%d"),
        "periodo_fim": ordens["data"].max().strftime("%Y-%m-%d"),
        "total_ordens": total,
        "ordens_com_retrabalho": n_rt,
        "taxa_retrabalho_pct": _pct(n_rt, total),
        "unidades_total": unidades_total,
        "unidades_retrabalho": unidades_rt,
        "horas_retrabalho": round(horas_rt, 1),
        "fpy": round(fpy, 4),
        "fpy_pct": round(fpy * 100, 1),
        "fpy_target_pct": round(policy.fpy_target * 100, 1),
        "custo_mao_obra_rs": round(custo_mao_obra, 2),
        "custo_material_rs": round(custo_material, 2),
        "custo_direto_rs": round(custo_direto, 2),
        "custo_oportunidade_rs": round(custo_oportunidade, 2),
        "custo_total_nao_qualidade_rs": round(custo_direto + custo_oportunidade, 2),
    }


def rank_by(ordens: pd.DataFrame, group_col: str) -> pd.DataFrame:
    """Ranking de impacto por dimensão."""
    if ordens.empty:
        return pd.DataFrame(
            columns=[
                group_col,
                "ordens",
                "ordens_com_rt",
                "taxa_rt_pct",
                "horas_retrabalho",
                "custo_direto_rs",
                "custo_oportunidade_rs",
                "custo_total_rs",
            ]
        )

    # Para causa, só ordens com retrabalho e causa preenchida
    base = ordens
    if group_col == "causa":
        base = ordens[(ordens["tem_retrabalho"]) & (ordens["causa"] != "")].copy()
        if base.empty:
            return pd.DataFrame(
                columns=[
                    group_col,
                    "ordens",
                    "ordens_com_rt",
                    "taxa_rt_pct",
                    "horas_retrabalho",
                    "custo_direto_rs",
                    "custo_oportunidade_rs",
                    "custo_total_rs",
                ]
            )

    grouped = (
        base.groupby(group_col, as_index=False)
        .agg(
            ordens=("id", "count"),
            ordens_com_rt=("tem_retrabalho", "sum"),
            horas_retrabalho=("horas_retrabalho", "sum"),
            custo_direto_rs=("custo_direto_rs", "sum"),
            custo_oportunidade_rs=("custo_oportunidade_rs", "sum"),
            custo_total_rs=("custo_total_rs", "sum"),
        )
    )
    grouped["ordens_com_rt"] = grouped["ordens_com_rt"].astype(int)
    grouped["taxa_rt_pct"] = grouped.apply(
        lambda r: _pct(r["ordens_com_rt"], r["ordens"]), axis=1
    )
    grouped = grouped.sort_values(
        by=["custo_total_rs", "horas_retrabalho"], ascending=False
    ).reset_index(drop=True)

    return grouped[
        [
            group_col,
            "ordens",
            "ordens_com_rt",
            "taxa_rt_pct",
            "horas_retrabalho",
            "custo_direto_rs",
            "custo_oportunidade_rs",
            "custo_total_rs",
        ]
    ]
