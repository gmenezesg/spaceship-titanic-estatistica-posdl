# Conclusões – Correlação, Regressão Linear e Regressão Logística

**Seção T3:** 5. Correlação, Regressão e Modelos Preditivos · **Tickets:** KAN-30, KAN-31, KAN-32, KAN-33, KAN-34 · **Conclusão:** KAN-35
**Notebook de origem:** [`notebooks/05_correlacao_regressoes.ipynb`](../../notebooks/05_correlacao_regressoes.ipynb) · **Base:** `data/processed/spaceship_titanic_clean.csv` (8.693 passageiros)
**Responsável:** Renatta · **Revisor:** Gustavo

> As referências entre colchetes indicam a **seção do notebook** (por exemplo, [§12.2]) em que está a célula correspondente. Os números de execução (`In [n]`) não são usados porque podem mudar em novas execuções.
> Todos os resultados são **associações observacionais**. Os ORs e os efeitos marginais são associações ajustadas pelas demais preditoras, e não efeitos causais.

---

## 1. Análise de correlação de Pearson e Spearman (KAN-30)

**O que foi feito.** Matrizes de Pearson (relação linear) e de Spearman (relação monotônica, por postos) das 8 variáveis quantitativas: `Age`, os cinco gastos, `TotalSpend` e `GroupSize`. Os coeficientes foram calculados nos **valores originais** [§4], com heatmaps anotados [§5], dispersões selecionadas por critério explícito [§7] e um pairplot compacto [§7.1].

**Principais achados:**
- **Os gastos têm distribuição muito assimétrica.** Entre 62% e 66% dos passageiros não gastam nada em cada serviço, e 41,9% não gastam em nenhum deles. A assimetria vai de 4,4 a 12,8 [§3]. Por isso Pearson e Spearman foram comparados lado a lado, e o `log1p` foi usado só na visualização.
- **As correlações mais fortes são de cada gasto com `TotalSpend`.** A maior é `FoodCourt` × `TotalSpend` (r = 0,74; ρ = 0,67). O resultado é esperado **por construção**, porque o total é a soma dos gastos.
- **Entre os gastos, o Pearson é fraco** (r ≤ 0,23), mas o **Spearman é maior** (até ρ = 0,52). Na verificação exploratória restrita a `TotalSpend > 0`, os ρ ficam entre −0,32 e 0,24 [§6]. Isso é um **indício** de que os zeros coincidentes, como os dos passageiros em criossono, influenciam o ρ da base completa.
- **A relação negativa mais forte, `Age` × `GroupSize`, é fraca** (r = −0,18).
- **Multicolinearidade das preditoras da regressão linear** [§8]:
  - `Age`, `GroupSize` e `VIP` mostram pouca evidência de multicolinearidade (VIF de 1,05 a 1,13);
  - `HomePlanet` e `CabinDeck` se sobrepõem: os decks A, B, C e T só têm passageiros de Europa, e o G só tem de Earth. GVIF equivalente de 3,22 e 1,40; VIF de `HomePlanet_Europa` = 7,99.

Figuras: `report/figures/kan30_heatmap_pearson.png`, `kan30_heatmap_spearman.png`, `kan30_dispersao_*.png` e `kan30_pairplot.png`.

---

## 2. Regressão linear para gastos e diagnóstico de resíduos (KAN-31)

**Modelo.**
- OLS (`statsmodels`) de **`log1p(TotalSpend)`**, escala escolhida antes do ajuste por causa da assimetria, sobre `Age`, `HomePlanet`, `CabinDeck`, `VIP` e `GroupSize`.
- Divisão própria de 80/20 (`random_state=42`, sem estratificar por `Transported`), com a codificação aprendida só no treino (referências `Earth`, `F` e `False`) [§11.1].

**Ajuste e erro** [§11.2]:

| Métrica | Valor | Escala |
|---|---|---|
| R² / R² ajustado | 0,257 / 0,256 | log1p, treino |
| Estatística F | 200,2 (p < 0,001) | log1p, treino |
| RMSE treino / teste | 3,18 / 3,18 | log1p |
| RMSE teste ao prever a média do treino | 3,71 | log1p |
| RMSE teste | ≈ 3.079 | dinheiro, via `expm1`; essa inversão **não** estima o gasto médio esperado |

**Associações**, como variação aproximada (e^β − 1) em `1 + TotalSpend`, mantidas as demais preditoras:
- **VIP:** cerca de +950%;
- **idade:** +4,8% por ano;
- **tamanho do grupo:** −13% por pessoa;
- **planeta e deck:** diferenças fortes, que não devem ser lidas separadamente por causa da sobreposição entre as duas variáveis;
- **deck T:** não interpretável, com n = 5.

**Diagnóstico** [§11.3; figura `report/figures/kan31_diagnostico_residuos.png`]:
- **Normalidade:** o QQ-plot tem formato de S e caudas curtas (curtose em excesso −1,02). Os resíduos **não são normais**.
- **Homocedasticidade:** o gráfico de resíduos × ajustados mostra **duas faixas**, e a dos passageiros com gasto zero é uma reta (resíduo = −ajustado). Há **heterocedasticidade** e estrutura não capturada. A transformação `log1p` não resolve a mistura de zeros com gastos positivos.
- **Inferência robusta HC3** [§11.3.1]: os coeficientes são os mesmos e as conclusões a 5% se mantêm, exceto o deck E (p de 0,083 para 0,048, no limite e portanto incerto).
- **VIF no treino** [§11.3]: `HomePlanet_Europa` = **7,98**, acima do limite de 5 do card. ⚠️ **Pendência:** nenhuma variável foi excluída, e a decisão é do grupo e do revisor.

**Limitações.** `CryoSleep`, fortemente ligada ao gasto zero, não faz parte das preditoras definidas no card. A resposta mistura zeros com gastos positivos. Modelos em duas partes seriam uma alternativa, mas ficam fora do escopo.

---

## 3. Desempenho da regressão logística e interpretação dos Odds Ratios (KAN-33 e KAN-34)

**Divisão de referência** [§10.1]: 80/20 com `random_state=42` e `stratify=y` (6.954 / 1.739; 50,4% de transportados nos dois conjuntos).

**Modelo** [§12.1]:
- `Pipeline` com `OneHotEncoder` (referências do treino), `StandardScaler` e `log1p` com `StandardScaler` nos gastos;
- `LogisticRegression` sem regularização, ajustada **apenas no treino**, sem vazamento;
- preditoras definidas a priori: `CryoSleep`, `HomePlanet`, `Destination`, `CabinDeck`, `CabinSide`, `VIP`, `Age`, `GroupSize` e os cinco gastos.

**Odds Ratios, com IC 95% via `statsmodels` na mesma matriz do treino** [§12.2], e **efeitos marginais médios** [§12.3]. Ambos são associações ajustadas, e não efeitos causais:

| Variável (referência) | OR (IC 95%) | Efeito marginal médio (associação ajustada) |
|---|---|---|
| `CryoSleep` = True (False) | **3,21** (2,61 – 3,94) | +20,8 p.p. |
| `HomePlanet` = Europa (Earth) | **3,97** (2,58 – 6,10) | +21,0 p.p. |
| `HomePlanet` = Mars (Earth) | 1,40 (1,14 – 1,72) | +5,3 p.p. |
| `CabinDeck` = G / E / A (F) | 0,53 / 0,55 / 0,53 | ≈ −9 a −10 p.p. |
| `CabinSide` = P (S) | 0,60 (0,53 – 0,67) | — |
| Gastos em Spa / VRDeck / RoomService (por 1 DP de log1p) | 0,48 / 0,51 / 0,55 | — |
| Gastos em FoodCourt / ShoppingMall (por 1 DP de log1p) | 1,48 / 1,24 | — |

**Como ler estes resultados:**
- O efeito do criossono é medido **já descontando os gastos**, e nenhum passageiro em criossono gastou. As duas variáveis devem ser lidas em conjunto.
- O efeito de Europa é estimado dentro dos decks em que os planetas coexistem.
- O deck T não é interpretável (IC de 0,03 a 7,14).
- Pseudo-R² de McFadden no treino = 0,311.

**Desempenho no teste** [§13.1–13.3]:
- Com o limiar **0,5 fixado a priori**, a matriz de confusão tem VP = 697, VN = 657, FP = 206 e FN = 179.
- ROC-AUC = **0,862** e Average Precision = 0,880.

Figuras: `report/figures/kan34_matriz_confusao.png` e `kan34_curvas_roc_pr.png`.

---

## 4. Tabela comparativa de métricas: modelo × baseline (KAN-32 e KAN-34)

Teste (n = 1.739), com `Transported = True` como classe positiva. Os baselines estão em [§10.2], e a comparação, em [§13.2].

| Modelo | Acurácia | Precisão | Recall | Especificidade | F1 | ROC-AUC |
|---|---|---|---|---|---|---|
| Baseline `most_frequent` | 0,504 | 0,504 | 1,000 | 0,000 | 0,670 | 0,500 |
| Baseline `stratified` | 0,524 | 0,528 | 0,523 | 0,525 | 0,525 | 0,524 |
| **Regressão logística** (limiar 0,5) | **0,779** | **0,772** | 0,796 | **0,761** | **0,784** | **0,862** |
| Ganho sobre o melhor baseline | +0,255 | +0,244 | −0,204 | +0,236 | +0,114 | +0,338 |

**Leitura:**
- O modelo agrega valor real em relação às regras ingênuas, com **+25,5 p.p. de acurácia** e **+0,34 de ROC-AUC**.
- O recall menor que o do `most_frequent` é esperado: o recall de 1,0 do baseline vem com especificidade 0, porque ele prevê todos como transportados.
- O F1 de 0,67 do `most_frequent` mostra que um F1 alto, sozinho, não indica discriminação.

**Limitações gerais da seção:**
- O resultado vem de um único conjunto de teste, sem intervalo de incerteza.
- A divisão é por passageiro, e não por grupo de viagem, o que pode deixar a avaliação otimista, em magnitude desconhecida.
- O limiar 0,5 não foi otimizado. Outros limiares trocam recall por especificidade, e a escolha depende do custo de cada erro.
- Pendência do KAN-31: VIF de 7,98 em `HomePlanet_Europa`.
