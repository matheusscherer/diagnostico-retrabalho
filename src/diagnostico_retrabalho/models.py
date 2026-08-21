"""Modelos de domínio do diagnóstico de retrabalho."""

from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd


@dataclass(frozen=True)
class RetrabalhoPolicy:
    """Parâmetros de política do diagnóstico."""

    # Meta de First Pass Yield (informativa no relatório)
    fpy_target: float = 0.95

    def __post_init__(self) -> None:
        if not 0.0 < self.fpy_target <= 1.0:
            raise ValueError("fpy_target deve estar entre 0 e 1 (exclusive 0)")


@dataclass
class DiagnosisResult:
    """Resultado completo do diagnóstico."""

    detail: pd.DataFrame
    summary: dict
    by_processo: pd.DataFrame
    by_produto: pd.DataFrame
    by_causa: pd.DataFrame
    by_operador: pd.DataFrame
    by_turno: pd.DataFrame
    policy: RetrabalhoPolicy
    generated_at: str
    notes: list[str] = field(default_factory=list)

    @property
    def custo_direto(self) -> float:
        return float(self.summary.get("custo_direto_rs", 0.0))

    @property
    def custo_oportunidade(self) -> float:
        return float(self.summary.get("custo_oportunidade_rs", 0.0))

    @property
    def custo_total_nao_qualidade(self) -> float:
        return self.custo_direto + self.custo_oportunidade
