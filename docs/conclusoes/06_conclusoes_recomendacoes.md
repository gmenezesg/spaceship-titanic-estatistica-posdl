# 06 — Conclusões e Recomendações Práticas

- **Seção T3:** 6. Conclusões e Recomendações Práticas
- **Ticket:** [KAN-44](https://megamatic.atlassian.net/browse/KAN-44) — fechamento das pendências de conteúdo e consolidação
- **Notebook de Origem:** [`notebooks/06_conclusoes_recomendacoes.ipynb`](../../notebooks/06_conclusoes_recomendacoes.ipynb)
- **Base de Dados:** `data/processed/spaceship_titanic_clean.csv` — 8.693 passageiros × 22 colunas, 0 valores ausentes
- **Responsável:** Gustavo Menezes Gonçalves
- **Revisora:** Daniela Amaro

> Este documento **sintetiza** as Seções 1 a 5. Ele não é fonte primária de números: cada linha aponta a seção de origem. Todos os resultados são **observacionais**; nenhuma recomendação afirma causalidade.

---

## Sumário executivo

O estudo procurou entender o que distingue os passageiros transportados dos não transportados no incidente da *Spaceship Titanic*. A base reúne **8.693 passageiros e 22 variáveis**, sem valores ausentes, e a taxa de transporte é de **50,36%** (4.378 pessoas) — praticamente metade da amostra.

Três achados organizam a resposta. Primeiro, o **estado de criossono** é a variável isolada mais associada ao desfecho: 81,47% dos passageiros em criossono foram transportados, contra 32,82% dos acordados (V de Cramér = 0,467, associação muito forte). Segundo, a **origem planetária** também segmenta o resultado: Europa 66,05%, Marte 52,44% e Terra 42,33% (χ² = 338,82; p < 10⁻⁷³). Terceiro, o **consumo a bordo** distingue os grupos, mas exige cuidado: 41,92% não gastaram nada, e a mediana dos transportados é zero contra US$ 907,00 dos não transportados.

O conjunto das variáveis permite prever o desfecho com **77,9% de acurácia** no teste e **ROC-AUC de 0,862**, um ganho de 25,5 pontos percentuais sobre a regra ingênua. É um modelo útil para triagem, não para decisão automática.

## Painel de evidências

| Indicador | Valor | Origem |
| :--- | ---: | :--- |
| Taxa global de transporte | 50,36% (4.378 de 8.693) | Seção 2 |
| Transporte por origem (Europa / Marte / Terra) | 66,05% / 52,44% / 42,33% | Seção 2, `fig_01` |
| Transporte em criossono × acordado | 81,47% × 32,82% | Seção 2, `fig_02` |
| Passageiros sem nenhum gasto | 41,92% (3.644) | Seção 3 |
| Gasto mediano por desfecho (transp. × não) | US$ 0,00 × US$ 907,00 | Seção 4 |
| Idade — aderência à Normal | W = 0,980; D = 0,076 | Seção 3 |
| Gastos positivos — aderência à Log-Normal | W = 0,891; D = 0,126 | Seção 3 |
| Modelo logístico — acurácia / ROC-AUC | 77,9% / 0,862 | Seção 5 |

## Recomendações

1. **Priorizar a inspeção das cápsulas de criossono.** É a associação mais forte do estudo (81,47% contra 32,82%). Tratar as cápsulas como área crítica na apuração e na comunicação às famílias.
2. **Investigar a diferença por origem planetária.** Cruzar origem com deck e classe da cabine para verificar se o efeito é de localização física a bordo. A origem **não** deve ser critério isolado de priorização.
3. **Não usar gasto como proxy de importância ou de presença.** Quatro em cada dez passageiros não gastaram nada. Para reconstruir a alocação a bordo, usar cabine, grupo de viagem e estado de criossono.
4. **Usar o modelo como apoio à triagem, com revisão humana.** O limiar de 0,5 foi fixado *a priori* e o recall é de 0,796; recalibrar conforme o custo de cada tipo de erro antes de qualquer uso operacional.
5. **Comunicar com medianas e proporções, não com médias.** A assimetria de 4,40 no gasto infla a média; mediana, proporção de gasto zero e taxa por grupo são mais honestas.

## Limitações

- **Associação não é causa.** O desenho é observacional e não isola mecanismos.
- **Divisão única de treino e teste**, sem intervalo de incerteza.
- **Divisão por passageiro, não por grupo de viagem**: famílias podem aparecer dos dois lados, o que tende a deixar a avaliação otimista em magnitude desconhecida.
- **Imputação pela moda** em 2,1% a 2,5% das categóricas; a sensibilidade documentada chega a 0,64 p.p. e não muda as conclusões.
- **`HomePlanet_Europa` com VIF de 7,98**, pendência do KAN-31: os coeficientes dessa variável devem ser lidos com cautela.

## Próximo passo

O **KAN-39** transforma este documento no relatório técnico de 10 a 15 páginas, apoiado nas figuras `fig_01` a `fig_08` do catálogo. O **KAN-40** faz a revisão cruzada dos números, o **KAN-41** valida a reprodução, e o **KAN-42** e o **KAN-43** fecham o PDF e o pacote final.

---

*Documento produzido no âmbito do KAN-44, que repara as pendências de conteúdo apontadas pela auditoria de 08/11/2026.*
