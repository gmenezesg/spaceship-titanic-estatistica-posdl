# KAN-26 Comparar TotalSpend por Transported Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the statistical comparison of `TotalSpend` by `Transported` in the project's official inferential notebook (`notebooks/04_testes_hipoteses_anova.ipynb`), providing didactic theory, LaTeX formulas, Levene's test, Welch's t-test (primary with 95% CI and Cohen's d), Mann-Whitney U test (complementary with Rosenthal's r), and business insights.

**Architecture:** Extend `notebooks/04_testes_hipoteses_anova.ipynb` by adding dedicated analytical sections for KAN-26 following the established KAN-24 and KAN-25 format. All calculations consume `data/processed/spaceship_titanic_clean.csv`. A verification script will execute the notebook end-to-end to ensure reproducibility and validate exact numerical contracts.

**Tech Stack:** Python 3.10+, Jupyter Notebook (`nbformat`, `nbclient`), pandas, NumPy, SciPy (`scipy.stats.levene`, `scipy.stats.ttest_ind`, `scipy.stats.mannwhitneyu`), matplotlib, seaborn.

**Spec:** Jira KAN-26, "Comparar TotalSpend por Transported".

## Global Constraints

- Use processed training data `data/processed/spaceship_titanic_clean.csv` (8,693 rows x 22 columns).
- Pre-fixed significance level $\alpha = 0.05$.
- Primary test: Welch's t-test (`equal_var=False`) with 95% confidence interval and Cohen's d.
- Complementary test: Mann-Whitney U test with Rosenthal's r ($|Z| / \sqrt{N}$).
- Pre-requisite assumption test: Levene's test centered at the median (`center='median'`, Brown-Forsythe).
- Adhere to Git conventions: branch `feature/daniela-gastos-teletransporte`, commit prefix `[KAN-26]`, PR review assigned to Renatta.

## Review Focus

- Correct Levene variant: must use `center='median'` due to extreme skewness and zero-inflation.
- Correct Welch parameter: `scipy.stats.ttest_ind` must explicitly pass `equal_var=False`.
- Degree of freedom calculation: Welch-Satterthwaite formula must match the fractional df output by Welch's t-test.
- Two-sided test: Mann-Whitney must use `alternative='two-sided'`.
- Effect size formulas: Cohen's d using pooled standard deviation; Rosenthal's r using $Z / \sqrt{N}$.

---

### Task 1: Setup Branch and Synchronize Hypothesis Definitions

**Files:**
- Branch: create `feature/daniela-gastos-teletransporte` from `feature/daniela-associacao-categoricas`
- Modify: `notebooks/04_testes_hipoteses_anova.ipynb` (ensure cells 8-10 incorporate PR #6 review updates)

- [ ] **Step 1: Create and checkout branch `feature/daniela-gastos-teletransporte`**
- [ ] **Step 2: Sync cells 8-10 with latest KAN-24 review adjustments from commit `e775cfc`**
- [ ] **Step 3: Verify clean notebook read via nbformat**

---

### Task 2: Implement KAN-26 Sections in `04_testes_hipoteses_anova.ipynb`

**Files:**
- Modify: `notebooks/04_testes_hipoteses_anova.ipynb`

**Interfaces:**
- Consumes: `df['TotalSpend']`, `df['Transported']` from loaded dataset
- Produces: Formatted tables, figures, Levene test results, Welch t-test results (t, df, p-value, 95% CI, Cohen's d), Mann-Whitney U results (U, Z, p-value, Rosenthal's r), and consolidated synthesis DataFrame.

- [ ] **Step 1: Add Markdown teaching section for Question 3**
Explain why traditional Student t-test fails under heteroscedasticity, the role of Central Limit Theorem for Welch t-test, and the role of Mann-Whitney U as a complementary rank-based robustness check.

- [ ] **Step 2: Add code cell for descriptive diagnostics and Levene test**
Calculate sample size, mean, std, median, IQR, zero percentage, and execute `scipy.stats.levene(..., center='median')`.

- [ ] **Step 3: Add code cell for Welch's t-test, 95% CI, and Cohen's d**
Run `scipy.stats.ttest_ind(..., equal_var=False)`. Compute Welch-Satterthwaite degrees of freedom, 95% confidence interval for $(\mu_{\text{False}} - \mu_{\text{True}})$, and Cohen's $d$.

- [ ] **Step 4: Add code cell for Mann-Whitney U test and Rosenthal's r**
Run `scipy.stats.mannwhitneyu(..., alternative='two-sided')`. Compute asymptotic $Z$ score and Rosenthal's $r = |Z| / \sqrt{N}$.

- [ ] **Step 5: Add code cell consolidating KAN-26 results into a styled summary table**
Display comparative summary with columns: Teste, Parametro, Estatistica, p-valor, IC 95%, Tamanho do Efeito, Classificacao e Decisao.

- [ ] **Step 6: Add Markdown synthesis and business interpretation section**
Explain the economic findings and why `CryoSleep` accounts for the observed difference.

---

### Task 3: Verification and End-to-End Notebook Execution

**Files:**
- Test: Notebook execution via `nbclient.NotebookClient`

- [ ] **Step 1: Execute all cells in `04_testes_hipoteses_anova.ipynb` from clean kernel**
- [ ] **Step 2: Verify all outputs are generated without any errors or NaNs**
- [ ] **Step 3: Verify numerical consistency with KAN-24 hypotheses**

---

### Task 4: Commit, Push, Open PR and Update Jira

**Files:**
- Plan: `docs/superpowers/plans/2026-10-26-kan-26-comparar-totalspend-transported.md`
- Notebook: `notebooks/04_testes_hipoteses_anova.ipynb`

- [ ] **Step 1: Commit changes with message `[KAN-26] Comparar TotalSpend por Transported com Welch e Mann-Whitney`**
- [ ] **Step 2: Push branch `feature/daniela-gastos-teletransporte` to origin**
- [ ] **Step 3: Open Pull Request with detailed description and assign Renatta as reviewer**
- [ ] **Step 4: Transition Jira issue KAN-26 and log governance comment**
