# Guia Detalhado de Apresentação — Projeto Final de Estatística

> **Para quem é este documento.** É o guia do apresentador. Ele explica o projeto inteiro,
> seção por seção, com a narrativa, os números, os métodos, as figuras, as perguntas
> prováveis e as respostas. Pode ser lido do começo ao fim na véspera e consultado durante
> o ensaio. A versão curta de bolso é [`roteiro_apresentacao.md`](roteiro_apresentacao.md).

- **Disciplina:** Estatística Avançada e Fundamentos Probabilísticos para IA — Pós-Graduação em Deep Learning (CIn/UFPE)
- **Entrega:** Trabalho Final (T3) — Relatório Técnico em PDF + Notebook Jupyter
- **Tema:** *Spaceship Titanic* — o que distingue os passageiros transportados dos não transportados
- **Notebook entregável:** [`notebooks/00_projeto_final_estatistica.ipynb`](../../notebooks/00_projeto_final_estatistica.ipynb)
- **Ticket de consolidação:** [KAN-37](https://megamatic.atlassian.net/browse/KAN-37)
- **Pesos da avaliação:** 30% qualidade técnica · 50% clareza e objetividade · 20% organização e reprodutibilidade

---

## 0. Como usar este guia

1. **Leia a Seção 1** para fixar a mensagem central. Tudo o que for dito deve caber nela.
2. **Ensaie a Seção 4** (roteiro minuto a minuto) com cronômetro. É o texto que será falado.
3. **Domine a Seção 5** (aprofundamento). É onde a banca vai apertar.
4. **Decore a Seção 8** (números de bolso). Nunca cite um número sem a seção de origem.
5. **Tenha a Seção 7** (perguntas e respostas) aberta no ensaio. Ela cobre 90% do que será perguntado.

**Regra de ouro:** todo número citado tem uma seção de origem. Se a banca pedir a fonte, a
resposta é “Seção X do notebook” ou “documento de conclusões da Seção X”. Isso é o que separa
uma apresentação de um desfile de gráficos.

---

## 1. A mensagem central em 60 segundos

> “Recebemos o registro de **8.693 passageiros** de uma nave que atravessou uma anomalia
> espaço-temporal. Metade foi transportada para outra dimensão. Nosso trabalho foi descobrir
> **o que distingue quem foi de quem não foi**, com rigor estatístico e sem confundir
> associação com causa. Descobrimos que o **estado de criossono** é o sinal mais forte —
> **81,47%** dos passageiros em criossono foram transportados, contra **32,82%** dos acordados.
> A **origem planetária** vem em segundo lugar: Europa **66,05%**, Marte **52,44%**, Terra
> **42,33%**. O **gasto a bordo** engana: quatro em cada dez passageiros não gastaram nada, e
> a mediana dos transportados é zero. Com essas variáveis, um modelo logístico simples prevê
> o desfecho com **77,9% de acurácia** e **ROC-AUC de 0,862** — útil para triagem, não para
> decisão automática.”

**As três frases que o ouvinte precisa levar para casa:**

1. **O criossono é o que mais separa os grupos.** A associação é muito forte (V de Cramér = 0,467).
2. **Origem e deck contam a mesma história por caminhos diferentes.** Europa e os decks B/C
   concentram as maiores taxas; a origem está entrelaçada com a localização física.
3. **O gasto não é um bom atalho.** A zero-inflação (41,92% sem gasto) faz a média mentir;
   mediana e proporção de zeros são as medidas honestas.

**A frase de cautela que deve ser repetida pelo menos duas vezes:**

> “Tudo isto é **observacional**. Nós descrevemos associações; não afirmamos que criossono,
> origem ou gasto *causaram* o transporte.”

---

## 2. Ficha técnica do projeto

| Item | Valor |
| :--- | :--- |
| Dataset | *Spaceship Titanic* (Kaggle) |
| Base bruta de treino | `data/raw/train.csv` — 8.693 linhas × 14 colunas; 2.324 células ausentes (1,91%) |
| Base bruta de teste | `data/raw/test.csv` — 4.277 linhas × 13 colunas; 1.117 células ausentes (2,01%) |
| Base tratada | `data/processed/spaceship_titanic_clean.csv` — 8.693 × 22; **0 ausentes** |
| Base tratada de teste | `data/processed/spaceship_titanic_test_clean.csv` — 4.277 × 21; **0 ausentes** |
| Variável-alvo | `Transported` (booleana): 4.378 verdadeiros (50,36%) e 4.315 falsos (49,64%) |
| Variáveis derivadas | 8: `Group`, `GroupSize`, `IsAlone`, `CabinDeck`, `CabinNum`, `CabinSide`, `TotalSpend`, `HasSpent` |
| Semente aleatória | `42` em todas as etapas que sorteiam dados |
| Notebook consolidado | 227 células (87 de código e 140 de Markdown), executa *Restart & Run All* sem erros |
| Figuras do relatório | 8 figuras a 300 DPI em `report/figures/` (`fig_01` a `fig_08`) |
| Equipe e frentes | Gustavo (dados e consolidação), Helton (descritiva), Luciana (probabilidade), Daniela (testes), Renatta (correlação e modelo) |

### 2.1. O problema de negócio

O “cliente” é o **Comando de Operações Espaciais** e a **equipe de resgate** da nave. Eles
precisam de duas coisas:

1. **Entender** quais perfis estavam mais expostos ao teletransporte (para apurar
   responsabilidades, comunicar famílias e revisar protocolos de emergência).
2. **Prever**, a partir dos registros danificados, quais passageiros da base não rotulada
   foram transportados (para priorizar busca e reconstrução de registros).

### 2.2. A pergunta analítica

> “Quais características demográficas, de acomodação e de comportamento a bordo estão
> associadas ao desfecho `Transported`, qual é a magnitude dessas associações e quão bem
> elas permitem prever o desfecho?”

### 2.3. O que o projeto **não** é

- **Não é causal.** O desenho é observacional e não isola mecanismos.
- **Não é uma competição de Kaggle.** O objetivo é a análise estatística completa e a
  comunicação, não maximizar uma métrica.
- **Não remove outliers.** Os valores extremos de gasto são clientes reais e foram mantidos.

---

## 3. Mapa do notebook consolidado

O notebook mestre foi gerado pelo script `src/consolidar_notebooks.py`, a partir dos notebooks
de cada trilha, e executado do zero em kernel limpo. Ele é dividido em seis seções, na ordem
exigida pelo T3:

| Seção | Conteúdo | Faixa aproximada de células | Tickets de origem |
| :---: | :--- | :---: | :--- |
| — | Cabeçalho geral e índice | 0–1 | KAN-37 |
| **1** | Contexto, saneamento e engenharia de atributos | 1–39 | KAN-10, KAN-11, KAN-12 |
| **2** | Estatística descritiva e visual | 40–65 | KAN-14, KAN-15, KAN-16, KAN-17 |
| **3** | Probabilidade e distribuições | 66–110 | KAN-19, KAN-20, KAN-21, KAN-22 |
| **4** | Testes de hipóteses e ANOVA | 111–141 | KAN-24 a KAN-28 |
| **5** | Correlação, regressão e modelo preditivo | 142–219 | KAN-30 a KAN-34 |
| **6** | Conclusões e recomendações práticas | 220–226 | KAN-44 |

**O que mostrar ao vivo, se houver tempo:** o cabeçalho (índice), a célula que carrega a base
tratada, a tabela de transporte por criossono (Seção 2), a tabela de aderência (Seção 3), a
tabela-resumo dos testes (Seção 4) e a célula da Seção 6 que recomputa os números de manchete.

---

## 4. Roteiro minuto a minuto (13 minutos)

> **Orçamento:** 13 minutos de fala + 2 minutos de margem para perguntas curtas.
> Se o tempo apertar, corte da Seção 2 (descritiva) e preserve as Seções 4, 5 e 6.

### 4.1. Abertura — 1 minuto

**Fale:**

> “Boa noite. Nosso projeto analisa o incidente da *Spaceship Titanic*. A nave atravessou uma
> anomalia espaço-temporal e **metade dos 8.693 passageiros foi transportada** para outra
> dimensão. Nosso cliente é o comando de resgate, que precisa entender quem estava mais exposto
> e prever quem foi transportado. Vou mostrar o que os dados dizem — e o que eles **não**
> autorizam dizer.”

**Número de apoio:** 8.693 passageiros; 50,36% transportados.
**Figura:** nenhuma.
**Transição:** “Antes de analisar, foi preciso arrumar a base.”

### 4.2. Contexto e saneamento — 2 minutos

**Fale:**

> “A base chegou com **1,91% das células ausentes** e 24% das linhas com pelo menos um valor
> faltando. A solução óbvia — apagar as linhas incompletas — jogaria fora quase um quarto da
> amostra. Optamos por **imputação em 10 etapas**, com regras de negócio primeiro e estatística
> depois: se o passageiro estava em criossono, as despesas ausentes são zero; se era criança,
> também; se a cabine aparece em outro membro do mesmo grupo, ela é recuperada. Só depois
> entram mediana e moda. O resultado é uma base de **8.693 × 22, sem nenhum valor ausente**,
> com **zero vazamento de dados**: todos os parâmetros foram estimados só no treino.”

**Números de apoio:** 2.324 células ausentes (1,91%); 24,01% das linhas com ausência; 10 etapas
de imputação; 842 células recuperadas por regra determinística (36,23% das ausentes); mudança
máxima de **0,64 p.p.** nas proporções e **0,77 p.p.** nas taxas de transporte.
**Figura:** nenhuma (ou uma tabela de completude, se o PDF abrir espaço).
**Pergunta provável:** “A imputação não distorce?” → Testamos a sensibilidade: a maior mudança
em qualquer categoria foi 0,64 p.p., e a maior mudança em taxa de transporte foi 0,77 p.p.
Isso não muda nenhuma conclusão.

### 4.3. Descritiva — 3 minutos

**Fale:**

> “A primeira pista é o confinamento. Passageiros em **criossono foram transportados em 81,47%
> dos casos**, contra **32,82% dos acordados** — uma diferença de quase 49 pontos percentuais.
> É a associação mais forte de todo o conjunto. A segunda pista é a origem: **Europa 66,05%**,
> **Marte 52,44%**, **Terra 42,33%**. Mas atenção: **72,6% dos europeus ocupam os decks B e C**,
> e os decks B e C são justamente os de maior taxa. Origem e deck são a mesma história contada
> de dois jeitos; não podemos dizer que um ‘causa’ o outro.”

**Números de apoio:** 50,36% global; 81,47% × 32,82%; 66,05% / 52,44% / 42,33%; decks B 72,95%
e C 68,07%; 41,92% sem gasto; mediana de gasto **US$ 0,00** entre transportados × **US$ 907,00**
entre não transportados.
**Figuras:** `fig_02` (criossono) e `fig_01` (planeta). Se houver tempo, `fig_04` (gasto por desfecho).
**Pergunta provável:** “Por que não usar a média de gasto?” → Porque 41,92% gastaram zero e a
assimetria é 4,40. A média é puxada pela cauda; a mediana e a proporção de zeros são mais honestas.
**Transição:** “Para escolher os testes certos, precisávamos entender a forma das distribuições.”

### 4.4. Probabilidade e distribuições — 2 minutos

**Fale:**

> “A idade se comporta aproximadamente como uma Normal: W de Shapiro de 0,980 e D de 0,076 —
> um desvio pequeno. Já o gasto é uma variável em duas partes: primeiro ‘gastou ou não’, depois
> ‘quanto gastou’. Nos positivos, o logaritmo praticamente zera a assimetria (de 4,40 para
> −0,19), mas as caudas continuam pesadas (curtose 4,93). Conclusão prática: podemos usar média
> e teste t para idade; para gasto, precisamos de testes robustos e de reportar mediana.”

**Números de apoio:** `Age` W = 0,980, D = 0,076; `log1p(TotalSpend)` W = 0,891, D = 0,126;
assimetria do gasto 4,40; curtose dos positivos 4,93; 41,92% de zeros.
**Figuras:** `fig_07` (idade × Normal) e `fig_08` (zero × log-normal). QQ-plots inline no notebook.
**Pergunta provável:** “Se o teste rejeita a normalidade, por que usar teste paramétrico?” →
Porque com n grande o p sempre rejeita; a decisão se apoia no **tamanho do desvio** (W e D) e o
teste de Welch é robusto para n desta ordem. Além disso, normalidade da preditora não é
pressuposto de regressão.

### 4.5. Testes de hipóteses — 3 minutos

**Fale:**

> “Aqui separamos o que é estatisticamente sustentável do que é ruído. No qui-quadrado,
> **criossono tem V de Cramér de 0,467** — associação muito forte. Planeta tem **0,197** —
> moderada. VIP tem **0,037** — estatisticamente significativa, mas irrelevante na prática:
> é o exemplo perfeito de que p-valor pequeno não significa efeito grande. Para gasto, o teste
> de Levene mostrou variâncias muito desiguais, então trocamos o t de Student por **Welch**;
> a diferença é de **US$ 1.120,74** por passageiro, com **d de Cohen de 0,407**. Entre planetas,
> a **ANOVA de Welch** deu F = 407,57 e **η² = 0,171**: a origem explica 17% da variância do
> gasto, um efeito grande.”

**Números de apoio:** χ² planeta 338,82 / V 0,197; χ² criossono 1.897,71 / V 0,467;
χ² VIP 12,07 / V 0,037; Welch t = 18,94, d = 0,407, Δ = US$ 1.120,74, IC [1.004,76; 1.236,71];
ANOVA de Welch F = 407,57, η² = 0,171; Kruskal-Wallis H = 271,97; Games-Howell Europa × Terra
+US$ 2.768,76.
**Figura:** `fig_03` (idade) e `fig_04` (gasto por desfecho).
**Pergunta provável:** “ANOVA clássica ou de Welch?” → Welch, porque Levene rejeitou a
homocedasticidade e a razão de variâncias entre Europa e Terra passa de 37×; o pós-hoc é
Games-Howell.
**Transição:** “Com as variáveis certas, passamos ao modelo conjunto.”

### 4.6. Correlação e modelo — 3 minutos

**Fale:**

> “As correlações mais fortes são de cada gasto com o total — o que é esperado, porque o total
> é a soma. Entre serviços, a correlação de Pearson é fraca, mas a de Spearman chega a 0,52:
> quem usa um serviço tende a usar outros. Na regressão logística, o **criossono tem OR de 3,21**
> — chance 3,2 vezes maior de transporte, já descontando as demais variáveis. Europa tem **OR
> de 3,97**. No teste, o modelo acerta **77,9%**, com **ROC-AUC de 0,862** e **F1 de 0,784** —
> **25,5 pontos percentuais acima** da regra ingênua. É um apoio à triagem, não uma sentença.”

**Números de apoio:** OR criossono 3,21 (2,61–3,94); OR Europa 3,97 (2,58–6,10); acurácia
0,779; precisão 0,772; recall 0,796; especificidade 0,761; F1 0,784; ROC-AUC 0,862; AP 0,880;
ganho de +25,5 p.p. sobre o baseline.
**Figuras:** `kan34_matriz_confusao.png` e `kan34_curvas_roc_pr.png` (artefatos de notebook,
fora do catálogo de 8 figuras).
**Pergunta provável:** “Por que o limiar é 0,5?” → Foi fixado *a priori* para não otimizar no
teste; recalibrar exige saber o custo relativo de falso positivo e falso negativo.

### 4.7. Conclusões — 1 minuto

**Fale:**

> “Três recomendações. Primeira: **priorizar a inspeção das cápsulas de criossono** — é a
> associação mais forte e a mais acionável. Segunda: **investigar a diferença por origem**
> cruzando com deck e classe, porque origem e localização física estão entrelaçadas. Terceira:
> **não usar gasto como proxy de importância ou de presença** — quatro em cada dez passageiros
> não gastaram nada. E uma cautela final: tudo isto é associação observacional, não causalidade.
> O próximo passo é o relatório técnico e a validação numérica cruzada.”

**Números de apoio:** 81,47% × 32,82%; 41,92% sem gasto.
**Figura:** nenhuma (fechar com `fig_02`, se quiser deixar a imagem na tela).
**Pergunta provável:** “Isso é causal?” → Não. Desenho observacional; as recomendações são de
triagem e de investigação.

---

## 5. Aprofundamento por seção (para a banca)

### 5.1. Seção 1 — Contexto, saneamento e engenharia de atributos

**O problema.** A base bruta tem 14 colunas em `train.csv` e 13 em `test.csv`, com valores
ausentes espalhados por 12 das 13 preditoras. Apagar linhas incompletas eliminaria 24,01% do
treino e impediria prever 23,29% do teste.

**O método.** Imputação em duas camadas e 10 etapas:

- **Camada 1 — regras determinísticas e inferência relacional (etapas 1 a 4):** recupera
  **842 das 2.324 células ausentes do treino (36,23%)** sem aproximação estatística.
  Exemplos: `CryoSleep == True` → despesas ausentes = 0; `Age <= 12` → despesas = 0 e
  `VIP = False`; soma de despesas > 0 → `CryoSleep = False`; cabine e planeta inferidos pelo
  grupo de viagem, deck e sobrenome.
- **Camada 2 — imputação estatística condicional (etapas 5 a 10):** moda para categóricas,
  mediana agrupada por `HomePlanet`, `CryoSleep` e `VIP` para despesas, mediana agrupada por
  `HomePlanet` e `VIP` para idade. **Todos os parâmetros são estimados apenas no treino.**

**Por que não `dropna()`.** Porque a ausência é compatível com MCAR (teste χ² do indicador de
ausência contra `Transported` deu p entre 0,2196 e 1,0000 em 100% das variáveis), mas o valor
oculto é estruturalmente determinável por outras colunas. Descartar seria perder informação
recuperável.

**As 8 variáveis derivadas.** `Group` e `GroupSize` (a partir de `PassengerId`), `IsAlone`,
`CabinDeck`, `CabinNum` e `CabinSide` (a partir de `Cabin`), `TotalSpend` (soma das 5 rubricas)
e `HasSpent`. O ticket KAN-12 audita as 9 regras de integridade: 0 NaNs, 0 grupos
compartilhados entre treino e teste, reconstrução bijetora da cabine, erro algébrico máximo de
`TotalSpend` da ordem de 10⁻¹¹ e 0 violações de coerência física.

**Limitação a declarar.** A imputação pela moda atinge 2,1% a 2,5% das categóricas. A
sensibilidade documentada mostra impacto máximo de 0,64 p.p. nas proporções e 0,77 p.p. nas
taxas; isso sustenta a estabilidade, mas não prova ausência de viés.

### 5.2. Seção 2 — Estatística descritiva e visual

**Perfil da amostra.** 54,24% embarcaram na Terra, 25,01% em Europa e 20,75% em Marte; 70,14%
iam para TRAPPIST-1e; 36,06% viajaram em criossono; 2,29% eram VIP; os decks F (32,99%) e G
(29,77%) concentram 62,76%; 55,3% viajavam sozinhos; a idade média é 28,78 anos (mediana 27;
dp 14,35); 9,3% eram crianças de até 12 anos, incluindo 178 bebês com idade 0.

**Zero-inflação.** Entre 62,3% e 65,8% não gastaram nada em cada rubrica; 41,92% (3.644) não
gastaram nada no total. A mediana de `TotalSpend` é US$ 717,00 e a média, US$ 1.447,46 — razão
de aproximadamente 2. Entre os 5.049 que gastaram, a média sobe para US$ 2.492,13 e a mediana
para US$ 1.192,00.

**Outliers.** Pela regra de Tukey (1,5 × IQR), 21,0% a 21,9% aparecem como extremos em cada
rubrica — percentual alto porque a massa de zeros comprime o IQR. Em `TotalSpend`, o limite
superior é US$ 3.610,00 e 938 passageiros (10,8%) ficam acima; esse grupo tem 3,7 vezes mais
VIPs (8,4% contra 2,29%) e **nenhum** passageiro em criossono. **Decisão: nenhum registro foi
removido.** Os extremos são clientes reais, não erros de digitação.

**Ranking de associação (n ≥ 30).** Criossono 81,47% (+31,10 p.p.), deck B 72,95% (+22,59),
deck C 68,07% (+17,71), acordado 32,82% (−17,54), Europa 66,05% (+15,69), deck E 36,05%
(−14,32), VIP 38,19% (−12,17), destino 55 Cancri e 61,00% (+10,64).

**O entrelaçamento origem–deck.** 72,6% dos europeus ocupam B e C; 99,98% dos terráqueos
ocupam E, F e G; o deck G é exclusivamente terrestre. Consequência: comparar taxa por deck sem
mencionar origem compara, em boa parte, perfis de origem diferentes.

**Robustez à imputação.** A auditoria compara base bruta e tratada: maior diferença de
proporção de 0,64 p.p. e maior diferença de taxa de transporte de 0,77 p.p. (ambas em
categorias com n ≥ 30, exceto deck T).

### 5.3. Seção 3 — Probabilidade e distribuições

**A decisão mais importante: qual população testar.** `TotalSpend` não é contínua; é uma
mistura *hurdle* — uma decisão binária (“gastou ou não”) e, condicionada a gastar, um valor
positivo. Testar a variável completa contra uma lei contínua mede a mistura, não a forma dos
gastos. Por isso as populações foram declaradas antes dos testes:

| População | n | Zeros | Para quê |
| :--- | ---: | ---: | :--- |
| `Age` (todos) | 8.693 | 178 (2,05%) | Aderência à Normal |
| `Age > 0` | 8.515 | 0 | Sensibilidade |
| `TotalSpend` (todos) | 8.693 | 3.644 (41,92%) | Retrato da mistura |
| `log1p(TotalSpend)` entre positivos | 5.049 | 0 | Aderência à Normal na escala log |

**Momentos.** `Age`: média 28,78, dp 14,35, assimetria 0,43, curtose 0,16. `TotalSpend`:
média 1.447,46, dp 2.808,28, assimetria 4,40, curtose 27,28. `log1p` positivo: média 7,34,
dp 0,95, assimetria −0,19, curtose 4,93.

**QQ-plots.** Em `Age`, o miolo fica abaixo da reta, há um patamar em 0 (bebês) e a cauda
superior volta acima: o desenho em S combina átomo em zero, discretização (80 valores inteiros)
e concentração entre 20 e 40 anos. Em `log1p(TotalSpend)`, a perna esquerda quase vertical
mostra um excesso de gastos positivos mínimos (US$ 1 a US$ 30) e a curtose 4,93.

**Testes formais.** Shapiro-Wilk (`W`) e Kolmogorov-Smirnov com correção de Lilliefors (`D`).
Todas as populações rejeitam a normalidade (p minúsculo), mas o p não é o critério útil com n
desta ordem. O critério é o tamanho do desvio: `Age` tem W = 0,980 e D = 0,076 (desvio pequeno);
`log1p(TotalSpend)` tem W = 0,891 e D = 0,126 (desvio moderado a grande).

**Sensibilidade que contraria a intuição.** Retirar os 178 bebês **piora** a aderência de
`Age`: W cai de 0,980 para 0,975 e D sobe de 0,076 para 0,085. A rejeição não vem do pico em
zero; vem da discretização e da concentração central.

**Implicação para a Seção 4.** `Age`: média com t de Welch, Mann-Whitney como salvaguarda.
`TotalSpend`: Levene → Welch + Mann-Whitney. Serviços: Mann-Whitney ou Kruskal-Wallis, nunca t
de Student. Categóricas: qui-quadrado. `log1p` com erro-padrão HC3 na regressão linear.

### 5.4. Seção 4 — Testes de hipóteses e ANOVA

**Qui-quadrado (associação categórica).** Três hipóteses de independência contra `Transported`:

| Relação | χ² | gl | p | V de Cramér | Leitura |
| :--- | ---: | ---: | ---: | ---: | :--- |
| `HomePlanet` × `Transported` | 338,82 | 2 | 2,663 × 10⁻⁷⁴ | 0,197 | associação moderada |
| `CryoSleep` × `Transported` | 1.897,71 | 1 | < 10⁻³⁰⁰ | 0,467 | associação muito forte |
| `VIP` × `Transported` | 12,07 | 1 | 5,126 × 10⁻⁴ | 0,037 | significativa, mas desprezível |

O pressuposto de Cochran (frequência esperada ≥ 5) foi atendido em 100% das células. O caso VIP
é a lição metodológica do projeto: **p-valor pequeno não é efeito grande**.

**Gasto por desfecho (Welch + Mann-Whitney).** Levene centrado na mediana: W = 131,36
(p = 3,407 × 10⁻³⁰), com desvio-padrão de US$ 3.142,61 nos não transportados contra
US$ 2.302,98 nos transportados. Welch: t(7.906,3) = 18,94, p = 2,666 × 10⁻⁷⁸; médias
US$ 2.011,89 × US$ 891,15; Δ = US$ 1.120,74 (IC 95% [1.004,76; 1.236,71]); d de Cohen = 0,407.
Mann-Whitney: U = 13.846.862, Z = 37,62, r de Rosenthal = 0,404; medianas US$ 907,00 × US$ 0,00.

**Gasto por planeta (ANOVA de Welch + Kruskal-Wallis).** Levene W = 1.592,08 (p < 10⁻³⁰⁰);
razão de variâncias Europa/Terra > 37×. ANOVA de Welch: F(2; 3.000,9) = 407,57,
p = 2,571 × 10⁻¹⁵⁷, η² = 0,171, ω² = 0,171. Kruskal-Wallis: H(2) = 271,97, p = 8,772 × 10⁻⁶⁰,
ε² = 0,031. Pós-hoc de Games-Howell: Europa × Terra +US$ 2.768,76; Europa × Marte +US$ 2.384,27;
Marte × Terra +US$ 384,49 — todas com p < 0,001.

**A armadilha causal.** Gasto e transporte caminham em sentidos opostos, mas por intermediação
do criossono: quem está em criossono não consome e foi transportado com muito mais frequência.
O gasto é, na prática, um *proxy* de vigília e mobilidade. Dizer que “gastar protege” seria
falácia.

### 5.5. Seção 5 — Correlação, regressão e modelo preditivo

**Correlação (Pearson × Spearman).** As maiores correlações são de cada gasto com `TotalSpend`
— `FoodCourt` × `TotalSpend` r = 0,74 e ρ = 0,67 —, esperado por construção. Entre serviços, o
Pearson é fraco (r ≤ 0,23), mas o Spearman chega a 0,52 (`FoodCourt` × `VRDeck`), indicando que
os zeros coincidentes influenciam o coeficiente. A relação negativa mais forte, `Age` ×
`GroupSize`, é fraca (r = −0,18). `Age` × `TotalSpend` tem ρ = 0,26.

**Regressão linear para `log1p(TotalSpend)`.** OLS sobre `Age`, `HomePlanet`, `CabinDeck`, `VIP`
e `GroupSize`, com divisão 80/20 (`random_state=42`). R² = 0,257 (ajustado 0,256); F = 200,2;
RMSE treino/teste 3,18 na escala log. Associações: VIP ≈ +950%; idade +4,8% por ano; tamanho do
grupo −13% por pessoa. Diagnóstico: resíduos **não normais** (QQ em S, curtose −1,02) e
**heterocedásticos** (duas faixas, uma delas reta em zero). A inferência robusta HC3 mantém as
conclusões, exceto o deck E, que fica no limite. VIF de `HomePlanet_Europa` = 7,98 — acima do
limite de 5, pendência declarada.

**Regressão logística para `Transported`.** Pipeline com one-hot, padronização e log1p nos
gastos; sem regularização; ajustada só no treino. Divisão 80/20 estratificada (6.954/1.739;
50,4% de positivos). Pseudo-R² de McFadden = 0,311.

| Preditora (referência) | OR (IC 95%) | Efeito marginal |
| :--- | ---: | ---: |
| `CryoSleep` = True (False) | 3,21 (2,61–3,94) | +20,8 p.p. |
| `HomePlanet` = Europa (Earth) | 3,97 (2,58–6,10) | +21,0 p.p. |
| `HomePlanet` = Mars (Earth) | 1,40 (1,14–1,72) | +5,3 p.p. |
| `CabinSide` = P (S) | 0,60 (0,53–0,67) | — |
| Spa / VRDeck / RoomService (por 1 dp de log1p) | 0,48 / 0,51 / 0,55 | — |
| FoodCourt / ShoppingMall (por 1 dp de log1p) | 1,48 / 1,24 | — |

**Desempenho no teste (n = 1.739; limiar 0,5 fixado a priori).** VP = 697, VN = 657,
FP = 206, FN = 179. Acurácia 0,779; precisão 0,772; recall 0,796; especificidade 0,761;
F1 0,784; ROC-AUC 0,862; Average Precision 0,880. Contra o baseline `most_frequent` (acurácia
0,504, AUC 0,500), o ganho é de **+25,5 p.p. de acurácia** e **+0,338 de AUC**.

**Como ler os ORs.** São associações ajustadas pelas demais preditoras, não efeitos causais.
O OR do criossono é medido já descontando os gastos — e nenhum passageiro em criossono gastou;
as duas variáveis devem ser lidas em conjunto. O efeito de Europa é estimado dentro dos decks
em que os planetas coexistem. O deck T (n = 5) não é interpretável.

### 5.6. Seção 6 — Conclusões e recomendações

**Sumário executivo.** Três achados organizam a resposta: criossono (81,47% × 32,82%), origem
(66,05% / 52,44% / 42,33%) e consumo (41,92% sem gasto; mediana zero entre transportados ×
US$ 907,00 entre não transportados). O modelo logístico atinge 77,9% de acurácia e ROC-AUC de
0,862 — apoio à triagem, não decisão automática.

**Cinco recomendações:**

1. Priorizar a inspeção das cápsulas de criossono.
2. Investigar a diferença por origem, cruzando com deck e classe.
3. Não usar gasto como proxy de importância ou de presença.
4. Usar o modelo como apoio à triagem, com revisão humana.
5. Comunicar com medianas e proporções, não com médias.

**Limitações:** associação não é causa; divisão única de treino e teste, sem intervalo de
incerteza; divisão por passageiro e não por grupo de viagem (avaliação possivelmente otimista);
imputação pela moda em 2,1% a 2,5% das categóricas; VIF de 7,98 em `HomePlanet_Europa`.

---

## 6. Conceitos que a banca pode pedir para explicar

> Explique em uma frase simples e depois em uma frase técnica. O T3 valoriza clareza (50%).

| Conceito | Explicação simples | Explicação técnica |
| :--- | :--- | :--- |
| **MCAR / MAR / MNAR** | “O dado sumiu por acaso, ou some por causa de outra informação que temos, ou some por causa do próprio valor que sumiu.” | MCAR: independência do indicador de ausência em relação ao valor e ao desfecho. MAR: o valor ausente é condicionado a variáveis observadas. MNAR: depende do próprio valor não observado. |
| **Imputação por regra vs. estatística** | “Primeiro usamos o que a física do navio obriga; só depois chutamos com mediana e moda.” | Regras determinísticas recuperam valores exatos; a imputação estatística usa mediana/moda condicional estimada no treino. |
| **Data leakage** | “O modelo não pode espiar o futuro nem a resposta.” | Parâmetros de imputação, codificação e escala são estimados apenas no treino; o teste é transformado com esses parâmetros. |
| **Zero-inflação** | “Muita gente não gastou nada, então a média fica artificialmente alta.” | Mistura de uma massa pontual em zero com uma distribuição contínua positiva; média não é um bom resumo. |
| **Assimetria e curtose** | “Assimetria mede o quanto a distribuição puxa para um lado; curtose, o peso das caudas.” | Terceiro e quarto momentos padronizados; assimetria 4,40 e curtose 27,28 em `TotalSpend` indicam cauda longa à direita. |
| **QQ-plot** | “É um teste visual: se os pontos ficam na reta, a distribuição teórica serve.” | Compara quantis empíricos com quantis teóricos; desvios sistemáticos indicam afastamento da lei proposta. |
| **Shapiro-Wilk** | “Testa se os dados vêm de uma Normal.” | Teste de aderência com boa potência em amostras pequenas; p deixa de ser confiável acima de ~5.000 observações. |
| **Kolmogorov-Smirnov / Lilliefors** | “Mede a maior distância entre a distribuição dos dados e a teórica.” | KS compara funções de distribuição acumulada; Lilliefors corrige o viés quando média e desvio são estimados da amostra. |
| **Qui-quadrado** | “Testa se duas variáveis categóricas andam juntas.” | Compara frequências observadas e esperadas sob independência; exige frequência esperada ≥ 5 e reporta V de Cramér como tamanho de efeito. |
| **V de Cramér** | “É o tamanho da associação entre categorias, de 0 a 1.” | Medida de associação baseada no χ², normalizada pelo n e pelos graus de liberdade. |
| **t de Welch** | “Compara duas médias sem exigir variâncias iguais.” | Aproximação de Welch-Satterthwaite para graus de liberdade; robusta à heterocedasticidade. |
| **ANOVA de Welch** | “Compara três ou mais médias sem exigir variâncias iguais.” | Teste omnibus com ponderação por variâncias; pós-hoc de Games-Howell controla o erro familiar. |
| **Mann-Whitney / Kruskal-Wallis** | “Comparam grupos usando postos, não médias.” | Testes não paramétricos de dominância estocástica; robustos a assimetria e outliers. |
| **d de Cohen / η²** | “Dizem o tamanho prático da diferença, não só se ela existe.” | d padroniza a diferença de médias pelo desvio; η² é a proporção da variância explicada pelo fator. |
| **Pearson vs. Spearman** | “Pearson mede relação em linha reta; Spearman, relação em ordem.” | Correlação linear vs. correlação de postos, menos sensível a outliers e a relações monotônicas não lineares. |
| **VIF** | “Mede se duas preditoras dizem quase a mesma coisa.” | Fator de inflação da variância: valores acima de 5 indicam multicolinearidade relevante. |
| **Odds Ratio** | “Quantas vezes a chance do desfecho muda quando a variável muda.” | Razão de chances em modelo logístico, ajustada pelas demais preditoras. |
| **ROC-AUC** | “Mede a capacidade de separar as classes em qualquer limiar.” | Área sob a curva TPR × FPR; 0,5 é aleatório e 1,0 é separação perfeita. |
| **Limiar de 0,5** | “O ponto de corte para classificar como transportado.” | Probabilidade prevista acima de 0,5 vira classe positiva; fixado *a priori* para evitar otimização no teste. |

---

## 7. Perguntas prováveis e respostas

**1. Qual é o cliente e qual decisão ele toma com isso?**
O Comando de Operações Espaciais e a equipe de resgate. A decisão é triagem: quais cápsulas e
quais perfis priorizar na apuração e na comunicação. Não é uma decisão automática.

**2. Por que *Spaceship Titanic* e não outro dataset?**
É público, tem um problema de classificação claro (`Transported`), mistura variáveis
categóricas, quantitativas, zero-infladas e com ausência estrutural — o que permite cobrir
todas as etapas do T3 sem simplificar os métodos.

**3. A base é grande o suficiente?**
Sim para os métodos usados: 8.693 passageiros, 50,36% de positivos. O n grande é uma vantagem
para os testes de Welch e para o modelo, mas obriga a interpretar o p-valor com cautela.

**4. Por que não apagar as linhas com valores ausentes?**
Porque 24,01% das linhas têm pelo menos um ausente. Apagar reduziria o poder dos testes e
impediria prever 23,29% do teste. Além disso, boa parte da ausência é recuperável por regra de
negócio.

**5. A imputação não inventa dados?**
Recupera o que a física do navio obriga (ex.: criossono não consome) e, no restante, usa
mediana/moda condicional estimada no treino. A sensibilidade mostra impacto máximo de 0,64 p.p.
nas proporções e 0,77 p.p. nas taxas.

**6. Como vocês evitaram *data leakage*?**
Todos os parâmetros — medianas, modas, mapeamentos de sobrenome, codificação one-hot, escala e
limiar — foram estimados apenas no treino. O teste foi transformado com esses parâmetros.

**7. Por que `TotalSpend` foi tratado como mistura?**
Porque 41,92% são zeros exatos. Uma lei contínua não descreve um átomo em zero. Separamos
“quem gasta” de “quanto gasta” e testamos o log dos positivos.

**8. Por que rejeitar a normalidade e ainda usar teste paramétrico?**
Porque o p sempre rejeita com n grande; o critério é o tamanho do desvio. `Age` tem W = 0,980 e
D = 0,076 (desvio pequeno), e o teste de Welch é robusto para n desta ordem. O Mann-Whitney
entra como salvaguarda.

**9. Por que ANOVA de Welch e não a clássica?**
Levene rejeitou a homocedasticidade e a razão de variâncias Europa/Terra passa de 37×. A ANOVA
clássica e o Tukey-Kramer não são apropriados; Welch e Games-Howell controlam o erro familiar
sob variâncias desiguais.

**10. O que significa V de Cramér = 0,467?**
Associação muito forte entre criossono e transporte. É o maior efeito categórico do estudo.
Já o V de 0,037 do VIP é desprezível, apesar do p pequeno.

**11. Por que o gasto cai entre os transportados?**
Porque o criossono confunde a relação: quem está em criossono não consome e foi transportado
com muito mais frequência. O gasto é um *proxy* de vigília e mobilidade, não um fator protetor.

**12. O modelo é bom?**
Sim para triagem: 77,9% de acurácia, ROC-AUC 0,862 e F1 0,784, contra 50,4% do baseline. Mas a
divisão é única, não há intervalo de incerteza e a separação é por passageiro, não por grupo.

**13. Por que 77,9% e não 90%?**
Porque as variáveis disponíveis não capturam tudo. O modelo é simples e interpretável, o que é
uma escolha deliberada. Melhorar exigiria features adicionais e validação cruzada por grupo.

**14. Por que o limiar é 0,5?**
Foi fixado *a priori* para não otimizar no teste. Outros limiares trocam recall por
especificidade; a escolha depende do custo de cada erro, que o cliente precisa definir.

**15. O que é o VIF de 7,98 e por que isso importa?**
É multicolinearidade entre `HomePlanet_Europa` e os decks. Os coeficientes dessa variável devem
ser lidos com cautela; não removemos a variável, mas declaramos a limitação.

**16. Por que não remover os outliers de gasto?**
Porque são clientes reais de alto consumo, não erros. Remover distorceria a receita e a
distribuição. Usamos testes robustos e reportamos mediana e proporção de zeros.

**17. Como vocês garantiram a reprodutibilidade?**
Semente 42, caminhos relativos, execução *Restart & Run All* em kernel limpo, notebook
consolidado por script e manifesto de mapeamento. Nenhum caminho absoluto no código ou nas
saídas.

**18. Qual é a maior limitação do trabalho?**
O desenho observacional. Também pesam a divisão única de treino/teste e a separação por
passageiro, que pode deixar a avaliação otimista. Nada disso autoriza causalidade.

**19. O que vocês fariam com mais tempo?**
Validação cruzada agrupada por família, modelo em duas partes para o gasto, calibração do
limiar pelo custo de erro e uma análise de mediação formal do criossono.

**20. Onde está o código de cada análise?**
No notebook consolidado, Seção 1 a 6. O mapeamento ticket → notebook está em
`notebooks/consolidacao.json`, e cada documento de conclusão referencia a seção correspondente.

**21. Por que o notebook tem 227 células e 140 de Markdown?**
Porque o T3 valoriza interpretação (50% da nota). Cada saída relevante tem uma célula de texto
explicando o que o cliente deve concluir. O código é comentado e não há *prints* soltos.

**22. A apresentação usou os mesmos números do relatório?**
Sim. A fonte é o notebook consolidado executado; os documentos `docs/conclusoes/01` a `06` e o
catálogo de figuras citam a mesma execução.

---

## 8. Números de bolso (nunca cite errado)

| Indicador | Valor | Origem |
| :--- | ---: | :--- |
| Passageiros analisados | 8.693 | Seção 1 |
| Taxa global de transporte | 50,36% (4.378) | Seção 2 |
| Criossono × acordado | 81,47% × 32,82% | Seção 2 |
| Origem: Europa / Marte / Terra | 66,05% / 52,44% / 42,33% | Seção 2 |
| Decks B / C | 72,95% / 68,07% | Seção 2 |
| VIP × não VIP | 38,19% × 50,65% | Seção 2 |
| Sem nenhum gasto | 41,92% (3.644) | Seção 3 |
| Gasto mediano: transportado × não | US$ 0,00 × US$ 907,00 | Seção 4 |
| Idade: média / mediana / dp | 28,78 / 27 / 14,35 | Seção 2 |
| Idade: W / D de aderência | 0,980 / 0,076 | Seção 3 |
| Gasto positivo: W / D de aderência | 0,891 / 0,126 | Seção 3 |
| χ² criossono / V | 1.897,71 / 0,467 | Seção 4 |
| χ² planeta / V | 338,82 / 0,197 | Seção 4 |
| χ² VIP / V | 12,07 / 0,037 | Seção 4 |
| Welch: t / d / Δ | 18,94 / 0,407 / US$ 1.120,74 | Seção 4 |
| ANOVA de Welch: F / η² | 407,57 / 0,171 | Seção 4 |
| Acurácia / ROC-AUC / F1 | 77,9% / 0,862 / 0,784 | Seção 5 |
| Ganho sobre o baseline | +25,5 p.p. de acurácia | Seção 5 |
| OR criossono / Europa | 3,21 / 3,97 | Seção 5 |

---

## 9. Limitações e riscos — como falar deles sem enfraquecer o trabalho

1. **Associação não é causa.** Diga primeiro, repita no fim. É o que mostra maturidade
   analítica. A banca tende a valorizar quem reconhece o limite.
2. **Divisão única de treino e teste.** Não há intervalo de incerteza. A validação cruzada
   fica como próximo passo.
3. **Divisão por passageiro, não por grupo.** Famílias podem aparecer dos dois lados; a
   avaliação pode ser otimista em magnitude desconhecida.
4. **Imputação pela moda em 2,1% a 2,5% das categóricas.** A sensibilidade máxima é 0,77 p.p.
   nas taxas; não muda as conclusões.
5. **VIF de 7,98 em `HomePlanet_Europa`.** Coeficientes dessa variável devem ser lidos com
   cautela.
6. **Amostras pequenas.** VIP (199) e deck T (5) não sustentam estimativas estáveis.
7. **O modelo não é uma sentença.** É apoio à triagem, com revisão humana.

**Como encerrar uma pergunta sobre limitação:**

> “Esse é um limite real e nós o declaramos no relatório. Ele não invalida a associação que
> encontramos; limita o que podemos afirmar sobre causa e sobre generalização.”

---

## 10. Demonstração ao vivo (se houver)

**Antes da apresentação:**

```bash
# Na raiz do projeto, com o ambiente ativo
source .venv/bin/activate
python src/consolidar_notebooks.py --validar-mapa
```

**Se precisar mostrar o notebook:**

1. Abra `notebooks/00_projeto_final_estatistica.ipynb`.
2. Mostre o índice (primeira célula) e diga que são seis seções.
3. Role até a tabela de criossono (Seção 2) e a tabela-resumo (Seção 4).
4. Mostre a célula da Seção 6 que recomputa os números de manchete.

**Se precisar reexecutar (só se a banca pedir):**

```bash
jupyter nbconvert --to notebook --execute --inplace \
  --ExecutePreprocessor.timeout=600 \
  notebooks/00_projeto_final_estatistica.ipynb
```

**Plano B:** se a máquina falhar, use as figuras de `report/figures/` e os documentos
`docs/conclusoes/`. Todos os números estão neles.

---

## 11. Checklist de ensaio

- [ ] Cronometrar os 13 minutos; cortar 1 minuto da descritiva se estourar.
- [ ] Abrir as figuras na ordem: `fig_02`, `fig_01`, `fig_03`, `fig_04`, `fig_07`, `fig_08`.
- [ ] Repetir em voz alta a frase de cautela: “associação observacional, não causal”.
- [ ] Decorar os 8 números de bolso principais: 50,36%; 81,47% × 32,82%; 66,05% / 52,44% / 42,33%; 41,92%; 77,9%; 0,862.
- [ ] Ter o notebook consolidado aberto na Seção 6.
- [ ] Preparar a resposta sobre limitações (Seção 9).
- [ ] Testar o projetor e o tamanho das fontes dos gráficos.
- [ ] Levar o PDF do relatório e uma cópia das figuras em pendrive.

---

## 12. Glossário para quem não é da área

| Termo | Tradução para o cliente |
| :--- | :--- |
| **Dataset** | Tabela de dados com uma linha por passageiro e uma coluna por informação. |
| **Variável-alvo** | A coluna que queremos prever: `Transported` (foi ou não transportado). |
| **Valor ausente** | Informação que se perdeu no registro da nave. |
| **Imputação** | Preencher o valor ausente com uma regra ou com uma estimativa. |
| **Outlier** | Valor muito distante do padrão; nem sempre é erro. |
| **Mediana** | O valor do meio: metade dos passageiros está abaixo, metade acima. |
| **Média** | Soma dividida pelo número de passageiros; é sensível a valores extremos. |
| **Associação** | Duas coisas acontecem juntas com mais frequência do que ao acaso. |
| **Causalidade** | Uma coisa provoca a outra. Associação não prova causalidade. |
| **p-valor** | Probabilidade de ver um resultado tão extremo se não houver efeito real. |
| **Tamanho de efeito** | O quanto a diferença importa na prática, não apenas se ela existe. |
| **Modelo preditivo** | Regra matemática que estima a probabilidade de um passageiro ter sido transportado. |
| **Acurácia** | Percentual de acertos do modelo. |
| **ROC-AUC** | Capacidade de separar transportados de não transportados em qualquer limiar. |
| **Recall** | Dos que foram transportados, quantos o modelo identificou. |
| **Especificidade** | Dos que não foram, quantos o modelo identificou corretamente. |
| **Reprodutibilidade** | Qualquer pessoa consegue rodar o notebook e obter os mesmos resultados. |

---

## 13. Anexos

### 13.1. Arquivos que o apresentador deve conhecer

| Arquivo | Para que serve |
| :--- | :--- |
| `notebooks/00_projeto_final_estatistica.ipynb` | Entregável principal; notebook consolidado. |
| `docs/conclusoes/01_ambiente_dados.md` | Contexto, dicionário, imputação e variáveis derivadas. |
| `docs/conclusoes/02_descritiva_visual.md` | Perfil, consumo, outliers e galeria de figuras. |
| `docs/conclusoes/03_probabilidade_distribuicoes.md` | QQ-plots, testes de aderência e implicações. |
| `docs/conclusoes/04_testes_hipoteses_anova.md` | Qui-quadrado, Welch, ANOVA e pós-hoc. |
| `docs/conclusoes/05_correlacao_regressoes.md` | Correlação, OLS, logística, ORs e métricas. |
| `docs/conclusoes/06_conclusoes_recomendacoes.md` | Sumário executivo e recomendações. |
| `docs/catalogo_figuras.md` | As 8 figuras do relatório, com legendas formais. |
| `report/figures/` | PNGs a 300 DPI. |
| `docs/apresentacao/roteiro_apresentacao.md` | Versão curta deste guia. |

### 13.2. Mapa ticket → seção → notebook

| Seção T3 | Tickets | Notebook de origem |
| :---: | :--- | :--- |
| 1 | KAN-10, KAN-11, KAN-12 | `01_preparacao_dados.ipynb` |
| 2 | KAN-14, KAN-15, KAN-16, KAN-17 | `02_estatistica_descritiva.ipynb`, `04_kan15_resumos_quantitativos.ipynb`, `03_kan17_valores_extremos.ipynb` |
| 3 | KAN-19, KAN-20, KAN-21, KAN-22 | `05_kan19_variaveis_aleatorias_distribuicoes.ipynb`, `03_probabilidade_distribuicoes.ipynb` |
| 4 | KAN-24 a KAN-28 | `04_testes_hipoteses_anova.ipynb` |
| 5 | KAN-30 a KAN-34 | `05_correlacao_regressoes.ipynb` |
| 6 | KAN-44 | `06_conclusoes_recomendacoes.ipynb` |

### 13.3. Frases de transição prontas

- “Antes de analisar, arrumamos a base.”
- “A primeira pista é o confinamento.”
- “A segunda pista é a origem — mas ela anda junto com o deck.”
- “Para escolher o teste certo, olhamos a forma da distribuição.”
- “Aqui separamos o que é estatisticamente sustentável do que é ruído.”
- “Com as variáveis certas, passamos ao modelo conjunto.”
- “O modelo ajuda a triagem; não substitui a decisão humana.”
- “E a cautela que vale para todo o projeto: associação não é causa.”

---

*Guia produzido no âmbito do KAN-37, alinhado ao notebook consolidado e aos documentos de
conclusão das Seções 1 a 6. Nenhum número foi citado sem seção de origem.*
