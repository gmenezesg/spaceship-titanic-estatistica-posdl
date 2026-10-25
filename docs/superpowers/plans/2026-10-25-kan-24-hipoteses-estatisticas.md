# KAN-24 Hypotheses Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a didactic, reproducible notebook that formalizes the four statistical hypotheses and decision rules required before the project's inferential tests.

**Architecture:** Add one standalone notebook, `notebooks/04_testes_hipoteses_anova.ipynb`, which reads only the processed training dataset. Markdown cells teach the inferential concepts and formalize H0/H1; code cells validate the analytic dataset and display only descriptive structure needed to confirm the variables are available. No inferential statistic, p-value, effect size, confidence interval, or test conclusion is calculated in this ticket.

**Tech Stack:** Python 3.10+, Jupyter Notebook, pandas, NumPy, SciPy (reserved for subsequent tickets).

**Spec:** Jira KAN-24, "Definir hipóteses estatísticas antes dos testes".

## Global Constraints

- Read `data/processed/spaceship_titanic_clean.csv`, the approved and merged KAN-12 training dataset with 8,693 rows and 22 columns.
- Fix the significance level to `alpha = 0.05` before any inferential analysis.
- Define hypotheses for `HomePlanet` x `Transported`, `CryoSleep` x `Transported`, `TotalSpend` by `Transported`, and `TotalSpend` by `HomePlanet`.
- Preserve the scope boundary: executing chi-square, Welch t, Mann-Whitney, Welch ANOVA, Kruskal-Wallis, post-hoc tests, effect sizes, and confidence intervals belongs to KAN-25, KAN-26, and KAN-27.
- Write explanatory material in Portuguese, with mathematical notation rendered in Markdown/LaTex where it improves clarity.
- Do not modify the merged KAN-12 dataset, its notebook, or source data.
- Follow contribution conventions: branch `docs/daniela-testes-hipoteses`, Portuguese commit message beginning with `[KAN-24]`, and PR review by Renatta.

## Review Focus

- Missing or wrongly typed columns: the setup must fail with an explanatory message before analysis if any required variable is absent.
- Wrong dataset path: the notebook must use the processed training CSV, never raw data or the unlabelled Kaggle test set.
- Target encoding: the setup must verify `Transported` has exactly two observed categories before stating the categorical hypotheses.
- Planet categories: the setup must show the three planned `HomePlanet` groups and flag an unexpected category rather than silently treating it as planned.
- Scope creep: execution must contain no inferential-test calls or results; this notebook only pre-registers questions and rules.

---

### Task 1: Create The Didactic KAN-24 Notebook

**Files:**
- Create: `notebooks/04_testes_hipoteses_anova.ipynb`

**Interfaces:**
- Consumes: `data/processed/spaceship_titanic_clean.csv` with `HomePlanet`, `CryoSleep`, `TotalSpend`, and `Transported`.
- Produces: A reproducible KAN-24 notebook that KAN-25, KAN-26, and KAN-27 can cite as their pre-registered hypothesis specification.

- [ ] **Step 1: Create the notebook title and orientation cells**

Include the Jira identifier, objective, data source, author/reviewer responsibilities, and a concise explanation that hypotheses are written before inferential results to avoid p-hacking.

- [ ] **Step 2: Add an environment and data-loading code cell**

Import `Path`, `pandas as pd`, and `numpy as np`. Resolve the project root from the notebook working directory, load `data/processed/spaceship_titanic_clean.csv`, define `alpha = 0.05`, and print the dataset shape and configured alpha.

- [ ] **Step 3: Add a data-contract validation code cell**

Require `HomePlanet`, `CryoSleep`, `TotalSpend`, and `Transported`; raise a `ValueError` listing missing names. Verify zero null values in these fields, exactly two `Transported` categories, and exactly the expected planet set `{Earth, Europa, Mars}`. Print category counts only; do not calculate inferential statistics.

- [ ] **Step 4: Add a teaching cell on hypotheses and decision rules**

Explain H0, H1, alpha, Type I error, p-value, and the distinction between rejecting H0 and proving H0 false. State the prospective rule: reject H0 when `p < 0.05`; otherwise, do not reject H0.

- [ ] **Step 5: Add the four pre-registered hypothesis sections**

Define each question with its variables, unit of analysis, H0, H1, planned test family, and rationale:

1. `HomePlanet` and `Transported`: independence versus association; chi-square in KAN-25.
2. `CryoSleep` and `Transported`: independence versus association; chi-square in KAN-25.
3. `TotalSpend` by `Transported`: equal location/central tendency versus difference; Welch t and Mann-Whitney in KAN-26 because the spending distribution is zero-inflated and right-skewed.
4. `TotalSpend` by `HomePlanet`: equal location/central tendency across Earth, Europa, and Mars versus at least one group differing; Welch ANOVA and Kruskal-Wallis in KAN-27.

- [ ] **Step 6: Add an explicit scope-boundary cell**

State that the notebook deliberately does not calculate test statistics, p-values, intervals, effect sizes, post-hoc comparisons, or final conclusions; identify the Jira tickets that will perform each of those activities.

- [ ] **Step 7: Execute the notebook from a clean kernel**

Run every cell and retain outputs for the data shape, alpha, and categorical contract summary. Confirm that the notebook has no test statistic or p-value output.

- [ ] **Step 8: Validate notebook structure and contents**

Run:

```powershell
python -c "import nbformat; p='notebooks/04_testes_hipoteses_anova.ipynb'; nb=nbformat.read(p, as_version=4); assert nb.nbformat == 4; assert any('KAN-24' in ''.join(cell.source) for cell in nb.cells); print(f'{p}: {len(nb.cells)} cells, valid nbformat v4')"
```

Expected: successful validation with a nonzero number of cells.

- [ ] **Step 9: Review the rendered notebook**

Confirm the teaching narrative introduces each concept before its use, all four planned questions have H0/H1, all statements use the processed training data, and no conclusions are made from unexecuted tests.

- [ ] **Step 10: Commit the delivery**

```powershell
git add notebooks/04_testes_hipoteses_anova.ipynb
git commit -m "[KAN-24] Definir hipóteses estatísticas antes dos testes"
```

## Self-Review

- Spec coverage: the plan creates the specified notebook; writes formal H0/H1 for all four required questions; fixes alpha at 0.05; uses the KAN-12 derived dataset; and makes the methodology available for the three dependent tickets.
- Step scan: each notebook section has an assigned implementation and verification action. There is no software feature requiring a failing automated test, so notebook execution and `nbformat` validation are the appropriate reproducibility checks.
- Type consistency: the plan consistently references `HomePlanet`, `CryoSleep`, `TotalSpend`, and `Transported` as the data contract.
- Review focus: the data-contract cell covers missing columns, category validation, and use of the labelled processed dataset; the final scope review prevents inference from being moved into KAN-24.
- Proportion: one notebook is created, with no refactoring or changes outside the ticket's direct scope.
