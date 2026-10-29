# KAN-28 & KAN-29 Tabela-Resumo e Conclusões dos Testes de Hipóteses Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Complete the remaining hypothesis testing tasks allocated to Daniela Amaro:
1. **KAN-28:** Consolidate all statistical hypothesis tests and ANOVAs into a structured pandas summary table containing strictly 9 normative columns and export to Markdown within `notebooks/04_testes_hipoteses_anova.ipynb`.
2. **KAN-29:** Author and publish the executive technical conclusions report in `docs/conclusoes/04_testes_hipoteses_anova.md` with dedicated sections for each test, full summary table, explicit discussion of effect sizes, and a rigorous epistemological warning that statistical association does not imply direct causality.
3. Update Jira dependency map (`src/gerar_mapa_dependencias.py`) to reflect Luciana's completed work (KAN-19 Done) and Daniela's submissions (KAN-28 and KAN-29 In Review).
4. Submit branches, open Pull Requests, and transition Jira issues to "In Review".

**Architecture:**
- Extend `notebooks/04_testes_hipoteses_anova.ipynb` with Section 15 and 16.
- Create automated pytest test `tests/test_kan28.py` asserting all 9 columns and exact test statistics.
- Create Markdown publication `docs/conclusoes/04_testes_hipoteses_anova.md`.
- Regenerate visual dependency maps in `docs/` via `src/gerar_mapa_dependencias.py`.

**Tech Stack:** Python 3.10+, Jupyter Notebook, pandas, SciPy, nbformat, nbclient, pytest, matplotlib, Mermaid.js, Graphviz.

---

### Task 1: Implement KAN-28 Summary Table in Notebook and Automated Tests
- [x] Create branch `feature/daniela-tabela-resumo-hipoteses` from `feature/daniela-gastos-origem`
- [x] Add Sections 15 & 16 to `notebooks/04_testes_hipoteses_anova.ipynb` with 10 rows and 9 normative columns
- [x] Create automated test `tests/test_kan28.py` and verify all tests pass (`pytest tests/ -v`)
- [x] Commit changes: `[KAN-28] Criar tabela-resumo consolidada dos testes de hipoteses e ANOVA`

### Task 2: Implement KAN-29 Technical Conclusions Markdown
- [x] Create branch `docs/daniela-conclusoes-testes-hipoteses` from `feature/daniela-tabela-resumo-hipoteses`
- [x] Author comprehensive conclusions report in `docs/conclusoes/04_testes_hipoteses_anova.md` with:
  - Notebook traceability mapping
  - Dedicated sections for categorical associations, TotalSpend comparisons, and HomePlanet Welch ANOVA
  - Formatted 9-column summary table
  - Prominent section on association vs causality (intervening variables like CryoSleep)
  - Strategic executive recommendations

### Task 3: Update Jira Dependency Map and Assets
- [ ] Update `src/gerar_mapa_dependencias.py`:
  - KAN-19 status: `'Concluído'` (Luciana completed on Jira)
  - KAN-28 status: `'In Review'`
  - KAN-29 status: `'In Review'`
- [ ] Regenerate `docs/mapa_dependencias_jira.png`, `.mmd`, `.dot`, and `.md` via script execution

### Task 4: Git Push, PRs, and Jira Governance
- [ ] Push branches `feature/daniela-tabela-resumo-hipoteses` and `docs/daniela-conclusoes-testes-hipoteses`
- [ ] Open PR for KAN-28 (base: `feature/daniela-gastos-origem`) and assign reviewer Renatta
- [ ] Open PR for KAN-29 (base: `feature/daniela-tabela-resumo-hipoteses`) and assign reviewer Renatta
- [ ] Transition Jira issues KAN-28 and KAN-29 to "In Review" (transition id 31) with governance comments
