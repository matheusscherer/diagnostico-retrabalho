"""Geração de relatórios Markdown e Excel."""

from __future__ import annotations

from pathlib import Path
from typing import Union

import pandas as pd

from diagnostico_retrabalho.models import DiagnosisResult

PathLike = Union[str, Path]


def _fmt_brl(value: float) -> str:
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _fmt_num(value: float, digits: int = 1) -> str:
    return f"{value:,.{digits}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _rank_table(
    df: pd.DataFrame,
    key: str,
    lines: list[str],
    limit: int = 10,
) -> None:
    if df.empty:
        lines.append("_Sem dados._")
        return
    lines.append(
        f"| {key.capitalize()} | Ordens | Com RT | Taxa | Horas RT | Custo direto | Oportunidade | Total |"
    )
    lines.append(
        "|---|---:|---:|---:|---:|---:|---:|---:|"
    )
    for _, row in df.head(limit).iterrows():
        lines.append(
            f"| {row[key]} | {int(row['ordens'])} | {int(row['ordens_com_rt'])} | "
            f"{_fmt_num(row['taxa_rt_pct'])}% | {_fmt_num(row['horas_retrabalho'])} | "
            f"{_fmt_brl(row['custo_direto_rs'])} | {_fmt_brl(row['custo_oportunidade_rs'])} | "
            f"{_fmt_brl(row['custo_total_rs'])} |"
        )


def build_markdown_report(result: DiagnosisResult) -> str:
    """Monta o relatório executivo em Markdown."""
    s = result.summary

    lines = [
        "# Diagnóstico de Retrabalho",
        "",
        f"**Período:** {s['periodo_inicio']} a {s['periodo_fim']}",
        f"**Gerado em:** {result.generated_at}",
        "",
        "> Objetivo: quantificar o **custo de não-qualidade** — mão de obra, material e capacidade consumida duas vezes.",
        "",
        "---",
        "",
        "## Resumo executivo",
        "",
        "| Métrica | Valor |",
        "|---------|-------|",
        f"| Ordens analisadas | {s['total_ordens']} |",
        f"| Ordens com retrabalho | {s['ordens_com_retrabalho']} |",
        f"| **Taxa de retrabalho** | **{_fmt_num(s['taxa_retrabalho_pct'])}%** |",
        f"| Unidades totais | {_fmt_num(s['unidades_total'], 0)} |",
        f"| Unidades em retrabalho | {_fmt_num(s['unidades_retrabalho'], 0)} |",
        f"| Horas de retrabalho | {_fmt_num(s['horas_retrabalho'])} h |",
        f"| **First Pass Yield (FPY)** | **{_fmt_num(s['fpy_pct'])}%** (meta {s['fpy_target_pct']}%) |",
        f"| Custo mão de obra (RT) | {_fmt_brl(s['custo_mao_obra_rs'])} |",
        f"| Custo material (RT) | {_fmt_brl(s['custo_material_rs'])} |",
        f"| **Custo direto** | **{_fmt_brl(s['custo_direto_rs'])}** |",
        f"| **Custo de oportunidade** | **{_fmt_brl(s['custo_oportunidade_rs'])}** |",
        f"| **Custo total de não-qualidade** | **{_fmt_brl(s['custo_total_nao_qualidade_rs'])}** |",
        "",
        "---",
        "",
        "## Por processo",
        "",
    ]
    _rank_table(result.by_processo, "processo", lines)

    lines.extend(["", "---", "", "## Por produto", ""])
    _rank_table(result.by_produto, "produto", lines)

    lines.extend(["", "---", "", "## Por causa-raiz", ""])
    _rank_table(result.by_causa, "causa", lines)

    lines.extend(["", "---", "", "## Por operador", ""])
    _rank_table(result.by_operador, "operador", lines)

    lines.extend(["", "---", "", "## Por turno", ""])
    _rank_table(result.by_turno, "turno", lines)

    lines.extend(["", "---", "", "## Premissas", ""])
    for note in result.notes:
        lines.append(f"- {note}")

    lines.extend(
        [
            "",
            "---",
            "",
            "## Próximas ações sugeridas",
            "",
            "1. Atacar as **top 3 causas** por custo total (não por volume).",
            "2. Revisar padrão do processo com maior custo de oportunidade.",
            "3. Treinar/padronizar onde o FPY está longe da meta.",
            "4. Separar falha de processo vs falha de material — ações diferentes.",
            "5. Medir de novo no próximo ciclo: FPY e custo total de não-qualidade.",
            "",
        ]
    )
    return "\n".join(lines)


def save_reports(
    result: DiagnosisResult,
    output_dir: PathLike,
    prefix: str = "diagnostico_retrabalho",
) -> dict:
    """Salva relatório Markdown + Excel detalhado."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    md_path = output_dir / f"{prefix}.md"
    xlsx_path = output_dir / f"{prefix}.xlsx"

    md_path.write_text(build_markdown_report(result), encoding="utf-8")

    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
        result.detail.to_excel(writer, sheet_name="detalhe", index=False)
        result.by_processo.to_excel(writer, sheet_name="por_processo", index=False)
        result.by_produto.to_excel(writer, sheet_name="por_produto", index=False)
        result.by_causa.to_excel(writer, sheet_name="por_causa", index=False)
        result.by_operador.to_excel(writer, sheet_name="por_operador", index=False)
        result.by_turno.to_excel(writer, sheet_name="por_turno", index=False)
        pd.DataFrame([result.summary]).to_excel(writer, sheet_name="resumo", index=False)

    return {"markdown": str(md_path), "excel": str(xlsx_path)}
