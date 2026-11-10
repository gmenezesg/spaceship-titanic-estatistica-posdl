import math
from pathlib import Path

import nbformat
import numpy as np
import pandas as pd
import pytest
from nbclient import NotebookClient


NOTEBOOK_PATH = Path("notebooks/04_testes_hipoteses_anova.ipynb")
CONCLUSIONS_PATH = Path("docs/conclusoes/04_testes_hipoteses_anova.md")
DATA_PATH = Path("data/processed/spaceship_titanic_clean.csv")


@pytest.fixture(scope="module")
def executed_notebook() -> nbformat.NotebookNode:
    notebook = nbformat.read(NOTEBOOK_PATH, as_version=4)
    NotebookClient(notebook, timeout=240, kernel_name="python3").execute()
    return notebook


def _notebook_sources(notebook: nbformat.NotebookNode) -> str:
    return "\n".join(cell.source for cell in notebook.cells)


def _notebook_outputs(notebook: nbformat.NotebookNode) -> str:
    texts = []
    for cell in notebook.cells:
        for output in cell.get("outputs", []):
            if output.output_type == "stream":
                texts.append(output.get("text", ""))
            elif output.output_type in ("display_data", "execute_result"):
                texts.append(output.get("data", {}).get("text/plain", ""))
    return "\n".join(texts)


def _tie_corrected_mann_whitney_effect() -> tuple[float, float, float]:
    data = pd.read_csv(DATA_PATH)
    group_false = data.loc[~data["Transported"], "TotalSpend"].dropna().to_numpy()
    group_true = data.loc[data["Transported"], "TotalSpend"].dropna().to_numpy()

    n1, n2 = len(group_false), len(group_true)
    total_n = n1 + n2
    ranks = pd.Series(np.concatenate([group_false, group_true])).rank(method="average").to_numpy()
    u_stat = ranks[:n1].sum() - n1 * (n1 + 1) / 2
    tie_counts = pd.Series(np.concatenate([group_false, group_true])).value_counts().to_numpy()
    tie_sum = np.sum(tie_counts**3 - tie_counts)
    variance = n1 * n2 / 12 * ((total_n + 1) - tie_sum / (total_n * (total_n - 1)))
    continuity = 0.5 if u_stat > n1 * n2 / 2 else -0.5
    z_score = (u_stat - n1 * n2 / 2 - continuity) / math.sqrt(variance)
    effect = abs(z_score) / math.sqrt(total_n)
    return u_stat, z_score, effect


def test_kan25_documents_pearson_without_yates(executed_notebook):
    sources = _notebook_sources(executed_notebook)
    conclusions = CONCLUSIONS_PATH.read_text(encoding="utf-8")

    assert "chi2_contingency(observed, correction=False)" in sources
    assert "Correção de Yates" not in sources
    assert "Correção de Yates" not in conclusions
    assert "Qui-Quadrado de Pearson sem correção de continuidade" in conclusions


def test_kan26_uses_tie_corrected_mann_whitney_effect(executed_notebook):
    u_stat, z_score, effect = _tie_corrected_mann_whitney_effect()
    sources = _notebook_sources(executed_notebook)
    outputs = _notebook_outputs(executed_notebook)
    conclusions = CONCLUSIONS_PATH.read_text(encoding="utf-8")

    assert u_stat == 13_846_861.5
    assert round(z_score, 2) == 39.09
    assert round(effect, 3) == 0.419
    assert "tie_counts" in sources
    assert "tie_correction" in sources
    assert "U = 13,846,861.5, Z = 39.09" in outputs
    assert "r de Rosenthal = 0.419" in outputs
    assert "Z = 39{,}09" in conclusions
    assert "0{,}419" in conclusions
    assert "13.846.862" not in conclusions
    assert "Z = 37{,}62" not in conclusions
    assert "0{,}404" not in conclusions


def test_kan27_reports_games_howell_degrees_of_freedom(executed_notebook):
    outputs = _notebook_outputs(executed_notebook)
    conclusions = CONCLUSIONS_PATH.read_text(encoding="utf-8")

    for expected in ("2226.6", "2290.6", "2573.3"):
        assert expected in outputs

    for expected in ("2.226{,}6", "2.290{,}6", "2.573{,}3"):
        assert expected in conclusions

    assert "2.455{,}8" not in conclusions
    assert "2.871{,}4" not in conclusions
    assert "2.378{,}1" not in conclusions


def test_kan28_and_kan29_share_corrected_values(executed_notebook):
    sources = _notebook_sources(executed_notebook)
    outputs = _notebook_outputs(executed_notebook)
    conclusions = CONCLUSIONS_PATH.read_text(encoding="utf-8")

    assert "U = {stat_mwu:,.1f} (Z = {z_mwu:.2f})" in sources
    assert "r de Rosenthal = {r_rosenthal:.3f}" in sources
    assert "p < 1e-300" in sources
    assert "Pearson sem correção de continuidade" in outputs
    assert "q = 37.60 (df = 2226.6)" in outputs
    assert "q = 31.15 (df = 2573.3)" in outputs
    assert "q = 16.12 (df = 2290.6)" in outputs
    assert "13.846.861{,}5" in conclusions
    assert "Z = 39{,}09" in conclusions
    assert "r \\text{ de Rosenthal} = 0{,}419" in conclusions
    assert "p < 10^{-16}" not in conclusions
