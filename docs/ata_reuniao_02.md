# Ata da Reunião 2 — Alinhamento Geral, Compartilhamento de Conhecimento e Apresentações Cruzadas

- **Projeto:** Spaceship Titanic — Análise Estatística Avançada e Modelagem Preditiva
- **Disciplina:** Estatística Avançada e Fundamentos Probabilísticos para IA (Pós-Graduação em Deep Learning — CIn/UFPE)
- **Data da Reunião:** 31 de outubro de 2026
- **Ticket Jira:** [KAN-36](https://megamatic.atlassian.net/browse/KAN-36)
- **Coordenador da Reunião:** Gustavo Menezes Gonçalves
- **Participantes (Quórum Integral):**
  1. Gustavo Menezes Gonçalves (Engenharia de Dados & Preparação — Trilha 0)
  2. Helton (Estatística Descritiva e Visualização — Trilha 1)
  3. Luciana (Probabilidade, Distribuições e QQ-Plots — Trilha 2)
  4. Daniela (Testes de Hipóteses e ANOVA — Trilha 3)
  5. Renatta (Correlação, Regressões e Interpretação Preditiva — Trilha 4)

---

## 1. Contexto e Objetivo Estratégico

### 1.1. Visão de Negócio
Garantir o domínio analítico unificado de todo o ciclo de vida do projeto por todos os cinco integrantes do grupo, eliminando completamente **silos de conhecimento**. Como cada membro liderou uma trilha técnica específica, a **Reunião 2** estabelece um momento formal de nivelamento conceitual e metodológico. Ao final desta dinâmica, qualquer membro da equipe está capacitado a defender integralmente a metodologia, as decisões estatísticas, os números canônicos e as recomendações práticas perante a banca avaliadora e partes interessadas.

### 1.2. Protocolo de Validação Cruzada (Apresentações Espelho)
A dinâmica seguiu um ciclo fechado de auditoria e reexplicação:
1. O **autor da trilha** apresenta em até 5 minutos a síntese de sua entrega estruturada em 4 eixos obrigatórios:
   - **Pergunta Central:** O que se buscou responder?
   - **Método Adotado:** Qual foi a técnica estatística/computacional e por que foi escolhida?
   - **Resultado Canônico:** Quais foram os números, tabelas e testes empíricos obtidos?
   - **Limitações & Cuidados:** O que não se pode inferir (riscos de interpretação)?
2. O **revisor dedicado** assume a fala em seguida e reexplica com suas próprias palavras o trabalho do colega, respondendo a perguntas desafiadoras do grupo para comprovar domínio pleno dos conceitos.

```
       ┌────────────────────────────────────────────────────────┐
       │             CICLO DE VALIDAÇÃO CRUZADA                 │
       └────────────────────────────────────────────────────────┘
         Gustavo (Trilha 0)  ────────>  Revisado por Helton
         Helton  (Trilha 1)  ────────>  Revisado por Luciana
         Luciana (Trilha 2)  ────────>  Revisado por Daniela
         Daniela (Trilha 3)  ────────>  Revisado por Renatta
         Renatta (Trilha 4)  ────────>  Revisado por Gustavo
```

---

## 2. Roteiro Detalhado do Projeto: Explicação Capítulo a Capítulo

Abaixo está o compêndio técnico detalhado de cada seção analítica do projeto, servindo como guia de estudo e nivelamento para toda a equipe.

---

### Capítulo 1: Preparação de Dados, Limpeza e Engenharia de Atributos
- **Responsável Principal:** Gustavo Menezes Gonçalves
- **Revisor Dedicado:** Helton
- **Notebook de Origem:** `notebooks/01_preparacao_dados.ipynb`
- **Documento Técnico:** `docs/conclusoes/01_ambiente_dados.md`
- **Artefato Gerado:** `data/processed/spaceship_titanic_clean.csv`

#### Pergunta Central
Como transformar um conjunto bruto de dados com valores ausentes, tipos heterogêneos e variáveis estruturadas em strings em uma base tratada e enriquecida, garantindo 100% de integridade sem gerar distorções distributivas (*bias*) nem vazamento de dados (*data leakage*)?

#### Método e Decisões Técnicas
1. **Unidade Amostral e Dimensões:** A base de treino conta com **8.693 passageiros** e 14 colunas brutas.
2. **Tratamento de Nulos:**
   - Variáveis categóricas (`HomePlanet`, `CryoSleep`, `Destination`, `VIP`) possuíam entre 2,1% e 2,5% de valores ausentes (~200 registros cada).
   - Realizou-se teste formal de sensibilidade comparando as proporções pré e pós-imputação pela moda condicional/geral. A variação máxima observada foi de apenas **0,64 ponto percentual**, provando a preservação da estrutura populacional.
   - Variáveis numéricas de consumo (`RoomService`, `FoodCourt`, `ShoppingMall`, `Spa`, `VRDeck`) foram imputadas pela mediana condicional (priorizando `CryoSleep=True` $\rightarrow 0$), já que passageiros em criossono estão fisicamente confinados e não consomem a bordo.
3. **Engenharia de Atributos Derivados:**
   - `PassengerId` ($gggg\_pp$): Decomposto em `GroupId` (identificador da família/grupo) e `GroupSize` (tamanho do grupo). Criação da flag binária `IsAlone` (grupo unitário vs acompanhado).
   - `Cabin` ($Deck/Num/Side$): Decomposto em `Deck` (conveses A a G e T), `CabinNum` (número da cabine) e `Side` (bombordo `P` vs boreste `S`).
   - `TotalSpend`: Soma vetorial das 5 comodidades pagas (`RoomService + FoodCourt + ShoppingMall + Spa + VRDeck`).
   - `HasSpended`: Indicador booleano de gasto nulo vs positivo.
   - `AgeGroup`: Categorização etária em faixas (0–12 Criança, 13–17 Adolescente, 18–25 Jovem Adulto, 26–35 Adulto Jovem, 36–50 Meia-idade, 51+ Sênior).
4. **Governança de Outliers:** Nenhum outlier de despesa foi excluído arbitrariamente. Passageiros de alta renda em suítes de luxo fazem parte da população legítima da nave; a modelagem posterior é quem deve adotar transformações logarítmicas ou métodos robustos a caudas pesadas.

#### Números Canônicos do Capítulo 1
- Registros finais: **8.693 linhas e 22 colunas** (sem nenhum valor faltante).
- Passageiros em criossono com despesa estritamente zero: **100%** (consistência física garantida).
- Proporção de passageiros viajando desacompanhados (`IsAlone`): **55,30%**.

#### Pontos de Atenção para a Validação Cruzada (Helton reexplica Gustavo)
- *Por que não descartamos as linhas com valores nulos?* Porque descartar ~2.000 passageiros com nulos parciais reduziria a amostra em quase 25% e introduziria viés de seleção desnecessário.
- *Onde está o risco de vazamento de dados?* A imputação deve ser calculada estritamente com os dados do conjunto de treino em pipelines futuros de validação cruzada.

---

### Capítulo 2: Análise Estatística Descritiva e Visual
- **Responsável Principal:** Helton
- **Revisora Dedicada:** Luciana
- **Notebook de Origem:** `notebooks/02_estatistica_descritiva.ipynb`
- **Documento Técnico:** `docs/conclusoes/02_descritiva_visual.md`

#### Pergunta Central
Quais são as características sociodemográficas, espaciais e econômicas dos passageiros da Spaceship Titanic e como elas se associam empiricamente com a probabilidade de transporte para a outra dimensão?

#### Método e Decisões Técnicas
1. **Medidas de Tendência Central e Dispersão:** Avaliação sistemática de média, desvio-padrão, mediana, intervalo interquartil (IQR), assimetria (*skewness*) e curtose para todas as variáveis quantitativas.
2. **Análise de Frequências Categóricas:** Tabulação cruzada de proporções relativas e taxas de transporte estratificadas por cabine, planeta e status biológico.
3. **Constatação da Zero-Inflação de Gastos:** Identificação de que a distribuição de despesas não pode ser resumida pela média aritmética convencional, sob pena de conclusões errôneas de negócio.

#### Números Canônicos do Capítulo 2
- **Taxa Global de Transporte:** **50,36%** (4.378 transportados de 8.693).
- **O Fenômeno do Criossono (`CryoSleep`):**
  * Em criossono: **81,47%** de transporte (2.483 transportados / 3.048 passageiros).
  * Acordados: **32,82%** de transporte (1.789 transportados / 5.451 passageiros).
  * Razão de chances bruta aparente $> 9\times$.
- **Planeta de Origem (`HomePlanet`):**
  * Europa: **66,05%** de transporte (1.439 / 2.179).
  * Marte: **52,44%** de transporte (930 / 1.773).
  * Terra: **42,33%** de transporte (1.987 / 4.693).
- **Destino (`Destination`):** 55 Cancri e (61,00%), PSO J318.5-22 (50,38%), TRAPPIST-1e (47,12%).
- **Perfil de Despesas (`TotalSpend`):**
  * **41,92%** de todos os passageiros gastaram exatamente **US$ 0,00** a bordo.
  * Assimetria da distribuição de despesas brutas: **4,40** (fortíssima cauda à direita).
  * Mediana dos transportados: **US$ 0,00** (devido à dominância do criossono).
  * Mediana dos não-transportados: **US$ 907,00**.
  * Médias brutas (infladas): US$ 994,00 (transportados) vs US$ 1.954,00 (não-transportados).

#### Pontos de Atenção para a Validação Cruzada (Luciana reexplica Helton)
- *Por que a média de gastos é uma armadilha?* A média de ~US$ 1.480 mascara o fato de que mais de 40% da tripulação não gastou um único centavo. A mediana e o IQR são os parâmetros estatísticos honestos para a tomada de decisão.
- *Qual o padrão nos decks?* Decks B e C (onde predominam passageiros de Europa) apresentam taxas de transporte superiores a 70%, enquanto conveses inferiores (Deck E, F e G) apresentam menores índices.

---

### Capítulo 3: Teoria de Probabilidade, Distribuições e QQ-Plots
- **Responsável Principal:** Luciana
- **Revisora Dedicada:** Daniela
- **Notebook de Origem:** `notebooks/03_probabilidade_distribuicoes.ipynb`
- **Documento Técnico:** `docs/conclusoes/03_probabilidade_distribuicoes.md`

#### Pergunta Central
As variáveis quantitativas contínuas (`Age` e `TotalSpend`) seguem distribuições teóricas clássicas (Normal ou Log-Normal)? O que a geometria das distribuições empíricas dita sobre a escolha dos testes inferenciais subsequentes?

#### Método e Decisões Técnicas
1. **Tríade Probatória:** Diagnóstico combinando (a) inspeção visual de histogramas e densidades kernel (KDE), (b) Quantile-Quantile plots (QQ-plots) teóricos e (c) testes formais de aderência:
   - **Shapiro-Wilk:** Avaliação de normalidade via correlação dos quantis amostrais com quantis normais teóricos.
   - **Kolmogorov-Smirnov (KS):** Comparação da função de distribuição acumulada empírica ($EDF$) contra a distribuição teórica calibrada por máxima verossimilhança.
2. **Transformações Estabilizadoras:** Aplicação de transformação logarítmica $\log(1 + x)$ nas despesas para investigar hipótese de distribuição Log-Normal.

#### Números Canônicos do Capítulo 3
- **Distribuição de Idade (`Age`):**
  * Estatística de Shapiro-Wilk: $W = 0,980$ ($p < 10^{-15}$).
  * Estatística de Kolmogorov-Smirnov: $D = 0,076$ ($p < 10^{-15}$).
  * **Interpretação:** Embora o $p$-valor seja minúsculo devido à hipersensibilidade do teste com $n=8.693$, o valor de $W$ extremamente próximo de $1,0$ e a aderência visual no QQ-plot mostram que `Age` é **aproximadamente normal** no miolo da distribuição, com discreto truncamento em zero (crianças) e leve afinamento em idades avançadas ($>60$).
- **Distribuição de Gastos Positivos (`log1p(TotalSpend)`):**
  * Shapiro-Wilk no log dos gastos: $W = 0,891$ ($p < 10^{-15}$).
  * Kolmogorov-Smirnov: $D = 0,126$. Curtose: $4,93$.
  * **Interpretação:** A variável despesa possui uma distribuição **bimodal mista**: uma massa pontual de probabilidade em zero (*zero-inflated point mass* de 41,92%) combinada com uma cauda contínua que se assemelha a uma Log-Normal de cauda pesada.
3. **Implicação Prática Inferencial:**
   - Não é lícito aplicar o Teste $t$ de Student clássico nem ANOVA unilateral clássica de Fisher, que exigem homocedasticidade e normalidade estrita dos resíduos.
   - É obrigatório o emprego de **testes robustos à heterocedasticidade (Teste $t$ de Welch e ANOVA de Welch)** e de testes não-paramétricos (Mann-Whitney / Kruskal-Wallis).

#### Pontos de Atenção para a Validação Cruzada (Daniela reexplica Luciana)
- *Por que o teste de Shapiro-Wilk rejeita a normalidade mesmo quando a curva parece normal?* Porque a potência de testes formais de aderência tende a 1 conforme $n \to \infty$. Qualquer desvio milimétrico se torna "estatisticamente significante". A decisão metodológica deve se guiar pelo tamanho do desvio ($W, D$) e pela análise visual do QQ-plot.
- *Por que não simplesmente logaritmizar toda a base e usar estatística clássica?* Porque $\log(0)$ é indefinido; mesmo com $\log(1+x)$, a concentração maciça em zero distorce completamente a simetria teórica da gaussiana.

---

### Capítulo 4: Testes de Hipóteses, Comparações Múltiplas e ANOVA
- **Responsável Principal:** Daniela
- **Revisora Dedicada:** Renatta
- **Notebook de Origem:** `notebooks/04_testes_hipoteses_anova.ipynb`
- **Documento Técnico:** `docs/conclusoes/04_testes_hipoteses_anova.md`

#### Pergunta Central
As discrepâncias observadas entre passageiros transportados e não-transportados (em criossono, planeta de origem, conveses e despesas) são estatisticamente significativas ou podem ser explicadas por mero ruído amostral? Qual a magnitude do efeito (*effect size*) dessas diferenças?

#### Método e Decisões Técnicas
1. **Associação Categórica:** Teste de Independência Qui-Quadrado de Pearson ($\chi^2$), acompanhado da medida padronizada de tamanho de efeito **$V$ de Cramér**.
2. **Comparação de Duas Médias:** Teste $t$ de Welch (que dispensa suposição de variâncias iguais) e teste não-paramétrico de Mann-Whitney U, reportando $d$ de Cohen e $r$ de correlação bisserial por postos.
3. **Comparação de Três ou Mais Grupos:** ANOVA de Welch para comparar despesas entre planetas de origem, após o teste de Levene confirmar heterocedasticidade severa ($p < 10^{-15}$). Pós-hoc executado pelo teste de **Games-Howell** (específico para variâncias desiguais), computando $\eta^2$ (Eta ao quadrado).

#### Números Canônicos do Capítulo 4
- **Criossono $\times$ Transporte:**
  * $\chi^2 = 1.897,71$ (graus de liberdade = 1, $p < 10^{-15}$).
  * **$V$ de Cramér = 0,467** (associação de grande magnitude — o maior preditor do estudo).
- **Planeta de Origem $\times$ Transporte:**
  * $\chi^2 = 338,82$ (graus de liberdade = 2, $p < 10^{-15}$).
  * **$V$ de Cramér = 0,197** (associação moderada a forte).
- **Deck de Cabine $\times$ Transporte:**
  * $\chi^2 = 389,01$ (graus de liberdade = 7, $p < 10^{-15}$), $V = 0,212$.
- **Despesas (`log1p(TotalSpend)`) entre Transportados e Não-Transportados:**
  * Teste de Levene: $W = 1.488,4, p < 10^{-15}$ (rejeição categórica de homocedasticidade).
  * Teste $t$ de Welch: $t = 18,94$ ($p < 10^{-15}$).
  * Tamanho de efeito: $d\text{ de Cohen} = 0,407$ (efeito moderado: quem não foi transportado gastou substancialmente mais).
- **Despesas (`log1p(TotalSpend)`) por Planeta de Origem:**
  * Razão de variâncias intergrupos ultrapassa $37\times$.
  * ANOVA de Welch: $F = 407,57$ ($p < 10^{-15}$).
  * Tamanho de efeito: $\eta^2 = 0,171$ (17,1% da variância de gastos explicada pela origem).
  * Pós-hoc Games-Howell: Todas as comparações pareadas (Europa-Terra, Europa-Marte, Marte-Terra) são estatisticamente distintas com $p < 10^{-6}$. Europa apresenta o maior nível de consumo a bordo.

#### Pontos de Atenção para a Validação Cruzada (Renatta reexplica Daniela)
- *Por que não utilizar a ANOVA clássica de Fisher?* Porque a violação da suposição de homogeneidade de variâncias inflaria a taxa de erro Tipo I ($\alpha$), levando a conclusões falso-positivas.
- *Por que relatar o tamanho de efeito além do p-valor?* Com $n=8.693$, virtualmente qualquer teste atinge $p < 0,05$. O tamanho de efeito ($V$ de Cramér, $d$ de Cohen, $\eta^2$) é a única métrica que indica se a diferença possui relevância prática ou se é um achado trivial.

---

### Capítulo 5: Correlações, Regressão Linear e Modelagem Preditiva
- **Responsável Principal:** Renatta
- **Revisor Dedicado:** Gustavo Menezes Gonçalves
- **Notebook de Origem:** `notebooks/05_correlacao_regressoes.ipynb`
- **Documento Técnico:** `docs/conclusoes/05_correlacao_regressoes.md`

#### Pergunta Central
Como as variáveis preditoras se correlacionam mutuamente e qual a capacidade preditiva de um modelo logístico simples para antecipar o transporte de passageiros, preservando a interpretabilidade dos coeficientes para a liderança operacional?

#### Método e Decisões Técnicas
1. **Análise de Correlação Não-Linear:** Matriz de correlação de Spearman (adequada a distribuições assimétricas e variáveis ordinais).
2. **Regressão Linear Múltipla para Despesas:** Ajuste por Mínimos Quadrados Ordinários (OLS) em $\log(1 + \text{TotalSpend})$ para compreender determinantes do gasto.
3. **Regressão Logística para `Transported`:**
   - Divisão estratificada e reprodutível treino/teste ($80\% / 20\%$, semente 42).
   - Padronização de numéricas e One-Hot Encoding de variáveis categóricas.
   - Avaliação rigorosa com matriz de confusão, Curva ROC ($AUC$), Precision-Recall ($AP$), F1-Score, Sensibilidade (Recall) e Especificidade.
   - Comparação contra baseline ingênuo (*Dummy Classifier* que prevê a classe majoritária).

#### Números Canônicos do Capítulo 5
- **Regressão Linear para Consumo:** $R^2 = 0,314$ (as variáveis explicam 31,4% da variabilidade dos gastos a bordo; idade, planeta e deck são os maiores coeficientes positivos).
- **Regressão Logística (Desempenho no Teste, $n=1.739$):**
  * Baseline ingênuo: Acurácia de **50,36%** (sem poder discriminativo, $AUC = 0,500$).
  * **Acurácia:** **77,9%** (+27,5 pontos percentuais sobre o baseline).
  * **ROC-AUC:** **0,862** (excelente capacidade de ordenação de risco).
  * **Average Precision (PR-AUC):** **0,880**.
  * **Precisão:** **77,2%** | **Recall (Sensibilidade):** **79,6%** | **F1-Score:** **78,4%**.
  * **Especificidade:** **76,1%**.
- **Interpretação dos Coeficientes (Odds Ratios):**
  * `CryoSleep`: Maior coeficiente positivo com folga ($OR > 8,5$). Estar em criossono multiplica a chance de ser transportado por mais de oito vezes, controlando por todas as demais variáveis.
  * Consumo em amenidades (`Spa`, `VRDeck`, `RoomService`): Coeficientes logísticos negativos expressivos.
  * `HomePlanet_Earth`: Coeficiente negativo relativo à Europa.

#### Pontos de Atenção para a Validação Cruzada (Gustavo reexplica Renatta)
- *O modelo pode ser usado para decisão automática de resgate?* **Não.** Com 77,9% de acurácia, ainda há cerca de 22% de classificações incorretas (falsos positivos e falsos negativos). Trata-se de um modelo para **apoio à triagem e priorização investigativa**, não para tomada de decisão autônoma.
- *Por que não tunamos hiperparâmetros ou mudamos o threshold de 0,5?* Para manter a integridade metodológica de um modelo baseline parcimonioso e interpretável, sem risco de sobreajuste (*overfitting*) no conjunto de teste.

---

### Capítulo 6: Síntese de Negócio, Limitações e Recomendações
- **Síntese Coletiva**
- **Documento Técnico:** `docs/conclusoes/06_conclusoes_recomendacoes.md`

#### As Três Conclusões Cardeais para o Cliente
1. **O Criossono é o epicentro do fenômeno:** 81,47% de transporte em cápsulas contra 32,82% em cabines comuns. A hipótese física sugere que os sistemas das câmaras de estase entraram em ressonância com a anomalia ou que passageiros isolados em cápsulas não puderam reagir às manobras de emergência da nave.
2. **Origem e localização física estão conectadas:** Passageiros de Europa (66,05%) e decks intermediários/altos (B e C) sofreram impacto desproporcional. A demografia está colinear à planta estrutural da nave.
3. **Consumo a bordo é uma falsa pista se analisado isoladamente:** Não é o ato de gastar dinheiro que "protege" o passageiro; passageiros acordados gastam porque estão circulando nas áreas de convivência (decks inferiores), onde o transporte foi estatisticamente menor.

#### Limitações e Cautelas Imperativas
- **Natureza Estritamente Observacional:** Associação estatística não implica causalidade. Não se pode afirmar que o criossono causou a anomalia.
- **Divisão Amostral Ampla:** A nave transportou famílias e grupos com correlação espacial interna. O modelo tratou os passageiros como observações independentes.

---

## 3. Registro da Sessão de Validação Cruzada

| Ordem | Apresentador (Autor) | Revisor Dedicado | Tema Defendido | Avaliação do Grupo |
| :---: | :--- | :--- | :--- | :---: |
| 1 | **Gustavo Menezes** | **Helton** | Limpeza de nulos, sensibilidade (<0,64 p.p.) e engenharia de atributos | **Aprovado com Louvor** |
| 2 | **Helton** | **Luciana** | Descritiva, zero-inflação (41,92%), contrastes de criossono e decks | **Aprovado com Louvor** |
| 3 | **Luciana** | **Daniela** | Aderência Normal/Log-Normal, $W, D$, heterocedasticidade e escolha de testes | **Aprovado com Louvor** |
| 4 | **Daniela** | **Renatta** | $\chi^2$, $V$ de Cramér, $t$ de Welch, ANOVA de Welch e Games-Howell | **Aprovado com Louvor** |
| 5 | **Renatta** | **Gustavo Menezes** | Regressão linear, modelo logístico, métricas (ROC-AUC 0,862) e limites operacionais | **Aprovado com Louvor** |

---

## 4. Tabela de Bolso para Defesa Perante a Banca (Resumo Executivo)

| Variável / Métrica | Valor Canônico | Interpretação Prática | Seção / Origem |
| :--- | :---: | :--- | :---: |
| **Amostra Total Analisada** | **8.693 passageiros** | População completa sem exclusão de outliers | Cap. 1 / `01_preparacao` |
| **Taxa Global de Transporte** | **50,36%** (4.378) | Classes equilibradas (não requer balanceamento artificial) | Cap. 2 / `02_descritiva` |
| **Transporte em Criossono** | **81,47%** vs **32,82%** | Maior contraste univariado de todo o estudo | Cap. 2 / `02_descritiva` |
| **Taxa Europa / Marte / Terra** | **66,05% / 52,44% / 42,33%** | Forte estratificação de desfecho por planeta natal | Cap. 2 / `02_descritiva` |
| **Taxa de Gastos Nulos** | **41,92%** (3.644) | Exige análise por mediana e proíbe média cega | Cap. 2 e 3 / `02_descritiva` |
| **Shapiro-Wilk Idade (`Age`)** | $W = 0,980$ ($D = 0,076$) | Aproximadamente Normal no corpo central | Cap. 3 / `03_distribuicoes` |
| **Associação Criossono ($\chi^2$)** | $\chi^2 = 1.897,71$ ($V = 0,467$) | Associação de grande magnitude ($p < 10^{-15}$) | Cap. 4 / `04_hipoteses` |
| **Associação Planeta ($\chi^2$)** | $\chi^2 = 338,82$ ($V = 0,197$) | Associação de moderada a forte magnitude | Cap. 4 / `04_hipoteses` |
| **Diferença Gastos ($t$ Welch)** | $t = 18,94$ ($d = 0,407$) | Não-transportados gastam mais (efeito médio) | Cap. 4 / `04_hipoteses` |
| **ANOVA Welch Planeta Gastos** | $F = 407,57$ ($\eta^2 = 0,171$) | Origem explica 17,1% da variação de consumo | Cap. 4 / `04_hipoteses` |
| **Acurácia Regressão Logística** | **77,9%** | +27,5 p.p. superior ao baseline majoritário | Cap. 5 / `05_modelagem` |
| **ROC-AUC Modelo Logístico** | **0,862** | Elevado poder discriminativo para triagem | Cap. 5 / `05_modelagem` |

---

## 5. Deliberações Finais e Próximos Passos
1. **Domínio Unificado Confirmado:** Os cinco membros demonstraram conhecimento profundo e articulado de todas as fases da investigação, cumprindo 100% o objetivo da Reunião 2 e do ticket [KAN-36](https://megamatic.atlassian.net/browse/KAN-36).
2. **Homologação para o Fechamento do Projeto:** Com a validação cruzada concluída, a equipe autoriza o prosseguimento das entregas subsequentes:
   - Finalização do catálogo de figuras (`KAN-38`);
   - Consolidação textual do Relatório Técnico final de 10–15 páginas (`KAN-39` a `KAN-42`);
   - Consolidação dos notebooks no notebook mestre `00_projeto_final_estatistica.ipynb` sob demanda via Skill oficial (`KAN-37`).

---

## 6. Assinatura da Ata

Recife, 31 de outubro de 2026.

- **Gustavo Menezes Gonçalves** (Coordenador & Autor Trilha 0)
- **Helton** (Autor Trilha 1)
- **Luciana** (Autora Trilha 2)
- **Daniela** (Autora Trilha 3)
- **Renatta** (Autora Trilha 4)
