# Inventário e Dicionário de Dados — Spaceship Titanic (`KAN-10`, `KAN-11` e `KAN-12`)

- **Tickets Relacionados (Jira):**
  - [KAN-10 — Criar inventário e dicionário de dados](https://megamatic.atlassian.net/browse/KAN-10)
  - [KAN-11 — Analisar valores ausentes e duplicados](https://megamatic.atlassian.net/browse/KAN-11)
  - [KAN-12 — Criar variáveis derivadas do Spaceship Titanic](https://megamatic.atlassian.net/browse/KAN-12)
- **Fonte Oficial dos Dados:** [Kaggle — Spaceship Titanic Competition](https://www.kaggle.com/competitions/spaceship-titanic)
- **Notebook Mestre de Referência:** [`notebooks/00_projeto_final_estatistica.ipynb`](../notebooks/00_projeto_final_estatistica.ipynb)
- **Responsável Principal:** Gustavo
- **Revisor Dedicado:** Helton

---

## 1. Visão Geral e Contexto de Negócio

O conjunto de dados **Spaceship Titanic** simula os registros de bordo do transatlântico intergaláctico *Spaceship Titanic*, lançado no ano de **2912** com quase 13.000 passageiros a bordo em uma viagem inaugural rumo a três exoplanetas recém-habitáveis a partir de três planetas de origem no Sistema Solar.

Durante o trajeto ao redor de *Alpha Centauri*, a espaçonave colidiu com uma anomalia espaço-temporal oculta dentro de uma nuvem de poeira cósmica. Embora a estrutura física da nave tenha permanecido intacta, quase metade dos passageiros foi teletransportada para uma **dimensão alternativa** (`Transported = True`).

O objetivo analítico e estatístico do projeto consiste em compreender os fatores demográficos, de acomodação, de grupo familiar e de consumo a bordo associados ao evento de transporte (`Transported`), sustentando análises descritivas, inferência estatística, testes de hipóteses e modelagem preditiva.

---

## 2. Inventário de Dados Brutos (`data/raw/`) e Processados (`data/processed/`)

Os arquivos originais da competição foram armazenados de forma imutável no diretório `data/raw/`, enquanto os datasets tratados (sem valores ausentes) e enriquecidos com as 8 variáveis derivadas do `KAN-12` foram exportados para `data/processed/`:

| Arquivo | Caminho Relativo | Linhas (Registros) | Colunas | Tamanho em Disco | Unidade Amostral (Granularidade) | Presença da Variável Alvo (`Transported`) | Registros Duplicados | Total de Células Ausentes (`NaN`) |
| :--- | :--- | :---: | :---: | :---: | :--- | :---: | :---: | :---: |
| **`train.csv`** | `data/raw/train.csv` | 8.693 | 14 | ~787 KB (805.421 B) | 1 linha = 1 passageiro (`PassengerId`) | Sim (Booleana) | 0 | 2.324 (1,91% das células) |
| **`test.csv`** | `data/raw/test.csv` | 4.277 | 13 | ~364 KB (372.487 B) | 1 linha = 1 passageiro (`PassengerId`) | Não (Conjunto de avaliação Kaggle) | 0 | 1.117 (2,01% das células) |
| **`sample_submission.csv`** | `data/raw/sample_submission.csv` | 4.277 | 2 | ~59 KB (59.902 B) | 1 linha = 1 predição por passageiro | Template (`PassengerId`, `Transported`) | 0 | 0 (0,00%) |
| **`spaceship_titanic_clean.csv`** | `data/processed/spaceship_titanic_clean.csv` | 8.693 | 22 | ~1,04 MB (1.092.085 B) | 1 linha = 1 passageiro (`PassengerId`) | Sim (Booleana) | 0 | **0 (0,00%)** |
| **`spaceship_titanic_test_clean.csv`** | `data/processed/spaceship_titanic_test_clean.csv` | 4.277 | 21 | ~502 KB (513.565 B) | 1 linha = 1 passageiro (`PassengerId`) | Não (Conjunto de avaliação Kaggle) | 0 | **0 (0,00%)** |

> **Escopo das Análises Estatísticas:** As etapas de exploração descritiva, intervalos de confiança, testes de hipóteses, correlação/regressão e validação supervisionada utilizam primariamente a base rotulada **`train.csv`** ($n = 8.693$ passageiros), garantindo ausência de vazamento de dados (*data leakage*) e presença do desfecho observado `Transported`.

### 2.1. Inventário de Completude e Cardinalidade por Coluna (`train.csv` vs. `test.csv`)

| # | Nome da Coluna | Tipo Bruto (`pandas`) | Não-Nulos (`train`) | Ausentes (`train`) | % Ausentes (`train`) | Valores Únicos (`train`) | Ausentes (`test`) | % Ausentes (`test`) | Valores Únicos (`test`) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | `PassengerId` | `object` / `str` | 8.693 | 0 | 0,00% | 8.693 | 0 | 0,00% | 4.277 |
| 2 | `HomePlanet` | `object` / `str` | 8.492 | 201 | 2,31% | 3 | 87 | 2,03% | 3 |
| 3 | `CryoSleep` | `object` (`bool`) | 8.476 | 217 | 2,50% | 2 | 93 | 2,17% | 2 |
| 4 | `Cabin` | `object` / `str` | 8.494 | 199 | 2,29% | 6.560 | 100 | 2,34% | 3.265 |
| 5 | `Destination` | `object` / `str` | 8.511 | 182 | 2,09% | 3 | 92 | 2,15% | 3 |
| 6 | `Age` | `float64` | 8.514 | 179 | 2,06% | 80 | 91 | 2,13% | 79 |
| 7 | `VIP` | `object` (`bool`) | 8.490 | 203 | 2,34% | 2 | 93 | 2,17% | 2 |
| 8 | `RoomService` | `float64` | 8.512 | 181 | 2,08% | 1.273 | 82 | 1,92% | 842 |
| 9 | `FoodCourt` | `float64` | 8.510 | 183 | 2,11% | 1.507 | 106 | 2,48% | 902 |
| 10 | `ShoppingMall` | `float64` | 8.485 | 208 | 2,39% | 1.115 | 98 | 2,29% | 715 |
| 11 | `Spa` | `float64` | 8.510 | 183 | 2,11% | 1.327 | 101 | 2,36% | 833 |
| 12 | `VRDeck` | `float64` | 8.505 | 188 | 2,16% | 1.306 | 80 | 1,87% | 796 |
| 13 | `Name` | `object` / `str` | 8.493 | 200 | 2,30% | 8.473 | 94 | 2,20% | 4.176 |
| 14 | `Transported` | `bool` | 8.693 | 0 | 0,00% | 2 | — | — | — |

---

## 3. Dicionário de Dados Formal (14 Variáveis Originais)

A tabela a seguir apresenta a especificação formal das 14 colunas originais segundo a tipologia estatística padronizada no ticket **KAN-10**:

| Nome da Coluna | Tipo do Dado | Tipologia Estatística | Escala de Medida | Descrição de Negócio | Valores Possíveis / Amplitude (`train.csv`) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`PassengerId`** | Texto (`string`) | **Categórica Estruturada** | Nominal (Identificador Composto) | Identificador único de cada passageiro no formato `gggg_pp`, onde `gggg` identifica o grupo de viagem ao qual o passageiro pertence e `pp` é o número sequencial do indivíduo dentro daquele grupo. | Formato `0001_01` a `9280_02`.<br>• 8.693 IDs únicos (sem nulos)<br>• 6.217 grupos distintos (`0001` a `9280`)<br>• Índice no grupo `pp`: `01` a `08` |
| **`HomePlanet`** | Texto (`string`) | **Categórica Nominal** | Nominal | Planeta de residência permanente / embarque do passageiro antes do início da jornada espacial. | 3 categorias possíveis (+ `NaN`):<br>• `Earth` (4.602; 52,94%)<br>• `Europa` (2.131; 24,51%)<br>• `Mars` (1.759; 20,23%)<br>• Ausentes: 201 (2,31%) |
| **`CryoSleep`** | Booleano (`bool` / `object` com `NaN`) | **Categórica Nominal** (Dicotômica) | Nominal (Binária) | Indica se o passageiro optou por permanecer em animação suspensa (*criossono*) durante toda a viagem. Passageiros em criossono permanecem confinados em suas cabines e não realizam gastos em serviços de bordo. | 2 valores possíveis (+ `NaN`):<br>• `False` (5.439; 62,57%)<br>• `True` (3.037; 34,94%)<br>• Ausentes: 217 (2,50%) |
| **`Cabin`** | Texto (`string`) | **Categórica Estruturada** | Nominal / Composta (`deck/num/side`) | Código da cabine de alojamento do passageiro no formato `deck/num/side`, onde `deck` é o convés da nave, `num` é o número da cabine no convés e `side` indica o lado da embarcação (`P` = *Port* / Bombordo; `S` = *Starboard* / Boreste). Pessoas na mesma cabine frequentemente compartilham o mesmo grupo familiar. | 6.560 cabines distintas (+ `NaN`):<br>• `deck`: `{A, B, C, D, E, F, G, T}`<br>• `num`: `0` a `1894` (inteiro)<br>• `side`: `P` (Bombordo) ou `S` (Boreste)<br>• Ausentes: 199 (2,29%) |
| **`Destination`** | Texto (`string`) | **Categórica Nominal** | Nominal | Exoplaneta de destino para o qual o passageiro está desembarcando ao término da viagem. | 3 categorias possíveis (+ `NaN`):<br>• `TRAPPIST-1e` (5.915; 68,04%)<br>• `55 Cancri e` (1.800; 20,71%)<br>• `PSO J318.5-22` (796; 9,16%)<br>• Ausentes: 182 (2,09%) |
| **`Age`** | Numérico (`float64` representando anos inteiros) | **Quantitativa Discreta** | Razão (Discreta em anos completos) | Idade biológica do passageiro em anos completos no momento do embarque (`0` indica bebês com menos de 1 ano de vida). Armazenada como `float64` no CSV devido à presença de valores `NaN`. | Inteiros em $[0, 79]$ anos:<br>• Mínimo: `0` anos \| Máximo: `79` anos<br>• Média: `28,83` \| Desvio-padrão: `14,49`<br>• Mediana ($Q_2$): `27,0` \| IIQ ($Q_1$–$Q_3$): `19,0`–`38,0`<br>• Ausentes: 179 (2,06%) |
| **`VIP`** | Booleano (`bool` / `object` com `NaN`) | **Categórica Nominal** (Dicotômica) | Nominal (Binária) | Indica se o passageiro contratou o pacote especial de serviço exclusivo de alta prioridade (*Very Important Person*) durante a viagem. | 2 valores possíveis (+ `NaN`):<br>• `False` (8.291; 95,38%)<br>• `True` (199; 2,29%)<br>• Ausentes: 203 (2,34%) |
| **`RoomService`** | Numérico (`float64`) | **Quantitativa Contínua** | Razão | Valor monetário total faturado pelo passageiro em pedidos de serviço de quarto (*Room Service*) ao longo da viagem. | Valores reais não-negativos em $[0,0;\; 14.327,0]$:<br>• Mín: `0,0` \| Mediana: `0,0` \| $P_{95}$: `1.274,25` \| Máx: `14.327,0`<br>• Média: `224,69` \| Desvio-padrão: `666,72`<br>• Ausentes: 181 (2,08%) |
| **`FoodCourt`** | Numérico (`float64`) | **Quantitativa Contínua** | Razão | Valor monetário total faturado pelo passageiro na praça de alimentação e restaurantes (*Food Court*) da espaçonave. | Valores reais não-negativos em $[0,0;\; 29.813,0]$:<br>• Mín: `0,0` \| Mediana: `0,0` \| $P_{95}$: `2.748,50` \| Máx: `29.813,0`<br>• Média: `458,08` \| Desvio-padrão: `1.611,49`<br>• Ausentes: 183 (2,11%) |
| **`ShoppingMall`** | Numérico (`float64`) | **Quantitativa Contínua** | Razão | Valor monetário total faturado pelo passageiro no centro comercial (*Shopping Mall*) da espaçonave. | Valores reais não-negativos em $[0,0;\; 23.492,0]$:<br>• Mín: `0,0` \| Mediana: `0,0` \| $P_{95}$: `927,80` \| Máx: `23.492,0`<br>• Média: `173,73` \| Desvio-padrão: `604,70`<br>• Ausentes: 208 (2,39%) |
| **`Spa`** | Numérico (`float64`) | **Quantitativa Contínua** | Razão | Valor monetário total faturado pelo passageiro no centro de relaxamento e bem-estar (*Spa*) da espaçonave. | Valores reais não-negativos em $[0,0;\; 22.408,0]$:<br>• Mín: `0,0` \| Mediana: `0,0` \| $P_{95}$: `1.607,10` \| Máx: `22.408,0`<br>• Média: `311,14` \| Desvio-padrão: `1.136,71`<br>• Ausentes: 183 (2,11%) |
| **`VRDeck`** | Numérico (`float64`) | **Quantitativa Contínua** | Razão | Valor monetário total faturado pelo passageiro no convés de simulação de realidade virtual (*Virtual Reality Deck*). | Valores reais não-negativos em $[0,0;\; 24.133,0]$:<br>• Mín: `0,0` \| Mediana: `0,0` \| $P_{95}$: `1.534,20` \| Máx: `24.133,0`<br>• Média: `304,85` \| Desvio-padrão: `1.145,72`<br>• Ausentes: 188 (2,16%) |
| **`Name`** | Texto (`string`) | **Categórica Estruturada** | Nominal (Texto Composto: Nome + Sobrenome) | Nome completo do passageiro composto por prenome e sobrenome de família (`FirstName LastName`), permitindo identificar vínculos familiares entre passageiros do mesmo grupo ou cabine. | 8.473 nomes distintos (+ `NaN`):<br>• Ex: `Maham Ofracculy`, `Juanna Vines`<br>• 2.217 sobrenomes únicos em `train.csv`<br>• Ausentes: 200 (2,30%) |
| **`Transported`** | Booleano (`bool`) | **Categórica Nominal** (Alvo / Desfecho Binário) | Nominal (Binária) | **Variável resposta (Target):** indica se o passageiro foi teletransportado para outra dimensão após a colisão com a anomalia espaço-temporal (`True`) ou se permaneceu a bordo em segurança (`False`). | 2 valores possíveis (sem nulos em `train.csv`):<br>• `True` (4.378; 50,36%)<br>• `False` (4.315; 49,64%)<br>• Classes perfeitamente balanceadas |

### 3.1. Dicionário de Dados Formal das 8 Variáveis Derivadas (`KAN-12` — `data/processed/`)

As 8 variáveis derivadas a seguir foram construídas sobre as bases imputadas (`KAN-11`) e adicionadas a `data/processed/spaceship_titanic_clean.csv` ($8.693 \times 22$) e `data/processed/spaceship_titanic_test_clean.csv` ($4.277 \times 21$) com **0% de valores ausentes** e **zero vazamento de dados**:

| Nome da Coluna | Variável de Origem | Tipo do Dado | Tipologia Estatística | Escala de Medida | Descrição de Negócio e Regra de Derivação | Valores Possíveis / Amplitude (`spaceship_titanic_clean.csv`) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`Group`** | `PassengerId` (`gggg_pp`) | Texto (`string`) | **Categórica Estruturada** | Nominal (Código de Grupo) | Código identificador de 4 dígitos (`gggg`) do grupo de viagem extraído do prefixo de `PassengerId` (`PassengerId.str.split('_').str[0]`). | 6.217 grupos exclusivos no treino (`'0001'` a `'9280'`) e 3.063 grupos exclusivos no teste (interseção nula entre treino e teste; `0` ausentes). |
| **`GroupSize`** | `Group` (de `PassengerId`) | Numérico Inteiro (`int64`) | **Quantitativa Discreta** | Razão (Contagem de Membros) | Quantidade total de passageiros pertencentes ao mesmo grupo `Group` (`groupby('Group')['Group'].transform('count')`), coincidindo em 100% dos casos com o maior índice sequencial `pp` do grupo. | Inteiros em $[1, 8]$ passageiros:<br>• Mín: `1` \| Mediana: `1,0` \| $Q_3$: `3,0` \| Máx: `8`<br>• Média: `2,04` \| Desvio-padrão: `1,60`<br>• Ausentes: `0` (0,00%) |
| **`IsAlone`** | `GroupSize` | Booleano (`bool`) | **Categórica Nominal** (Dicotômica) | Nominal (Binária) | Flag binária que indica se o passageiro viaja sozinho, sem outros integrantes no grupo (`GroupSize == 1`). | 2 valores possíveis (`0` ausentes):<br>• `True` — Viaja sozinho: 4.805 (55,27%)<br>• `False` — Em grupo ($\ge 2$): 3.888 (44,73%) |
| **`CabinDeck`** | `Cabin` (`deck/num/side`) | Texto (`string`) | **Categórica Nominal / Ordinal** | Nominal / Ordinal (Convés) | Letra identificadora do convés da cabine onde o passageiro está alojado (`Cabin.str.split('/').str[0]`), refletindo a localização vertical e estratificação da acomodação. | 8 categorias possíveis (`0` ausentes):<br>• `F` (2.868; 32,99%), `G` (2.588; 29,77%), `E` (885; 10,18%), `B` (817; 9,40%), `C` (761; 8,75%), `D` (507; 5,83%), `A` (262; 3,01%), `T` (5; 0,06%) |
| **`CabinNum`** | `Cabin` (`deck/num/side`) | Numérico Inteiro (`int64`) | **Quantitativa Discreta** | Intervalar / Posicional (Número da Cabine) | Número sequencial da cabine dentro do respectivo convés (`Cabin.str.split('/').str[1].astype(int64)`). | Inteiros em $[0, 1894]$:<br>• Mín: `0` \| $Q_1$: `166,0` \| Mediana: `426,0` \| $Q_3$: `1.006,0` \| Máx: `1.894`<br>• Média: `600,20` \| Desvio-padrão: `512,29`<br>• Ausentes: `0` (0,00%) |
| **`CabinSide`** | `Cabin` (`deck/num/side`) | Texto (`string`) | **Categórica Nominal** (Dicotômica) | Nominal (Binária) | Lado da espaçonave em que a cabine está localizada (`Cabin.str.split('/').str[2]`): `P` = *Port* (Bombordo) ou `S` = *Starboard* (Boreste / Estibordo). | 2 categorias possíveis (`0` ausentes):<br>• `S` (*Starboard* / Boreste): 4.384 (50,43%)<br>• `P` (*Port* / Bombordo): 4.309 (49,57%) |
| **`TotalSpend`** | `RoomService`, `FoodCourt`, `ShoppingMall`, `Spa`, `VRDeck` | Numérico Real (`float64`) | **Quantitativa Contínua** | Razão | Soma algébrica do consumo monetário do passageiro nas 5 comodidades de luxo da espaçonave (`RoomService + FoodCourt + ShoppingMall + Spa + VRDeck`). | Reais não-negativos em $[0,0;\; 35.987,0]$:<br>• Mín: `0,0` \| $Q_1$: `0,0` \| Mediana: `717,0` \| $Q_3$: `1.444,0` \| $P_{95}$: `6.486,0` \| Máx: `35.987,0`<br>• Média: `1.447,46` \| Desvio-padrão: `2.808,28`<br>• Zeros (`== 0,0`): 3.644 (41,92%) \| Ausentes: `0` |
| **`HasSpent`** | `TotalSpend` | Booleano (`bool`) | **Categórica Nominal** (Dicotômica) | Nominal (Binária) | Flag binária que indica se o passageiro realizou algum gasto positivo a bordo durante a viagem (`TotalSpend > 0`). | 2 valores possíveis (`0` ausentes):<br>• `True` (`TotalSpend > 0`): 5.049 (58,08%)<br>• `False` (`TotalSpend == 0`): 3.644 (41,92%) |

---

## 4. Síntese da Classificação segundo a Tipologia Estatística

Conforme diretriz técnica do card `KAN-10`, as 14 colunas originais dividem-se em 4 grupos tipológicos fundamentais:

1. **Categóricas Nominais (5 variáveis):**
   - **Politômicas (3 categorias):** `HomePlanet` (`Earth`, `Europa`, `Mars`) e `Destination` (`TRAPPIST-1e`, `55 Cancri e`, `PSO J318.5-22`).
   - **Dicotômicas / Binárias (2 categorias):** `CryoSleep` (`True`/`False`), `VIP` (`True`/`False`) e a variável alvo `Transported` (`True`/`False`).
   - *Propriedade estatística:* Não possuem ordenação intrínseca natural entre as categorias; devem ser analisadas por tabelas de contingência, proporções binomiais/multinomiais, testes Qui-Quadrado de independência ($\chi^2$) e Razão de Chances (*Odds Ratio*).

2. **Categóricas Estruturadas (3 variáveis):**
   - `PassengerId` (`gggg_pp`), `Cabin` (`deck/num/side`) e `Name` (`FirstName LastName`).
   - *Propriedade estatística:* Possuem alta cardinalidade em sua forma bruta textual (não devendo ser usadas diretamente como *one-hot encoding*), mas carregam **subestruturas relacionais e espaciais** ricas que permitem extrair variáveis derivadas de alto valor explicativo (tamanho do grupo, indicador de viagem solo, convés da cabine, lado bombordo/boreste e agrupamento por sobrenome).

3. **Quantitativa Discreta (1 variável):**
   - `Age` (idade em anos inteiros de `0` a `79`).
   - *Propriedade estatística:* Escala de razão assumindo valores inteiros contáveis. Embora lida inicialmente como `float64` pelo `pandas` devido à presença de 179 valores ausentes (`NaN`), todos os valores observados possuem parte fracionária nula (`.0`).

4. **Quantitativas Contínuas (5 variáveis):**
   - `RoomService`, `FoodCourt`, `ShoppingMall`, `Spa` e `VRDeck`.
   - *Propriedade estatística:* Escala de razão com zero absoluto (ausência total de consumo na respectiva comodidade). Apresentam distribuição fortemente **assimétrica à direita (positiva)** e inflacionada de zeros (*zero-inflated*), uma vez que passageiros em `CryoSleep == True` e crianças pequenas (`Age <= 12`) apresentam consumo zero.

---

## 5. Regras de Negócio e Relações Estruturais Relevantes

O mapeamento exaustivo das colunas evidencia regras de domínio essenciais para as etapas subsequentes (`KAN-11` e `KAN-12`):

1. **Regra do Criossono (`CryoSleep == True`) vs. Despesas a Bordo:**
   - Passageiros em animação suspensa (`CryoSleep == True`) estão fisicamente impossibilitados de consumir serviços de quarto, alimentação, compras, spa ou realidade virtual. Portanto, qualquer valor ausente nas 5 colunas de gastos para passageiros com `CryoSleep == True` corresponde deterministicamente a **`0.0`**, e vice-versa (passageiros com gasto positivo não estavam em criossono).
2. **Faixa Etária Infantil (`Age <= 12`) vs. Consumo e VIP:**
   - Passageiros de 0 a 12 anos não registram faturamento próprio nas comodidades pagas nem status `VIP == True`.
3. **Estrutura de Grupos (`PassengerId` -> `gggg_pp`):**
   - O prefixo `gggg` agrupa passageiros que viajaram juntos. Membros de um mesmo grupo frequentemente compartilham o mesmo `HomePlanet`, o mesmo sobrenome (`Name`) e a mesma cabine ou mesmo lado (`CabinSide`).
4. **Decomposição Espacial da Cabine (`Cabin` -> `deck/num/side`):**
   - O convés (`CabinDeck`, de `A` a `G` mais `T`) reflete a estratificação socioeconômica e física na espaçonave (por exemplo, passageiros de `Europa` concentram-se nos conveses superiores `A`, `B`, `C`, enquanto passageiros da `Earth` predominam nos conveses `E`, `F`, `G`), podendo inclusive apresentar uma ordenação funcional na engenharia de recursos (`KAN-12`).
