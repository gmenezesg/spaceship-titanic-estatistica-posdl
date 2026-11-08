# Guia de Consolidação dos Notebooks (`KAN-37`)

O notebook final `notebooks/00_projeto_final_estatistica.ipynb` é **gerado exclusivamente** pelo script [`src/consolidar_notebooks.py`](../src/consolidar_notebooks.py) (e pela Skill `consolidar-notebooks`), a partir dos notebooks de cada ticket/trilha na ordem e mapeamento definidos em [`notebooks/consolidacao.json`](../notebooks/consolidacao.json), em conformidade com os objetivos de `docs/T3 Projeto Final Estatística PosDL.docx`.

---

## Regras de Governança

1. **Cada ticket Jira (`KAN-XX`) tem como alvo seu próprio notebook de origem** mapeado em `notebooks/consolidacao.json`. Todos os notebooks das trilhas analíticas (Seções 2 a 5) leem apenas a base tratada `data/processed/spaceship_titanic_clean.csv` e nunca repetem a preparação dos dados.
2. **Proibido editar `notebooks/00_projeto_final_estatistica.ipynb` manualmente ou alterá-lo em PRs de tickets individuais.** Qualquer implementação ou correção deve ser feita apenas no notebook de origem do ticket correspondente.
3. **Mapeamento centralizado em `notebooks/consolidacao.json`.** Para consultar, incluir ou reordenar o mapeamento entre tickets Jira e notebooks, utilize o manifesto `notebooks/consolidacao.json` e valide com `python src/consolidar_notebooks.py --validar-mapa`.
4. **Conformidade em todos os commits e consolidação sob demanda no final do projeto (`KAN-37`).** Cada commit de notebook de origem deve estar 100% conforme (zero caminhos absolutos no código e nas saídas, semente `42` fixada e execução limpa *Restart & Run All*). A geração do `00_projeto_final_estatistica.ipynb` via Skill `consolidar-notebooks` ocorre **apenas sob demanda** no fechamento do projeto (`KAN-37` / `KAN-43`) ou quando solicitada explicitamente, garantindo uma consolidação única e sem conflitos.

---

## Mapa de Tickets Analíticos $\rightarrow$ Notebooks (`notebooks/consolidacao.json`)

| Seção T3 | Tickets Jira | Notebook(s) de Origem | Conclusão Markdown |
| :--- | :--- | :--- | :--- |
| **1. Contexto, Saneamento e Engenharia de Atributos** | `KAN-10`, `KAN-11`, `KAN-12` | `notebooks/01_preparacao_dados.ipynb` | `docs/conclusoes/01_ambiente_dados.md` (`KAN-13`) |
| **2. Análise Descritiva e Visualização** | `KAN-14`<br>`KAN-15`<br>`KAN-17`<br>`KAN-16` | `notebooks/02_estatistica_descritiva.ipynb`<br>`notebooks/04_kan15_resumos_quantitativos.ipynb`<br>`notebooks/03_kan17_valores_extremos.ipynb` | `docs/conclusoes/02_descritiva_visual.md` (`KAN-18`) |
| **3. Probabilidade e Distribuições** | `KAN-19`<br>`KAN-20`, `KAN-21`, `KAN-22` | `notebooks/05_kan19_variaveis_aleatorias_distribuicoes.ipynb`<br>`notebooks/03_probabilidade_distribuicoes.ipynb` | `docs/conclusoes/03_probabilidade_distribuicoes.md` (`KAN-23`) |
| **4. Testes de Hipóteses e ANOVA** | `KAN-24`, `KAN-25`, `KAN-26`, `KAN-27`, `KAN-28` | `notebooks/04_testes_hipoteses_anova.ipynb` | `docs/conclusoes/04_testes_hipoteses_anova.md` (`KAN-29`) |
| **5. Correlação, Regressão e Modelos Preditivos** | `KAN-30`, `KAN-31`, `KAN-32`, `KAN-33`, `KAN-34` | `notebooks/05_correlacao_regressoes.ipynb` | `docs/conclusoes/05_correlacao_regressoes.md` (`KAN-35`) |
| **6. Conclusões e Recomendações Práticas** | `KAN-44` | `notebooks/06_conclusoes_recomendacoes.ipynb` | `docs/conclusoes/06_conclusoes_recomendacoes.md` (`KAN-44`) |

---

## Como Usar

Na raiz do repositório, com o ambiente virtual ativo (`.venv`):

| Objetivo | Comando |
| :--- | :--- |
| Consultar o notebook-alvo de um ticket Jira específico | `.venv/bin/python src/consolidar_notebooks.py --ticket KAN-19` |
| Validar integridade, completude e existência dos arquivos do `notebooks/consolidacao.json` | `.venv/bin/python src/consolidar_notebooks.py --validar-mapa` |
| Prévia com os notebooks já existentes (sem tocar no `00_`) | `.venv/bin/python src/consolidar_notebooks.py --permitir-faltantes --saida notebooks/_previa_consolidado.ipynb` |
| Prévia executada com os notebooks disponíveis (sem tocar no `00_`) | `.venv/bin/python src/consolidar_notebooks.py --permitir-faltantes --forcar --executar --saida notebooks/_previa_consolidado.ipynb` |
| Gerar o notebook final oficial completo (exige todos os notebooks presentes) | `.venv/bin/python src/consolidar_notebooks.py --forcar --executar` |

Arquivos de prévia (`notebooks/_previa*.ipynb`) servem apenas para conferência local e já estão ignorados no `.gitignore`.

**Validação de existência.** O `--validar-mapa` verifica duas coisas: a consistência estrutural do manifesto e a **existência física** dos arquivos citados (notebooks e conclusões das seções, artefatos extras por ticket, notebooks de origem e arquivos de `mapa_reparos`). Ele retorna código 1 e lista cada arquivo ausente. Essa checagem roda apenas nesse modo: o `--permitir-faltantes` continua permitindo gerar a prévia quando um notebook ainda não existe.

---

## O que o Script e a Skill Garantem

- **Rastreabilidade e Validação de Mapa (`--validar-mapa` / `--ticket`):** valida se todos os 41 tickets do Jira (`KAN-4` a `KAN-44`) possuem mapeamento consistente em `notebooks/consolidacao.json` e se os arquivos citados existem no repositório.
- **Objetividade alinhada ao T3 (`modo_objetivo`):** higieniza automaticamente metadados burocráticos repetitivos de PRs/tickets (tabelas administrativas de revisor/prioridade, checklists internos de card), mantendo 100% do rigor técnico, visualizações e interpretações de negócio exigidos por `docs/T3 Projeto Final Estatística PosDL.docx`.
- **Sem duplicação:** células de código equivalentes já incluídas são puladas automaticamente.
- **Exclusão explícita (`pular-consolidacao`):** células marcadas com a tag `pular-consolidacao` nos metadados da célula não entram no notebook final.
- **Preservação ou Execução Limpa (`--executar`):** preserva saídas pré-renderizadas quando executado de forma rápida ou executa integralmente do zero em kernel limpo (*Restart & Run All*) com `--executar`.
- **Auditoria T3:** verifica ausência de caminhos absolutos (`C:\...`, `/home/...`), presença de sementes aleatórias fixas (`seed(42)` / `random_state=42`) e equilíbrio entre células de código e interpretação em Markdown.
