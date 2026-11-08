# Roteiro de Apresentação — Projeto Final de Estatística

- **Seção T3 de referência:** 6. Conclusões e Recomendações Práticas
- **Ticket:** [KAN-44](https://megamatic.atlassian.net/browse/KAN-44)
- **Duração-alvo:** 13 minutos de fala + 2 minutos de margem
- **Base de todos os números:** notebook consolidado (Seções 1 a 6) e `docs/conclusoes/01` a `06`

> **Regra de ouro.** Nenhum número é citado sem a seção de origem. Se a banca pedir a fonte, a resposta é a seção indicada na coluna "Origem". Este roteiro **não substitui** o KAN-36 (apresentações cruzadas da Reunião 2); ele é o apoio da apresentação final.

---

## 1. Orçamento de tempo

| Bloco | Tempo | Pergunta que responde |
| :--- | ---: | :--- |
| Abertura | 1 min | Qual é o problema e por que ele importa? |
| Contexto e dados | 2 min | Que dados temos e quais são suas limitações? |
| Descritiva | 3 min | Quem são os passageiros e o que os distingue? |
| Probabilidade | 2 min | As distribuições permitem os testes que usamos? |
| Testes de hipóteses | 3 min | As diferenças observadas são estatisticamente sustentáveis? |
| Correlação e modelo | 3 min | O que prevê o desfecho e com qual desempenho? |
| Conclusões | 1 min | O que o cliente deve fazer com isso? |

## 2. Bloco a bloco

### Abertura (1 min)

- **Mensagem:** "Recebemos o registro de 8.693 passageiros de uma nave. Queremos entender o que distingue quem foi transportado de quem não foi — e o que isso permite recomendar."
- **Número de apoio:** 50,36% transportados.
- **Figura:** nenhuma.
- **Origem:** Seção 1.
- **Pergunta provável:** "Qual é o cliente?" → A companhia que investiga o incidente e precisa priorizar apuração, comunicação e alocação de recursos.

### Contexto e dados (2 min)

- **Mensagem:** "A base chegou crua, com valores ausentes e colunas compostas. O pipeline da Seção 1 entregou 8.693 × 22 sem nulos, sem remover outliers."
- **Números de apoio:** 8.693 passageiros; 22 colunas; 0 valores ausentes; imputação em 2,1% a 2,5% das categóricas, com sensibilidade de até 0,64 p.p.
- **Figura:** nenhuma.
- **Origem:** Seção 1, `docs/conclusoes/01_ambiente_dados.md`.
- **Pergunta provável:** "A imputação não distorce?" → A checagem de sensibilidade está na Seção 1 e as proporções não mudam além de 0,64 p.p.

### Descritiva (3 min)

- **Mensagem:** "A primeira pista é o confinamento: passageiros em criossono foram transportados em 81,5% dos casos, contra 32,8% dos acordados. A origem também pesa: Europa 66,1%, Marte 52,4%, Terra 42,3%."
- **Números de apoio:** 50,36% global; 81,47% × 32,82%; 66,05% / 52,44% / 42,33%; 41,92% sem gasto; mediana de gasto US$ 0,00 × US$ 907,00.
- **Figuras:** `fig_02` (criossono) e `fig_01` (planeta).
- **Origem:** Seção 2, `docs/conclusoes/02_descritiva_visual.md`.
- **Pergunta provável:** "Por que não usar a média de gasto?" → A assimetria é 4,40 e 41,92% gastaram zero; a média é inflada pela cauda.

### Probabilidade (2 min)

- **Mensagem:** "Testamos a forma das distribuições para escolher os testes certos, não por formalidade. A idade é aproximadamente Normal; o gasto positivo é Log-Normal no corpo, com caudas pesadas."
- **Números de apoio:** `Age` W = 0,980 e D = 0,076; `log1p(TotalSpend)` W = 0,891 e D = 0,126; curtose 4,93.
- **Figura:** `fig_07` e `fig_08` (KAN-19); QQ-plots inline no notebook 03.
- **Origem:** Seção 3, `docs/conclusoes/03_probabilidade_distribuicoes.md`.
- **Pergunta provável:** "Se o teste rejeita a normalidade, por que usar teste paramétrico?" → Porque a decisão se apoia no tamanho do desvio (W e D), não no p com n grande; e o teste de Welch é robusto à não normalidade com n desta ordem.

### Testes de hipóteses (3 min)

- **Mensagem:** "As diferenças não são ruído. Criossono tem a associação mais forte (V = 0,467); planeta vem em seguida (V = 0,197). Em gasto, a heterocedasticidade foi severa, então trocamos o t de Student por Welch."
- **Números de apoio:** χ² = 1.897,71 (criossono); χ² = 338,82 (planeta); t de Welch = 18,94, d = 0,407; ANOVA de Welch F = 407,57, η² = 0,171.
- **Figura:** nenhuma nova; usar `fig_03` (idade) e `fig_04` (gasto por desfecho).
- **Origem:** Seção 4, `docs/conclusoes/04_testes_hipoteses_anova.md`.
- **Pergunta provável:** "ANOVA clássica ou de Welch?" → Welch, porque o teste de Levene rejeitou homocedasticidade e a razão de variâncias passa de 37×; o pós-hoc é Games-Howell.

### Correlação e modelo (3 min)

- **Mensagem:** "O modelo logístico prevê o desfecho com 77,9% de acurácia e ROC-AUC de 0,862 — 25,5 pontos acima da regra ingênua. É apoio à triagem, não decisão automática."
- **Números de apoio:** acurácia 0,779; precisão 0,772; recall 0,796; especificidade 0,761; F1 0,784; ROC-AUC 0,862; AP 0,880.
- **Figura:** `kan34_matriz_confusao.png` e `kan34_curvas_roc_pr.png` (artefatos de notebook, não catalogados).
- **Origem:** Seção 5, `docs/conclusoes/05_correlacao_regressoes.md`.
- **Pergunta provável:** "Por que o limiar é 0,5?" → Fixado *a priori* para evitar otimização no teste; recalibrar exige definir o custo relativo de falso positivo e falso negativo.

### Conclusões (1 min)

- **Mensagem:** "Três recomendações: priorizar a inspeção das cápsulas de criossono; investigar a diferença por origem cruzando com deck e classe; e parar de usar gasto como proxy de presença."
- **Número de apoio:** 81,47% × 32,82% (criossono); 41,92% sem gasto.
- **Figura:** nenhuma.
- **Origem:** Seção 6, `docs/conclusoes/06_conclusoes_recomendacoes.md`.
- **Pergunta provável:** "Isso é causal?" → Não. Todo o estudo é observacional; as recomendações são de triagem e de investigação.

## 3. Números que não podem ser citados errado

| Indicador | Valor | Seção |
| :--- | ---: | :--- |
| Taxa global de transporte | 50,36% (4.378 de 8.693) | 2 |
| Criossono × acordado | 81,47% × 32,82% | 2 |
| Origem: Europa / Marte / Terra | 66,05% / 52,44% / 42,33% | 2 |
| Sem nenhum gasto | 41,92% (3.644) | 3 |
| Gasto mediano: transportado × não | US$ 0,00 × US$ 907,00 | 4 |
| χ² criossono / V de Cramér | 1.897,71 / 0,467 | 4 |
| χ² planeta / V de Cramér | 338,82 / 0,197 | 4 |
| Acurácia / ROC-AUC do logístico | 77,9% / 0,862 | 5 |

## 4. Checklist de ensaio

- [ ] Cronometrar cada bloco e cortar da descritiva se estourar.
- [ ] Abrir as figuras antes da fala: `fig_01`, `fig_02`, `fig_03`, `fig_04`, `fig_07`, `fig_08`.
- [ ] Repetir em voz alta a frase de cautela: "associação observacional, não causal".
- [ ] Ter o notebook 06 aberto para mostrar a célula que recomputa os números.
- [ ] Preparar a resposta sobre limitações: divisão única, sem intervalo de incerteza, divisão por passageiro e não por grupo.
