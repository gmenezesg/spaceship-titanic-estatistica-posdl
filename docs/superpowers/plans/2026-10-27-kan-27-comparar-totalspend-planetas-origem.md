# KAN-27 Comparar TotalSpend entre Planetas de Origem Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the statistical comparison of `TotalSpend` across passenger origins (`HomePlanet`: Earth, Europa, Mars) in the project's official inferential notebook (`notebooks/04_testes_hipoteses_anova.ipynb`), providing didactic theory on topics not traditionally taught (Welch's ANOVA, Kruskal-Wallis, Games-Howell post-hoc, Dunn's test with Bonferroni correction, and effect sizes $\eta^2$ and $\epsilon^2$), LaTeX formulas, diagnostic plots, hypothesis testing, consolidated results table, and strategic business interpretation.

**Architecture:** Extend `notebooks/04_testes_hipoteses_anova.ipynb` by adding dedicated analytical sections for KAN-27 following the established KAN-24, KAN-25, and KAN-26 standards. All calculations consume `data/processed/spaceship_titanic_clean.csv`. A verification test (`tests/test_kan27.py`) will execute the notebook end-to-end to ensure reproducibility and validate exact numerical contracts.

**Tech Stack:** Python 3.10+, Jupyter Notebook (`nbformat`, `nbclient`), pandas, NumPy, SciPy (`scipy.stats.levene`, `scipy.stats.kruskal`, `scipy.stats.f`, `scipy.stats.studentized_range`, `scipy.stats.norm`), matplotlib, seaborn.

**Spec:** Jira KAN-27, "Comparar TotalSpend entre planetas de origem".

## Global Constraints

- Use processed training data `data/processed/spaceship_titanic_clean.csv` (8,693 rows x 22 columns).
- Pre-fixed significance level $\alpha = 0.05$.
- Test for homoscedasticity: Levene's test centered at the median (`center='median'`, Brown-Forsythe).
- Primary omnibus test: One-Way Welch's ANOVA (accounting for unequal variances and sample sizes).
- Complementary omnibus test: Kruskal-Wallis $H$ test (robustness check on ranks).
- Pairwise Post-Hoc:
  - Primary: Games-Howell test (for Welch's ANOVA, pairwise Welch t-statistics with Welch-Satterthwaite df and Studentized Range distribution).
  - Complementary: Dunn's test with Bonferroni correction for FWER control on rank differences.
- Effect sizes:
  - $\eta^2$ (Eta-squared) and $\omega^2$ (Omega-squared) for Welch's ANOVA.
  - $\epsilon^2$ (Epsilon-squared) for Kruskal-Wallis.
- Adhere to Git conventions: branch `feature/daniela-gastos-origem`, commit prefix `[KAN-27]`, PR review assigned to Renatta.

## Review Focus

- Didactic explanation of non-standard topics: explain why standard Fisher's ANOVA fails under heteroscedasticity and why Welch's weighted formulation resolves the issue.
- Mathematical rigor: Welch $F$-statistic, Welch-Satterthwaite degrees of freedom ($df_1, df_2$), Games-Howell pairwise Studentized Range statistic ($q = \sqrt{2} \cdot t$) and critical values.
- Pairwise comparisons: all 3 pairs (Earth vs Europa, Earth vs Mars, Europa vs Mars) must report difference, standard error, test statistic, adjusted p-value, and 95% confidence intervals.
- Business synthesis: explain the luxury/affluence profile of Europa versus economy profile of Earth and intermediate profile of Mars, connecting to amenity consumption and mission operations.

---

### Task 1: Setup Branch and Implementation Plan

**Files:**
- Branch: `feature/daniela-gastos-origem` created from `feature/daniela-gastos-teletransporte`
- Plan: `docs/superpowers/plans/2026-10-27-kan-27-comparar-totalspend-planetas-origem.md`

- [x] **Step 1: Create and checkout branch `feature/daniela-gastos-origem`**
- [x] **Step 2: Document implementation plan and numerical contracts**

---

### Task 2: Implement KAN-27 Sections in `04_testes_hipoteses_anova.ipynb`

**Files:**
- Modify: `notebooks/04_testes_hipoteses_anova.ipynb`

**Interfaces:**
- Consumes: `df['TotalSpend']`, `df['HomePlanet']` from loaded dataset
- Produces: Formatted tables, figures, Levene test results, Welch ANOVA results ($F$, $df_1$, $df_2$, $p$, $\eta^2$), Kruskal-Wallis results ($H$, $df$, $p$, $\epsilon^2$), Games-Howell post-hoc table with 95% CI, Dunn post-hoc table with Bonferroni correction, and consolidated summary table.

- [ ] **Step 1: Add Markdown teaching section for Question 4 (KAN-27)**
  Explain the theoretical gap of classical Fisher ANOVA under heteroscedasticity, the mechanics of Welch ANOVA (weights, adjusted df), Kruskal-Wallis, Games-Howell post-hoc, and Dunn-Bonferroni.
- [ ] **Step 2: Add code cell for descriptive diagnostics and Levene test across the 3 planets**
  Compute sample size, mean, std, median, IQR, zero-spending %, and execute `scipy.stats.levene(..., center='median')`.
- [ ] **Step 3: Add code cell for One-Way Welch's ANOVA and effect sizes ($\eta^2$, $\omega^2$)**
  Implement Welch (1951) $F$ test, compute exact $F$, $df_1$, $df_2$, $p$-value, $\eta^2$ and $\omega^2$.
- [ ] **Step 4: Add code cell for Kruskal-Wallis and Epsilon-squared ($\epsilon^2$)**
  Execute `scipy.stats.kruskal`, calculate $H$, $p$-value, and $\epsilon^2 = H / (N - 1)$.
- [ ] **Step 5: Add code cell for Games-Howell Post-Hoc comparisons with 95% CI**
  Compute pairwise difference, Welch SE, df, Studentized Range $q$, p-value, and 95% CI for all 3 pairs.
- [ ] **Step 6: Add code cell for Dunn's Post-Hoc test with Bonferroni correction**
  Compute mean ranks, pairwise rank difference, tie-corrected standard error, $Z$ statistics, and Bonferroni-adjusted p-values.
- [ ] **Step 7: Add code cell consolidating KAN-27 results into a styled summary table**
- [ ] **Step 8: Add Markdown synthesis and strategic business interpretation section**

---

### Task 3: Verification and Automated Notebook Execution

**Files:**
- Create: `tests/test_kan27.py`

- [ ] **Step 1: Write test script executing notebook end-to-end via `nbclient.NotebookClient`**
- [ ] **Step 2: Assert presence of all KAN-27 statistics, tables, and exact numerical contracts**
- [ ] **Step 3: Execute `pytest tests/test_kan27.py` and verify all tests pass**

---

### Task 4: Commit, Push, Open PR and Update Jira

**Files:**
- Notebook: `notebooks/04_testes_hipoteses_anova.ipynb`
- Test: `tests/test_kan27.py`
- Plan: `docs/superpowers/plans/2026-10-27-kan-27-comparar-totalspend-planetas-origem.md`

- [ ] **Step 1: Commit changes with message `[KAN-27] Comparar TotalSpend entre planetas de origem com Welch ANOVA e Kruskal-Wallis`**
- [ ] **Step 2: Push branch `feature/daniela-gastos-origem` to origin**
- [ ] **Step 3: Open Pull Request via `gh pr create` with base `feature/daniela-gastos-teletransporte` and assign reviewer Renatta**
- [ ] **Step 4: Transition Jira issue KAN-27 to "In Review" and post governance comment**
