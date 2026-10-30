# KAN-25 Categorical Associations Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend the hypothesis notebook with reproducible Pearson chi-square analyses and Cramer's V interpretations for the three categorical predictors specified in KAN-25.

**Architecture:** Add a self-contained KAN-25 section to `notebooks/04_testes_hipoteses_anova.ipynb`, after the KAN-24 pre-registration. A small reusable notebook function will create a contingency table, calculate expected counts, verify the expected-frequency assumption, run `scipy.stats.chi2_contingency`, calculate Cramer's V, and present a result table plus a written interpretation for each predictor.

**Tech Stack:** Python 3.10+, Jupyter Notebook, pandas, NumPy, SciPy 1.10+.

**Spec:** Jira KAN-25, "Testar associação entre variáveis categóricas"; KAN-24 hypotheses in `notebooks/04_testes_hipoteses_anova.ipynb`.

## Global Constraints

- Use only `data/processed/spaceship_titanic_clean.csv`, the processed labelled training dataset.
- Analyse exactly `HomePlanet`, `CryoSleep`, and `VIP` against `Transported`.
- Use Pearson's chi-square independence test through `scipy.stats.chi2_contingency` with `correction=False`; the Jira ticket requests Pearson's statistic and the sample is large.
- Verify and report the expected-frequency requirement: every expected cell frequency must be greater than 5.
- Report observed contingency tables, expected frequencies, chi-square statistic, degrees of freedom, p-value, sample size, Cramer's V, and a practical-strength interpretation.
- Retain `alpha = 0.05` defined in KAN-24 and state reject/do-not-reject decisions without saying that non-rejection proves independence.
- Interpret Cramer's V as weak below 0.10, medium from 0.10 inclusive to below 0.30, and strong from 0.30 inclusive; label thresholds as project communication conventions, not universal laws.
- Keep the subsequent scope separate: KAN-26 and KAN-27 own continuous-outcome tests, intervals, and their effect sizes.
- Write explanatory material in Portuguese and preserve outputs in the executed notebook.
- Follow repository governance: branch `feature/daniela-associacao-categoricas`, Portuguese commits beginning with `[KAN-25]`, PR review by Renatta.

## Review Focus

- Pearson versus Yates: each 2x2 table must explicitly use `correction=False`, otherwise SciPy applies a continuity correction by default and reports a different statistic.
- Expected-count assumption: a result must surface the minimum expected frequency and whether all cells exceed 5 rather than silently assuming the condition holds.
- Cramer's V denominator: use `N * min(r - 1, c - 1)` from the observed table; do not use the number of cells or a fixed binary denominator.
- Variable orientation: `Transported` must remain the columns in each table so rates are directly comparable across predictor categories.
- Interpretation: distinguish statistical evidence (`p < alpha`) from practical magnitude (Cramer's V), especially because the large sample can make weak associations statistically significant.

---

### Task 1: Implement The KAN-25 Notebook Analysis

**Files:**
- Modify: `notebooks/04_testes_hipoteses_anova.ipynb`

**Interfaces:**
- Consumes: the `df` DataFrame and `alpha` scalar created by the KAN-24 setup cell.
- Produces: `analisar_associacao_categorica(df, predictor, outcome='Transported', alpha=0.05) -> dict` and executed notebook sections covering all three required associations.

- [ ] **Step 1: Write a failing notebook-validation command**

Run a Python one-liner that loads the notebook with `nbformat`, asserts the analysis function and all three predictor names occur in source, and asserts all code cells have executed without outputs of type `error`.

- [ ] **Step 2: Verify the validation fails before KAN-25 exists**

Run the command from step 1.

Expected: assertion failure because `analisar_associacao_categorica` is absent.

- [ ] **Step 3: Add a teaching section for Pearson chi-square and Cramer's V**

Explain observed versus expected frequencies, the independence model, expected-frequency condition, chi-square statistic, p-value, degrees of freedom, and why effect size must accompany statistical significance.

- [ ] **Step 4: Add `analisar_associacao_categorica`**

Import `chi2_contingency` from `scipy.stats`. The function must form `pd.crosstab(df[predictor], df[outcome])`; call `chi2_contingency(observed, correction=False)`; create labelled expected-frequency and result DataFrames; calculate Cramer's V using the Jira formula; classify it under the project thresholds; and return all artifacts plus an `assumption_met` boolean.

- [ ] **Step 5: Add and execute three analysis sections**

Run the function for `HomePlanet`, `CryoSleep`, and `VIP`. For each, display observed and expected tables, report the minimum expected frequency, chi-square, df, p-value, Cramer's V, and formal decision relative to alpha. Explain the result in both statistical and practical terms without implying causation.

- [ ] **Step 6: Add a KAN-25 summary section**

Create a single DataFrame with one row per predictor and columns for `chi2`, `df`, `p_value`, `cramers_v`, `forca_pratica`, `min_frequencia_esperada`, `pressuposto_atendido`, and `decisao`. Follow it with a concise prose synthesis that differentiates evidence of association from its strength.

- [ ] **Step 7: Execute the notebook from a clean kernel**

Run:

```powershell
jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=120 notebooks/04_testes_hipoteses_anova.ipynb
```

Expected: execution completes without cell errors and stores results in the notebook.

- [ ] **Step 8: Run the KAN-25 notebook validation command**

Run the command created in step 1 plus checks that no expected frequency is at or below 5 and no code-cell output reports an error.

Expected: validation passes.

- [ ] **Step 9: Review numeric outputs against direct recomputation**

Run an independent Python command reading the processed CSV and recomputing each `chi2_contingency(..., correction=False)` result. Confirm all reported notebook values agree after displayed rounding.

- [ ] **Step 10: Commit the delivery**

```powershell
git add notebooks/04_testes_hipoteses_anova.ipynb
git commit -m "[KAN-25] Testar associação entre variáveis categóricas"
```

## Self-Review

- Spec coverage: all three Jira-specified predictors, Pearson chi-square, expected frequencies, chi-square, df, p-value, Cramer's V, and statistical/practical interpretation are covered in Task 1.
- Step scan: the task has one notebook deliverable with an explicit RED validation, notebook execution, independent numeric recomputation, and a commit.
- Type consistency: the analysis function returns all tables and scalar metrics required by the summary and narrative sections.
- Review focus: direct validation and review steps cover correction choice, expected frequencies, Cramer's V denominator, table orientation, and distinct statistical/practical interpretation.
- Proportion: one existing notebook is extended; no unnecessary scripts, dependencies, or separate data artifacts are introduced.
