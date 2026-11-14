# Spaceship Titanic — Análise Estatística, Modelagem Preditiva e Recomendações Operacionais

> **Relatório Técnico Final — T3**  
> **Disciplina:** Estatística Avançada e Fundamentos Probabilísticos para IA  
> **Programa:** Pós-Graduação em Inteligência Artificial / Deep Learning — Centro de Informática (CIn/UFPE)  
> **Equipe Técnica:** Daniela Amaro, Renatta Batista, Gustavo Menezes Gonçalves, Helton Gomes Soares de Lima, Luciana Almeida  
> **Data:** Novembro de 2026  
> **Repositório do Projeto:** `https://github.com/gmenezesg/spaceship-titanic-estatistica-posdl`  
> **Artefatos Vinculados:** Notebook Mestre (`notebooks/00_projeto_final_estatistica.ipynb`), Catálogo de Figuras (`docs/catalogo_figuras.md`), Apresentação Executiva (`report/apresentacao_final.pdf`)

---

## 1. Resumo Executivo

O estudo analisa os registros de 8.693 passageiros da nave fictícia *Spaceship Titanic*. O objetivo é ajudar o Comando de Operações Espaciais a entender quais perfis tiveram as maiores taxas de transporte e avaliar se um modelo pode apoiar a triagem.

A equipe tratou registros incompletos, comparou grupos de passageiros e avaliou um modelo de classificação em uma parte reservada da base.

- **Criossono.** Foram transportados 81,47% dos passageiros em criossono e 32,82% dos acordados. Essa foi a maior diferença entre os grupos categóricos destacados.
- **Origem e cabine.** A taxa foi de 66,05% entre passageiros de Europa, 52,44% entre os de Marte e 42,33% entre os da Terra. Como origem e convés se sobrepõem, os dois registros devem ser investigados em conjunto.
- **Gastos.** Cerca de 42% dos passageiros não registraram despesas. O gasto típico foi de US$ 0 entre os transportados e US$ 907 entre os não transportados.
- **Triagem.** O modelo acertou 77,9% das classificações no teste interno, ante 52,4% do classificador de referência. O resultado precisa ser confirmado em novos grupos antes de uso operacional.

Recomenda-se conferir os registros de criossono e de cabine, comunicar os gastos com medianas e proporções de zeros e validar o modelo em novos grupos antes de definir regras de triagem. As diferenças observadas orientam a investigação dos perfis e locais a bordo. Suas causas permanecem em aberto.

---

## 2. Introdução e Governança

### 2.1. O Problema de Negócio e os Objetivos do Cliente
O cliente institucional desta análise é o **Comando de Operações Espaciais da Federação**, entidade responsável pela regulação da rota comercial e coordenação das forças de resposta a desastres espaciais. A perda de contato dimensional com 4.378 almas exige uma investigação técnica pautada em dados objetivos.

A meta analítica decompõe-se em duas vertentes complementares:
1. **Compreender:** Identificar quais atributos pessoais, cabines ocupadas, gastos e estados fisiológicos exibem correlação estatística com o teletransporte, discernindo o tamanho real do efeito da mera significância provocada pelo tamanho amostral expressivo ($N = 8.693$).
2. **Prever:** Fornecer um modelo probabilístico que ranqueie passageiros conforme o risco de teletransporte, permitindo que as equipes de emergência atribuam recursos limitados de salvamento às zonas e perfis prioritários.

O estudo usa os dados do desafio *Spaceship Titanic*, do Kaggle. Os critérios de preparação, os gráficos e os resultados podem ser rastreados nos notebooks de origem e no notebook mestre.

## 3. Preparação e Engenharia de Dados

### 3.1. Dicionário, inventário e dados ausentes
O dataset original fornecido continha 8.693 linhas e 14 atributos heterogêneos. A investigação inicial realizou a checagem rigorosa de tipos, nulidades e duplicatas.

| Variável Original | Tipo Primitivo | Descrição Operacional | Nulos ($n$) | Taxa de Nulos |
| :--- | :---: | :--- | :---: | :---: |
| `PassengerId` | Texto (Chave) | Identificador único no formato `gggg_pp` (grupo e pessoa) | 0 | $0{,}00\%$ |
| `HomePlanet` | Categórica | Planeta de residência permanente (`Earth`, `Europa`, `Mars`) | 201 | $2{,}31\%$ |
| `CryoSleep` | Booleana | Confinamento voluntário em câmara criogênica durante a viagem | 217 | $2{,}50\%$ |
| `Cabin` | Texto | Código da acomodação física no formato `Deck/Num/Side` | 199 | $2{,}29\%$ |
| `Destination` | Categórica | Planeta de destino (`TRAPPIST-1e`, `55 Cancri e`, `PSO J318.5-22`) | 182 | $2{,}09\%$ |
| `Age` | Numérica | Idade cronológica do passageiro em anos terrestres | 179 | $2{,}06\%$ |
| `VIP` | Booleana | Contratação de serviço executivo/VIP de bordo | 203 | $2{,}34\%$ |
| `RoomService` | Contínua | Despesa acumulada em serviço de quarto de cabine (US$) | 181 | $2{,}08\%$ |
| `FoodCourt` | Contínua | Despesa acumulada na praça de alimentação e alta gastronomia | 183 | $2{,}11\%$ |
| `ShoppingMall` | Contínua | Despesa acumulada nas lojas comerciais da nave | 188 | $2{,}16\%$ |
| `Spa` | Contínua | Despesa acumulada em tratamentos estéticos e relaxamento | 183 | $2{,}11\%$ |
| `VRDeck` | Contínua | Despesa acumulada em entretenimento por realidade virtual | 188 | $2{,}16\%$ |
| `Name` | Texto | Nome de registro civil do passageiro | 200 | $2{,}30\%$ |
| `Transported` | Booleana (Alvo) | Ocorrência do sinistro de teletransporte (`True` / `False`) | 0 | $0{,}00\%$ |

O diagnóstico de integridade confirmou **zero duplicatas integrais de registros** e **zero duplicatas no identificador `PassengerId`**. 

Havia 2.324 valores ausentes distribuídos entre 2.087 passageiros. Os testes qui-quadrado por coluna compararam o indicador de ausência com `Transported`. Os valores-p acima de 0,05 e V de Cramér abaixo de 0,02 indicam que a análise não detectou associação com esse desfecho. Como outras características observadas e não observadas não foram avaliadas por esse diagnóstico, o mecanismo de ausência permanece indeterminado.

### 3.2. Saneamento e variáveis derivadas

O notebook 01 trata lacunas nas bases originais do Kaggle com regras de consistência e imputação. Células ausentes de gasto foram preenchidas com zero quando aplicável às regras de criossono e idade. Gastos observados positivos informaram a imputação de criossono quando esse campo estava ausente. A preparação usou vínculos de grupo, convés ou sobrenome onde previstos e modas de referência para categorias remanescentes.

A idade foi imputada pela mediana por planeta e status VIP. Gastos residuais foram imputados pela mediana por planeta, criossono e VIP, com mediana global quando necessário. As oito derivadas são `Group`, `GroupSize`, `IsAlone`, `CabinDeck`, `CabinNum`, `CabinSide`, `TotalSpend` e `HasSpent`. A base tratada ficou sem valores ausentes. A imputação precedeu a divisão interna de validação do modelo, discutida na seção 7.4.

---

## 4. Análise Descritiva e Visual dos Passageiros

### 4.1. Perfil Demográfico da Tripulação e Passageiros
A composição qualitativa da tripulação está sintetizada na Tabela T1 (selecionada no Catálogo de Figuras e Tabelas do `KAN-38`).

| Variável | Categoria | Frequência ($n$) | Proporção Relativa ($\%$) | Taxa de Transporte ($\%$) |
| :--- | :--- | :---: | :---: | :---: |
| **`Transported` (Alvo)** | `True` / `False` | $4.378$ / $4.315$ | $50{,}36\%$ / $49{,}64\%$ | — |
| **`HomePlanet`** | Terra (*Earth*) | 4.715 | 54,24% | 42,33% |
| | Europa (*Europa*) | 2.174 | 25,01% | 66,05% |
| | Marte (*Mars*) | 1.804 | 20,75% | 52,44% |
| **`CryoSleep`** | Acordado (`False`) | 5.558 | 63,94% | 32,82% |
| | Em Criossono (`True`) | 3.135 | 36,06% | 81,47% |
| **`CabinSide`** | Boreste (`S`) | 4.384 | 50,43% | 55,54% |
| | Bombordo (`P`) | 4.309 | 49,57% | 45,09% |
| **`VIP`** | Não-VIP (`False`) | 8.494 | 97,71% | 50,65% |
| | VIP (`True`) | 199 | 2,29% | 38,19% |
| **`IsAlone`** | Grupo Familiar (`False`)| 3.888 | 44,73% | 56,69% |
| | Solitário (`True`) | 4.805 | 55,27% | 45,24% |

A análise da distribuição etária revela uma tripulação prioritariamente jovem: média de **$28{,}8$ anos** e mediana de **$27{,}0$ anos**, com desvio-padrão de $14{,}4$ anos e amplitude interquartil de $18{,}0$ anos ($Q_1 = 19, Q_3 = 37$). Nota-se uma assimetria positiva moderada ($0{,}43$) impulsionada pela presença de passageiros idosos de até 79 anos e por uma concentração atípica de 806 crianças com até 12 anos ($9{,}27\%$ da base), incluindo 178 lactentes com idade registrada zero.

A Figura 1 compara as taxas de transporte por planeta.

![Figura 1: Taxa de transporte por planeta de origem](figures/fig_01_transporte_por_planeta.png)

*Figura 1 — Taxa de transporte por origem entre 8.693 passageiros. A linha tracejada indica a taxa global de 50,36%.*

A Figura 2 compara passageiros em criossono e acordados.

![Figura 2: Taxa de transporte por criossono](figures/fig_02_transporte_por_criossono.png)

*Figura 2 — Taxa de transporte por criossono entre 8.693 passageiros. A diferença observada foi de 48,65 pontos percentuais.*

A Figura 3 mostra a concentração de idades e o pico em zero.

![Figura 3: Distribuição da idade dos passageiros](figures/fig_03_idade_distribuicao.png)

*Figura 3 — Histograma de idade dos 8.693 passageiros em intervalos de dois anos, com curva de densidade estimada.*

### 4.2. Estrutura Espacial das Cabines e Conveses
A ocupação foi desigual entre os conveses. Os decks F e G concentram nada menos que **$62{,}76\%$ de toda a população** ($2.868$ e $2.588$ passageiros, respectivamente). A Tabela T3 destaca as categorias que mais se afastam da taxa global, entre aquelas com pelo menos 30 passageiros.

| Variável | Categoria | n | Taxa de transporte | Diferença da taxa global |
| --- | --- | ---: | ---: | ---: |
| `CryoSleep` | Em criossono | 3.135 | 81,47% | 31,10 p.p. |
| `CabinDeck` | B | 817 | 72,95% | 22,59 p.p. |
| `CabinDeck` | C | 761 | 68,07% | 17,71 p.p. |
| `CryoSleep` | Acordado | 5.558 | 32,82% | -17,54 p.p. |
| `HomePlanet` | Europa | 2.174 | 66,05% | 15,69 p.p. |
| `CabinDeck` | E | 885 | 36,05% | -14,32 p.p. |
| `VIP` | VIP | 199 | 38,19% | -12,17 p.p. |
| `Destination` | 55 Cancri e | 1.800 | 61,00% | 10,64 p.p. |

As taxas por planeta e por convés devem ser lidas em conjunto. Na base tratada, 72,6% dos passageiros de Europa estavam nos conveses B e C. Essa sobreposição dificulta separar as associações com origem e localização.

### 4.3. Padrões de Consumo e Valores Extremos (Outliers)
As cinco rubricas de consumo monetário a bordo exibem comportamento assimétrico e altamente atípico. A Tabela T2 detalha a distribuição das variáveis financeiras.

| Rubrica | Zeros (n) | Zeros (%) | Mediana (US$) | Média (US$) | Desvio-padrão (US$) | Máximo (US$) | CV |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `RoomService` | 5.671 | 65,24% | 0,00 | 221,58 | 660,80 | 14.327,00 | 2,98 |
| `FoodCourt` | 5.549 | 63,83% | 0,00 | 451,40 | 1.596,28 | 29.813,00 | 3,54 |
| `ShoppingMall` | 5.720 | 65,80% | 0,00 | 169,95 | 597,95 | 23.492,00 | 3,52 |
| `Spa` | 5.412 | 62,26% | 0,00 | 305,45 | 1.125,46 | 22.408,00 | 3,68 |
| `VRDeck` | 5.598 | 64,40% | 0,00 | 299,09 | 1.134,08 | 24.133,00 | 3,79 |
| `TotalSpend` | 3.644 | 41,92% | 717,00 | 1.447,46 | 2.808,28 | 35.987,00 | 1,94 |

A assimetria global de `TotalSpend` é de **$4{,}40$**, com curtose em excesso de **$27{,}28$**. Pelo critério de Tukey (KAN-17), utilizando o intervalo interquartil ($Q_1 = 0, Q_3 = 1.444, IQR = 1.444$), o limiar superior de valores extremos fixou-se em **US$ 3.610,00** ($Q_3 + 1{,}5 \times IQR$). Foram detectados **938 passageiros ($10{,}79\%$)** classificados como *outliers* superiores.

Os valores extremos foram mantidos para preservar a dispersão observada. O critério de Tukey sinaliza valores atípicos na distribuição e não identifica erros de registro.

A Tabela T4 compara o gasto total por desfecho e por planeta.

| Recorte | Grupo | n | Gasto zero | Mediana (US$) | Média (US$) |
| --- | --- | ---: | ---: | ---: | ---: |
| Desfecho | Transportados | 4.378 | 65,53% | 0,00 | 891,15 |
| Desfecho | Não transportados | 4.315 | 17,96% | 907,00 | 2.011,89 |
| Origem | Terra | 4.715 | 37,45% | 705,00 | 675,24 |
| Origem | Europa | 2.174 | 48,11% | 1.914,00 | 3.444,00 |
| Origem | Marte | 1.804 | 46,12% | 950,00 | 1.059,73 |

A Figura 4 compara o gasto total por desfecho.

![Figura 4: Gasto total a bordo por desfecho em escala symlog](figures/fig_04_gasto_por_transporte.png)

*Figura 4 — Distribuição do gasto total por desfecho entre 8.693 passageiros, em escala linear perto de zero e logarítmica para valores mais altos. A linha tracejada marca US$ 3.610.*

A Figura 5 detalha a dispersão dos gastos por planeta.

![Figura 5: Gasto total a bordo por planeta de origem](figures/fig_05_gasto_por_planeta.png)

*Figura 5 — Distribuição do gasto total por origem entre 8.693 passageiros. As medianas são US$ 1.914 em Europa, US$ 950 em Marte e US$ 705 na Terra.*

A Figura 6 reúne o número de passageiros e a taxa de transporte por convés.

![Figura 6: Passageiros por deck da cabine e taxa de transporte](figures/fig_06_passageiros_por_deck.png)

*Figura 6 — Ocupação e taxa de transporte por convés entre 8.693 passageiros. F e G reúnem 62,76% da amostra. O convés T tem cinco passageiros.*

---

## 5. Probabilidade, Variáveis Aleatórias e Distribuições

### 5.1. Variáveis Aleatórias Discretas e Processos de Bernoulli
O desfecho operacional `Transported` foi formalizado como uma **variável aleatória de Bernoulli**, onde:
$$Y \sim \text{Bernoulli}(p), \quad p = P(Y = 1) = \frac{4.378}{8.693} \approx 0{,}5036$$
A variância estimada está próxima do máximo de 0,25:
$$\sigma_Y^2 = p(1 - p) = 0{,}5036 \times 0{,}4964 \approx 0{,}2499 \quad (\sigma_Y \approx 0{,}5000)$$
A proporção amostral atua, portanto, como a medida canônica central. Em virtude do equilíbrio ($50{,}36\%$), qualquer classificador que pretenda demonstrar utilidade operacional deve ser comparado com classificadores de referência no mesmo conjunto de avaliação.

Similarmente, o estado de sono criogênico modela-se como:
$$C \sim \text{Bernoulli}(p_c), \quad p_c = \frac{3.135}{8.693} \approx 0{,}3606$$

### 5.2. Investigação Formal de Aderência Teórica: Idade
A idade foi registrada em anos inteiros, com concentração em zero. Na base tratada, a média foi 28,78 e o desvio-padrão, 14,35 anos. O QQ-plot do notebook 03 mostra a maioria dos pontos centrais abaixo da reta. O histograma e os diagnósticos Shapiro–Wilk (W = 0,980, p aproximado de 3,46 × 10⁻³³) e Lilliefors (D = 0,076, p aproximado de 2,50 × 10⁻¹³⁶) indicam desvio da Normal. A exclusão dos registros de idade zero aumentou D para 0,085. Acima de 5.000 observações, o valor-p de Shapiro–Wilk pode ser impreciso. W e D são estatísticas de diagnóstico, e D mede a distância máxima entre as funções de distribuição. [Documentação do SciPy](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.shapiro.html).

A Figura 7 mostra o ajuste da curva Normal ao histograma de idade.

![Figura 7 — Idade observada e Normal ajustada](figures/fig_07_idade_normal_ajustada.png)

*Figura 7 — Idade observada e curva Normal ajustada para 8.693 passageiros. A curva atribui probabilidade a idades negativas e subestima a concentração em zero.*

### 5.3. Gastos zero e distribuição dos valores positivos

Na base completa, 41,92% dos gastos totais são zero, a assimetria é 4,40 e a curtose em excesso é 27,28. Nos 5.049 gastos positivos, o diagnóstico de `log1p(TotalSpend)` encontrou assimetria de −0,19 e curtose em excesso de 4,93. A comparação com o total bruto muda tanto a escala quanto a população. O gráfico usa o log natural dos gastos positivos. Os testes foram aplicados ao log de um mais o gasto.

Os dois painéis da Figura 8 separam a frequência de gasto zero da distribuição de gastos positivos.

![Figura 8 — Proporção de zeros e distribuição dos gastos positivos](figures/fig_08_gasto_zero_e_log_normal.png)

*Figura 8 — Proporção de gastos zero na base de 8.693 passageiros e distribuição em escala logarítmica entre os 5.049 passageiros com gasto positivo.*

No recorte positivo transformado, Shapiro–Wilk produziu W = 0,891 (p aproximado de 8,57 × 10⁻⁵¹) e Lilliefors produziu D = 0,126 (p aproximado de 1,14 × 10⁻²²²). Os diagnósticos e o QQ-plot mostram desvios da Normal, mesmo após transformação. Os valores-p de Shapiro recebem a mesma ressalva de tamanho amostral aplicada à idade.

### 5.4. Escolha dos testes inferenciais

O teste t de Welch compara médias de gasto por desfecho e a ANOVA de Welch compara médias entre planetas. Ambos admitem variâncias desiguais. Os desvios-padrão de gasto são US$ 3.142,61 e US$ 2.302,98 entre não transportados e transportados, respectivamente. Entre Terra, Europa e Marte, são US$ 788,02, US$ 4.825,46 e US$ 1.347,61. Isso corresponde a razões entre a maior e a menor variância de cerca de 1,86 e 37,50, respectivamente, em linha com os diagnósticos de Levene centrado na mediana. Os grupos grandes favorecem a aproximação para médias sob independência e variâncias finitas. Games–Howell estima contrastes entre médias de planetas com variâncias e tamanhos desiguais.

Mann–Whitney bilateral e Kruskal–Wallis comparam postos. São complementares porque respondem a perguntas distintas das comparações de médias. Os zeros geram muitos empates, tratados nos cálculos. Diferenças de forma e dispersão podem contribuir para a rejeição, portanto as medianas são descritas separadamente. Os testes convencionais pressupõem observações independentes. O agrupamento por viagem pode afetar os valores-p e intervalos, e a inferência com ajuste por grupo não foi estimada. [SciPy — Mann–Whitney](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mannwhitneyu.html) e [SciPy — Kruskal–Wallis](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.kruskal.html).

---

## 6. Inferência Estatística, Testes de Hipóteses e ANOVA

### 6.1. Protocolo Formal e Tabela-Resumo Consolidada (KAN-28)
O nível nominal é 5% por teste. Games–Howell e Dunn–Bonferroni ajustam as comparações dentro de suas respectivas famílias. A tabela não presume controle global entre todas as perguntas. Resultados arredondados a zero pela rotina numérica são apresentados com limite conservador, sem afirmar valor-p literal zero.

| Pergunta de Pesquisa / Relação | Hipótese Nula ($H_0$) e Alternativa ($H_1$) | Teste Estatístico Aplicado | Pressupostos e diagnósticos | Estatística do Teste | Valor-$p$ Observado | Tamanho do Efeito | Decisão ($\alpha=0{,}05$) | Conclusão e Significado de Negócio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **P1: `HomePlanet` $\times$ `Transported`** | $H_0$: Variáveis independentes<br>$H_1$: Há associação | Qui-Quadrado de Pearson | Frequências esperadas $\ge 5$ atendidas ($100\%$; mín: $895{,}5$) | $\chi^2 = 338{,}82$<br>($df = 2$) | $2{,}66 \times 10^{-74}$ | $V \text{ de Cramér} = 0{,}197$<br>(Associação média) | **Rejeita $H_0$** | Europa apresentou maior taxa observada que Marte e Terra. |
| **P2: `CryoSleep` $\times$ `Transported`** | $H_0$: Variáveis independentes<br>$H_1$: Há associação | Qui-Quadrado de Pearson (sem Yates) | Frequências esperadas $\ge 5$ atendidas ($100\%$; mín: $1.556{,}1$) | $\chi^2 = 1.897{,}71$<br>($df = 1$) | $< 0{,}001$ | $V \text{ de Cramér} = 0{,}467$<br>(Associação muito forte) | **Rejeita $H_0$** | O grupo em criossono apresentou maior taxa observada de transporte. |
| **P3: `VIP` $\times$ `Transported`** | $H_0$: Variáveis independentes<br>$H_1$: Há associação | Qui-Quadrado de Pearson (sem Yates) | Frequências esperadas $\ge 5$ atendidas ($100\%$; mín: $98{,}8$) | $\chi^2 = 12{,}07$<br>($df = 1$) | $5{,}13 \times 10^{-4}$ | $V \text{ de Cramér} = 0{,}037$<br>(Associação desprezível) | **Rejeita $H_0$** | Associação de pequena magnitude na amostra. |
| **P4: `TotalSpend` por `Transported` (Paramétrico)** | $H_0$: $\mu_{\text{Não}} = \mu_{\text{Sim}}$<br>$H_1$: $\mu_{\text{Não}} \neq \mu_{\text{Sim}}$ | Teste $t$ de Welch (Amostras Independentes) | Levene refuta homocedasticidade ($W = 131{,}36, p < 0{,}001$); aproximação para médias em grupos grandes, sob independência | $t = 18{,}94$<br>($df = 7.906{,}3$) | $2{,}67 \times 10^{-78}$ | $d \text{ de Cohen} = 0{,}407$<br>(Efeito moderado; $\Delta = +\$1.120{,}74$) | **Rejeita $H_0$** | O gasto médio foi maior entre os não transportados. |
| **P4: `TotalSpend` por `Transported` (Não-Paramétrico)** | $H_0$: Distribuições iguais<br>$H_1$: Diferença entre distribuições na comparação por postos | Teste $U$ de Mann-Whitney (Wilcoxon) | Independência assumida; correção de empates e continuidade | $U = 13.846.861{,}5$<br>($Z = 39{,}09$) | $< 0{,}001$ | $r \text{ de Rosenthal} = 0{,}419$<br>(Efeito moderado) | **Rejeita $H_0$** | Os postos de gasto diferiram entre os grupos. A mediana foi US$ 0 entre transportados e US$ 907 entre não transportados. |
| **P5: `TotalSpend` por `HomePlanet` (Paramétrico)** | $H_0$: $\mu_{\text{Terra}} = \mu_{\text{Europa}} = \mu_{\text{Marte}}$<br>$H_1$: Ao menos uma difere | ANOVA de Welch a Um Fator (*One-Way*) | Levene indica severa heterocedasticidade ($W = 1.592{,}08, p < 0{,}001$); Welch robusto | $F = 407{,}57$<br>($df_1 = 2, df_2 = 3.000{,}9$) | $2{,}57 \times 10^{-157}$ | $\eta^2 = 0{,}1714$<br>($\omega^2 = 0{,}1712$; Efeito grande) | **Rejeita $H_0$** | Houve evidência de diferenças de médias de gasto entre planetas. η² descreve a fração da variabilidade amostral associada aos grupos. |
| **P5: `TotalSpend` por `HomePlanet` (Não-Paramétrico)**| $H_0$: Postos de gasto idênticos<br>$H_1$: Ao menos um planeta difere | Teste de Kruskal-Wallis ($H$) | Independência assumida; empates tratados | $H = 271{,}97$<br>($df = 2$) | $8{,}77 \times 10^{-60}$ | $\epsilon^2 = 0{,}0313$<br>(Efeito ordinal relevante) | **Rejeita $H_0$** | Houve evidência de diferenças globais nos postos de gasto. |
| **P5 (Pós-Hoc): Europa vs Terra** | $H_0$: $\mu_{\text{Europa}} = \mu_{\text{Terra}}$<br>$H_1$: $\mu_{\text{Europa}} \neq \mu_{\text{Terra}}$ | Procedimento Pós-Hoc de Games-Howell | Controle familiar de erro Tipo I sob variâncias desiguais | $q = 37{,}60$<br>($df = 2.226{,}6$) | $4{,}94 \times 10^{-13}$ | $\Delta = +\$2.768{,}76$<br>(IC 95%: $[\$2.524{,}55; \$3.012{,}96]$) | **Rejeita $H_0$** | Europa apresentou maior gasto médio que Terra. |
| **P5 (Pós-Hoc): Europa vs Marte** | $H_0$: $\mu_{\text{Europa}} = \mu_{\text{Marte}}$<br>$H_1$: $\mu_{\text{Europa}} \neq \mu_{\text{Marte}}$ | Procedimento Pós-Hoc de Games-Howell | Variâncias e amostras desiguais compensadas | $q = 31{,}15$<br>($df = 2.573{,}3$) | $< 0{,}001$ | $\Delta = +\$2.384{,}27$<br>(IC 95%: $[\$2.130{,}42; \$2.638{,}11]$) | **Rejeita $H_0$** | Europa apresentou maior gasto médio que Marte. |
| **P5 (Pós-Hoc): Marte vs Terra** | $H_0$: $\mu_{\text{Marte}} = \mu_{\text{Terra}}$<br>$H_1$: $\mu_{\text{Marte}} \neq \mu_{\text{Terra}}$ | Procedimento Pós-Hoc de Games-Howell | Controle sob heterocedasticidade moderada | $q = 16{,}12$<br>($df = 2.290{,}6$) | $1{,}20 \times 10^{-12}$ | $\Delta = +\$384{,}49$<br>(IC 95%: $[\$305{,}36; \$463{,}61]$) | **Rejeita $H_0$** | Marte apresentou maior gasto médio que Terra. |

### 6.2. Tamanhos de efeito e análise complementar

A tabela reporta V de Cramér para todas as associações categóricas significantes e diferenças de médias ou magnitudes padronizadas para cada comparação de gastos. V = 0,037 indica associação pequena para VIP, enquanto V = 0,467 indica associação mais pronunciada para criossono. O valor-p informa a evidência contra a hipótese nula sob os pressupostos do teste. A magnitude responde à relevância prática. As razões de variância na seção 5.4 contextualizam os dois diagnósticos de Levene.

Dunn–Bonferroni complementou Kruskal–Wallis. As diferenças abaixo, na escala dos postos médios globais, indicam direção e magnitude observadas e dependem da amostra. Elas não expressam diferenças monetárias.

| Contraste | Diferença de postos médios (primeiro menos segundo) | Valor-p ajustado |
| --- | ---: | ---: |
| Terra – Europa | −1.027,32 | 5,18 × 10⁻⁶⁰ |
| Terra – Marte | −431,16 | 3,40 × 10⁻¹⁰ |
| Europa – Marte | +596,16 | 2,76 × 10⁻¹⁴ |

### 6.3. Criossono e interpretação observacional

As regras de preparação e os registros observados relacionam criossono e gasto zero. Como o criossono também está associado ao desfecho, é uma explicação possível para parte da diferença de gasto entre transportados e não transportados. O estudo não identifica efeitos de gastar ou permanecer em criossono sobre o transporte.

---

## 7. Correlações, Regressão e Modelagem Preditiva Multivariada

### 7.1. Matriz de Correlação Bivariada: Pearson vs Spearman
Avaliou-se a estrutura de correlação entre as 8 variáveis numéricas contínuas e discretas do dataset. Dada a severa assimetria e caudas pesadas das despesas, comparou-se a matriz paramétrica linear de **Pearson ($r$)** com a matriz ordinal não-paramétrica de **Spearman ($\rho$)**.

| Par de Variáveis Analisado | Pearson ($r$) | Spearman ($\rho$) | Interpretação Metodológica |
| :--- | :---: | :---: | :--- |
| `FoodCourt` $\times$ `TotalSpend` | **$0{,}75$** | **$0{,}67$** | Associação descritiva na base completa. |
| `VRDeck` $\times$ `TotalSpend` | $0{,}57$ | $0{,}59$ | Associação descritiva na base completa. |
| `Spa` $\times$ `TotalSpend` | $0{,}56$ | $0{,}57$ | Associação descritiva na base completa. |
| `FoodCourt` $\times$ `VRDeck` | $0{,}23$ | **$0{,}52$** | Associação descritiva na base completa. |
| `FoodCourt` $\times$ `Spa` | $0,22$ | **$0{,}49$** | Associação descritiva na base completa. |
| `Age` $\times$ `GroupSize` | **$-0{,}19$** | **$-0{,}18$** | Associação descritiva na base completa. |
| `Age` $\times$ `TotalSpend` | $+0{,}11$ | $+0{,}13$ | Associação descritiva na base completa. |

O notebook 05 mostra que as associações entre serviços mudam ao restringir a análise a quem gastou. Os zeros compartilhados podem influenciar as correlações da amostra completa.

### 7.2. Diagnóstico de Multicolinearidade
O VIF de `HomePlanet_Europa` foi 7,99 na amostra completa e 7,98 no treino da regressão linear. A concentração de passageiros de alguns planetas em determinados conveses limita a interpretação isolada desses fatores. Esses VIFs descrevem os desenhos avaliados para a regressão linear.

### 7.3. Modelo secundário de gastos

A regressão linear ajustou `log1p(TotalSpend)` em função de idade, tamanho do grupo, origem, convés e VIP. O R² ajustado no treino foi 0,256. O RMSE no teste foi 3,18 na escala logarítmica. O diagnóstico de resíduos indicou heterocedasticidade e estrutura compatível com a mistura de gastos nulos e positivos. Os erros-padrão HC3 ajustam a estimativa de incerteza dos coeficientes diante de heterocedasticidade. A forma da distribuição dos resíduos permanece uma limitação do ajuste.

### 7.4. Modelo Preditivo Principal: Regressão Logística para `Transported`
A regressão logística binária foi estimada por máxima verossimilhança **sem penalização**. O pipeline codifica criossono, origem, destino, convés, bordo e VIP. Padroniza idade e tamanho do grupo e aplica `log1p` seguido de padronização às cinco rubricas de gasto. As referências categóricas são False, Terra, TRAPPIST-1e, F, boreste e False, nessa ordem.

A divisão interna por passageiro foi estratificada pelo desfecho, com 6.954 observações de treino e 1.739 de teste e semente 42. A codificação, a padronização e a estimação do modelo usaram o treino interno. A limpeza e a imputação da base Kaggle ocorreram antes dessa divisão. Estatísticas usadas no saneamento podem incorporar informação das futuras observações de teste interno, limitando a interpretação da avaliação como desempenho em dados completamente novos. O limiar de 0,50 foi fixado antes da avaliação.

#### Avaliação de desempenho contra o classificador de referência

A tabela compara a logística com o classificador ingênuo estratificado no teste interno.

| Métrica de Desempenho | Baseline Estratificado | Modelo Logístico Proposto | Diferença observada |
| :--- | :---: | :---: | :---: |
| **Acurácia Global (*Accuracy*)** | $52{,}4\%$ | **$77{,}9\%$** | **$+25{,}5$ pontos percentuais** |
| **Área sob a Curva ROC (ROC-AUC)** | $0{,}524$ | **$0{,}862$** | **$+0{,}338$ ** |
| **F1 da classe positiva** | $0{,}525$ | **$0{,}784$** | **$+0{,}259$ ** |
| **Sensibilidade / Revocação (*Recall*)** | $0{,}523$ | **$0{,}796$** | $+0{,}273$  |
| **Precisão (*Precision*)** | $0{,}528$ | **$0{,}772$** | $+0{,}244$  |


O pseudo-R² de McFadden foi 0,311 no treino. No teste, ao limiar de 0,50, a matriz de confusão contém **657 verdadeiros negativos, 206 falsos positivos, 179 falsos negativos e 697 verdadeiros positivos**. A sensibilidade foi de aproximadamente 79,6%.

#### Interpretação dos Odds Ratios (Razões de Chance)
Para conferir inteligibilidade técnica, os coeficientes logísticos estimados no treino foram convertidos em **Odds Ratios ($OR = e^{\beta}$)** acompanhados de seus respectivos Intervalos de Confiança assintóticos de 95%.

| Variável / Preditor | Coeficiente ($\beta$) | Erro-Padrão ($SE$) | *Odds Ratio* ($OR$) | IC 95% do *Odds Ratio* | Interpretação em Lógica de Negócio |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **`HomePlanet_Europa`** | $1{,}3781$ | $0{,}2199$ | **$3{,}97$** | $[2{,}58; 6{,}10]$ | Europa em relação à Terra. |
| **`CryoSleep_True`** | $1{,}1656$ | $0{,}1052$ | **$3{,}21$** | $[2{,}61; 3{,}94]$ | Criossono em relação ao estado acordado. |
| **`FoodCourt` (por 1 DP de `log1p`)** | $0{,}3899$ | $0{,}0414$ | **$1{,}48$** | $[1{,}36; 1{,}60]$ | Maior chance ajustada a cada DP de gasto transformado. |
| **`HomePlanet_Mars`** | $0{,}3376$ | $0{,}1053$ | **$1{,}40$** | $[1{,}14; 1{,}72]$ | Marte em relação à Terra. |
| **`ShoppingMall` (por 1 DP de `log1p`)**| $0{,}2111$ | $0{,}0348$ | **$1{,}24$** | $[1{,}15; 1{,}32]$ | Maior chance ajustada a cada DP de gasto transformado. |
| **`CabinSide_P` (Bombordo)** | $-0{,}5172$ | $0{,}0611$ | **$0{,}60$** | $[0{,}53; 0{,}67]$ | Bombordo em relação a boreste. |
| **`RoomService` (por 1 DP de `log1p`)** | $-0{,}6020$ | $0{,}0397$ | **$0{,}55$** | $[0{,}51; 0{,}59]$ | Menor chance ajustada a cada DP de gasto transformado. |
| **`CabinDeck_G`** | $-0{,}6377$ | $0{,}0957$ | **$0{,}53$** | $[0{,}44; 0{,}64]$ | Convés G em relação ao convés F. |
| **`Spa` (por 1 DP de `log1p`)** | $-0{,}7436$ | $0{,}0406$ | **$0{,}48$** | $[0{,}44; 0{,}51]$ | Menor chance ajustada a cada DP de gasto transformado. |

Os ORs são razões de chances ajustadas e não equivalem a razões de probabilidades. A associação de criossono deve ser lida em conjunto com o padrão de gasto zero. O OR de Europa depende dos conveses em que há sobreposição entre origens. Para o deck T, a contagem reduzida torna a estimativa instável. O modelo assume termos aditivos e relação linear no logito nas escalas das preditoras numéricas. A forma funcional e a calibração não foram validadas. Os ICs assintóticos devem ser lidos como exploratórios diante do possível agrupamento de passageiros.

---

## 8. Conclusões e Trabalhos Futuros

### 8.1. Síntese dos resultados

Criossono, origem e cabine estão associados às taxas de transporte na base tratada. A comparação de gastos mostra diferenças de médias e de postos, numa distribuição com muitos zeros. A regressão logística atingiu acurácia de 77,9% e ROC-AUC de 0,862 no teste interno. Esses resultados permitem priorizar hipóteses para investigação.

### 8.2. Recomendações ao comando operacional

1. Conferir os registros das cápsulas de criossono e a distribuição dos passageiros pelos conveses, onde foram observadas diferenças de taxa de transporte.
2. Investigar conjuntamente origem, cabine e gasto. As variáveis disponíveis não identificam mecanismos físicos, renda, evacuação ou sobrevivência.
3. Comunicar médias para comparações de consumo agregado e medianas e proporções de zeros para caracterizar a distribuição de gasto.
4. Avaliar o modelo como apoio à triagem em dados futuros. Definir custos dos erros, escolher o limiar em dados de validação separados e avaliar discriminação, calibração e desempenho com divisão por grupo antes de uso operacional.

### 8.3. Limitações metodológicas

- **Dados observacionais e imputados.** As associações não permitem atribuir causas. O teste de ausência em relação ao desfecho não estabelece MCAR. A análise de sensibilidade da preparação mediu a alteração das proporções e taxas em categorias avaliadas.
- **Dependência e validação interna.** Passageiros de um mesmo grupo, identificado por `Group`, podem aparecer em treino e teste. `GroupSize` é apenas o tamanho do grupo. A inferência não ajustou a dependência intragrupo e o teste interno se baseou em uma única partição da base previamente imputada. Isso pode afetar a incerteza e tornar as métricas otimistas, em magnitude desconhecida.
- **Generalização e decisão.** As métricas de teste não têm intervalos de incerteza, avaliação em novos grupos ou validação externa. A ROC-AUC mede discriminação. A calibração das probabilidades e a escolha de outro limiar exigem avaliação própria.
- **Especificação e sobreposição.** A linearidade no logito para termos numéricos foi assumida. Grupos raros e a concentração de origens em determinados conveses limitam a interpretação dos ORs ajustados.

### 8.4. Próximos Passos na Governança do Projeto
A conclusão do presente relatório técnico consolidado (**`KAN-39`**) desbloqueia a etapa subsequente de governança:
- **`KAN-40` — Revisão de Coerência Metodológica:** A cargo de **Luciana Almeida** (com co-revisão de Daniela Amaro e Renatta Batista), cujo objetivo é auditar o alinhamento cruzado entre as premissas de distribuições (Seção 5), a adequação dos testes inferenciais (Seção 6) e as conclusões interpretativas aqui formuladas.
- **`KAN-41` — Validação Numérica Cruzada:** Conduzida por **Daniela Amaro**, conferindo cada número, percentagem e intervalo de confiança deste relatório contra a saída de execução limpa do notebook consolidado mestre (`notebooks/00_projeto_final_estatistica.ipynb`).
- **`KAN-42` e `KAN-43` — Diagramação em PDF e Empacotamento Final:** Geração do documento oficial paginado em PDF para submissão à banca examinadora da Pós-Graduação em Deep Learning do CIn/UFPE.

---

*Relatório técnico consolidado no âmbito do card **KAN-39**, com dados auditados em 11 de novembro de 2026.*
