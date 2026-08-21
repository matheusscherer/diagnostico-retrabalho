"""Orquestração do diagnóstico de retrabalho."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from diagnostico_retrabalho.loader import load_ordens
from diagnostico_retrabalho.metrics import compute_summary, rank_by
from diagnostico_retrabalho.models import DiagnosisResult, RetrabalhoPolicy


def run_diagnosis(
    ordens_path: Path,
    policy: RetrabalhoPolicy | None = None,
) -> DiagnosisResult:
    """Executa o diagnóstico completo."""
    policy = policy or RetrabalhoPolicy()
    ordens = load_ordens(ordens_path)
    summary = compute_summary(ordens, policy)

    notes = [
        "Custo direto = (horas de retrabalho × custo/hora) + material descartado/reposto.",
        "Custo de oportunidade = horas de retrabalho × ticket/hora (capacidade que poderia faturar).",
        "FPY (First Pass Yield) = unidades boas de primeira ÷ unidades totais.",
        "Taxa de retrabalho = ordens com retrabalho ÷ total de ordens.",
        f"Meta de FPY usada no relatório: {policy.fpy_target:.0%}.",
        "Dados de exemplo são sintéticos.",
    ]

    return DiagnosisResult(
        detail=ordens,
        summary=summary,
        by_processo=rank_by(ordens, "processo"),
        by_produto=rank_by(ordens, "produto"),
        by_causa=rank_by(ordens, "causa"),
        by_operador=rank_by(ordens, "operador"),
        by_turno=rank_by(ordens, "turno"),
        policy=policy,
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
        notes=notes,
    )
