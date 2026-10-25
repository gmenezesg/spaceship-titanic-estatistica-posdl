# Inventário de Dados — Spaceship Titanic (`KAN-10`, `KAN-11` e `KAN-12`)

- **Tickets Relacionados (Jira):**
  - [KAN-10 — Criar inventário e dicionário de dados](https://megamatic.atlassian.net/browse/KAN-10)
  - [KAN-11 — Analisar valores ausentes e duplicados](https://megamatic.atlassian.net/browse/KAN-11)
  - [KAN-12 — Criar variáveis derivadas do Spaceship Titanic](https://megamatic.atlassian.net/browse/KAN-12)
- **Fonte Oficial dos Dados:** [Kaggle — Spaceship Titanic Competition](https://www.kaggle.com/competitions/spaceship-titanic)
- **Dicionário de Dados Complementar:** [`docs/dicionario_dados.md`](dicionario_dados.md)
- **Notebook de Referência:** [`notebooks/00_projeto_final_estatistica.ipynb`](../notebooks/00_projeto_final_estatistica.ipynb)
- **Responsável Principal:** Gustavo
- **Revisor Dedicado:** Helton

---

## 1. Catálogo de Ativos de Dados (`data/raw/` e `data/processed/`)

O inventário de dados cataloga todos os arquivos brutos provenientes da competição oficial do Kaggle **Spaceship Titanic** (`data/raw/`) e os ativos limpos e enriquecidos com variáveis derivadas (`data/processed/`), garantindo rastreabilidade, controle de integridade e padronização de leitura pelos notebooks do projeto.

### 1.1. Ativos Brutos Originais (`data/raw/` — Imutáveis)

| Ativo de Dados | Localização | Formato | Codificação | Separador | Registros ($n$) | Variáveis ($p$) | Tamanho em Disco | Papel no Projeto |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **`train.csv`** | `data/raw/train.csv` | CSV | UTF-8 | Vírgula (`,`) | 8.693 | 14 | 805.421 bytes (~787 KB) | Base principal de análise exploratória, inferência estatística, testes de hipóteses e treino supervisionado (contém o alvo `Transported`). |
| **`test.csv`** | `data/raw/test.csv` | CSV | UTF-8 | Vírgula (`,`) | 4.277 | 13 | 372.487 bytes (~364 KB) | Base de avaliação sem rótulo (`Transported` omitido), utilizada para avaliação final de generalização na competição Kaggle. |
| **`sample_submission.csv`** | `data/raw/sample_submission.csv` | CSV | UTF-8 | Vírgula (`,`) | 4.277 | 2 | 59.902 bytes (~59 KB) | Arquivo modelo de submissão contendo `PassengerId` e predição padrão para `Transported`. |

### 1.2. Ativos Limpos e Enriquecidos (`data/processed/` — `KAN-11` e `KAN-12`)

| Ativo de Dados | Localização | Formato | Codificação | Separador | Registros ($n$) | Variáveis ($p$) | Células Ausentes (`NaN`) | Tamanho em Disco | Papel no Projeto |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **`spaceship_titanic_clean.csv`** | `data/processed/spaceship_titanic_clean.csv` | CSV | UTF-8 | Vírgula (`,`) | 8.693 | 22 (14 originais + 8 derivadas) | 0 (0,00%) | 1.092.085 bytes (~1,04 MB) | Dataset oficial de treino saneado e enriquecido para as trilhas de Estatística Descritiva (`KAN-14`/`KAN-15`), Distribuições (`KAN-20`), Testes de Hipóteses (`KAN-24`) e Regressões (`KAN-30`/`KAN-32`). |
| **`spaceship_titanic_test_clean.csv`** | `data/processed/spaceship_titanic_test_clean.csv` | CSV | UTF-8 | Vírgula (`,`) | 4.277 | 21 (13 originais + 8 derivadas) | 0 (0,00%) | 513.565 bytes (~502 KB) | Dataset de teste tratado sem vazamento de dados (*zero data leakage*) e enriquecido com as mesmas 8 variáveis derivadas. |

---

## 2. Sumário de Volume e Integridade Estrutural

| Métrica de Inventário | `train.csv` | `test.csv` | Total Combinado (`train` + `test`) |
| :--- | :---: | :---: | :---: |
| **Total de Passageiros (Linhas)** | 8.693 | 4.277 | 12.970 |
| **Total de Colunas** | 14 | 13 | 14 (13 preditoras + 1 alvo) |
| **Total de Células ($n \times p$)** | 121.702 | 55.601 | 177.303 |
| **Total de Células Preenchidas** | 119.378 (98,09%) | 54.484 (97,99%) | 173.862 (98,06%) |
| **Total de Células Ausentes (`NaN`)** | 2.324 (1,91%) | 1.117 (2,01%) | 3.441 (1,94%) |
| **Linhas Completas (Sem nenhum `NaN`)** | 6.606 (75,99%) | 3.281 (76,71%) | 9.887 (76,23%) |
| **Linhas com $\ge 1$ Valor Ausente** | 2.087 (24,01%) | 996 (23,29%) | 3.083 (23,77%) |
| **Registros Duplicados (`duplicated()`)** | 0 (0,00%) | 0 (0,00%) | 0 (0,00%) |
| **IDs Únicos (`PassengerId`)** | 8.693 (100%) | 4.277 (100%) | 12.970 (100%) |
| **Grupos de Viagem Distintos (`gggg`)** | 6.217 | 3.063 | 9.280 (`0001` a `9280`) |

---

## 3. Inventário Técnico por Variável (`train.csv` e `test.csv`)

| Ordem | Variável | Tipologia Estatística (`KAN-10`) | Escala | Tipo Bruto (`pandas`) | Preenchidos (`train`) | Ausentes (`train`) | % Ausentes (`train`) | Cardinalidade (`train`) | Preenchidos (`test`) | Ausentes (`test`) | % Ausentes (`test`) | Cardinalidade (`test`) |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 01 | `PassengerId` | Categórica Estruturada | Nominal | `object` / `str` | 8.693 | 0 | 0,00% | 8.693 | 4.277 | 0 | 0,00% | 4.277 |
| 02 | `HomePlanet` | Categórica Nominal | Nominal | `object` / `str` | 8.492 | 201 | 2,31% | 3 | 4.190 | 87 | 2,03% | 3 |
| 03 | `CryoSleep` | Categórica Nominal | Nominal | `object` (`bool`) | 8.476 | 217 | 2,50% | 2 | 4.184 | 93 | 2,17% | 2 |
| 04 | `Cabin` | Categórica Estruturada | Nominal | `object` / `str` | 8.494 | 199 | 2,29% | 6.560 | 4.177 | 100 | 2,34% | 3.265 |
| 05 | `Destination` | Categórica Nominal | Nominal | `object` / `str` | 8.511 | 182 | 2,09% | 3 | 4.185 | 92 | 2,15% | 3 |
| 06 | `Age` | Quantitativa Discreta | Razão | `float64` | 8.514 | 179 | 2,06% | 80 | 4.186 | 91 | 2,13% | 79 |
| 07 | `VIP` | Categórica Nominal | Nominal | `object` (`bool`) | 8.490 | 203 | 2,34% | 2 | 4.184 | 93 | 2,17% | 2 |
| 08 | `RoomService` | Quantitativa Contínua | Razão | `float64` | 8.512 | 181 | 2,08% | 1.273 | 4.195 | 82 | 1,92% | 842 |
| 09 | `FoodCourt` | Quantitativa Contínua | Razão | `float64` | 8.510 | 183 | 2,11% | 1.507 | 4.171 | 106 | 2,48% | 902 |
| 10 | `ShoppingMall` | Quantitativa Contínua | Razão | `float64` | 8.485 | 208 | 2,39% | 1.115 | 4.179 | 98 | 2,29% | 715 |
| 11 | `Spa` | Quantitativa Contínua | Razão | `float64` | 8.510 | 183 | 2,11% | 1.327 | 4.176 | 101 | 2,36% | 833 |
| 12 | `VRDeck` | Quantitativa Contínua | Razão | `float64` | 8.505 | 188 | 2,16% | 1.306 | 4.197 | 80 | 1,87% | 796 |
| 13 | `Name` | Categórica Estruturada | Nominal | `object` / `str` | 8.493 | 200 | 2,30% | 8.473 | 4.183 | 94 | 2,20% | 4.176 |
| 14 | `Transported` | Categórica Nominal (Alvo) | Nominal | `bool` | 8.693 | 0 | 0,00% | 2 | — | — | — | — |

### 3.1. Inventário Técnico das 8 Variáveis Derivadas (`KAN-12` — `data/processed/`)

Após o pipeline de imputação sem vazamento de dados (`KAN-11`), as 8 variáveis derivadas do ticket `KAN-12` foram geradas com **100% de completude (`0` ausentes)** em `spaceship_titanic_clean.csv` e `spaceship_titanic_test_clean.csv`:

| Ordem | Variável Derivada | Variável de Origem | Tipologia Estatística (`KAN-12`) | Escala | Dtype (`pandas`) | Preenchidos (`train`) | Ausentes (`train`) | Cardinalidade (`train`) | Preenchidos (`test`) | Ausentes (`test`) | Cardinalidade (`test`) |
| :---: | :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 15 | `Group` | `PassengerId` (`gggg_pp`) | Categórica Estruturada | Nominal | `object` / `str` | 8.693 | 0 | 6.217 | 4.277 | 0 | 3.063 |
| 16 | `GroupSize` | `Group` | Quantitativa Discreta | Razão | `int64` | 8.693 | 0 | 8 (`1`–`8`) | 4.277 | 0 | 8 (`1`–`8`) |
| 17 | `IsAlone` | `GroupSize` | Categórica Nominal (Binária) | Nominal | `bool` | 8.693 | 0 | 2 | 4.277 | 0 | 2 |
| 18 | `CabinDeck` | `Cabin` (`deck/num/side`) | Categórica Nominal / Ordinal | Nominal / Ordinal | `object` / `str` | 8.693 | 0 | 8 (`A`–`G`, `T`) | 4.277 | 0 | 8 (`A`–`G`, `T`) |
| 19 | `CabinNum` | `Cabin` (`deck/num/side`) | Quantitativa Discreta | Intervalar / Posicional | `int64` | 8.693 | 0 | 1.817 | 4.277 | 0 | 1.506 |
| 20 | `CabinSide` | `Cabin` (`deck/num/side`) | Categórica Nominal (Binária) | Nominal | `object` / `str` | 8.693 | 0 | 2 (`P`, `S`) | 4.277 | 0 | 2 (`P`, `S`) |
| 21 | `TotalSpend` | 5 Despesas de Bordo | Quantitativa Contínua | Razão | `float64` | 8.693 | 0 | 2.325 | 4.277 | 0 | 1.434 |
| 22 | `HasSpent` | `TotalSpend` | Categórica Nominal (Binária) | Nominal | `bool` | 8.693 | 0 | 2 | 4.277 | 0 | 2 |

---

## 4. Resumo por Grupo Tipológico (`spaceship_titanic_clean.csv` — 22 Colunas)

| Tipologia Estatística | Colunas Originais (`KAN-10`) | Variáveis Derivadas (`KAN-12`) | Total de Colunas | Colunas Associadas | Escala de Medida |
| :--- | :---: | :---: | :---: | :--- | :---: |
| **Categórica Nominal / Ordinal** | 5 | 4 | **9** | Originais: `HomePlanet`, `Destination`, `CryoSleep`, `VIP`, `Transported`<br>Derivadas: `IsAlone`, `CabinDeck`, `CabinSide`, `HasSpent` | Nominal / Ordinal |
| **Categórica Estruturada** | 3 | 1 | **4** | Originais: `PassengerId`, `Cabin`, `Name`<br>Derivada: `Group` | Nominal (Composta / Código) |
| **Quantitativa Discreta** | 1 | 2 | **3** | Original: `Age`<br>Derivadas: `GroupSize`, `CabinNum` | Razão / Intervalar |
| **Quantitativa Contínua** | 5 | 1 | **6** | Originais: `RoomService`, `FoodCourt`, `ShoppingMall`, `Spa`, `VRDeck`<br>Derivada: `TotalSpend` | Razão ($\ge 0,0$) |
| **Total** | **14** | **8** | **22** | **14 variáveis originais preservadas + 8 variáveis derivadas validadas** | — |
