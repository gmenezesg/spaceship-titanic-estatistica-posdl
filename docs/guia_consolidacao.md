# Guia de Consolidação dos Notebooks (`KAN-37`)

O notebook final `notebooks/00_projeto_final_estatistica.ipynb` é **gerado exclusivamente** pelo script [`src/consolidar_notebooks.py`](../src/consolidar_notebooks.py) (e pela Skill `consolidar-notebooks`), a partir dos notebooks de cada ticket/trilha na ordem e mapeamento definidos em [`notebooks/consolidacao.json`](../notebooks/consolidacao.json), em conformidade com os objetivos de `docs/T3 Projeto Final Estatística PosDL.docx`.

---

## Regras de Governança

1. **Cada ticket Jira (`KAN-XX`) tem como alvo seu próprio notebook de origem** mapeado em `notebooks/consolidacao.json`. Todos os notebooks das trilhas analíticas (Seções 2 a 5) leem apenas a base tratada `data/processed/spaceship_titanic_clean.csv` e nunca repetem a preparação dos dados.
2. **Proibido editar `notebooks/00_projeto_final_estatistica.ipynb` manualmente.** Qualquer alteração ou correção deve ser feita no notebook de origem do ticket correspondente e consolidada via Skill `consolidar-notebooks` / `src/consolidar_notebooks.py`.
3. **Mapeamento centralizado em `notebooks/consolidacao.json`.** Para consultar, incluir ou reordenar o mapeamento entre tickets Jira e notebooks, utilize o manifesto `notebooks/consolidacao.json`.
4. **Consolidação obrigatória ao fim de cada ticket Jira.** Ao concluir a implementação de qualquer ticket do Jira, execute a Skill `consolidar-notebooks` (ou o comando abaixo) para atualizar e validar o `00_projeto_final_estatistica.ipynb`.

---

## Mapa de Tickets Analíticos $\rightarrow$ Notebooks (`notebooks/consolidacao.json`)

| Seção T3 | Tickets Jira | Notebook(s) de Origem | Conclusão Markdown |
| :--- | :--- | :--- | :--- |
| **1. Contexto, Saneamento e Engenharia de Atributos** | `KAN-10`, `KAN-11`, `KAN-12` | `notebooks/01_preparacao_dados.ipynb` | `docs/conclusoes/01_ambiente_dados.md` (`KAN-13`) |
| **2. Análise Descritiva e Visualização** | `KAN-15`<br>`KAN-17`<br>`KAN-14`, `KAN-16` | `notebooks/04_kan15_resumos_quantitativos.ipynb`<br>`notebooks/03_kan17_valores_extremos.ipynb`<br>`notebooks/02_estatistica_descritiva.ipynb` | `docs/conclusoes/02_descritiva_visual.md` (`KAN-18`) |
| **3. Probabilidade e Distribuições** | `KAN-19`<br>`KAN-20`, `KAN-21`, `KAN-22` | `notebooks/05_kan19_variaveis_aleatorias_distribuicoes.ipynb`<br>`notebooks/03_probabilidade_distribuicoes.ipynb` | `docs/conclusoes/03_probabilidade_distribuicoes.md` (`KAN-23`) |
| **4. Testes de Hipóteses e ANOVA** | `KAN-24`, `KAN-25`, `KAN-26`, `KAN-27`, `KAN-28` | `notebooks/04_testes_hipoteses_anova.ipynb` | `docs/conclusoes/04_testes_hipoteses_anova.md` (`KAN-29`) |
| **5. Correlação, Regressão e Modelos Preditivos** | `KAN-30`, `KAN-31`, `KAN-32`, `KAN-33`, `KAN-34` | `notebooks/05_correlacao_regressoes.ipynb` | `docs/conclusoes/05_correlacao_regressoes.md` (`KAN-35`) |

---

## Como Usar

Na raiz do repositório, com o ambiente virtual ativo (`.venv`):

| Objetivo | Comando |
| :--- | :--- |
| Consultar o notebook-alvo de um ticket Jira específico | `python src/consolidar_notebooks.py --ticket KAN-19` |
| Validar integridade e completude do `notebooks/consolidacao.json` | `python src/consolidar_notebooks.py --validar-mapa` |
| Prévia com os notebooks já existentes (sem tocar no `00_`) | `python src/consolidar_notebooks.py --permitir-faltantes --saida notebooks/_previa_consolidado.ipynb` |
| Atualizar e executar o `00_projeto_final_estatistica.ipynb` com os notebooks disponíveis | `python src/consolidar_notebooks.py --permitir-faltantes --forcar --executar` |
| Gerar o notebook final oficial completo (exige todos os notebooks presentes) | `python src/consolidar_notebooks.py --forcar --executar` |

Arquivos de prévia (`notebooks/_previa*.ipynb`) servem apenas para conferência local e já estão ignorados no `.gitignore`.

---

## O que o Script e a Skill Garantem

- **Rastreabilidade e Validação de Mapa (`--validar-mapa` / `--ticket`):** valida se todos os 40 tickets do Jira (`KAN-4` a `KAN-43`) possuem mapeamento consistente em `notebooks/consolidacao.json`.
- **Objetividade alinhada ao T3 (`modo_objetivo`):** higieniza automaticamente metadados burocráticos repetitivos de PRs/tickets (tabelas administrativas de revisor/prioridade, checklists internos de card), mantendo 100% do rigor técnico, visualizações e interpretações de negócio exigidos por `docs/T3 Projeto Final Estatística PosDL.docx`.
- **Sem duplicação:** células de código equivalentes já incluídas são puladas automaticamente.
- **Exclusão explícita (`pular-consolidacao`):** células marcadas com a tag `pular-consolidacao` nos metadados da célula não entram no notebook final.
- **Preservação ou Execução Limpa (`--executar`):** preserva saídas pré-renderizadas quando executado de forma rápida ou executa integralmente do zero em kernel limpo (*Restart & Run All*) com `--executar`.
- **Auditoria T3:** verifica ausência de caminhos absolutos (`C:\...`, `/home/...`), presença de sementes aleatórias fixas (`seed(42)` / `random_state=42`) e equilíbrio entre células de código e interpretação em Markdown.
