# Conclusões da Inferência Estatística e ANOVA (`04_testes_hipoteses_anova`)

- **Tickets Relacionados (Jira):** [`KAN-28`](https://megamatic.atlassian.net/browse/KAN-28) e [`KAN-29`](https://megamatic.atlassian.net/browse/KAN-29)
- **Responsável Principal:** Daniela Amaro (`@danamaro1-tech`)
- **Revisora Dedicada:** Renatta Batista (`@renattabatista`)
- **Notebook Fonte:** [`notebooks/04_testes_hipoteses_anova.ipynb`](../../notebooks/04_testes_hipoteses_anova.ipynb)
- **Conjunto de Dados Analisado:** `data/processed/spaceship_titanic_clean.csv` ($N = 8.693$ passageiros)
- **Nível de Significância Adotado:** $\alpha = 0{,}05$ (pré-fixado com controle de erro Tipo I)

---

## 1. Visão Executiva e Contexto de Negócio

No âmbito da missão de transporte interplanetário da nave *Spaceship Titanic*, a ocorrência da anomalia do feixe espaço-temporal resultou no teletransporte involuntário de aproximadamente metade dos passageiros para outra dimensão ($50{,}36\%$).

Este documento sintetiza de forma rigorosa, didática e desprovida de jargões desnecessários as conclusões de todo o arcabouço de **Inferência Estatística** (Capítulo 4 do projeto):
1. **Associação Categórica:** Como os atributos qualitativos de origem (`HomePlanet`), isolamento biológico (`CryoSleep`) e classe de acomodação (`VIP`) se associam à condição de sinistro (`Transported`).
2. **Comparação de Despesas por Desfecho:** De que maneira o consumo monetário total a bordo (`TotalSpend`) difere entre passageiros que foram ou não transportados.
3. **Disparidades de Gastos por Origem Planetária:** Como o planeta natal molda o comportamento de compra e consumo de amenidades a bordo da nave.

Todas as análises empíricas foram executadas com foco na **relevância substantiva (tamanho do efeito)**, evitando a armadilha de supervalorizar meras significâncias de amostras massivas ($N = 8.693$).

---

## 2. Mapeamento de Rastreabilidade com o Notebook

Para fins de auditoria acadêmica e reprodutibilidade científica (exigida pelos critérios de governança do CIn/UFPE), a tabela a seguir mapeia a correlação direta entre as seções analíticas deste relatório e as células executadas no notebook [`notebooks/04_testes_hipoteses_anova.ipynb`](../../notebooks/04_testes_hipoteses_anova.ipynb):

| Seção Metodológica | Tópico Analítico | Células no Notebook | Entregáveis Gerados |
| :--- | :--- | :--- | :--- |
| **KAN-24** | Definição Prévia de Hipóteses e Contrato | Células `[0]` a `[10]` | Formulação formal de $H_0$ e $H_1$, nível $\alpha = 0{,}05$, validação de integridade dos dados |
| **KAN-25** | Testes Qui-Quadrado de Independência | Células `[11]` a `[16]` | Tabelas de contingência (observada vs esperada), $\chi^2$, valor-$p$, $V$ de Cramér e resíduos ajustados |
| **KAN-26** | Comparação de Gastos por Teletransporte | Células `[17]` a `[21]` | Teste de Levene, Teste $t$ de Welch ($t, df, p$), Mann-Whitney $U$ ($Z, r$), $d$ de Cohen e IC 95% |
| **KAN-27** | ANOVA e Comparações entre Planetas | Células `[22]` a `[27]` | Levene, ANOVA de Welch ($F, \eta^2, \omega^2$), Kruskal-Wallis ($H, \epsilon^2$), Games-Howell e Dunn-Bonferroni |
| **KAN-28** | Tabela-Resumo Consolidada | Células `[28]` a `[30]` | DataFrame estruturado em 9 colunas normativas e exportação oficial em Markdown |
| **KAN-29** | Conclusões Técnicas Publicadas | Documento Atual | Síntese analítica, interpretações de negócio e advertência metodológica de causalidade |

---

## 3. Análise Detalhada dos Testes de Associação Categórica (`KAN-25`)

Foram investigadas três hipóteses de independência bivariada em relação ao evento `Transported` utilizando o teste **Qui-Quadrado de Pearson ($\chi^2$)**. Todas as relações cumpriram integralmente o pressuposto de Cochran (100% das frequências esperadas sob $H_0$ superiores a 5).

### 3.1. Planeta de Origem (`HomePlanet`) vs Teletransporte (`Transported`)
- **Estatística do Teste:** $\chi^2(2) = 338{,}82$, $p = 2{,}663 \times 10^{-74}$ (Rejeita $H_0$).
- **Tamanho do Efeito:** $V \text{ de Cramér} = 0{,}197$ (Associação de força média).
- **Taxas Empíricas de Teletransporte:**
  - **Europa:** $65{,}94\%$ teletransportados ($1.436$ de $2.174$).
  - **Marte:** $52{,}33\%$ teletransportados ($946$ de $1.804$).
  - **Terra:** $42{,}39\%$ teletransportados ($1.996$ de $4.715$).
- **Significado de Negócio:** Passageiros provenientes de Europa foram os mais atingidos, enquanto os da Terra tiveram taxa inferior à média global da nave ($50{,}36\%$). A segregação espacial das cabines por origem planetária concentrou determinados grupos em conveses mais expostos à anomalia.

### 3.2. Criossono (`CryoSleep`) vs Teletransporte (`Transported`)
- **Estatística do Teste:** $\chi^2(1) = 1.897{,}71$, $p < 10^{-300}$ (Rejeita $H_0$).
- **Tamanho do Efeito:** $V \text{ de Cramér} = 0{,}467$ ($\phi = 0{,}467$, Associação de magnitude muito forte).
- **Taxas Empíricas de Teletransporte:**
  - **Em Criossono:** $81{,}75\%$ teletransportados ($2.563$ de $3.135$).
  - **Acordados (Não em sono):** $32{,}90\%$ teletransportados ($1.815$ de $5.558$).
- **Significado de Negócio:** O estado de criossono é a **variável individual de maior poder preditivo** no conjunto de dados. Passageiros isolados nas cápsulas criogênicas não tiveram capacidade de resposta evasiva ou de evacuação de emergência perante o alarme do incidente, ficando totalmente vulneráveis ao evento dimensional.

### 3.3. Status VIP (`VIP`) vs Teletransporte (`Transported`)
- **Estatística do Teste:** $\chi^2(1) = 12{,}07$, $p = 5{,}126 \times 10^{-4}$ (Rejeita $H_0$).
- **Tamanho do Efeito:** $V \text{ de Cramér} = 0{,}037$ (Associação desprezível / negligível).
- **Taxas Empíricas de Teletransporte:**
  - **VIP:** $38{,}21\%$ teletransportados ($76$ de $199$).
  - **Não VIP:** $50{,}65\%$ teletransportados ($4.302$ de $8.494$).
- **Significado de Negócio:** Embora o teste aponte significância estatística em virtude do grande tamanho amostral ($p = 0{,}0005$), a magnitude prática é ínfima ($V = 0{,}037$). Conclui-se que o status VIP **não conferiu privilégio operacional mensurável** na proteção contra o teletransporte. Trata-se de um exemplo clássico em que significância estatística não se traduz em relevância operacional.

---

## 4. Comparação de Gastos por Teletransporte (`KAN-26`)

Investigou-se se os passageiros que foram teletransportados apresentavam um padrão de despesas acumuladas (`TotalSpend`) diferente daqueles que permaneceram na nave.

### 4.1. Diagnóstico de Pressupostos
- O teste de homocedasticidade de **Levene centrado na mediana (Brown-Forsythe)** revelou severa quebra de igualdade de variâncias: $W = 131{,}36$ ($p = 3{,}407 \times 10^{-30}$).
- O desvio-padrão dos não teletransportados ($s = \$3.142{,}61$) é amplamente superior ao dos teletransportados ($s = \$2.302{,}98$), com $41{,}9\%$ da amostra apresentando gasto rigorosamente igual a zero.
- **Decisão Metodológica:** O Teste $t$ clássico de Student foi terminantemente descartado, adotando-se o **Teste $t$ de Welch (1947)** como teste paramétrico principal e o **Teste $U$ de Mann-Whitney** como salvaguarda não paramétrica de dominância estocástica.

### 4.2. Resultados Paramétricos e Não Paramétricos
- **Teste $t$ de Welch:** $t(7.906{,}3) = 18{,}94$, $p = 2{,}666 \times 10^{-78}$ (Rejeita $H_0$).
  - Média Não Transportados: $\$2.011{,}89$
  - Média Transportados: $\$891{,}15$
  - Diferença Absoluta de Médias: $\Delta = +\$1.120{,}74$ em favor dos não transportados (IC 95%: $[\$1.004{,}76, \$1.236{,}71]$).
  - Tamanho do Efeito: $d \text{ de Cohen} = 0{,}407$ (Efeito moderado a expressivo).
- **Teste $U$ de Mann-Whitney:** $U = 13.846.862$, $Z = 37{,}62$, $p < 10^{-300}$ (Rejeita $H_0$).
  - Tamanho do Efeito: $r \text{ de Rosenthal} = 0{,}404$ (Efeito de magnitude moderada).
  - Mediana Não Transportados: $\$907{,}00$ vs Mediana Transportados: $\$0{,}00$.

### 4.3. Conclusão de Negócio
Passageiros que não foram transportados despenderam mais que o dobro (aprox. 2,3 vezes) da quantia média em comparação aos teletransportados. Este padrão reflete a dinâmica de mobilidade na nave: passageiros acordados circulavam ativamente pelos centros de conveniência (`FoodCourt`, `ShoppingMall`, `Spa`, `VRDeck`), enquanto os confinados em criossono registraram consumo nulo e foram afetados em massa pelo feixe.

---

## 5. Comparação de Gastos entre Planetas de Origem (`KAN-27`)

Avaliou-se a hipótese de que o padrão de consumo a bordo diverge segundo a procedência dos passageiros (`Earth`, `Europa` e `Mars`).

### 5.1. Diagnóstico de Heterocedasticidade
- Teste de Levene (Brown-Forsythe): $W = 1.592{,}08$, $p < 10^{-300}$.
- A variabilidade entre planetas é extremamente discrepante:
  - **Europa:** $\mu = \$3.444{,}00$, $s = \$4.825{,}46$ (amplitude interquartil IQR = $\$5.334{,}75$)
  - **Mars:** $\mu = \$1.059{,}73$, $s = \$1.347{,}61$ (IQR = $\$1.723{,}00$)
  - **Earth:** $\mu = \$675{,}24$, $s = \$788{,}02$ (IQR = $\$888{,}00$)
- A razão de variâncias entre Europa e Terra supera $37\times$. Por conseguinte, a **ANOVA clássica de Fisher e o teste de Tukey-Kramer foram rejeitados**, aplicando-se a **ANOVA de Welch (1951)** e o procedimento pós-hoc de **Games-Howell (1976)**.

### 5.2. Testes Globais (Omnibus)
- **ANOVA de Welch a Um Fator:**
  - $F(2, 3.000{,}9) = 407{,}57$, $p = 2{,}571 \times 10^{-157}$ (Rejeita $H_0$).
  - Tamanho do Efeito: $\eta^2 = 0{,}1714$ ($\omega^2 = 0{,}1712$).
  - **Interpretação:** A origem planetária é responsável por **$17{,}14\%$ de toda a dispersão de despesas observada na nave**. Na convenção de Cohen, valores de $\eta^2 > 0{,}14$ representam um efeito de **grande magnitude prática**.
- **Teste de Kruskal-Wallis ($H$):**
  - $H(2) = 271{,}97$, $p = 8{,}772 \times 10^{-60}$ (Rejeita $H_0$).
  - Tamanho do Efeito: $\epsilon^2 = 0{,}0313$ (Efeito confirmatório relevante nos postos).

### 5.3. Comparações Múltiplas Pós-Hoc Par a Par (Games-Howell)
Todas as três combinações bivariadas apresentaram diferenças altamente significantes com $p < 0{,}001$:

1. **Europa vs Terra:**
   - $\Delta = +\$2.768{,}76$ em favor de Europa.
   - IC 95%: $[\$2.524{,}55, \$3.012{,}96]$, $q = 37{,}60$, $p = 4{,}94 \times 10^{-13}$.
   - Os passageiros de Europa despenderam, em média, mais de $5\times$ o valor despendido pelos terrestres.
2. **Europa vs Marte:**
   - $\Delta = +\$2.384{,}27$ em favor de Europa.
   - IC 95%: $[\$2.130{,}42, \$2.638{,}11]$, $q = 31{,}15$, $p < 10^{-16}$.
   - O passageiro europeu supera o marciano em mais de $\$2.300$ per capita.
3. **Marte vs Terra:**
   - $\Delta = +\$384{,}49$ em favor de Marte.
   - IC 95%: $[\$305{,}36, \$463{,}61]$, $q = 16{,}12$, $p = 1{,}20 \times 10^{-12}$.
   - Os marcianos apresentam nível de despesa intermediário, superando moderadamente a classe básica da Terra.

### 5.4. Síntese de Segmentação Mercadológica
Estabelece-se uma hierarquia clara de consumo: $\mu_{\text{Europa}} (\$3.444) \gg \mu_{\text{Mars}} (\$1.060) > \mu_{\text{Earth}} (\$675)$. Europa funciona como uma classe aristocrática de alto poder aquisitivo e preferência por luxo (`FoodCourt`, `Spa` e `VRDeck`); Marte atua como classe trabalhadora operacional (`RoomService` e `ShoppingMall`); e a Terra agrupa a imigração econômica de massa, com gastos contidos e alta concentração de passageiros sem consumo.

---

## 6. Tabela-Resumo Consolidada dos Testes de Hipóteses (`KAN-28`)

A tabela a seguir cumpre rigorosamente as 9 colunas normativas especificadas no ticket de governança **KAN-28**, integrando todos os testes de hipótese e procedimentos de ANOVA executados nas trilhas inferenciais:

| Pergunta de Pesquisa / Relação Analisada | Hipótese Nula ($H_0$) e Alternativa ($H_1$) | Teste Estatístico Aplicado | Verificação dos Pressupostos | Valor da Estatística do Teste | Valor-$p$ Observado | Tamanho do Efeito | Decisão Estatística ($\alpha=0{,}05$) | Conclusão em Lógica de Negócio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Pergunta 1:** Associação entre Planeta de Origem (`HomePlanet`) e Teletransporte (`Transported`) | $H_0$: `HomePlanet` e `Transported` são independentes ($p_{ij} = p_{i\cdot} p_{\cdot j}$)<br>$H_1$: Há associação estatística entre as variáveis | Teste Qui-Quadrado de Independência (Pearson) | Atendido: 100% das frequências esperadas $\ge 5$ (mínimo observado: $895{,}46$; $N = 8.693$) | $\chi^2 = 338{,}82$<br>($df = 2$) | $2{,}663 \times 10^{-74}$ | $V \text{ de Cramér} = 0{,}197$<br>(Associação moderada) | **Rejeita $H_0$** | Passageiros de Europa apresentam taxa de transporte superior ($65{,}9\%$) em relação à Terra ($42{,}4\%$) e Marte ($52{,}3\%$), indicando segmentação espacial do sinistro. |
| **Pergunta 2:** Associação entre Criossono (`CryoSleep`) e Teletransporte (`Transported`) | $H_0$: `CryoSleep` e `Transported` são independentes<br>$H_1$: Há associação estatística entre as variáveis | Teste Qui-Quadrado de Independência (com Correção de Yates) | Atendido: 100% das frequências esperadas $\ge 5$ (mínimo observado: $1.556{,}14$; $N = 8.693$) | $\chi^2 = 1.897{,}71$<br>($df = 1$) | $< 10^{-300}$ | $V \text{ de Cramér} = 0{,}467$<br>(Associação muito forte) | **Rejeita $H_0$** | O confinamento em criossono é o preditor isolado mais expressivo de teletransporte ($81{,}8\%$ vs $32{,}9\%$), definindo o perfil crítico de passageiros afetados. |
| **Pergunta 3:** Associação entre Status VIP (`VIP`) e Teletransporte (`Transported`) | $H_0$: `VIP` e `Transported` são independentes<br>$H_1$: Há associação estatística entre as variáveis | Teste Qui-Quadrado de Independência (com Correção de Yates) | Atendido: 100% das frequências esperadas $\ge 5$ (mínimo observado: $98{,}78$; $N = 8.693$) | $\chi^2 = 12{,}07$<br>($df = 1$) | $5{,}126 \times 10^{-4}$ | $V \text{ de Cramér} = 0{,}037$<br>(Associação desprezível) | **Rejeita $H_0$** | Apesar da significância estatística proporcionada pelo $N$ elevado, a magnitude prática é irrelevante ($V = 0{,}037$; taxa VIP $38{,}2\%$ vs não-VIP $50{,}6\%$). |
| **Pergunta 4 (Paramétrico):** Comparação de Gasto Total (`TotalSpend`) por Teletransporte (`Transported`) | $H_0$: $\mu_{\text{Não Transportado}} = \mu_{\text{Transportado}}$<br>$H_1$: $\mu_{\text{Não Transportado}} \neq \mu_{\text{Transportado}}$ | Teste $t$ de Welch para Amostras Independentes (Heterocedástico) | Heterocedasticidade confirmada via Levene ($W = 131{,}36$, $p < 0{,}001$); robustez assintótica garantida pelo TCL ($N = 8.693$) | $t = 18{,}94$<br>($df = 7.906{,}3$) | $2{,}666 \times 10^{-78}$ | $d \text{ de Cohen} = 0{,}407$<br>(Efeito moderado; $\Delta = +\$1.120{,}74$) | **Rejeita $H_0$** | Não teletransportados gastaram substancialmente mais ($\$2.011{,}89$ vs $\$891{,}15$); passageiros ativos em trânsito consom mais amenidades e evitam zonas críticas. |
| **Pergunta 4 (Não Paramétrico):** Comparação de Postos de Gasto Total (`TotalSpend`) por Teletransporte | $H_0$: $P(X_{\text{Não}} > X_{\text{Sim}}) = 0{,}5$<br>$H_1$: Dominância estocástica de postos | Teste $U$ de Mann-Whitney (Soma de Postos de Wilcoxon) | Atendido: Variável contínua/ordinal sob amostragem independente (dispensa normalidade e homocedasticidade) | $U = 13.846.862$<br>($Z = 37{,}62$) | $< 10^{-300}$ | $r \text{ de Rosenthal} = 0{,}404$<br>(Efeito moderado) | **Rejeita $H_0$** | Robusta corroboração não paramétrica de que o grupo transportado concentra distribuição estocasticamente inferior de gastos (mediana $\$0{,}00$ vs $\$907{,}00$). |
| **Pergunta 5 (Global Paramétrico):** Comparação de Gastos entre Planetas de Origem (`TotalSpend` vs `HomePlanet`) | $H_0$: $\mu_{\text{Earth}} = \mu_{\text{Europa}} = \mu_{\text{Mars}}$<br>$H_1$: Pelo menos uma média populacional difere das demais | ANOVA de Welch a Um Fator (One-Way Welch ANOVA) | Severa heterocedasticidade confirmada via Levene ($W = 1.592{,}08$, $p < 0{,}001$; $s_{\text{Europa}}/s_{\text{Earth}} > 6\times$); robustez assintótica de Welch | $F = 407{,}57$<br>($df_1 = 2$, $df_2 = 3.000{,}9$) | $2{,}571 \times 10^{-157}$ | $\eta^2 = 0{,}1714$<br>($\omega^2 = 0{,}1712$; Efeito de grande magnitude) | **Rejeita $H_0$** | A origem explica $17{,}14\%$ da variância total de despesas na nave; Europa ($\$3.444{,}00$) concentra alta renda versus Marte ($\$1.059{,}73$) e Terra ($\$675{,}24$). |
| **Pergunta 5 (Global Não Paramétrico):** Comparação de Postos de Gastos entre Planetas de Origem | $H_0$: Postos de `TotalSpend` idênticos entre os 3 planetas<br>$H_1$: Ao menos um planeta difere em postos | Teste de Kruskal-Wallis ($H$) | Atendido: Amostragem independente de 3 grupos com variável quantitativa contínua sob empates tratados | $H = 271{,}97$<br>($df = 2$) | $8{,}772 \times 10^{-60}$ | $\epsilon^2 = 0{,}0313$<br>(Efeito prático relevante nos postos) | **Rejeita $H_0$** | Confirmação ordinal independente de que as disparidades de consumo entre planetas são estruturais e não causadas artificialmente por outliers. |
| **Pergunta 5 (Pós-Hoc):** Comparação Pareada Europa vs Terra | $H_0$: $\mu_{\text{Europa}} = \mu_{\text{Earth}}$<br>$H_1$: $\mu_{\text{Europa}} \neq \mu_{\text{Earth}}$ | Teste Pós-Hoc de Games-Howell (Studentized Range $q$) | Atendido: Controle rigoroso de taxa de erro Tipo I familiar sob variâncias e tamanhos desiguais | $q = 37{,}60$<br>($df = 2.455{,}8$) | $4{,}94 \times 10^{-13}$ | $\Delta = +\$2.768{,}76$<br>(IC 95%: $[\$2.524{,}55, \$3.012{,}96]$) | **Rejeita $H_0$** | Europa supera a Terra em mais de $\$2.700$ médios por passageiro, consolidando passageiros de Europa como consumidores prioritários de luxo. |
| **Pergunta 5 (Pós-Hoc):** Comparação Pareada Europa vs Marte | $H_0$: $\mu_{\text{Europa}} = \mu_{\text{Mars}}$<br>$H_1$: $\mu_{\text{Europa}} \neq \mu_{\text{Mars}}$ | Teste Pós-Hoc de Games-Howell (Studentized Range $q$) | Atendido: Controle de erro familiar sob heterocedasticidade acentuada | $q = 31{,}15$<br>($df = 2.871{,}4$) | $< 10^{-16}$ | $\Delta = +\$2.384{,}27$<br>(IC 95%: $[\$2.130{,}42, \$2.638{,}11]$) | **Rejeita $H_0$** | Passageiros de Europa mantêm gasto per capita $\$2.384$ superior ao de Marte, confirmando descolamento econômico da elite europeia. |
| **Pergunta 5 (Pós-Hoc):** Comparação Pareada Marte vs Terra | $H_0$: $\mu_{\text{Mars}} = \mu_{\text{Earth}}$<br>$H_1$: $\mu_{\text{Mars}} \neq \mu_{\text{Earth}}$ | Teste Pós-Hoc de Games-Howell (Studentized Range $q$) | Atendido: Variâncias e tamanhos amostrais desiguais ajustados pelo procedimento Games-Howell | $q = 16{,}12$<br>($df = 2.378{,}1$) | $1{,}20 \times 10^{-12}$ | $\Delta = +\$384{,}49$<br>(IC 95%: $[\$305{,}36, \$463{,}61]$) | **Rejeita $H_0$** | Marte gasta moderadamente mais que Terra ($+\$384{,}49$), caracterizando Marte como classe média operacional diante da classe econômica terrestre. |

---

## 7. Advertência Epistemológica Fundamental: Associação Estatística NÃO Implica Causalidade Direta

Um princípio basilar de inferência estatística, que deve orientar qualquer leitor deste documento e do futuro relatório executivo em PDF, é que **rejeitar uma hipótese nula de independência ou de igualdade de médias jamais autoriza inferir uma relação de causa e efeito direta entre as variáveis analisadas**.

### 7.1. O Mecanismo Interveniente do Criossono (`CryoSleep`)
A constatação de que passageiros não teletransportados gastaram muito mais ($\Delta = +\$1.120{,}74$) **não significa** que realizar compras a bordo gerou um escudo protetor contra o teletransporte. 
- O passageiro em criossono é **mecanicamente impedido de consumir amenidades** ($TotalSpend = \$0$).
- Ao mesmo tempo, passageiros em criossono estavam fisicamente confinados em compartimentos específicos da nave e sofreram teletransporte em $81{,}75\%$ dos casos.
- Logo, a variável `CryoSleep` atua como um **fator de confusão e mediação fundamental** na relação aparente entre despesas e sobrevivência.

### 7.2. Segregação Espacial e Rota de Viagem
A associação entre planeta de origem e teletransporte ($V = 0{,}197$) decorre primariamente da **arquitetura interna do navio**. Cidadãos de Europa ocupavam predominantemente os conveses superiores (`Deck A`, `Deck B`, `Deck C`), enquanto passageiros da Terra concentravam-se nos conveses inferiores (`Deck F`, `Deck G`). Caso a anomalia dimensional tenha interceptado preferencialmente determinados setores estruturais da nave, a origem planetária atua meramente como marcador indireto (proxy) da localização física no instante do incidente.

### 7.3. Implicações para a Modelagem Preditiva (Trilha 4)
As relações bivariadas analisadas neste capítulo fornecem subsídios descritivos essenciais, mas **não devem ser empregadas isoladamente como regras de decisão determinísticas**. Cabe aos modelos de regressão logística multivariada (desenvolvidos por Renatta em KAN-33 e KAN-34) isolar o efeito marginal de cada preditor, controlando simultaneamente por idade, criossono, convés e despesas.

---

## 8. Recomendações Estratégicas para o Relatório Executivo e Próximos Passos

1. **Priorização de Gráficos e Tabelas para o Relatório Final (KAN-38):**
   - Incorporar a **Tabela-Resumo Consolidada** (Seção 6) na íntegra no capítulo de resultados inferenciais.
   - Selecionar o diagrama comparativo de distribuições de gastos por planeta de origem e a matriz de resíduos padronizados do qui-quadrado de criossono.
2. **Subsidiar a Discussão Técnica Cruzada da Reunião 2 (KAN-36):**
   - Apresentar o contraste didático entre o efeito substantivo de `CryoSleep` ($V = 0{,}467$) e a irrelevância prática de `VIP` ($V = 0{,}037$), demonstrando maturidade analítica do grupo em não se deixar seduzir por valores-$p$ minúsculos.
   - Enfatizar a modelagem com variâncias heterogêneas (Welch e Games-Howell) como ponto forte metodológico do grupo diante de padrões severamente não normais.
3. **Conexão com a Trilha de Regressões (KAN-30 a KAN-35):**
   - Encaminhar os coeficientes de associação e diferenças de médias para a etapa de regressão logística, servindo como baseline contra o qual os odds ratios (razões de chance) multivariados serão comparados.
