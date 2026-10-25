# Inventário de Dados — Spaceship Titanic (`KAN-10`)

- **Ticket Relacionado (Jira):** [KAN-10 — Criar inventário e dicionário de dados](https://megamatic.atlassian.net/browse/KAN-10)
- **Fonte Oficial dos Dados:** [Kaggle — Spaceship Titanic Competition](https://www.kaggle.com/competitions/spaceship-titanic)
- **Dicionário de Dados Complementar:** [`docs/dicionario_dados.md`](dicionario_dados.md)
- **Notebook de Referência:** [`notebooks/00_projeto_final_estatistica.ipynb`](../notebooks/00_projeto_final_estatistica.ipynb)
- **Responsável Principal:** Gustavo
- **Revisor Dedicado:** Helton

---

## 1. Catálogo de Ativos de Dados (`data/raw/`)

O inventário de dados cataloga todos os arquivos brutos provenientes da competição oficial do Kaggle **Spaceship Titanic**, garantindo rastreabilidade, controle de integridade e padronização de leitura pelos notebooks do projeto.

| Ativo de Dados | Localização | Formato | Codificação | Separador | Registros ($n$) | Variáveis ($p$) | Tamanho em Disco | Papel no Projeto |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **`train.csv`** | `data/raw/train.csv` | CSV | UTF-8 | Vírgula (`,`) | 8.693 | 14 | 805.421 bytes (~787 KB) | Base principal de análise exploratória, inferência estatística, testes de hipóteses e treino supervisionado (contém o alvo `Transported`). |
| **`test.csv`** | `data/raw/test.csv` | CSV | UTF-8 | Vírgula (`,`) | 4.277 | 13 | 372.487 bytes (~364 KB) | Base de avaliação sem rótulo (`Transported` omitido), utilizada para avaliação final de generalização na competição Kaggle. |
| **`sample_submission.csv`** | `data/raw/sample_submission.csv` | CSV | UTF-8 | Vírgula (`,`) | 4.277 | 2 | 59.902 bytes (~59 KB) | Arquivo modelo de submissão contendo `PassengerId` e predição padrão para `Transported`. |

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

---

## 4. Resumo por Grupo Tipológico (`train.csv`)

| Tipologia Estatística | Quantidade de Colunas | Colunas Associadas | Escala de Medida |
| :--- | :---: | :--- | :---: |
| **Categórica Nominal** | 5 | `HomePlanet`, `Destination`, `CryoSleep`, `VIP`, `Transported` | Nominal |
| **Categórica Estruturada** | 3 | `PassengerId`, `Cabin`, `Name` | Nominal (Composta) |
| **Quantitativa Discreta** | 1 | `Age` | Razão (Inteiros de 0 a 79) |
| **Quantitativa Contínua** | 5 | `RoomService`, `FoodCourt`, `ShoppingMall`, `Spa`, `VRDeck` | Razão ($\ge 0,0$) |
| **Total** | **14** | **Todas as 14 colunas originais mapeadas** | — |
