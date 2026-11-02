# Regras Globais para Agentes de IA (`AGENTS.md`)

Este repositório possui regras obrigatórias de governança para todos os agentes de codificação (Antigravity, Claude Code, OpenCode, Cursor, GitHub Copilot, Windsurf, etc.). O cumprimento integral destas diretrizes é mandatório em todas as interações.

> **Fonte Única da Verdade (`.agents/`):** Todas as regras detalhadas e skills deste projeto residem exclusivamente em [`.agents/rules/`](.agents/rules/) e [`.agents/skills/`](.agents/skills/):
> - [`.agents/rules/planejamento-obrigatorio.md`](.agents/rules/planejamento-obrigatorio.md)
> - [`.agents/rules/governanca-notebooks-consolidacao.md`](.agents/rules/governanca-notebooks-consolidacao.md)
> - [`.agents/rules/objetivos-gerais-t3.md`](.agents/rules/objetivos-gerais-t3.md)
> - [`.agents/rules/padrao-rules-e-skills.md`](.agents/rules/padrao-rules-e-skills.md)
> - [`.agents/skills/consolidar-notebooks/SKILL.md`](.agents/skills/consolidar-notebooks/SKILL.md)

---

## Regra 1: Planejamento Obrigatório Antes de Qualquer Tarefa

1. **Planeje Sempre Antes de Executar:** Nenhum agente deve iniciar a escrita ou edição de código, notebooks ou documentação sem antes investigar o contexto e elaborar um plano estruturado de execução.
2. **Passos Obrigatórios do Planejamento:**
   - Identificar o ticket do Jira correspondente (`KAN-XX`) e consultar seu mapeamento exato em [`notebooks/consolidacao.json`](notebooks/consolidacao.json) executando:
     ```bash
     python src/consolidar_notebooks.py --ticket KAN-XX
     ```
   - Verificar os objetivos analíticos e critérios de avaliação exigidos em `docs/T3 Projeto Final Estatística PosDL.docx` (30% qualidade técnica, 50% clareza e objetividade, 20% organização e reprodutibilidade do notebook).
   - Apresentar ao usuário um plano conciso e objetivo (arquivos-alvo, etapas técnicas e validação) antes de aplicar alterações.

---

## Regra 2: Isolamento por Notebook, Conformidade por Commit e Consolidação Sob Demanda (`notebooks/00_projeto_final_estatistica.ipynb`)

1. **Cada Ticket Jira Altera Apenas Seu Próprio Notebook/Artefato de Origem:**
   - Toda implementação de funcionalidade ou análise estatística vinda do Jira (`https://megamatic.atlassian.net/jira/software/projects/KAN/boards/2`) deve ter como alvo **exclusivamente** o seu próprio arquivo mapeado em [`notebooks/consolidacao.json`](notebooks/consolidacao.json).
   - Notebooks das trilhas analíticas (Seções 2 a 5) devem consumir apenas a base tratada `data/processed/spaceship_titanic_clean.csv`, sem repetir o pipeline de limpeza da Seção 1 (`notebooks/01_preparacao_dados.ipynb`).

2. **Proibição Absoluta de Edição Manual ou Alteração Prematura de `notebooks/00_projeto_final_estatistica.ipynb`:**
   - O arquivo principal [`notebooks/00_projeto_final_estatistica.ipynb`](notebooks/00_projeto_final_estatistica.ipynb) **NUNCA** deve ser editado diretamente (nem por ferramentas de edição de arquivo/notebook, nem manualmente) e **não deve ser modificado nos commits/PRs de tickets individuais das trilhas**.
   - O arquivo `notebooks/00_projeto_final_estatistica.ipynb` **só pode ser gerado/atualizado sob demanda pela Skill `consolidar-notebooks` (através do script [`src/consolidar_notebooks.py`](src/consolidar_notebooks.py))**.

3. **Conformidade Obrigatória em Todos os Commits e Consolidação Sob Demanda no Final do Projeto (`KAN-37`):**
   - **Em todo commit/ticket Jira:** garanta que o notebook de origem esteja 100% pronto para a consolidação futura (zero caminhos absolutos no código e nas saídas/prints, `seed(42)` fixada, execução limpa *Restart & Run All* do próprio notebook e manifesto validado com `python src/consolidar_notebooks.py --validar-mapa`).
   - **Execução da Skill `consolidar-notebooks` apenas sob demanda:** a consolidação oficial (`python src/consolidar_notebooks.py --forcar --executar`) **só deve ser executada no final do projeto (`KAN-37` / `KAN-43`) ou quando explicitamente solicitada pelo usuário**, garantindo que ocorra de uma só vez e sem conflitos entre PRs.

---

## Regra 3: Observância Obrigatória aos Objetivos Gerais do `T3 Projeto Final Estatística PosDL.docx`

Toda implementação por agente de IA deve observar estritamente os **Objetivos Gerais**, **Entregáveis** e **Critérios de Avaliação** definidos em [`docs/T3 Projeto Final Estatística PosDL.docx`](docs/T3%20Projeto%20Final%20Estat%C3%ADstica%20PosDL.docx) (detalhados em [`.agents/rules/objetivos-gerais-t3.md`](.agents/rules/objetivos-gerais-t3.md)):

1. **Integração Aplicada e Estudo Analítico Completo:**
   - Contextualizar todas as análises estatísticas com insights práticos baseados em dados para o problema de classificação (`Transported`) do dataset *Spaceship Titanic*.
   - Garantir cobertura rigorosa das etapas exigidas no T3:
     - **Contexto do Problema e do Dataset:** quem é o "cliente", o que se quer prever/entender, fonte, estrutura (linhas, colunas, tipos) e limitações;
     - **Análise Descritiva e Visual:** estatísticas descritivas, histogramas, boxplots, gráficos de barras, padrões, outliers e valores faltantes;
     - **Probabilidade e Distribuições:** investigação de aderência a distribuições em variáveis quantitativas com histograma, QQ-plot, teste formal (Shapiro-Wilk / Kolmogorov-Smirnov) e implicações práticas;
     - **Testes de Hipóteses ou ANOVA:** comparação de médias/medianas entre grupos, Qui-Quadrado para categorias, diferença de proporções e ANOVA/Kruskal-Wallis ($>2$ grupos), explicitando hipóteses ($H_0/H_1$), $p$-valor e conclusão traduzida para o cliente;
     - **Correlação, Regressão e Modelo Preditivo Simples:** matriz de correlação, explicação das relações mais fortes, treinamento de modelo preditivo simples (Regressão Linear/Logística) com métricas e interpretação;
     - **Conclusões e Recomendações Práticas:** principais insights acionáveis, pontos de atenção e próximos passos compreensíveis por alguém sem formação técnica (apoiando o Resumo Executivo de 1 página e o Relatório Técnico de 10–15 páginas).
2. **Critérios de Avaliação e Qualidade Obrigatória:**
   - **Clareza e Objetividade (50% da nota):** nunca apresente apenas *prints* de código ou tabelas cruas; toda saída estatística ou visual deve ser acompanhada de interpretação prática em Markdown voltada ao cliente.
   - **Qualidade Técnica da Análise (30% da nota):** validar pressupostos estatísticos, justificar a escolha de testes paramétricos/não-paramétricos e prevenir *data leakage*.
   - **Organização, Reprodutibilidade e Originalidade do Notebook (20% da nota):** código autoral comentado (sem plágio de Kaggle/GitHub), ausência total de caminhos absolutos (usar caminhos relativos à raiz do projeto), fixação de semente aleatória (`np.random.seed(42)` / `random_state=42`) e execução limpa (*Restart & Run All*).
3. **Padrões de Repositório e Governança de Rules/Skills:**
   - Siga as convenções de branch (`<tipo>/<nome-membro>-<descricao>`) e commit (`[KAN-XX] Descrição clara da alteração`) definidas em [`CONTRIBUTING.md`](CONTRIBUTING.md).
   - Ao criar ou editar rules e skills, mantenha a fonte única em [`.agents/`](.agents/) e use apenas stubs `@caminho` multiplataforma (Linux, macOS e Windows), conforme [`.agents/rules/padrao-rules-e-skills.md`](.agents/rules/padrao-rules-e-skills.md).
