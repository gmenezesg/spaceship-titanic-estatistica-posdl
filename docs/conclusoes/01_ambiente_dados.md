# 01 — Conclusões da Preparação, Saneamento e Engenharia de Atributos (`KAN-13`)

- **Ticket Principal (Jira):** [KAN-13 — Publicar conclusões de preparação em Markdown](https://megamatic.atlassian.net/browse/KAN-13)
- **Tickets Consolidados da Trilha 0 (Preparação de Dados):**
  - [KAN-10 — Criar inventário e dicionário de dados](https://megamatic.atlassian.net/browse/KAN-10)
  - [KAN-11 — Analisar valores ausentes e duplicados](https://megamatic.atlassian.net/browse/KAN-11)
  - [KAN-12 — Criar variáveis derivadas do Spaceship Titanic](https://megamatic.atlassian.net/browse/KAN-12)
- **Fonte Oficial dos Dados:** [Kaggle — Spaceship Titanic Competition](https://www.kaggle.com/competitions/spaceship-titanic)
- **Notebook Base da Trilha:** [`notebooks/01_preparacao_dados.ipynb`](../../notebooks/01_preparacao_dados.ipynb)
- **Notebook Mestre Consolidado:** [`notebooks/00_projeto_final_estatistica.ipynb`](../../notebooks/00_projeto_final_estatistica.ipynb)
- **Artefatos Complementares:** [`docs/inventario_dados.md`](../inventario_dados.md) · [`docs/dicionario_dados.md`](../dicionario_dados.md) · `data/processed/spaceship_titanic_clean.csv` · `data/processed/spaceship_titanic_test_clean.csv`
- **Responsável Principal:** Gustavo
- **Revisor Dedicado:** Helton

---

## 1. Visão Geral do Dataset e Qualidade dos Dados (`KAN-10`)

### 1.1. Contexto do Problema e do Cliente
No ano de **2912**, o transatlântico intergaláctico *Spaceship Titanic* partiu em sua viagem inaugural com quase 13.000 emigrantes a bordo, partindo de três planetas de origem no Sistema Solar (`Earth`, `Europa` e `Mars`) rumo a três exoplanetas recém-habitáveis (`TRAPPIST-1e`, `55 Cancri e` e `PSO J318.5-22`). Ao contornar *Alpha Centauri*, a espaçonave colidiu com uma anomalia espaço-temporal oculta em uma nuvem de poeira cósmica. Embora a estrutura física da nave tenha permanecido intacta, **quase metade dos passageiros foi teletransportada para uma dimensão alternativa (`Transported = True`)**.

- **Quem é o "cliente" (Tomador de Decisão):** O Comando de Operações Espaciais e a Equipe de Resgate e Segurança de Navegação da *Spaceship Titanic*, que necessitam recuperar os registros danificados do computador de bordo, compreender quais perfis demográficos, espaciais (alojamento por convés/lado) e comportamentais (criossono e gastos em comodidades) estiveram mais expostos ao teletransporte e prever com precisão quais passageiros da partição não rotulada sofreram o evento.
- **Objetivo Analítico e Preditivo:** Entregar uma base de dados **100% íntegra, auditável e livre de vazamento de informação (*zero data leakage*)**, sustentando as trilhas subsequentes de **Análise Descritiva e Visual (`KAN-14` a `KAN-18`)**, **Probabilidade e Distribuições (`KAN-19` a `KAN-23`)**, **Testes de Hipóteses e ANOVA (`KAN-24` a `KAN-29`)** e **Correlação e Regressões (`KAN-30` a `KAN-35`)**.

### 1.2. Catálogo e Volumetria dos Ativos Brutos (`data/raw/`) e Processados (`data/processed/`)

Os ativos originais foram preservados de maneira imutável em `data/raw/`, enquanto os ativos saneados e enriquecidos foram persistidos em `data/processed/`:

| Ativo de Dados | Caminho Relativo | Registros ($n$) | Colunas ($p$) | Células Totais ($n \times p$) | Células Ausentes (`NaN`) | Linhas com $\ge 1$ `NaN` | Linhas Duplicadas | Papel no Projeto |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **`train.csv`** | `data/raw/train.csv` | 8.693 | 14 | 121.702 | 2.324 (1,91%) | 2.087 (24,01%) | 0 (0,00%) | Base bruta principal de análise estatística, testes inferenciais e treino supervisionado (contém o alvo `Transported`). |
| **`test.csv`** | `data/raw/test.csv` | 4.277 | 13 | 55.601 | 1.117 (2,01%) | 996 (23,29%) | 0 (0,00%) | Base bruta de avaliação sem o rótulo `Transported`. |
| **`sample_submission.csv`** | `data/raw/sample_submission.csv` | 4.277 | 2 | 8.554 | 0 (0,00%) | 0 (0,00%) | 0 (0,00%) | Template oficial de submissão (`PassengerId`, `Transported`). |
| **`spaceship_titanic_clean.csv`** | `data/processed/spaceship_titanic_clean.csv` | 8.693 | 22 | 191.246 | **0 (0,00%)** | **0 (0,00%)** | 0 (0,00%) | **Base oficial tratada e enriquecida** (14 originais + 8 derivadas) consumida pelas Seções 2 a 5 do projeto. |
| **`spaceship_titanic_test_clean.csv`** | `data/processed/spaceship_titanic_test_clean.csv` | 4.277 | 21 | 89.817 | **0 (0,00%)** | **0 (0,00%)** | 0 (0,00%) | Base de teste tratada sem vazamento de dados e enriquecida com as mesmas 8 variáveis derivadas. |

### 1.3. Estrutura e Tipologia Estatística das Variáveis (`KAN-10` e `KAN-12`)

A classificação tipológica padronizada em [`docs/dicionario_dados.md`](../dicionario_dados.md) e [`docs/inventario_dados.md`](../inventario_dados.md) organiza as **22 variáveis** da base limpa em quatro grupos estatísticos fundamentais:

| Grupo Tipológico | Qtd. Originais (`KAN-10`) | Qtd. Derivadas (`KAN-12`) | Total | Variáveis Contempladas | Escala de Medida | Diretriz Metodológica para as Próximas Trilhas |
| :--- | :---: | :---: | :---: | :--- | :---: | :--- |
| **Categóricas Nominais / Ordinais** | 5 | 4 | **9** | Originais: `HomePlanet`, `Destination`, `CryoSleep`, `VIP`, `Transported` (Alvo)<br>Derivadas: `IsAlone`, `CabinDeck`, `CabinSide`, `HasSpent` | Nominal / Ordinal | Analisar via tabelas de contingência, proporções binomiais/multinomiais, teste Qui-Quadrado ($\chi^2$), $V$ de Cramér e *Odds Ratio*. |
| **Categóricas Estruturadas** | 3 | 1 | **4** | Originais: `PassengerId` (`gggg_pp`), `Cabin` (`deck/num/side`), `Name` (`First Last`)<br>Derivada: `Group` (`gggg`) | Nominal (Composta / Código) | Alta cardinalidade textual; não devem sofrer *one-hot encoding* bruto, servindo de fonte para extração de atributos relacionais e espaciais. |
| **Quantitativas Discretas** | 1 | 2 | **3** | Original: `Age` ($0$ a $79$ anos)<br>Derivadas: `GroupSize` ($1$ a $8$), `CabinNum` ($0$ a $1.894$) | Razão / Intervalar | Valores inteiros contáveis; `Age` possui distribuição aproximadamente simétrica (média $28,78$, mediana $27,0$ anos após limpeza). |
| **Quantitativas Contínuas** | 5 | 1 | **6** | Originais: `RoomService`, `FoodCourt`, `ShoppingMall`, `Spa`, `VRDeck`<br>Derivada: `TotalSpend` | Razão ($\ge 0,0$) | Fortemente assimétricas à direita e inflacionadas de zeros (*zero-inflated*); exigem reporte conjunto de mediana/IIQ, média/DP e % de zeros, além de testes não-paramétricos ou robustos (Welch / Mann-Whitney / Kruskal-Wallis). |
| **Total Geral** | **14** | **8** | **22** | **14 originais preservadas + 8 derivadas validadas** | — | **100% de completude e tipagem estrita** |

### 1.4. Auditoria de Duplicidades e Integridade Amostral (`KAN-11`)

A verificação de duplicidade foi conduzida em cinco níveis de rigor no notebook [`notebooks/01_preparacao_dados.ipynb`](../../notebooks/01_preparacao_dados.ipynb) (Célula `17` / `kan11_duplicates_code`):

| Nível de Verificação de Integridade / Duplicidade | `train.csv` ($n=8.693$) | `test.csv` ($n=4.277$) | `sample_submission.csv` | Diagnóstico Técnico e Decisão |
| :--- | :---: | :---: | :---: | :--- |
| **1. Linhas completas duplicadas (`df.duplicated().sum()`)** | `0` | `0` | `0` | Nenhuma linha duplicada exata em nenhuma das bases. |
| **2. Chave primária duplicada (`PassengerId.duplicated().sum()`)** | `0` | `0` | `0` | Unicidade de 100% do identificador `PassengerId`. |
| **3. Interseção de `PassengerId` entre `train` e `test`** | `0` | `0` | — | Partições de treino e teste estritamente disjuntas (zero vazamento amostral). |
| **4. Perfis idênticos omitindo `PassengerId` e `Name`** | `15` | `3` | — | Coincidências legítimas de perfil (familiares na mesma cabine em `CryoSleep == True`, com gastos zero e mesma idade). **Mantidos.** |
| **5. Homônimos (`Name` repetido com `PassengerId` distinto)** | `20` | `7` | — | Passageiros distintos (grupos, cabines e idades diferentes) que compartilham nome e sobrenome por coincidência onomástica natural. **Mantidos.** |

### 1.5. Limitações Estruturais do Dataset e Cuidados Analíticos
1. **Inflação de Zeros (*Zero-Inflation*) e Assimetria Extrema nas Despesas:** Entre $62,3\%$ e $65,8\%$ dos passageiros registram gasto igual a `0,0` em cada serviço individual, e $41,92\%$ têm gasto total nulo (`TotalSpend == 0,0`), em grande parte devido ao confinamento físico do criossono (`CryoSleep == True`) e à restrição etária infantil (`Age <= 12`).
2. **Categorias Raras em `CabinDeck` e `VIP`:** O convés `CabinDeck == 'T'` possui apenas $n = 5$ passageiros ($0,06\%$) no treino, violando a frequência esperada mínima ($E_{ij} \ge 5$) em testes Qui-Quadrado se não for agrupado ou tratado. De forma similar, `VIP == True` representa apenas $2,29\%$ da base ($n = 199$).
3. **Confundimento Estrutural entre Origem (`HomePlanet`) e Convés (`CabinDeck`):** Os conveses `A`, `B`, `C` e `T` abrigam exclusivamente passageiros de `Europa`, enquanto o convés `G` abriga exclusivamente passageiros de `Earth`. Análises bivariadas isoladas não separam o efeito de `HomePlanet` do efeito de `CabinDeck`, exigindo controle multivariado na etapa de regressão logística (`KAN-33`/`KAN-34`).

---

## 2. Decisões de Tratamento de Valores Ausentes (`KAN-11`)

### 2.1. Diagnóstico da Volumetria de Ausência: Por que Não Usar Exclusão *Listwise* (`dropna()`)

Embora a fração global de células ausentes seja baixa (**$1,91\%$ em `train.csv`**, com $2.324$ `NaN`s em $121.702$ células, e **$2,01\%$ em `test.csv`**, com $1.117$ `NaN`s em $55.601$ células), a ausência distribui-se de forma pulverizada entre 12 das 14 colunas preditoras (apenas `PassengerId` e `Transported` possuem $0\%$ de ausência):

| Qtd. de Colunas Ausentes no Mesmo Passageiro | Passageiros em `train.csv` ($n=8.693$) | % em `train.csv` | Passageiros em `test.csv` ($n=4.277$) | % em `test.csv` |
| :---: | :---: | :---: | :---: | :---: |
| **0 colunas ausentes (Registro Completo)** | 6.606 | 75,99% | 3.281 | 76,71% |
| **1 coluna ausente** | 1.867 | 21,48% | 879 | 20,55% |
| **2 colunas ausentes** | 203 | 2,34% | 113 | 2,64% |
| **3 colunas ausentes** | 17 | 0,20% | 4 | 0,09% |
| **Subtotal com $\ge 1$ valor ausente** | **2.087** | **24,01%** | **996** | **23,29%** |

> **Conclusão Metodológica para o Cliente:** Descartar linhas incompletas (*listwise deletion* / `dropna()`) eliminaria **24,01% da base de treinamento ($2.087$ passageiros)**, reduzindo severamente o poder estatístico dos testes de hipóteses, além de impedir a geração de predições para **$996$ passageiros ($23,29\%$)** da base de teste. Portanto, a **imputação estruturada** é mandatória.

### 2.2. Diagnóstico do Mecanismo de Ausência: MCAR na Falha de Registro + MAR Estrutural no Valor Subjacente

À luz da taxonomia de Rubin (1976), investigamos formalmente se o mecanismo gerador de dados ausentes é **MCAR (*Missing Completely at Random*)**, **MAR (*Missing at Random*)** ou **MNAR (*Missing Not at Random*)**:

1. **O Evento de Falha de Registro é Compatível com MCAR (Teste $\chi^2$ contra `Transported`):**
   Testamos a independência estatística entre o indicador binário de ausência (`df[col].isna()`) de cada uma das 12 variáveis incompletas e o desfecho `Transported` (Célula `21` / `kan11_mechanism_code`). Em **100% das variáveis**, o $p$-valor superou com folga o nível de significância $\alpha = 0,05$ (variando de $p = 0,2196$ a $p = 1,0000$), confirmando que a corrupção dos registros no computador de bordo ocorreu de modo aleatório e não seletivo em relação ao teletransporte:

| Variável (Indicador `isna`) | Ausentes em `train` ($n$) | % `Transported` (quando Ausente) | % `Transported` (quando Observado) | Estatística $\chi^2$ (vs. `Transported`) | $p$-valor | Diagnóstico ($\alpha = 0,05$) |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **`HomePlanet`** | 201 | 51,24% | 50,34% | 0,0329 | 0,8560 | Independente de `Transported` (Compatível com MCAR) |
| **`CryoSleep`** | 217 | 48,85% | 50,40% | 0,1468 | 0,7016 | Independente de `Transported` (Compatível com MCAR) |
| **`Cabin`** | 199 | 50,25% | 50,36% | 0,0000 | 1,0000 | Independente de `Transported` (Compatível com MCAR) |
| **`Destination`** | 182 | 50,55% | 50,36% | 0,0000 | 1,0000 | Independente de `Transported` (Compatível com MCAR) |
| **`Age`** | 179 | 50,28% | 50,36% | 0,0000 | 1,0000 | Independente de `Transported` (Compatível com MCAR) |
| **`VIP`** | 203 | 51,23% | 50,34% | 0,0323 | 0,8575 | Independente de `Transported` (Compatível com MCAR) |
| **`RoomService`** | 181 | 45,86% | 50,46% | 1,3229 | 0,2501 | Independente de `Transported` (Compatível com MCAR) |
| **`FoodCourt`** | 183 | 54,10% | 50,28% | 0,8966 | 0,3437 | Independente de `Transported` (Compatível com MCAR) |
| **`ShoppingMall`** | 208 | 54,81% | 50,25% | 1,5072 | 0,2196 | Independente de `Transported` (Compatível com MCAR) |
| **`Spa`** | 183 | 49,73% | 50,38% | 0,0098 | 0,9211 | Independente de `Transported` (Compatível com MCAR) |
| **`VRDeck`** | 188 | 52,13% | 50,32% | 0,1728 | 0,6776 | Independente de `Transported` (Compatível com MCAR) |
| **`Name`** | 200 | 50,50% | 50,36% | 0,0000 | 1,0000 | Independente de `Transported` (Compatível com MCAR) |

2. **O Valor Subjacente Segue Estrutura MAR / Determinística Condicional às Variáveis Observadas:**
   Embora a perda do dado seja aleatória, o **valor real oculto sob o `NaN`** é fortemente determinado por restrições físicas e relacionais de outras colunas observadas no mesmo passageiro ou em seu grupo de viagem (**0% de violações em toda a base observada**):

| Regra Estrutural / Restrição Física de Domínio | Registros Válidos Verificados (`train`) | Violações Observadas | Células `NaN` Recuperáveis Exatamente (`train`) | Células `NaN` Recuperáveis Exatamente (`test`) |
| :--- | :---: | :---: | :---: | :---: |
| **`CryoSleep == True` $\rightarrow$ Todas as 5 Despesas $= 0,0$** | 3.037 | **0 (0,00%)** | 361 | 170 |
| **Soma das Despesas $> 0$ $\rightarrow$ `CryoSleep == False`** | 5.040 | **0 (0,00%)** | 119 | 55 |
| **`Age <= 12` (Crianças) $\rightarrow$ Todas as 5 Despesas $= 0,0$ e `VIP == False`** | 806 | **0 (0,00%)** | 114 | 45 |
| **`HomePlanet == 'Earth'` $\rightarrow$ `VIP == False` (Terráqueos nunca são VIP)** | 4.487 | **0 (0,00%)** | 115 | 44 |
| **Homogeneidade Relacional (`Group` / `CabinDeck` / `LastName` $\rightarrow$ `HomePlanet` e `Cabin`)** | 6.217 grupos | **0 (0,00%)** | 293 | 119 |

### 2.3. Pipeline Hierárquico de Imputação em 10 Etapas (Sem *Data Leakage*)

Com base nesse diagnóstico, implementamos na função `executar_pipeline_imputacao()` (Célula `23` / `kan11_imputation_code`) uma arquitetura em **duas camadas sequenciais** — onde todos os parâmetros estatísticos (modas, medianas agrupadas e mapeamentos de sobrenome) são **estimados exclusivamente em `train.csv`** e aplicados em `train` e `test`:

- **Camada 1 (Etapas 1 a 4 — Regras de Negócio Determinísticas e Inferência Relacional):** Recupera exatamente **`842` das `2.324` células ausentes do treino ($36,23\%$)** e **`370` das `1.117` células ausentes do teste ($33,12\%$)** sem recorrer a aproximações estatísticas.
- **Camada 2 (Etapas 5 a 10 — Imputação Estatística Condicional por Mediana Agrupada e Moda):** Preenche os casos remanescentes respeitando a assimetria das variáveis contínuas (mediana de despesas agrupada por `HomePlanet`, `CryoSleep` e `VIP`), a natureza discreta da idade (mediana de `Age` agrupada por `HomePlanet` e `VIP`) e a distribuição modal condicional das categóricas.

| Etapa / Regra do Pipeline de Imputação (`KAN-11`) | Tipo de Tratamento | Células Imputadas (`train`) | `NaN`s Restantes (`train`) | Células Imputadas (`test`) | `NaN`s Restantes (`test`) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **1.** `CryoSleep == True` $\rightarrow$ Despesas ausentes $= 0,0$ | Regra de Negócio Determinística | 361 | 1.963 | 170 | 947 |
| **2.** `Age <= 12` $\rightarrow$ Despesas ausentes $= 0,0$ e `VIP = False` | Regra de Negócio Determinística | 69 | 1.894 | 26 | 921 |
| **3.** Soma de Despesas $> 0$ $\rightarrow$ `CryoSleep = False` | Regra de Negócio Determinística | 119 | 1.775 | 55 | 866 |
| **4.** Inferência Relacional (`Cabin` por Grupo; `HomePlanet` por Grupo/Deck/Sobrenome) | Inferência Estrutural / Relacional | 293 | 1.482 | 119 | 747 |
| **5.** Imputação de `HomePlanet` (`'Earth'`) e `Destination` (`'TRAPPIST-1e'`) pela Moda | Moda (Categóricas Nominais) | 190 | 1.292 | 97 | 650 |
| **6.** `VIP` ausente $\rightarrow$ `False` em `Earth` + Moda Global (`False`) | Regra de Negócio + Moda | 179 | 1.113 | 89 | 561 |
| **7.** Imputação de `Age` por Mediana Agrupada (`HomePlanet`, `VIP`) + Regra Infantil | Mediana Agrupada (Quantitativa Discreta) | 179 | 934 | 91 | 470 |
| **8.** Imputação de `CryoSleep` (Moda Condicional dado Gasto $= 0$ e `HomePlanet`) + Zeros Associados | Moda Condicional + Regra de Negócio | 103 | 831 | 39 | 431 |
| **9.** Imputação de Despesas Remanescentes por Mediana Agrupada (`HomePlanet`, `CryoSleep`, `VIP`) | Mediana Agrupada (Quantitativas Contínuas) | 532 | 299 | 274 | 157 |
| **10.** Imputação Estruturada de `Cabin` (Moda por `HomePlanet`) e `Name` (`Unknown` + Sobrenome do Grupo) | Moda Condicional / Inferência de Grupo | 299 | **0** | 157 | **0** |
| **Total Consolidado** | **Pipeline Completo (10 Etapas)** | **2.324 (100%)** | **0 (0,00%)** | **1.117 (100%)** | **0 (0,00%)** |

### 2.4. Tabelas Comparativas de Estatísticas Antes vs. Depois da Imputação (`KAN-11`)

#### 2.4.1. Completude e Tipagem por Variável Antes vs. Depois (`train.csv` e `test.csv`)

| # | Variável | `Dtype` Antes | `Dtype` Depois | Ausentes Antes (`train`) | % Antes (`train`) | Ausentes Depois (`train`) | % Depois (`train`) | Ausentes Antes (`test`) | % Antes (`test`) | Ausentes Depois (`test`) | % Depois (`test`) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 01 | **`PassengerId`** | `str` / `object` | `str` / `object` | 0 | 0,00% | **0** | **0,00%** | 0 | 0,00% | **0** | **0,00%** |
| 02 | **`HomePlanet`** | `str` / `object` | `str` / `object` | 201 | 2,31% | **0** | **0,00%** | 87 | 2,03% | **0** | **0,00%** |
| 03 | **`CryoSleep`** | `object` (`bool` c/ `NaN`) | `bool` | 217 | 2,50% | **0** | **0,00%** | 93 | 2,17% | **0** | **0,00%** |
| 04 | **`Cabin`** | `str` / `object` | `str` / `object` | 199 | 2,29% | **0** | **0,00%** | 100 | 2,34% | **0** | **0,00%** |
| 05 | **`Destination`** | `str` / `object` | `str` / `object` | 182 | 2,09% | **0** | **0,00%** | 92 | 2,15% | **0** | **0,00%** |
| 06 | **`Age`** | `float64` | `float64` | 179 | 2,06% | **0** | **0,00%** | 91 | 2,13% | **0** | **0,00%** |
| 07 | **`VIP`** | `object` (`bool` c/ `NaN`) | `bool` | 203 | 2,34% | **0** | **0,00%** | 93 | 2,17% | **0** | **0,00%** |
| 08 | **`RoomService`** | `float64` | `float64` | 181 | 2,08% | **0** | **0,00%** | 82 | 1,92% | **0** | **0,00%** |
| 09 | **`FoodCourt`** | `float64` | `float64` | 183 | 2,11% | **0** | **0,00%** | 106 | 2,48% | **0** | **0,00%** |
| 10 | **`ShoppingMall`** | `float64` | `float64` | 208 | 2,39% | **0** | **0,00%** | 98 | 2,29% | **0** | **0,00%** |
| 11 | **`Spa`** | `float64` | `float64` | 183 | 2,11% | **0** | **0,00%** | 101 | 2,36% | **0** | **0,00%** |
| 12 | **`VRDeck`** | `float64` | `float64` | 188 | 2,16% | **0** | **0,00%** | 80 | 1,87% | **0** | **0,00%** |
| 13 | **`Name`** | `str` / `object` | `str` / `object` | 200 | 2,30% | **0** | **0,00%** | 94 | 2,20% | **0** | **0,00%** |
| 14 | **`Transported`** | `bool` | `bool` | 0 | 0,00% | **0** | **0,00%** | — | — | — | — |
| — | **Total Geral** | — | — | **2.324** | **1,91%** | **0** | **0,00%** | **1.117** | **2,01%** | **0** | **0,00%** |

#### 2.4.2. Preservação de Parâmetros das Variáveis Quantitativas Antes vs. Depois (`train.csv`)

A imputação preservou integralmente a tendência central (medianas inalteradas em **100% das variáveis quantitativas**), a dispersão e a proporção de zeros:

| Variável Quantitativa | $N$ Válidos Antes | $N$ Válidos Depois | Média Antes | Média Depois | DP Antes | DP Depois | Mediana Antes | Mediana Depois | IIQ Antes | IIQ Depois | % Zeros Antes | % Zeros Depois |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`Age`** | 8.514 | 8.693 | 28,83 | 28,78 | 14,49 | 14,35 | **27,00** | **27,00** | 19,00 | 17,00 | 2,09% | 2,05% |
| **`RoomService`** | 8.512 | 8.693 | 224,69 | 221,58 | 666,72 | 660,80 | **0,00** | **0,00** | 47,00 | 43,00 | 65,52% | 65,24% |
| **`FoodCourt`** | 8.510 | 8.693 | 458,08 | 451,40 | 1.611,49 | 1.596,28 | **0,00** | **0,00** | 76,00 | 67,00 | 64,11% | 63,83% |
| **`ShoppingMall`** | 8.485 | 8.693 | 173,73 | 169,95 | 604,70 | 597,95 | **0,00** | **0,00** | 27,00 | 23,00 | 65,85% | 65,80% |
| **`Spa`** | 8.510 | 8.693 | 311,14 | 305,45 | 1.136,71 | 1.125,46 | **0,00** | **0,00** | 59,00 | 56,00 | 62,56% | 62,26% |
| **`VRDeck`** | 8.505 | 8.693 | 304,85 | 299,09 | 1.145,72 | 1.134,08 | **0,00** | **0,00** | 46,00 | 41,00 | 64,61% | 64,40% |

#### 2.4.3. Preservação de Proporções das Variáveis Categóricas Nominais Antes vs. Depois (`train.csv`)

As frequências relativas de todas as categorias sofreram variação absoluta máxima de apenas **$0,64$ ponto percentual** (`Destination == 'TRAPPIST-1e'`), e inferior a **$0,25$ p.p.** em `HomePlanet`, `CryoSleep` e `VIP`, comprovando ausência de distorção:

| Variável Categórica | Categoria | Contagem Antes (Válidos) | % Válidos Antes | Contagem Depois (Limpo) | % Depois (Limpo) | Variação Absoluta (p.p.) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **`HomePlanet`** | `Earth` | 4.602 | 54,19% | 4.715 | 54,24% | $+0,05$ p.p. |
| **`HomePlanet`** | `Europa` | 2.131 | 25,09% | 2.174 | 25,01% | $-0,09$ p.p. |
| **`HomePlanet`** | `Mars` | 1.759 | 20,71% | 1.804 | 20,75% | $+0,04$ p.p. |
| **`Destination`** | `TRAPPIST-1e` | 5.915 | 69,50% | 6.097 | 70,14% | $+0,64$ p.p. |
| **`Destination`** | `55 Cancri e` | 1.800 | 21,15% | 1.800 | 20,71% | $-0,44$ p.p. |
| **`Destination`** | `PSO J318.5-22` | 796 | 9,35% | 796 | 9,16% | $-0,20$ p.p. |
| **`CryoSleep`** | `False` | 5.439 | 64,17% | 5.558 | 63,94% | $-0,23$ p.p. |
| **`CryoSleep`** | `True` | 3.037 | 35,83% | 3.135 | 36,06% | $+0,23$ p.p. |
| **`VIP`** | `False` | 8.291 | 97,66% | 8.494 | 97,71% | $+0,05$ p.p. |
| **`VIP`** | `True` | 199 | 2,34% | 199 | 2,29% | $-0,05$ p.p. |
| **`Transported`** | `True` | 4.378 | 50,36% | 4.378 | 50,36% | $0,00$ p.p. |
| **`Transported`** | `False` | 4.315 | 49,64% | 4.315 | 49,64% | $0,00$ p.p. |

---

## 3. Engenharia de Atributos Criados e *Rationale* (`KAN-12`)

### 3.1. Fundamentação de Negócio e Estatística (*Rationale*)

Sobre as bases imputadas (`df_train_clean` e `df_test_clean`), a função `criar_variaveis_derivadas()` (Célula `28` / `kan12_engineering_code`) construiu **8 variáveis derivadas** organizadas em três dimensões analíticas de alto valor explicativo para o problema do cliente:

1. **Dimensão Social e de Grupo Familiar (`PassengerId` $\rightarrow$ `Group`, `GroupSize`, `IsAlone`):**
   - *Rationale:* O código `PassengerId` (`gggg_pp`) em sua forma textual bruta tem cardinalidade igual ao tamanho da amostra ($n = 8.693$) e não pode ser utilizado diretamente em modelos ou testes. A extração do prefixo `Group` (`gggg`), a contagem de integrantes `GroupSize` ($1$ a $8$) e o indicador binário de viagem solo `IsAlone` (`GroupSize == 1`) capturam o comportamento coletivo de embarque e alojamento familiar.
2. **Dimensão Espacial e de Acomodação (`Cabin` $\rightarrow$ `CabinDeck`, `CabinNum`, `CabinSide`):**
   - *Rationale:* O identificador composto `Cabin` (`deck/num/side`) possui $6.560$ valores distintos no treino, ocultando a geometria tridimensional do navio. Sua decomposição separa a posição vertical/socioeconômica por convés (`CabinDeck` de `A` a `G` e `T`), a posição longitudinal ao longo do corredor (`CabinNum` de `0` a `1.894`) e o lado transversal da embarcação (`CabinSide`: `P` = *Port* / Bombordo vs. `S` = *Starboard* / Boreste), variáveis cruciais para mapear a zona de impacto da anomalia espaço-temporal.
3. **Dimensão de Consumo Global a Bordo (`RoomService..VRDeck` $\rightarrow$ `TotalSpend`, `HasSpent`):**
   - *Rationale:* As cinco rubricas individuais de gasto são altamente colineares em torno do zero e fragmentam o poder aquisitivo do passageiro. A soma algébrica `TotalSpend` sintetiza o volume financeiro total movimentado pelo indivíduo ($0,0$ a $35.987,0$), enquanto a flag binária `HasSpent` (`TotalSpend > 0`) separa o regime estrutural de abstenção ($41,92\%$ da base) do regime de consumo ativo ($58,08\%$), viabilizando análises condicionais (Leitura A vs. Leitura B na `KAN-15` e testes em `KAN-26`/`KAN-27`).

### 3.2. Especificação Técnica e Resumo Estatístico das 8 Variáveis Derivadas (`KAN-12`)

| # | Variável Derivada | Variável de Origem | Regra de Construção | `Dtype` | Tipologia Estatística | Escala | Ausentes (`train`/`test`) | Resumo Estatístico / Distribuição em `spaceship_titanic_clean.csv` ($n=8.693$) |
| :---: | :--- | :--- | :--- | :---: | :--- | :---: | :---: | :--- |
| 15 | **`Group`** | `PassengerId` (`gggg_pp`) | `PassengerId.str.split('_').str[0]` | `str` / `object` | Categórica Estruturada | Nominal | `0 / 0` | $6.217$ grupos distintos no treino (`'0001'` a `'9280'`) e $3.063$ no teste (interseção nula). |
| 16 | **`GroupSize`** | `Group` | `groupby('Group')['Group'].transform('count')` | `int64` | Quantitativa Discreta | Razão | `0 / 0` | Inteiros em $[1, 8]$ · Média: `2,04` · DP: `1,60` · $Q_1$: `1,0` · Mediana: `1,0` · $Q_3$: `3,0` · $P_{95}$: `6,0`. |
| 17 | **`IsAlone`** | `GroupSize` | `GroupSize == 1` | `bool` | Categórica Nominal (Binária) | Nominal | `0 / 0` | `True` (Viaja sozinho): $4.805$ ($55,27\%$) · `False` (Em grupo $\ge 2$): $3.888$ ($44,73\%$). |
| 18 | **`CabinDeck`** | `Cabin` (`deck/num/side`) | `Cabin.str.split('/').str[0]` | `str` / `object` | Categórica Nominal / Ordinal | Nominal / Ordinal | `0 / 0` | 8 conveses: `F` ($32,99\%$), `G` ($29,77\%$), `E` ($10,18\%$), `B` ($9,40\%$), `C` ($8,75\%$), `D` ($5,83\%$), `A` ($3,01\%$), `T` ($0,06\%$). |
| 19 | **`CabinNum`** | `Cabin` (`deck/num/side`) | `Cabin.str.split('/').str[1].astype(int64)` | `int64` | Quantitativa Discreta | Intervalar / Posicional | `0 / 0` | Inteiros em $[0, 1.894]$ · Média: `600,20` · DP: `512,29` · $Q_1$: `166,0` · Mediana: `426,0` · $Q_3$: `1.006,0` · $P_{95}$: `1.561,0`. |
| 20 | **`CabinSide`** | `Cabin` (`deck/num/side`) | `Cabin.str.split('/').str[2]` | `str` / `object` | Categórica Nominal (Binária) | Nominal | `0 / 0` | `S` (*Starboard* / Boreste): $4.384$ ($50,43\%$) · `P` (*Port* / Bombordo): $4.309$ ($49,57\%$). |
| 21 | **`TotalSpend`** | 5 Despesas de Bordo | `RoomService + FoodCourt + ShoppingMall + Spa + VRDeck` | `float64` | Quantitativa Contínua | Razão | `0 / 0` | Reais em $[0,0;\; 35.987,0]$ · Zeros: $3.644$ ($41,92\%$) · Média: `1.447,46` · DP: `2.808,28` · Mediana: `717,0` · $Q_3$: `1.444,0` · $P_{95}$: `6.486,0`. |
| 22 | **`HasSpent`** | `TotalSpend` | `TotalSpend > 0.0` | `bool` | Categórica Nominal (Binária) | Nominal | `0 / 0` | `True` (Gastou $> 0$): $5.049$ ($58,08\%$) · `False` (Gasto Zero): $3.644$ ($41,92\%$). |

### 3.3. Evidência Empírica do Poder Explicativo das Variáveis Derivadas vs. `Transported`

A inspeção preliminar na Célula `32` (`kan12_stats_code`) comprova que todas as variáveis categóricas derivadas exibem forte associação estatística com o alvo `Transported` ($p < 10^{-21}$):

| Variável Derivada | Categoria / Estrato | Passageiros ($n$) | % da Base (`train`) | Transportados ($n$) | Taxa de Transporte (%) | $\chi^2$ Global (vs. `Transported`) | $p$-valor | Interpretação Prática para o Cliente |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **`HasSpent`** | `False` (`TotalSpend == 0`) | 3.644 | 41,92% | 2.869 | **78,73%** | **2.017,98** | $< 10^{-300}$ | Passageiros sem gastos a bordo tiveram risco de teletransporte **2,63 vezes maior** que consumidores ativos. |
| **`HasSpent`** | `True` (`TotalSpend > 0`) | 5.049 | 58,08% | 1.509 | **29,89%** | 2.017,98 | $< 10^{-300}$ | Forte efeito protetor aparente associado a estar acordado (`CryoSleep == False`) e consumindo. |
| **`CabinDeck`** | `B` / `C` (Superiores Europa) | 817 / 761 | 9,40% / 8,75% | 596 / 518 | **72,95% / 68,07%** | **396,96** | $1,07 \times 10^{-81}$ | Conveses `B` e `C` concentram as maiores taxas de teletransporte da espaçonave. |
| **`CabinDeck`** | `E` / `D` / `F` | 885 / 507 / 2.868 | 10,18% / 5,83% / 32,99% | 319 / 220 / 1.257 | **36,05% / 43,39% / 43,83%** | 396,96 | $1,07 \times 10^{-81}$ | Conveses intermediários/inferiores `E`, `D` e `F` apresentam taxas abaixo da média global ($50,36\%$). |
| **`CabinDeck`** | `G` / `A` / `T` | 2.588 / 262 / 5 | 29,77% / 3,01% / 0,06% | 1.335 / 132 / 1 | **51,58% / 50,38% / 20,00%** | 396,96 | $1,07 \times 10^{-81}$ | Decks `G` e `A` próximos da média; deck `T` ($n=5$) possui amostra insuficiente para inferência isolada. |
| **`IsAlone`** | `False` (Em Grupo $\ge 2$) | 3.888 | 44,73% | 2.204 | **56,69%** | **112,10** | $3,39 \times 10^{-26}$ | Passageiros acompanhados foram significativamente mais teletransportados ($+11,45$ p.p.) que viajantes solo. |
| **`IsAlone`** | `True` (Viaja Sozinho) | 4.805 | 55,27% | 2.174 | **45,24%** | 112,10 | $3,39 \times 10^{-26}$ | Viajantes individuais apresentam maior proporção de adultos acordados em conveses `E`/`F`. |
| **`CabinSide`** | `S` (*Starboard* / Boreste) | 4.384 | 50,43% | 2.435 | **55,54%** | **94,53** | $2,41 \times 10^{-22}$ | O lado Boreste (`S`) sofreu $+10,45$ p.p. a mais de teletransporte que o lado Bombordo (`P`). |
| **`CabinSide`** | `P` (*Port* / Bombordo) | 4.309 | 49,57% | 1.943 | **45,09%** | 94,53 | $2,41 \times 10^{-22}$ | Evidencia assimetria transversal na propagação física da anomalia espaço-temporal. |

### 3.4. Auditoria de Integridade e Garantia de *Zero Data Leakage* (`KAN-12`)

A bateria de validação automatizada na Célula `30` (`kan12_validation_code`) confirmou o cumprimento integral dos 9 critérios de aceitação:

| # | Regra de Validação / Critério de Aceitação (`KAN-12`) | Resultado em `train` ($n=8.693$) | Resultado em `test` ($n=4.277$) | Status |
| :---: | :--- | :---: | :---: | :---: |
| **1** | Preservação integral das colunas originais ($14$ no treino, $13$ no teste) | `True` (`22` colunas totais) | `True` (`21` colunas totais) | **OK (100%)** |
| **2** | Ausência total de valores nulos (`NaN`) em todas as colunas | `0 NaNs` | `0 NaNs` | **OK (100%)** |
| **3** | Disjunção de `Group` entre `train` e `test` (*Zero Data Leakage* em `GroupSize`) | `6.217` grupos exclusivos | `3.063` grupos exclusivos (`Interseção = 0`) | **OK (Sem Vazamento)** |
| **4** | Coerência estrutural: `GroupSize == maior índice sequencial (pp)` do grupo | `8.693 / 8.693` (`100,0%`) | `4.277 / 4.277` (`100,0%`) | **OK (100%)** |
| **5** | Consistência lógica: `IsAlone == (GroupSize == 1)` | `8.693 / 8.693` (`100,0%`) | `4.277 / 4.277` (`100,0%`) | **OK (100%)** |
| **6** | Reconstrução bijetora: `CabinDeck + '/' + CabinNum + '/' + CabinSide == Cabin` | `8.693 / 8.693` (`100,0%`) | `4.277 / 4.277` (`100,0%`) | **OK (100%)** |
| **7** | Domínio válido de `CabinDeck` $\in \{A..G, T\}$ e `CabinSide` $\in \{P, S\}$ | `Decks=['A'..'G','T']`; `Sides=['P','S']` | `Decks=['A'..'G','T']`; `Sides=['P','S']` | **OK (100%)** |
| **8** | Exatidão algébrica de `TotalSpend` e equivalência `HasSpent == (TotalSpend > 0)` | `Erro máx = 0.0e+00` | `Erro máx = 0.0e+00` | **OK (100%)** |
| **9** | Coerência física: Passageiros em `CryoSleep == True` possuem `HasSpent == False` | `0 violações` | `0 violações` | **OK (0 Violações)** |

---

## 4. Links e Referências Diretas para as Células do Notebook `01_preparacao_dados.ipynb`

A tabela abaixo fornece o mapeamento completo e auditável de todas as **36 células (`Célula 00` a `Célula 35`)** do notebook base [`notebooks/01_preparacao_dados.ipynb`](../../notebooks/01_preparacao_dados.ipynb) (que compõem a **Seção 1** do notebook consolidado [`notebooks/00_projeto_final_estatistica.ipynb`](../../notebooks/00_projeto_final_estatistica.ipynb)), permitindo navegação direta para o código-fonte, tabelas geradas e documentação associada:

| Índice da Célula | ID da Célula (`.ipynb`) | Tipo | Ticket Jira | Seção / Referência Direta no Notebook `01_preparacao_dados.ipynb` | Descrição Técnica da Célula e Artefatos Associados |
| :---: | :--- | :---: | :---: | :--- | :--- |
| **Célula 00** | `05d0645e` | `markdown` | `KAN-10` | [1. Preparação de Dados: Inventário e Dicionário de Dados (`KAN-10`)](../../notebooks/01_preparacao_dados.ipynb#1.-Preparação-de-Dados:-Inventário-e-Dicionário-de-Dados-(KAN-10)) | Cabeçalho geral da Trilha 0, especificação oficial dos campos da competição Kaggle e introdução da Seção 1 (`KAN-10`). |
| **Célula 01** | `d5b50f69` | `code` | `KAN-10` | [1. Preparação de Dados: Setup e Leitura (`data/raw/`)](../../notebooks/01_preparacao_dados.ipynb#1.-Preparação-de-Dados:-Inventário-e-Dicionário-de-Dados-(KAN-10)) | Importação de bibliotecas (`pandas`, `numpy`, `scipy.stats`), fixação de semente (`np.random.seed(42)`) e leitura resiliente de `train.csv`, `test.csv` e `sample_submission.csv`. |
| **Célula 02** | `d89379df` | `markdown` | `KAN-10` | [2. Inventário dos Arquivos Brutos (`data/raw/`)](../../notebooks/01_preparacao_dados.ipynb#2.-Inventário-dos-Arquivos-Brutos-(data/raw/)) | Contextualização do inventário físico e estrutural dos arquivos brutos. Artefato: [`docs/inventario_dados.md`](../inventario_dados.md). |
| **Célula 03** | `71b70e49` | `code` | `KAN-10` | [2. Inventário dos Arquivos Brutos (Código)](../../notebooks/01_preparacao_dados.ipynb#2.-Inventário-dos-Arquivos-Brutos-(data/raw/)) | Construção do DataFrame `inventario_arquivos` com tamanho em bytes, registros, colunas, IDs únicos, duplicatas e células ausentes. |
| **Célula 04** | `c6ab56ac` | `markdown` | `KAN-10` | [2.1. Amostra Inicial dos Registros (`df_train.head()`)](../../notebooks/01_preparacao_dados.ipynb#2.1.-Amostra-Inicial-dos-Registros-(df_train.head())) | Introdução à inspeção visual das primeiras linhas da base de treinamento. |
| **Célula 05** | `f0c45c1f` | `code` | `KAN-10` | [2.1. Amostra Inicial dos Registros (Código)](../../notebooks/01_preparacao_dados.ipynb#2.1.-Amostra-Inicial-dos-Registros-(df_train.head())) | Execução de `display(df_train.head(10))` para verificação dos formatos brutos. |
| **Célula 06** | `faefb01c` | `markdown` | `KAN-10` | [2.2. Inventário Técnico de Completude e Cardinalidade por Coluna](../../notebooks/01_preparacao_dados.ipynb#2.2.-Inventário-Técnico-de-Completude-e-Cardinalidade-por-Coluna-(train.csv-e-test.csv)) | Explicação das métricas de não-nulos, ausentes e valores únicos por coluna em `train.csv` e `test.csv`. |
| **Célula 07** | `f160da6e` | `code` | `KAN-10` | [2.2. Inventário Técnico por Coluna (Código)](../../notebooks/01_preparacao_dados.ipynb#2.2.-Inventário-Técnico-de-Completude-e-Cardinalidade-por-Coluna-(train.csv-e-test.csv)) | Geração da tabela `df_inventario_colunas` comparando completude e cardinalidade das 14 variáveis entre treino e teste. |
| **Célula 08** | `c11a973b` | `markdown` | `KAN-10` | [3. Dicionário de Dados Formal e Tipologia Estatística (`KAN-10`)](../../notebooks/01_preparacao_dados.ipynb#3.-Dicionário-de-Dados-Formal-e-Tipologia-Estatística-(KAN-10)) | Definição da estrutura do Dicionário de Dados Formal. Artefato: [`docs/dicionario_dados.md`](../dicionario_dados.md). |
| **Célula 09** | `dcb6a195` | `code` | `KAN-10` | [3. Dicionário de Dados Formal (Código)](../../notebooks/01_preparacao_dados.ipynb#3.-Dicionário-de-Dados-Formal-e-Tipologia-Estatística-(KAN-10)) | Construção programática do DataFrame `dicionario_dados` para as 14 colunas originais com amplitudes extraídas dinamicamente de `train.csv`. |
| **Célula 10** | `835c2020` | `markdown` | `KAN-10` | [4. Inspeção Detalhada por Tipologia — 4.1. Categóricas Nominais](../../notebooks/01_preparacao_dados.ipynb#4.-Inspeção-Detalhada-por-Tipologia-Estatística) | Introdução à distribuição de frequências absolutas e relativas das 5 variáveis categóricas nominais. |
| **Célula 11** | `5e7eb3e1` | `code` | `KAN-10` | [4.1. Variáveis Categóricas Nominais (Código)](../../notebooks/01_preparacao_dados.ipynb#4.1.-Variáveis-Categóricas-Nominais-(HomePlanet,-Destination,-CryoSleep,-VIP,-Transported)) | Cálculo de `df_resumo_nominais` (`HomePlanet`, `Destination`, `CryoSleep`, `VIP`, `Transported`), incluindo contagem de `NaN`. |
| **Célula 12** | `3b6355cc` | `markdown` | `KAN-10` | [4.2. Variáveis Categóricas Estruturadas (`PassengerId`, `Cabin`, `Name`)](../../notebooks/01_preparacao_dados.ipynb#4.2.-Variáveis-Categóricas-Estruturadas-(PassengerId,-Cabin,-Name)) | Explicação dos padrões compostos `gggg_pp`, `deck/num/side` e `FirstName LastName`. |
| **Célula 13** | `d975cc65` | `code` | `KAN-10` | [4.2. Variáveis Categóricas Estruturadas (Código)](../../notebooks/01_preparacao_dados.ipynb#4.2.-Variáveis-Categóricas-Estruturadas-(PassengerId,-Cabin,-Name)) | Decomposição exploratória em `resumo_estruturadas` ($6.217$ grupos, $8$ decks, $2.217$ sobrenomes). |
| **Célula 14** | `a0c94c4c` | `markdown` | `KAN-10` | [4.3. Variáveis Quantitativas Discreta (`Age`) e Contínuas (`RoomService..VRDeck`)](../../notebooks/01_preparacao_dados.ipynb#4.3.-Variáveis-Quantitativas-Discreta-(Age)-e-Contínuas-(RoomService,-FoodCourt,-ShoppingMall,-Spa,-VRDeck)) | Introdução ao perfil posicional, quantílico e de inflação de zeros das 6 variáveis numéricas originais. |
| **Célula 15** | `318ee41b` | `code` | `KAN-10` | [4.3. Variáveis Quantitativas (Código)](../../notebooks/01_preparacao_dados.ipynb#4.3.-Variáveis-Quantitativas-Discreta-(Age)-e-Contínuas-(RoomService,-FoodCourt,-ShoppingMall,-Spa,-VRDeck)) | Geração da tabela `desc_quant` com média, DP, quantis ($25\%, 50\%, 75\%, 90\%, 95\%, 99\%$), `NaN`s e `% Zeros`. |
| **Célula 16** | `kan11_intro` | `markdown` | `KAN-11` | [5. Análise de Valores Ausentes, Duplicados e Estratégia de Imputação (`KAN-11`)](../../notebooks/01_preparacao_dados.ipynb#5.-Análise-de-Valores-Ausentes,-Duplicados-e-Estratégia-de-Imputação-(KAN-11)) | Abertura da etapa `KAN-11` e protocolo de verificação de duplicatas em 4 níveis (`5.1`). |
| **Célula 17** | `kan11_duplicates_code` | `code` | `KAN-11` | [5.1. Verificação e Auditoria de Registros Duplicados (Código)](../../notebooks/01_preparacao_dados.ipynb#5.1.-Verificação-e-Auditoria-de-Registros-Duplicados-(df.duplicated().sum())) | Geração de `df_auditoria_duplicatas` comprovando `0` duplicatas exatas, unicidade de IDs e natureza legítima das coincidências de perfil e homônimos. |
| **Célula 18** | `kan11_missing_summary_md` | `markdown` | `KAN-11` | [5.2. Contagem Absoluta e Percentual de Dados Ausentes (`missing count` e `% missing`)](../../notebooks/01_preparacao_dados.ipynb#5.2.-Contagem-Absoluta-e-Percentual-de-Dados-Ausentes-(missing-count-e-%-missing)) | Documentação da decisão sobre duplicatas e introdução ao levantamento de ausência por coluna e por linha. |
| **Célula 19** | `kan11_missing_table_code` | `code` | `KAN-11` | [5.2. Tabelas de Ausentes por Variável e por Passageiro (Código)](../../notebooks/01_preparacao_dados.ipynb#5.2.-Contagem-Absoluta-e-Percentual-de-Dados-Ausentes-(missing-count-e-%-missing)) | Cálculo de `df_tabela_ausentes` (ordenada por `missing count` no treino) e `df_dist_linhas_ausentes` ($24,01\%$ de linhas com $\ge 1$ `NaN`). |
| **Célula 20** | `kan11_mechanism_md` | `markdown` | `KAN-11` | [5.3. Avaliação do Mecanismo de Ausência (MCAR, MAR e MNAR)](../../notebooks/01_preparacao_dados.ipynb#5.3.-Avaliação-do-Mecanismo-de-Ausência-(MCAR,-MAR-e-MNAR)) | Fundamentação teórica de Rubin (1976), justificativa contra o `dropna()` e desenho dos testes empíricos de mecanismo de ausência. |
| **Célula 21** | `kan11_mechanism_code` | `code` | `KAN-11` | [5.3. Verificação `CryoSleep`, Regras de Domínio e Teste $\chi^2$ MCAR (Código)](../../notebooks/01_preparacao_dados.ipynb#5.3.-Avaliação-do-Mecanismo-de-Ausência-(MCAR,-MAR-e-MNAR)) | Geração de `df_analise_cryo` ($100\%$ de zeros em `CryoSleep == True`), `regras_dominio` ($0$ violações) e `df_testes_mcar` ($\chi^2$ de `isna` vs. `Transported`). |
| **Célula 22** | `kan11_imputation_md` | `markdown` | `KAN-11` | [5.4. Definição e Implementação da Estratégia de Imputação (`KAN-11`)](../../notebooks/01_preparacao_dados.ipynb#5.4.-Definição-e-Implementação-da-Estratégia-de-Imputação-(KAN-11)) | Síntese do diagnóstico MCAR/MAR e especificação formal das 2 camadas (Regras R1–R6 + Mediana Agrupada/Moda Condicional). |
| **Célula 23** | `kan11_imputation_code` | `code` | `KAN-11` | [5.4. Pipeline Hierárquico `executar_pipeline_imputacao()` (Código)](../../notebooks/01_preparacao_dados.ipynb#5.4.-Definição-e-Implementação-da-Estratégia-de-Imputação-(KAN-11)) | Implementação e execução das 10 etapas de imputação sem vazamento de dados, gerando `df_train_clean`, `df_test_clean` e `df_log_imputacao`. |
| **Célula 24** | `kan11_comparison_md` | `markdown` | `KAN-11` | [5.5. Tabela Comparativa Antes vs. Depois da Limpeza (`KAN-11`)](../../notebooks/01_preparacao_dados.ipynb#5.5.-Tabela-Comparativa-Antes-vs.-Depois-da-Limpeza-(KAN-11)) | Apresentação do protocolo de auditoria de preservação das distribuições pós-imputação. |
| **Célula 25** | `kan11_comparison_code` | `code` | `KAN-11` | [5.5. Tabelas Comparativas Antes vs. Depois (Código)](../../notebooks/01_preparacao_dados.ipynb#5.5.-Tabela-Comparativa-Antes-vs.-Depois-da-Limpeza-(KAN-11)) | Geração das 3 tabelas de validação: `df_comp_completude`, `df_comp_quant` e `df_comp_cat`. |
| **Célula 26** | `kan11_conclusions_md` | `markdown` | `KAN-11` | [5.6. Síntese Metodológica da Limpeza e Imputação (`KAN-11`)](../../notebooks/01_preparacao_dados.ipynb#5.6.-Síntese-Metodológica-da-Limpeza-e-Imputação-(KAN-11)) | Consolidação executiva dos resultados da limpeza e padronização de tipos (`bool` para `CryoSleep` e `VIP`). |
| **Célula 27** | `kan12_intro_md` | `markdown` | `KAN-12` | [6. Engenharia de Variáveis Derivadas e Exportação do Dataset Tratado (`KAN-12`)](../../notebooks/01_preparacao_dados.ipynb#6.-Engenharia-de-Variáveis-Derivadas-e-Exportação-do-Dataset-Tratado-(KAN-12)) | Visão de negócio e definição das 8 variáveis derivadas (`Group`, `GroupSize`, `IsAlone`, `CabinDeck`, `CabinNum`, `CabinSide`, `TotalSpend`, `HasSpent`). |
| **Célula 28** | `kan12_engineering_code` | `code` | `KAN-12` | [6.1. Implementação de `criar_variaveis_derivadas()` (Código)](../../notebooks/01_preparacao_dados.ipynb#6.1.-Implementação-da-Engenharia-de-Variáveis-Derivadas-(KAN-12)) | Construção isolada das 8 variáveis derivadas em `df_train_derived` ($8.693 \times 22$) e `df_test_derived` ($4.277 \times 21$). |
| **Célula 29** | `kan12_validation_md` | `markdown` | `KAN-12` | [6.2. Dicionário Técnico e Validação de Integridade das Variáveis Derivadas](../../notebooks/01_preparacao_dados.ipynb#6.2.-Dicionário-Técnico-e-Validação-de-Integridade-das-Variáveis-Derivadas-(Sem-Vazamento-de-Dados)) | Introdução ao dicionário das 8 novas colunas e à bateria de testes de integridade e *zero data leakage*. |
| **Célula 30** | `kan12_validation_code` | `code` | `KAN-12` | [6.2. Dicionário de Derivadas e Bateria de 9 Validações (Código)](../../notebooks/01_preparacao_dados.ipynb#6.2.-Dicionário-Técnico-e-Validação-de-Integridade-das-Variáveis-Derivadas-(Sem-Vazamento-de-Dados)) | Geração de `dicionario_derivadas` e `validacoes_kan12` (100% de aprovação nas 9 regras lógicas/algébricas e disjunção de grupos). |
| **Célula 31** | `kan12_stats_md` | `markdown` | `KAN-12` | [6.3. Resumo Estatístico e Sinal Explicativo das Variáveis Derivadas vs. `Transported`](../../notebooks/01_preparacao_dados.ipynb#6.3.-Resumo-Estatístico-e-Sinal-Explicativo-das-Variáveis-Derivadas-vs.-Transported) | Introdução à avaliação descritiva e de associação bivariada ($\chi^2$) das novas variáveis com o alvo `Transported`. |
| **Célula 32** | `kan12_stats_code` | `code` | `KAN-12` | [6.3. Estatísticas Descritivas e Testes $\chi^2$ das Derivadas (Código)](../../notebooks/01_preparacao_dados.ipynb#6.3.-Resumo-Estatístico-e-Sinal-Explicativo-das-Variáveis-Derivadas-vs.-Transported) | Geração de `resumo_quant_deriv` (`GroupSize`, `CabinNum`, `TotalSpend`) e `associacao_derivadas` (`IsAlone`, `HasSpent`, `CabinSide`, `CabinDeck` vs. `Transported`). |
| **Célula 33** | `kan12_export_md` | `markdown` | `KAN-12` | [6.4. Exportação e Auditoria dos Datasets Tratados (`data/processed/`)](../../notebooks/01_preparacao_dados.ipynb#6.4.-Exportação-e-Auditoria-dos-Datasets-Tratados-(data/processed/)) | Documentação da persistência das bases finais limpas. Artefatos: `data/processed/spaceship_titanic_clean.csv` e `data/processed/spaceship_titanic_test_clean.csv`. |
| **Célula 34** | `kan12_export_code` | `code` | `KAN-12` | [6.4. Exportação de `spaceship_titanic_clean.csv` e `assert`s Finais (Código)](../../notebooks/01_preparacao_dados.ipynb#6.4.-Exportação-e-Auditoria-dos-Datasets-Tratados-(data/processed/)) | Exportação para `data/processed/`, releitura de disco com `assert` de dimensões ($8.693 \times 22$ e $4.277 \times 21$) e zero `NaN`s, gerando `auditoria_exportacao`. |
| **Célula 35** | `kan12_conclusions_md` | `markdown` | `KAN-12` | [6.5. Síntese Metodológica da Engenharia de Variáveis Derivadas (`KAN-12`)](../../notebooks/01_preparacao_dados.ipynb#6.5.-Síntese-Metodológica-da-Engenharia-de-Variáveis-Derivadas-(KAN-12)) | Fechamento executivo da Seção 1 e entrega formal da base tratada para todas as trilhas analíticas do projeto. |
