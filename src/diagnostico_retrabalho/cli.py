"""Interface de linha de comando."""

from __future__ import annotations

import argparse
from pathlib import Path

from diagnostico_retrabalho.analyzer import run_diagnosis
from diagnostico_retrabalho.config import DEFAULT_ORDENS_PATH, DEFAULT_OUTPUT_DIR
from diagnostico_retrabalho.models import RetrabalhoPolicy
from diagnostico_retrabalho.report import build_markdown_report, save_reports


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="diagnostico-retrabalho",
        description="Diagnóstico de retrabalho: custo de não-qualidade.",
    )
    parser.add_argument(
        "--ordens",
        type=Path,
        default=DEFAULT_ORDENS_PATH,
        help="Caminho do CSV de ordens",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Diretório de saída dos relatórios",
    )
    parser.add_argument(
        "--fpy-target",
        type=float,
        default=0.95,
        help="Meta de First Pass Yield (default: 0.95)",
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Apenas imprime o relatório no terminal, sem salvar arquivos",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    policy = RetrabalhoPolicy(fpy_target=args.fpy_target)

    result = run_diagnosis(ordens_path=args.ordens, policy=policy)
    report = build_markdown_report(result)
    print(report)

    if not args.no_save:
        paths = save_reports(result, args.output)
        print("\nArquivos gerados:")
        print(f"  - {paths['markdown']}")
        print(f"  - {paths['excel']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
