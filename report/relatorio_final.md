# Spaceship Titanic — Análise Estatística, Modelagem Preditiva e Recomendações Operacionais

> **Relatório Técnico Final — T3**  
> **Disciplina:** Estatística Avançada e Fundamentos Probabilísticos para IA  
> **Programa:** Pós-Graduação em Inteligência Artificial / Deep Learning — Centro de Informática (CIn/UFPE)  
> **Equipe Técnica:** Daniela Amaro, Renatta Batista, Gustavo Menezes Gonçalves, Helton Gomes Soares de Lima, Luciana Almeida  
> **Data:** Novembro de 2026  
> **Repositório do Projeto:** `https://github.com/gmenezesg/spaceship-titanic-estatistica-posdl`  
> **Artefatos Vinculados:** Notebook Mestre (`notebooks/00_projeto_final_estatistica.ipynb`), Catálogo de Figuras (`docs/catalogo_figuras.md`), Apresentação Executiva (`report/apresentacao_final.pdf`)

---

## 1. Resumo Executivo (Executive Summary)

### 1.1. Contexto do Incidente e Demanda Operacional
Durante a rota inaugural de transporte interplanetário da nave espacial *Spaceship Titanic*, transportando passageiros civis e tripulação da Terra com destino a colônias em Kepler-186f e 55 Cancri e, a embarcação colidiu com uma anomalia de feixe espaço-temporal nas imediações da nuvem de poeira interestelar de Alpha Centauri. O incidente resultou no teletransporte involuntário e abrupto de aproximadamente metade das pessoas a bordo para outra dimensão dimensional.

O presente estudo analítico foi encomendado pelo **Comando de Operações Espaciais e pela Força de Resgate da Frota**, com dois objetivos centrais:
1. **Compreensão Retrospectiva (Diagnóstico e Auditoria):** Mapear os perfis demográficos, as condições de viagem e os padrões de localização a bordo que exibem maior vulnerabilidade ao feixe de teletransporte, permitindo a apuração de responsabilidades, o acolhimento transparente das famílias e a revisão das normas de segurança para futuras naves de passageiros.
2. **Triagem e Priorização Preditiva (Resgate Ativo):** Desenvolver um mecanismo preditivo transparente e estatisticamente auditável para estimar a probabilidade de teletransporte de passageiros cuja situação permanece não rotulada nos arquivos de emergência, orientando as equipes de busca e a reconstrução de prontuários.

### 1.2. O Conjunto de Dados e Governança
A investigação operou sobre o dataset oficial de registros de bordo recuperados, consolidando **8.693 passageiros e 22 variáveis estruturadas** após saneamento e engenharia de atributos (partindo de 14 colunas originais). A base de trabalho (`data/processed/spaceship_titanic_clean.csv`) exibe taxa de sinistro estritamente equilibrada: **$50{,}36\%$ transportados** ($4.378$ indivíduos) e **$49{,}64\%$ não transportados** ($4.315$ indivíduos). A taxa de dados faltantes originais situava-se em $1{,}91\%$ das células ($2.324$ ocorrências distribuídas em $24{,}01\%$ dos registros), cuja mecânica de ausência foi auditada como puramente aleatória (**MCAR** — *Missing Completely at Random*), viabilizando saneamento por regras de negócio e imputação condicional robusta sem qualquer descarte de passageiros.

### 1.3. Três Achados Capitais da Investigação
As análises descritivas, inferenciais e multivariadas convergiram em três pilares analíticos:

1. **O Confinamento em Criossono é o Sinal Isolado de Maior Magnitude:**  
   Passageiros em estado de sono criogênico induzido (`CryoSleep = True`) apresentaram **$81{,}47\%$ de taxa de teletransporte**, em contraste extremo com **$32{,}82\%$ entre os que estavam acordados** — uma disparidade massiva de **$48{,}65$ pontos percentuais** ($\chi^2 = 1.897{,}71, p < 10^{-300}, V \text{ de Cramér} = 0{,}467$). O isolamento em cápsulas pressurizadas retirou qualquer mobilidade evasiva da vítima diante dos alarmes de bordo.
2. **Origem Planetária e Conveses Físicos Estão Intrinsecamente Sobrepostos:**  
   As taxas de sinistro variam substancialmente por procedência: **Europa com $66{,}05\%$**, **Marte com $52{,}44\%$** e **Terra com $42{,}33\%$** ($\chi^2 = 338{,}82, p < 10^{-73}$). No entanto, a investigação espacial revelou que $72{,}6\%$ dos europeus ocupavam exclusivamente as cabines de luxo dos conveses B e C (onde as taxas ultrapassam $68\%$), ao passo que passageiros da Terra concentravam-se nos conveses inferiores F e G ($100\%$ das cabines do deck G eram da Terra). A nacionalidade atua primariamente como marcador vicário (*proxy*) da localização física na estrutura do navio atingida pelo feixe.
3. **O Consumo Financeiro a Bordo é uma Pista Enganosa (Zero-Inflação e Fator de Confusão):**  
   Embora os passageiros não transportados tenham consumido significativamente mais em amenidades (média de $\$2.011{,}89$ contra $\$891{,}15$ dos transportados; diferença de $+\$1.120{,}74$; $t = 18{,}94, p < 10^{-77}$), a distribuição financeira é severamente zero-inflacionada: **$41{,}92\%$ de todos os passageiros não gastaram absolutamente nada a bordo**, e entre os transportados essa proporção atinge **$65{,}49\%$** (mediana estrita de **US$ 0,00** contra **US$ 907,00** dos sobreviventes). O gasto monetário não concedeu blindagem física; indivíduos em criossono registraram consumo mecanicamente nulo, criando uma correlação espúria mediada pelo sono criogênico.

### 1.4. Modelo Preditivo de Triagem
Um modelo linear supervisionado de Regressão Logística com padronização via *Pipeline* foi treinado em divisão estratificada de 80/20 ($N_{\text{teste}} = 1.739$, semente fixa $42$). O modelo atingiu:
- **Acurácia de Teste:** **$77{,}9\%$**, representando um incremento substancial de **$+25{,}5$ pontos percentuais** sobre o classificador ingênuo estratificado de referência ($52{,}4\%$).
- **Capacidade Discriminatória (ROC-AUC):** **$0{,}862$**, confirmando excelente separação estocástica.
- **F1-Score Equilibrado:** **$0{,}784$** (Precisão de $0{,}773$ e Recall/Sensibilidade de $0{,}796$).
- **Controle Multivariado:** Após o ajuste conjunto pelas demais variáveis, o estado de criossono sustentou um *Odds Ratio* ajustado de **$3{,}21$** (IC 95%: $[2{,}61; 3{,}94]$) e a procedência de Europa exibiu $OR = 3{,}97$ (IC 95%: $[2{,}58; 6{,}10]$).

### 1.5. Quadro-Resumo Executivo de Indicadores
A Tabela 1 condensa os parâmetros oficiais do estudo validados no notebook mestre do projeto.

| Indicador Estratégico | Valor / Parâmetro Oficial | Leitura Operacional para Decisores |
| :--- | :---: | :--- |
| **Amostra Analisada ($N$)** | $8.693$ passageiros | Universo completo dos registros de treino auditados |
| **Taxa Global de Sinistro** | $50{,}36\%$ ($4.378$ indivíduos) | Desfecho perfeitamente equilibrado entre as classes |
| **Impacto do Criossono** | $81{,}47\%$ vs $32{,}82\%$ ($\Delta = 48{,}65$ p.p.) | Principal critério de risco individual ($V = 0{,}467$) |
| **Gradiente por Origem** | Europa $66{,}05\%$, Marte $52{,}44\%$, Terra $42{,}33\%$ | Segregação espacial por conveses físicos ($V = 0{,}197$) |
| **Passageiros com Gasto Zero** | $41{,}92\%$ ($3.644$ passageiros) | Mediana dos transportados é zero; assimetria severa ($4{,}40$) |
| **Desempenho Logístico (Teste)** | Acurácia $77{,}9\%$ · ROC-AUC $0{,}862$ · F1 $0{,}784$ | Ganho de $+25{,}5$ p.p. sobre baseline ingênuo ($52{,}4\%$) |

---

## 2. Contexto do Problema, Governança e Engenharia de Dados

### 2.1. O Problema de Negócio e os Objetivos do Cliente
O cliente institucional desta análise é o **Comando de Operações Espaciais da Federação**, entidade responsável pela regulação da rota comercial e coordenação das forças de resposta a desastres espaciais. A perda de contato dimensional com 4.378 almas exige uma investigação técnica pautada em dados objetivos.

A meta analítica decompõe-se em duas vertentes complementares:
1. **Compreender:** Identificar quais atributos pessoais, cabines ocupadas, gastos e estados fisiológicos exibem correlação estatística com o teletransporte, discernindo o tamanho real do efeito da mera significância provocada pelo tamanho amostral expressivo ($N = 8.693$).
2. **Prever:** Fornecer um modelo probabilístico que ranqueie passageiros conforme o risco de teletransporte, permitindo que as equipes de emergência atribuam recursos limitados de salvamento às zonas e perfis prioritários.

### 2.2. Dicionário, Inventário e Mecânica de Dados Ausentes
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

A análise das ausências revelou que 2.087 passageiros ($24{,}01\%$ da amostra) possuíam ao menos uma célula em branco, totalizando 2.324 valores nulos. Para testar o mecanismo de perda, foram realizados testes formais de Qui-Quadrado entre o indicador binário de ausência de cada coluna ($I_{\text{nulo}}$) e o desfecho `Transported`. Em todas as colunas analisadas, obteve-se $p > 0{,}05$ e coeficientes $V \text{ de Cramér} < 0{,}02$, confirmando o pressuposto de **ausência puramente aleatória (MCAR)**. Descartar um quarto da base via *complete-case analysis* provocaria perda injustificada de poder estatístico e violação das exigências de reprodutibilidade; procedeu-se, portanto, ao saneamento estruturado.

### 2.3. Pipeline de Saneamento em 10 Etapas e Variáveis Derivadas
O tratamento dos dados seguiu um pipeline estrito, sem vazamento de informação entre partições:

1. **Regras Determinísticas de Negócio:**
   - Passageiros em criossono (`CryoSleep = True`) não consom amenidades a bordo; todas as 5 rubricas de despesa foram preenchidas com $0{,}00$.
   - Crianças com idade $\le 12$ anos não possuem autorização financeira independente para contratação de amenidades; despesas preenchidas com $0{,}00$.
   - Passageiros com despesas positivas registradas em qualquer rubrica ($\sum > 0$) foram compulsoriamente imputados como `CryoSleep = False`.
   - Estas três regras recuperaram deterministicamente **842 células nulas**, reduzindo o volume de imputação estatística para menos de $1{,}5\%$ do total.
2. **Imputação Estatística Condicional:**
   - Variáveis contínuas (`Age` e rubricas de gasto residuais) foram preenchidas pela mediana condicional ao grupo de viagem e classe social.
   - Variáveis categóricas (`HomePlanet`, `Destination`, `Cabin`) foram preenchidas pela moda dos passageiros pertencentes ao mesmo grupo de cabine (`GroupSize > 1`). Para passageiros solitários, adotou-se a moda global do conves.
3. **Engenharia de 8 Atributos Derivados:**
   - `CabinDeck`: Convés da cabine (`A`, `B`, `C`, `D`, `E`, `F`, `G`, `T`).
   - `CabinNum`: Posição ordinal numérica da cabine no corredor.
   - `CabinSide`: Bordo da nave (`P` = Bombordo/*Port*, `S` = Boreste/*Starboard*).
   - `GroupSize`: Tamanho do grupo de viagem derivado do prefixo `gggg` de `PassengerId`.
   - `IsAlone`: Indicador binário de viagem solitária (`GroupSize == 1`).
   - `TotalSpend`: Somatório financeiro consolidado das 5 rubricas de despesas.
   - `HasSpent`: Indicador binário de atividade financeira a bordo (`TotalSpend > 0`).
   - `AgeGroup`: Categorização etária em faixas (`Criança` $\le 12$, `Adolescente` 13–17, `Adulto Jovem` 18–35, `Adulto` 36–59, `Idoso` $\ge 60$).

O dataset resultante reúne **8.693 passageiros, 22 colunas tratadas e zero valores faltantes residuais**, operando como a fonte única da verdade para todas as trilhas analíticas subsequentes.

---

## 3. Análise Descritiva e Visual dos Passageiros

### 3.1. Perfil Demográfico da Tripulação e Passageiros
A composição qualitativa da tripulação está sintetizada na Tabela T1 (selecionada no Catálogo de Figuras e Tabelas do `KAN-38`).

| Variável | Categoria | Frequência ($n$) | Proporção Relativa ($\%$) | Taxa de Transporte ($\%$) |
| :--- | :--- | :---: | :---: | :---: |
| **`Transported` (Alvo)** | `True` / `False` | $4.378$ / $4.315$ | $50{,}36\%$ / $49{,}64\%$ | — |
| **`HomePlanet`** | Terra (*Earth*) | $4.715$ | $54{,}24\%$ | $42{,}33\%$ |
| | Europa (*Europa*) | $2.174$ | $25{,}01\%$ | $66{,}05\%$ |
| | Marte (*Mars*) | $1.804$ | $20{,}75\%$ | $52{,}44\%$ |
| **`CryoSleep`** | Acordado (`False`) | $5.558$ | $63{,}94\%$ | $32{,}82\%$ |
| | Em Criossono (`True`) | $3.135$ | $36{,}06\%$ | $81{,}47\%$ |
| **`CabinSide`** | Boreste (`S`) | $4.395$ | $50{,}56\%$ | $55{,}43\%$ |
| | Bombordo (`P`) | $4.298$ | $49{,}44\%$ | $45{,}16\%$ |
| **`VIP`** | Não-VIP (`False`) | $8.494$ | $97{,}71\%$ | $50{,}65\%$ |
| | VIP (`True`) | $199$ | $2{,}29\%$ | $38{,}21\%$ |
| **`IsAlone`** | Grupo Familiar (`False`)| $3.888$ | $44{,}73\%$ | $55{,}58\%$ |
| | Solitário (`True`) | $4.805$ | $55{,}27\%$ | $46{,}24\%$ |

A análise da distribuição etária revela uma tripulação prioritariamente jovem: média de **$28{,}8$ anos** e mediana de **$27{,}0$ anos**, com desvio-padrão de $14{,}4$ anos e amplitude interquartil de $18{,}0$ anos ($Q_1 = 19, Q_3 = 37$). Nota-se uma assimetria positiva moderada ($0{,}43$) impulsionada pela presença de passageiros idosos de até 79 anos e por uma concentração atípica de 809 crianças com até 12 anos ($9{,}31\%$ da base), incluindo 178 lactentes com idade registrada zero.

![Figura 3: Distribuição da idade dos passageiros](figures/fig_03_idade_distribuicao.png)  
*Figura 3 — Distribuição da idade dos passageiros ($N = 8.693$). Histograma com classes de 2 anos e curva KDE estimada. Observa-se concentração no intervalo de 20 a 35 anos e o pico singular em idade 0 (bebês a bordo).*

### 3.2. Estrutura Espacial das Cabines e Conveses
A alocação nos conveses da nave seguiu uma rígida hierarquia socioeconômica. Os decks F e G concentram nada menos que **$62{,}76\%$ de toda a população** ($2.868$ e $2.588$ passageiros, respectivamente). A Tabela T3 destaca as maiores disparidades de sinistro observadas entre os conveses.

| Convés (`CabinDeck`) | População ($n$) | Participação ($\%$) | Transportados ($n$) | Taxa de Transporte ($\%$) | Planetas Predominantes |
| :---: | :---: | :---: | :---: | :---: | :--- |
| **B** | $779$ | $8{,}96\%$ | $568$ | **$72{,}95\%$** | Europa ($94{,}7\%$) |
| **C** | $747$ | $8{,}59\%$ | $508$ | **$68{,}07\%$** | Europa ($95{,}2\%$) |
| **A** | $256$ | $2{,}94\%$ | $127$ | **$49{,}61\%$** | Europa ($98{,}4\%$) |
| **D** | $495$ | $5{,}69\%$ | $215$ | **$43{,}43\%$** | Marte ($58\%$) / Europa ($42\%$) |
| **E** | $876$ | $10{,}08\%$ | $313$ | **$35{,}73\%$** | Terra ($45\%$) / Marte ($39\%$) / Europa ($16\%$) |
| **F** | $2.868$ | $32{,}99\%$ | $946$ | **$32{,}99\%$** | Marte ($54\%$) / Terra ($46\%$) |
| **G** | $2.588$ | $29{,}77\%$ | $898$ | **$34{,}70\%$** | Terra ($100{,}0\%$) |
| **T** | $5$ | $0{,}06\%$ | $1$ | **$20{,}00\%$** | Conves técnico / Amostra insuficiente |

![Figura 6: Passageiros por deck da cabine e taxa de transporte](figures/fig_06_passageiros_por_deck.png)  
*Figura 6 — Ocupação física e taxa de sinistro por deck da cabine ($N = 8.693$). Conveses B e C apresentam as maiores taxas de teletransporte, abrigando a elite europeia. O deck T figura isolado devido ao tamanho amostral residual ($n = 5$).*

![Figura 1: Taxa de transporte por planeta de origem](figures/fig_01_transporte_por_planeta.png)  
*Figura 1 — Taxa de transporte por planeta de procedência ($N = 8.693$). A linha tracejada demarca a média global da embarcação ($50{,}36\%$). Passageiros europeus sofrem o maior impacto relativo ($66{,}05\%$).*

A forte correlação visual entre a procedência de Europa (Figura 1) e os conveses B e C (Figura 6) comprova a segregação espacial: a quase totalidade dos europeus viajava nos conveses superiores, setor que coincide espacialmente com a penetração primária da anomalia dimensional. Em contrapartida, os conveses inferiores abrigavam a classe econômica de passageiros da Terra.

### 3.3. Padrões de Consumo e Valores Extremos (Outliers)
As cinco rubricas de consumo monetário a bordo exibem comportamento assimétrico e altamente atípico. A Tabela T2 detalha a distribuição das variáveis financeiras.

| Rubrica Financeira | Zeros ($n$) | Proporção Zeros ($\%$) | Mediana (US$) | Média (US$) | Desvio-Padrão (US$) | Máximo (US$) | Coef. Variação ($CV$) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `RoomService` | $5.577$ | $64{,}16\%$ | $0{,}00$ | $220{,}01$ | $660{,}54$ | $14.327{,}00$ | $3{,}00$ |
| `FoodCourt` | $5.456$ | $62{,}76\%$ | $0{,}00$ | $448{,}43$ | $1.595{,}60$ | $29.813{,}00$ | $3{,}56$ |
| `ShoppingMall`| $5.587$ | $64{,}27\%$ | $0{,}00$ | $169{,}57$ | $597{,}94$ | $23.492{,}00$ | $3{,}53$ |
| `Spa` | $5.324$ | $61{,}24\%$ | $0{,}00$ | $304{,}59$ | $1.125{,}56$ | $22.408{,}00$ | $3{,}70$ |
| `VRDeck` | $5.495$ | $63{,}21\%$ | $0{,}00$ | $298{,}25$ | $1.134{,}26$ | $24.133{,}00$ | $3{,}80$ |
| **`TotalSpend`** | **$3.644$** | **$41{,}92\%$** | **$716{,}00$** | **$1.445{,}46$** | **$2.793{,}55$** | **$35.987{,}00$** | **$1{,}93$** |

A assimetria global de `TotalSpend` é de **$4{,}40$**, com curtose de **$32{,}53$**. Pelo critério de Tukey (KAN-17), utilizando o intervalo interquartil ($Q_1 = 0, Q_3 = 1.444, IQR = 1.444$), o limiar superior de valores extremos fixou-se em **US$ 3.610,00** ($Q_3 + 1{,}5 \times IQR$). Foram detectados **992 passageiros ($11{,}41\%$)** classificados como *outliers* superiores. 

Conforme preconizado nas regras de governança acadêmica do projeto, **nenhum valor extremo foi removido da base**. Tratam-se de transações legítimas de passageiros abastados de Europa consumindo amenidades de luxo. Suprimir esses dados mascararia a real dispersão socioeconômica da tripulação.

![Figura 4: Gasto total a bordo por desfecho em escala symlog](figures/fig_04_gasto_por_transporte.png)  
*Figura 4 — Gasto total consolidado (`TotalSpend`) por desfecho em escala symlog ($N = 8.693$). A linha tracejada assinala o corte de outliers ($US\$ 3.610,00$). Nota-se o colapso da mediana dos transportados para zero.*

![Figura 5: Gasto total a bordo por planeta de origem](figures/fig_05_gasto_por_planeta.png)  
*Figura 5 — Gasto total por planeta de procedência em escala symlog ($N = 8.693$). Europa apresenta mediana de despesa quase três vezes superior à da Terra, evidenciando o abismo econômico entre as origens.*

![Figura 2: Taxa de transporte por criossono](figures/fig_02_transporte_por_criossono.png)  
*Figura 2 — Associação bivariada entre confinamento em criossono e teletransporte ($N = 8.693$). O criossono induz uma diferença brutal de 48,65 p.p. no risco de sinistro.*

---

## 4. Probabilidade, Variáveis Aleatórias e Distribuições

### 4.1. Variáveis Aleatórias Discretas e Processos de Bernoulli
O desfecho operacional `Transported` foi formalizado como uma **variável aleatória de Bernoulli**, onde:
$$Y \sim \text{Bernoulli}(p), \quad p = P(Y = 1) = \frac{4.378}{8.693} \approx 0{,}5036$$
A variância associada é maximal, dado o equilíbrio das classes:
$$\sigma_Y^2 = p(1 - p) = 0{,}5036 \times 0{,}4964 \approx 0{,}2499 \quad (\sigma_Y \approx 0{,}5000)$$
A proporção amostral atua, portanto, como a medida canônica central. Em virtude do equilíbrio ($50{,}36\%$), qualquer classificador que pretenda demonstrar utilidade operacional deve superar significativamente a taxa de acerto por palpite ingênuo (~$50\%$).

Similarmente, o estado de sono criogênico modela-se como:
$$C \sim \text{Bernoulli}(p_c), \quad p_c = \frac{3.135}{8.693} \approx 0{,}3606$$

### 4.2. Investigação Formal de Aderência Teórica: Idade
Investigou-se se a variável quantitativa contínua `Age` segue distribuição Normal teórica $\mathcal{N}(\mu, \sigma^2)$ ajustada com média $\mu = 28{,}82$ e desvio-padrão $\sigma = 14{,}44$.

Foram aplicados dois testes formais de aderência:
1. **Teste de Shapiro-Wilk:** $W = 0{,}980$, $p = 1{,}24 \times 10^{-32}$ (Rejeição categórica de $H_0$).
2. **Teste Kolmogorov-Smirnov (Lilliefors):** $D = 0{,}076$, $p < 0{,}001$ (Rejeição categórica de $H_0$).

![Figura 7: Idade observada contra a Normal teórica ajustada](figures/fig_07_idade_normal_ajustada.png)  
*Figura 7 — Aderência da Idade observada à curva Normal ajustada ($\mu = 28{,}8; \sigma = 14{,}4$). A Normal reproduz razoavelmente o miolo entre 20 e 40 anos, mas falha nas caudas ao alocar massa para idades negativas e subestimar os bebês em idade 0.*

Apesar da rejeição estatística pelo excesso de poder amostral ($N = 8.693$), o valor de $W = 0{,}980$ indica que o desvio da normalidade é pequeno na prática. Graças ao **Teorema Central do Limite (TCL)**, a distribuição amostral da média converge com rapidez, tornando testes baseados em médias (como o teste $t$) computacionalmente estáveis, desde que garantida a robustez à heterocedasticidade.

### 4.3. Modelagem de Despesas: Zero-Inflação e Log-Normal
O gasto financeiro `TotalSpend` quebra os pressupostos clássicos de continuidade e simetria:
- **Zero-Inflação:** 41,92% da população concentra-se exatamente em zero ($US\$ 0,00$).
- **Cauda Pesada Positiva:** Entre os 5.049 passageiros com despesa positiva, a assimetria atinge valores extremos.

Para tratar essa estrutura, aplicou-se a transformação logarítmica deslocada $Y_{\text{log}} = \ln(TotalSpend + 1)$. A transformação reduziu a assimetria de $+4{,}40$ para **$-0{,}19$**, aproximando o miolo da densidade da Log-Normal teórica ($\mu_{\ln} = 7{,}33; \sigma_{\ln} = 0{,}96$).

![Figura 8: Decomposição do gasto: zeros e Log-Normal condicional](figures/fig_08_gasto_zero_e_log_normal.png)  
*Figura 8 — Estrutura probabilística de despesas a bordo ($N = 8.693$). Painel esquerdo: Proporção de gasto zero por rubrica individual e consolidada ($41{,}9\%$). Painel direito: Histograma de $\ln(TotalSpend)$ para despesas positivas sobreposto ao ajuste Log-Normal.*

Entretanto, testes formais no subconjunto de gastos positivos rejeitam estritamente a hipótese Log-Normal pura:
- Shapiro-Wilk: $W = 0{,}891$, $p < 10^{-300}$.
- Kolmogorov-Smirnov: $D = 0{,}126$, $p < 10^{-300}$.

A curtose observada permanece elevada ($4{,}93$), indicando caudas leptocúrticas e múltiplos picos de consumo decorrentes da coexistência de classes sociais. 

### 4.4. Implicações para a Escolha dos Testes Inferenciais
A violação da normalidade e a heterogeneidade estrutural de variâncias impõem restrições metodológicas terminantes:
1. **Rejeição do Teste $t$ de Student Clássico e ANOVA de Fisher:** Ambos assumem igualdade de variâncias populacionais (homocedasticidade), pressuposto cabalmente refutado pelo teste de Levene ($p < 10^{-30}$).
2. **Adoção Obrigatória de Métodos Heterocedásticos e Robustos:** Exige-se o uso do **Teste $t$ de Welch** para comparações bivariadas, **ANOVA de Welch** e procedimento pós-hoc de **Games-Howell** para comparações multivariadas, complementados invariavelmente por salvaguardas não-paramétricas de postos (**Mann-Whitney $U$** e **Kruskal-Wallis $H$**).

---

## 5. Inferência Estatística, Testes de Hipóteses e ANOVA

### 5.1. Protocolo Formal e Tabela-Resumo Consolidada (KAN-28)
Todas as hipóteses inferenciais foram formuladas previamente à execução, fixando-se o nível de significância em **$\alpha = 0{,}05$** com controle estrito do erro Tipo I. A Tabela 2 apresenta a consolidação normativa com as 9 colunas padronizadas pelo ticket KAN-28.

| Pergunta de Pesquisa / Relação | Hipótese Nula ($H_0$) e Alternativa ($H_1$) | Teste Estatístico Aplicado | Pressupostos Verificados | Estatística do Teste | Valor-$p$ Observado | Tamanho do Efeito | Decisão ($\alpha=0{,}05$) | Conclusão e Significado de Negócio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **P1: `HomePlanet` $\times$ `Transported`** | $H_0$: Variáveis independentes<br>$H_1$: Há associação | Qui-Quadrado de Pearson | Frequências esperadas $\ge 5$ atendidas ($100\%$; mín: $895{,}5$) | $\chi^2 = 338{,}82$<br>($df = 2$) | $2{,}66 \times 10^{-74}$ | $V \text{ de Cramér} = 0{,}197$<br>(Associação média) | **Rejeita $H_0$** | Origem segmenta o sinistro: Europa tem maior taxa ($66{,}05\%$) que Marte ($52{,}44\%$) e Terra ($42{,}33\%$), refletindo segregação espacial de cabines. |
| **P2: `CryoSleep` $\times$ `Transported`** | $H_0$: Variáveis independentes<br>$H_1$: Há associação | Qui-Quadrado de Pearson (sem Yates) | Frequências esperadas $\ge 5$ atendidas ($100\%$; mín: $1.556{,}1$) | $\chi^2 = 1.897{,}71$<br>($df = 1$) | $< 10^{-300}$ | $V \text{ de Cramér} = 0{,}467$<br>(Associação muito forte) | **Rejeita $H_0$** | Criossono é o preditor isolado mais crítico ($81{,}47\%$ vs $32{,}82\%$). Confinamento impediu evacuação emergencial. |
| **P3: `VIP` $\times$ `Transported`** | $H_0$: Variáveis independentes<br>$H_1$: Há associação | Qui-Quadrado de Pearson (sem Yates) | Frequências esperadas $\ge 5$ atendidas ($100\%$; mín: $98{,}8$) | $\chi^2 = 12{,}07$<br>($df = 1$) | $5{,}13 \times 10^{-4}$ | $V \text{ de Cramér} = 0{,}037$<br>(Associação desprezível) | **Rejeita $H_0$** | Embora estatisticamente significante pela amostra massiva, o efeito prático é nulo ($V = 0{,}037$). O status VIP não conferiu proteção. |
| **P4: `TotalSpend` por `Transported` (Paramétrico)** | $H_0$: $\mu_{\text{Não}} = \mu_{\text{Sim}}$<br>$H_1$: $\mu_{\text{Não}} \neq \mu_{\text{Sim}}$ | Teste $t$ de Welch (Amostras Independentes) | Levene refuta homocedasticidade ($W = 131{,}36, p < 0{,}001$); TCL garante normalidade amostral | $t = 18{,}94$<br>($df = 7.906{,}3$) | $2{,}67 \times 10^{-78}$ | $d \text{ de Cohen} = 0{,}407$<br>(Efeito moderado; $\Delta = +\$1.120{,}74$) | **Rejeita $H_0$** | Não transportados gastaram substantivamente mais ($\$2.011{,}89$ vs $\$891{,}15$); passageiros acordados circulavam e consumiam. |
| **P4: `TotalSpend` por `Transported` (Não-Paramétrico)** | $H_0$: Postos idênticos entre grupos<br>$H_1$: Dominância estocástica | Teste $U$ de Mann-Whitney (Wilcoxon) | Amostras independentes; correção estrita de empates e continuidade | $U = 13.846.861{,}5$<br>($Z = 39{,}09$) | $< 10^{-300}$ | $r \text{ de Rosenthal} = 0{,}419$<br>(Efeito moderado) | **Rejeita $H_0$** | Corroboração ordinal de que os transportados exibem menor nível de gastos (mediana US$ 0,00 vs US$ 907,00). |
| **P5: `TotalSpend` por `HomePlanet` (Paramétrico)** | $H_0$: $\mu_{\text{Terra}} = \mu_{\text{Europa}} = \mu_{\text{Marte}}$<br>$H_1$: Ao menos uma difere | ANOVA de Welch a Um Fator (*One-Way*) | Levene indica severa heterocedasticidade ($W = 1.592{,}08, p < 0{,}001$); Welch robusto | $F = 407{,}57$<br>($df_1 = 2, df_2 = 3.000{,}9$) | $2{,}57 \times 10^{-157}$ | $\eta^2 = 0{,}1714$<br>($\omega^2 = 0{,}1712$; Efeito grande) | **Rejeita $H_0$** | Procedência explica $17{,}14\%$ da dispersão total de despesas na nave; Europa concentra riqueza perante Marte e Terra. |
| **P5: `TotalSpend` por `HomePlanet` (Não-Paramétrico)**| $H_0$: Postos de gasto idênticos<br>$H_1$: Ao menos um planeta difere | Teste de Kruskal-Wallis ($H$) | Amostragem independente com empates tratados | $H = 271{,}97$<br>($df = 2$) | $8{,}77 \times 10^{-60}$ | $\epsilon^2 = 0{,}0313$<br>(Efeito ordinal relevante) | **Rejeita $H_0$** | Confirmação não-paramétrica de disparidade estrutural de consumo independente de outliers. |
| **P5 (Pós-Hoc): Europa vs Terra** | $H_0$: $\mu_{\text{Europa}} = \mu_{\text{Terra}}$<br>$H_1$: $\mu_{\text{Europa}} \neq \mu_{\text{Terra}}$ | Procedimento Pós-Hoc de Games-Howell | Controle familiar de erro Tipo I sob variâncias desiguais | $q = 37{,}60$<br>($df = 2.226{,}6$) | $4{,}94 \times 10^{-13}$ | $\Delta = +\$2.768{,}76$<br>(IC 95%: $[\$2.524{,}55; \$3.012{,}96]$) | **Rejeita $H_0$** | Passageiros de Europa gastam, em média, mais de $5\times$ o valor dos terrestres, definindo o estrato de altíssimo luxo. |
| **P5 (Pós-Hoc): Europa vs Marte** | $H_0$: $\mu_{\text{Europa}} = \mu_{\text{Marte}}$<br>$H_1$: $\mu_{\text{Europa}} \neq \mu_{\text{Marte}}$ | Procedimento Pós-Hoc de Games-Howell | Variâncias e amostras desiguais compensadas | $q = 31{,}15$<br>($df = 2.573{,}3$) | $< 10^{-300}$ | $\Delta = +\$2.384{,}27$<br>(IC 95%: $[\$2.130{,}42; \$2.638{,}11]$) | **Rejeita $H_0$** | Europeus superam marcianos em mais de $\$2.380$ per capita, consolidando descolamento de consumo. |
| **P5 (Pós-Hoc): Marte vs Terra** | $H_0$: $\mu_{\text{Marte}} = \mu_{\text{Terra}}$<br>$H_1$: $\mu_{\text{Marte}} \neq \mu_{\text{Terra}}$ | Procedimento Pós-Hoc de Games-Howell | Controle sob heterocedasticidade moderada | $q = 16{,}12$<br>($df = 2.290{,}6$) | $1{,}20 \times 10^{-12}$ | $\Delta = +\$384{,}49$<br>(IC 95%: $[\$305{,}36; \$463{,}61]$) | **Rejeita $H_0$** | Marcianos apresentam consumo ligeiramente superior à Terra ($+\$384{,}49$), caracterizando classe operacional intermediária. |

### 5.2. Análise Detalhada dos Testes e Tamanhos de Efeito
A interpretação dos testes requer distinção categórica entre **significância estatística** (redução da probabilidade de falso positivo sob amostras grandes) e **relevância substantiva** (magnitude prática mensurada pelo tamanho do efeito):

1. **A Lição do Efeito Desprezível de VIP:**  
   O teste Qui-Quadrado para status `VIP` retornou $p = 5{,}13 \times 10^{-4}$ (estritamente abaixo de $\alpha = 0{,}05$), o que um analista incauto interpretaria como preditor relevante. Todavia, o **$V \text{ de Cramér}$ é de apenas $0{,}037$**. Em termos práticos, pertencer à classe VIP explica menos de $0{,}1\%$ da variação de probabilidade do desfecho. Este é o exemplo paradigmático de significância artificial provocada por $N = 8.693$.
2. **A Relevância Substantiva do Criossono e Origem:**  
   Em contraposição, o $V \text{ de Cramér}$ de `CryoSleep` atinge **$0{,}467$** ($\phi = 0{,}467$), classificado na literatura estatística como uma **associação de magnitude forte a extrema**. O $V$ de `HomePlanet` fixou-se em **$0{,}197$**, representando força média.
3. **Disparidades Financeiras e ANOVA de Welch:**  
   A quebra de homocedasticidade revelada pelo teste de Levene foi de proporções brutais: a razão de variâncias entre Europa e Terra ultrapassa $37{,}5\times$ ($s_{\text{Europa}} = \$4.825{,}46$ vs $s_{\text{Terra}} = \$788{,}02$). A aplicação da ANOVA clássica de Fisher induziria erro grosseiro de inflação de Tipo I. A ANOVA de Welch corrigida estabeleceu $F = 407{,}57$ com efeito $\eta^2 = 0{,}1714$. Pela convenção de Jacob Cohen, valores de $\eta^2 > 0{,}14$ representam um **efeito de grande magnitude**, confirmando que a nacionalidade molda substancialmente a dispersão orçamentária no espaço.

### 5.3. Advertência Causal: O Fator de Confusão do Criossono
Rejeitar a hipótese nula de que os gastos são idênticos entre grupos ($p < 10^{-77}$) **jamais autoriza afirmar que gastar dinheiro salvou passageiros do teletransporte**. 

Trata-se de um fenômeno clássico de **confundimento e mediação**:
- Passageiros em criossono não podem transitar nem consumir ($TotalSpend = 0$ obrigatório).
- Simultaneamente, estavam trancados em câmaras nos conveses expostos e foram teletransportados em $81{,}47\%$ das ocasiões.
- Passageiros acordados transitavam pela nave, consumiam ativamente e tiveram maior probabilidade de evasão.
Portanto, a variável `CryoSleep` atua como causa comum antecedente do consumo nulo e da vulnerabilidade ao sinistro. Modelos preditivos que atribuam causalidade ao gasto isolado incorrem em erro de interpretação.

---

## 6. Correlações, Regressão e Modelagem Preditiva Multivariada

### 6.1. Matriz de Correlação Bivariada: Pearson vs Spearman
Avaliou-se a estrutura de correlação entre as 8 variáveis numéricas contínuas e discretas do dataset. Dada a severa assimetria e caudas pesadas das despesas, comparou-se a matriz paramétrica linear de **Pearson ($r$)** com a matriz ordinal não-paramétrica de **Spearman ($\rho$)**.

| Par de Variáveis Analisado | Pearson ($r$) | Spearman ($\rho$) | Interpretação Metodológica |
| :--- | :---: | :---: | :--- |
| `FoodCourt` $\times$ `TotalSpend` | **$0{,}75$** | **$0{,}67$** | Forte dependência linear e monotônica (relação de parte-todo). |
| `VRDeck` $\times$ `TotalSpend` | $0{,}57$ | $0{,}59$ | Segunda rubrica com maior correlação com a despesa consolidada. |
| `Spa` $\times$ `TotalSpend` | $0{,}56$ | $0{,}57$ | Forte correlação de consumo com amenidades de alto padrão. |
| `FoodCourt` $\times$ `VRDeck` | $0{,}23$ | **$0{,}52$** | Spearman revela associação monotônica oculta de passageiros de elite consumindo ambos os serviços, atenuada em Pearson pelos zeros. |
| `FoodCourt` $\times$ `Spa` | $0,22$ | **$0{,}49$** | Co-ocorrência em amenidades de luxo concentradas em passageiros de Europa. |
| `Age` $\times$ `GroupSize` | **$-0{,}19$** | **$-0{,}18$** | Associação negativa fraca: grupos familiares concentram crianças e jovens; passageiros idosos viajam mais solitários. |
| `Age` $\times$ `TotalSpend` | $+0{,}11$ | $+0{,}13$ | Correlação linear insignificante com o volume global de despesas. |

A divergência sistemática entre Pearson e Spearman nas amenidades de luxo (ex.: `FoodCourt` $\times$ `VRDeck` saltando de $0{,}23$ para $0{,}52$) demonstra o poder da análise de postos diante de zero-inflação: o coeficiente de Spearman captura com fidelidade a aliança de consumo dos passageiros que efetivamente abriram gastos a bordo.

### 6.2. Diagnóstico de Multicolinearidade
Para a regressão linear e logística, calculou-se o Fator de Inflação da Variância (**VIF** — *Variance Inflation Factor*):
- O preditor dummy `HomePlanet_Europa` exibiu **VIF de $7{,}98$** no treino.
- Esse valor decorre da colinearidade espacial quase perfeita: $72{,}6\%$ dos europeus residem nos conveses B e C, e o convés G possui $100\%$ de terrestres ($VIF_{\text{Deck\_G}} = 4{,}12$).
- Embora não ultrapasse o limiar crítico de ruptura matemática ($VIF > 10$), a multicolinearidade exige cautela: os erros-padrão dos coeficientes de Europa e dos conveses B/C são inflacionados mutuamente.

### 6.3. Modelo Secundário: Regressão Linear para `TotalSpend`
Desenvolveu-se um modelo de Regressão Linear OLS com variáveis padronizadas para modelar a dispersão de `TotalSpend` a partir de `Age`, `GroupSize`, `HomePlanet`, `CabinDeck` e `VIP`. O modelo atingiu coeficiente de determinação ajustado de **$R^2 = 0{,}268$** ($F = 212{,}4, p < 10^{-200}$).

O diagnóstico formal de resíduos (gráfico de resíduos vs ajustados e QQ-plot residual) evidenciou heterocedasticidade grave e assimetria acentuada dos erros, decorrentes da inflação em zero. O modelo linear OLS cumpre finalidade descritiva útil na confirmação das hierarquias planetárias ($\beta_{\text{Europa}} = +2.410,2, p < 0{,}001$), mas é metodologicamente inadequado como motor preditivo de despesas individuais, demandando modelos da família Tobit ou Tweedie em desenvolvimentos futuros.

### 6.4. Modelo Preditivo Principal: Regressão Logística para `Transported`
Para cumprir a missão primordial de triagem, implementou-se uma **Regressão Logística Binária Multivariada** com regularização $L_2$ ($C = 1{,}0$) e penalização Ridge, integrada em um `Pipeline` estrito com padronização dos preditores contínuos (`StandardScaler`) e codificação dummy das categóricas.

#### Protocolo de Validação
- **Divisão Amostral:** 80% treino ($N = 6.954$) e 20% teste ($N = 1.739$).
- **Estratificação:** Partição estratificada pela variável resposta `Transported`, preservando com rigor a proporção de $50{,}36\%$ em ambos os conjuntos.
- **Semente Aleatória:** Fixação estrita em `seed(42)` e `random_state=42`.
- **Limiar de Decisão:** Fixado *a priori* em $\tau = 0{,}50$, sem calibração oportunista pós-teste.

#### Avaliação de Desempenho contra Baseline
O modelo foi confrontado com o classificador ingênuo estratificado (*Dummy Classifier* gerando predições aleatórias proporcionais à classe). A Tabela 3 consolida as métricas obtidas no conjunto de teste independente ($N = 1.739$).

| Métrica de Desempenho | Baseline Estratificado | Modelo Logístico Proposto | Ganho Operacional Absoluto |
| :--- | :---: | :---: | :---: |
| **Acurácia Global (*Accuracy*)** | $52{,}4\%$ | **$77{,}9\%$** | **$+25{,}5$ pontos percentuais** |
| **Área sob a Curva ROC (ROC-AUC)** | $0{,}500$ | **$0{,}862$** | **$+0{,}362$ de separabilidade** |
| **F1-Score Ponderado** | $0{,}524$ | **$0{,}784$** | **$+0{,}260$ de harmonia** |
| **Sensibilidade / Revocação (*Recall*)** | $0{,}521$ | **$0{,}796$** | $+0{,}275$ de captura de sinistros |
| **Precisão (*Precision*)** | $0{,}526$ | **$0{,}773$** | $+0{,}247$ de assertividade |
| **Pseudo-$R^2$ de McFadden** | $0{,}000$ | **$0{,}311$** | Excelente ajuste multivariado |

A matriz de confusão no teste ($N = 1.739$) confirma a solidez da triagem:
- **Verdadeiros Negativos ($VN$):** $658$ passageiros não transportados corretamente classificados.
- **Falsos Positivos ($FP$):** $204$ alarmes falsos de teletransporte.
- **Falsos Negativos ($FN$):** $179$ teletransportados que o modelo deixou escapar.
- **Verdadeiros Positivos ($VP$):** $698$ passageiros teletransportados resgatados na triagem.

A taxa de revocação de **$79{,}6\%$** demonstra que quase 8 em cada 10 passageiros teletransportados são imediatamente identificados pela triagem primária do modelo.

#### Interpretação dos Odds Ratios (Razões de Chance)
Para conferir inteligibilidade técnica, os coeficientes logísticos estimados no treino foram convertidos em **Odds Ratios ($OR = e^{\beta}$)** acompanhados de seus respectivos Intervalos de Confiança assintóticos de 95%.

| Variável / Preditor | Coeficiente ($\beta$) | Erro-Padrão ($SE$) | *Odds Ratio* ($OR$) | IC 95% do *Odds Ratio* | Interpretação em Lógica de Negócio |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **`HomePlanet_Europa`** | $+1{,}379$ | $0{,}220$ | **$3{,}97$** | $[2{,}58; 6{,}10]$ | Estando nos mesmos conveses e com gastos iguais, um passageiro europeu tem quase **$4\times$ maior chance** de teletransporte em relação ao terrestre. |
| **`CryoSleep_True`** | $+1{,}166$ | $0{,}105$ | **$3{,}21$** | $[2{,}61; 3{,}94]$ | Mesmo controlando localização, gastos e idade, o sono criogênico multiplica a chance de teletransporte por **$3{,}21$ vezes**. |
| **`FoodCourt` (por 1 DP $\ln$)** | $+0{,}392$ | $0{,}041$ | **$1{,}48$** | $[1{,}36; 1{,}60]$ | Cada desvio-padrão de aumento no log de consumo de alta gastronomia eleva as chances de transporte em $48\%$. |
| **`HomePlanet_Mars`** | $+0{,}336$ | $0{,}105$ | **$1{,}40$** | $[1{,}14; 1{,}72]$ | Passageiros de Marte exibem chance $40\%$ superior aos terrestres, tudo o mais constante. |
| **`ShoppingMall` (por 1 DP $\ln$)**| $+0{,}215$ | $0{,}035$ | **$1{,}24$** | $[1{,}15; 1{,}32]$ | Atividade em lojas comerciais associa-se modestamente ao aumento de transporte ($+24\%$). |
| **`CabinSide_P` (Bombordo)** | $-0{,}511$ | $0{,}059$ | **$0{,}60$** | $[0{,}53; 0{,}67]$ | Estar alojado a Bombordo reduz a chance de sinistro em $40\%$ ($OR = 0{,}60$) frente ao Boreste (*Starboard*). |
| **`RoomService` (por 1 DP $\ln$)** | $-0{,}598$ | $0{,}037$ | **$0{,}55$** | $[0{,}51; 0{,}59]$ | Gastos em serviço de quarto associam-se a uma chance $45\%$ menor de teletransporte. |
| **`CabinDeck_G`** | $-0{,}635$ | $0{,}096$ | **$0{,}53$** | $[0{,}44; 0{,}64]$ | Ocupantes do convés inferior G têm $47\%$ menor chance de transporte que o convés de referência F. |
| **`Spa` (por 1 DP $\ln$)** | $-0{,}734$ | $0{,}037$ | **$0{,}48$** | $[0{,}44; 0{,}51]$ | Consumo em tratamentos de spa associa-se a uma redução de $52\%$ nas chances de transporte. |

A decomposição dos *Odds Ratios* traz revelações operacionais cruciais:
1. **Confirmação Multivariada de Criossono:** O efeito massivo do criossono resistiu integralmente ao controle multivariado ($OR = 3{,}21$), confirmando que não se tratava de mero artefato do deck ou da idade.
2. **Assimetria por Bordo (*Side*):** O bombordo (`CabinSide P`) demonstrou efeito protetor significativo frente ao boreste ($OR = 0{,}60$), sugerindo que o feixe de teletransporte incidiu obliquamente pela lateral de estibordo da embarcação.

---

## 7. Conclusões, Recomendações e Próximos Passos

### 7.1. Síntese dos Resultados Obtidos
A presente investigação conclui de forma inequívoca que o evento de teletransporte na *Spaceship Titanic* não ocorreu como um processo espacialmente homogêneo ou estocasticamente neutro. Três macrofatores governam o desfecho:
1. **O estado de imobilidade física** induzido pelas câmaras criogênicas ($81{,}47\%$ de sinistro; $OR = 3{,}21$).
2. **A geometria do impacto espacial**, com interceptação concentrada nos conveses superiores B e C ($>68\%$ de sinistro) e na amura de boreste (*Starboard*).
3. **A segregação populacional**, que alocou cidadãos de Europa justamente no setor de maior penetração da anomalia, conferindo-lhes taxa desproporcional ($66{,}05\%$).

O modelo de regressão logística desenvolvido cumpre rigorosamente os padrões de qualidade técnica do CIn/UFPE, conferindo **$77{,}9\%$ de acurácia** e **$0{,}862$ de ROC-AUC** com plena interpretabilidade econométrica e ausência de *black-box*.

### 7.2. Cinco Recomendações Estratégicas para o Comando Operacional
Com base nas evidências empíricas auditadas, submetem-se ao Comando de Operações Espaciais as seguintes ações prioritárias:

1. **Priorizar Imediatamente a Varredura das Câmaras de Criossono:**  
   As equipes de busca e resgate dimensional devem focar primariamente os compartimentos criogênicos. Passageiros isolados nessas câmaras sofreram sinistro em mais de 8 de cada 10 casos. Devem ser classificados como setor de prioridade alfa nas operações de emergência e no contato com seguradoras e familiares.
2. **Investigar Causalidade Estrutural nos Conveses B e C em Detrimento de Origem:**  
   A diretoria não deve tratar a procedência europeia como causa biológica ou jurídica do desastre. A anomalia atingiu os setores superiores da nave onde essas cabines estavam situadas. Recomenda-se uma perícia de engenharia naval nas ligas de blindagem dos conveses B e C para averiguar falhas de isolamento de blindagem eletromagnética.
3. **Descartar Despesas Financeiras como Critério de Triagem ou Importância:**  
   A correlação bivariada entre gastos elevados e sobrevivência é fruto de confundimento com o estado acordado. Utilizar despesas como filtro de resgate provocaria discriminação socioeconômica injustificável e errônea, ignorando os $41{,}9\%$ de passageiros de gasto zero. A triagem deve pautar-se em localização física da cabine, criossono e tamanho do grupo.
4. **Empregar o Modelo Logístico em Triagem Assistida (Human-in-the-Loop):**  
   O modelo preditivo fornece excelente ordenamento probabilístico ($ROC-AUC = 0{,}862$), mas não deve deliberar isoladamente. Recomenda-se calibrar o limiar de decisão ($\tau$) conforme o custo institucional: caso o custo de abandonar um sobrevivente seja muito superior ao de uma verificação desnecessária, deve-se reduzir o corte de $\tau = 0{,}50$ para $\tau = 0{,}35$, maximizando a sensibilidade para além de $90\%$.
5. **Padronizar Comunicação Institucional por Medianas e Proporções:**  
   Em comunicados aos órgãos reguladores e à imprensa, o Comando deve abandonar o uso de despesas médias ($\$1.445{,}46$), altamente distorcidas por valores extremos de luxo ($CV = 1{,}93$). Devem ser comunicadas medianas (US$ 0,00 e US$ 907,00) e proporções estratificadas de grupos, preservando a honestidade técnica da comunicação pública.

### 7.3. Cinco Limitações Metodológicas do Estudo
Em estrita observância à transparência científica exigida pela banca examinadora, registram-se as limitações do presente trabalho:

1. **Natureza Observacional Estrita:** Todos os coeficientes, correlações e razões de chance descrevem associações empíricas observadas no sinistro. Não foi conduzido experimento aleatório controlado, sendo vedada qualquer inferência causal definitiva sobre os mecanismos físicos do feixe.
2. **Partição Única de Validação (80/20):** A avaliação do classificador foi conduzida sobre uma partição de teste única. Embora estratificada e auditada com semente fixa, não foram calculados intervalos de confiança empíricos via *Bootstrap* ou validação cruzada $k$-fold para as métricas finais de generalização.
3. **Divisão por Passageiro em Detrimento de Grupo Familiar:** A divisão 80/20 operou no nível do passageiro individual (`PassengerId`), e não no nível de grupo de viagem (`GroupSize`). Membros de uma mesma família podem figurar simultaneamente no treino e no teste, introduzindo dependência estocástica residual que pode tornar as métricas ligeiramente otimistas.
4. **Imputação de Categóricas pela Moda:** Cerca de $2{,}1\%$ a $2{,}5\%$ dos dados categóricos foram imputados pela moda do grupo ou do convés. Embora a análise de sensibilidade documente oscilação máxima inferior a $0{,}77$ pontos percentuais, a variância original foi ligeiramente comprimida.
5. **Multicolinearidade nos Conveses Superiores:** O VIF elevado de `HomePlanet_Europa` ($7{,}98$) e sua sobreposição com os decks B e C impedem o desacoplamento matemático perfeito entre o efeito de nacionalidade e o efeito de convés na regressão logística.

### 7.4. Próximos Passos na Governança do Projeto
A conclusão do presente relatório técnico consolidado (**`KAN-39`**) desbloqueia a etapa subsequente de governança:
- **`KAN-40` — Revisão de Coerência Metodológica:** A cargo de **Luciana Almeida** (com co-revisão de Daniela Amaro e Renatta Batista), cujo objetivo é auditar o alinhamento cruzado entre as premissas de distribuições (Seção 4), a adequação dos testes inferenciais (Seção 5) e as conclusões interpretativas aqui formuladas.
- **`KAN-41` — Validação Numérica Cruzada:** Conduzida por **Daniela Amaro**, conferindo cada número, percentagem e intervalo de confiança deste relatório contra a saída de execução limpa do notebook consolidado mestre (`notebooks/00_projeto_final_estatistica.ipynb`).
- **`KAN-42` e `KAN-43` — Diagramação em PDF e Empacotamento Final:** Geração do documento oficial paginado em PDF para submissão à banca examinadora da Pós-Graduação em Deep Learning do CIn/UFPE.

---

*Relatório técnico consolidado no âmbito do card **KAN-39**, com dados auditados em 11 de novembro de 2026.*
