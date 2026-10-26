# Rule: Observância Obrigatória aos Objetivos Gerais do Projeto (`docs/T3 Projeto Final Estatística PosDL.docx`)

Toda implementação, análise estatística, visualização, modelagem ou documentação realizada por qualquer agente de IA neste repositório deve observar estritamente os **Objetivos Gerais**, **Entregáveis** e **Critérios de Avaliação** definidos em [`docs/T3 Projeto Final Estatística PosDL.docx`](../../docs/T3%20Projeto%20Final%20Estat%C3%ADstica%20PosDL.docx).

## 1. Objetivo Geral e Escopo Analítico Obrigatório

O objetivo do trabalho é integrar todo o conteúdo da disciplina de **Estatística Avançada e Fundamentos Probabilísticos para IA** de forma aplicada no dataset *Spaceship Titanic*, contextualizando cada análise estatística com insights práticos baseados em dados voltados ao cliente/tomador de decisão.

Toda implementação deve contribuir para um estudo analítico completo que contemple:

1. **Contexto do Problema e do Dataset:**
   - Explicitar quem é o "cliente" (comando/operação espacial) e o que se quer prever ou entender (`Transported`);
   - Documentar fonte dos dados, estrutura (linhas, colunas, tipos de variáveis) e limitações do dataset.
2. **Análise Descritiva e Visual:**
   - Apresentar e interpretar estatísticas descritivas (tendência central, dispersão, assimetria), histogramas, boxplots e gráficos de barras;
   - Evidenciar principais padrões observados, tratamento de outliers e valores faltantes.
3. **Probabilidade e Distribuições:**
   - Investigar formalmente se variáveis quantitativas seguem distribuições teóricas;
   - Apresentar evidências combinadas: histograma, QQ-plot e teste formal de normalidade/aderência (Shapiro-Wilk ou Kolmogorov-Smirnov), explicando **por que isso importa** na prática (ex.: escolha entre testes paramétricos e não-paramétricos).
4. **Testes de Hipóteses e ANOVA:**
   - Aplicar testes estatísticos coerentes com a natureza dos dados: comparação de médias/medianas entre grupos, relação entre variáveis categóricas (Qui-Quadrado), diferença de proporções e ANOVA / Kruskal-Wallis (para $>2$ grupos);
   - Declarar obrigatoriamente: hipóteses ($H_0$ e $H_1$), estatística de teste, $p$-valor, tamanho de efeito e **conclusão traduzida para o cliente**.
5. **Correlação, Regressão e Modelo Preditivo Simples:**
   - Construir e interpretar matriz de correlação destacando as relações mais fortes;
   - Treinar e avaliar modelo(s) preditivo(s) simples (Regressão Linear / Logística) reportando métricas claras e interpretação prática dos coeficientes/preditores.
6. **Conclusões e Recomendações Práticas:**
   - Sintetizar os principais insights acionáveis (o que o cliente pode fazer com isso?), pontos de atenção e sugestão de próximos passos em linguagem acessível para decisores sem formação técnica.

## 2. Diretrizes de Execução e Critérios de Avaliação (Pesos do T3)

Cada célula de código ou Markdown gerada por agentes de IA deve respeitar os pesos oficiais de avaliação:

- **Clareza e Objetividade (50% da nota):**
  - **Proibido apresentar apenas *prints* de código ou tabelas cruas:** toda saída numérica, teste estatístico ou gráfico deve ser acompanhado imediatamente de interpretação clara em Markdown voltada ao cliente.
  - Manter linguagem profissional, objetiva e gráfica, servindo de base direta tanto para o Notebook final quanto para o Relatório Técnico (10–15 páginas, incluindo Resumo Executivo de 1 página).
- **Qualidade Técnica da Análise (30% da nota):**
  - Validar pressupostos estatísticos antes de escolher testes ou modelos; justificar escolhas metodológicas e evitar vazamento de dados (*data leakage*).
- **Organização, Qualidade e Reprodutibilidade do Notebook (20% da nota):**
  - Código limpo, modular e comentado em português;
  - **Reprodutibilidade estrita:** fixar semente aleatória (`np.random.seed(42)` / `random_state=42`), utilizar exclusivamente caminhos relativos à raiz do projeto (zero caminhos absolutos) e garantir execução sequencial sem erros (*Restart & Run All*);
  - **Originalidade:** código e textos autorais, sem plágio de notebooks externos do Kaggle ou GitHub.
