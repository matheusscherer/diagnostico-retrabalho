"""Caminhos e constantes padrão."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ORDENS_PATH = ROOT / "data" / "raw" / "ordens.csv"
DEFAULT_OUTPUT_DIR = ROOT / "outputs"
