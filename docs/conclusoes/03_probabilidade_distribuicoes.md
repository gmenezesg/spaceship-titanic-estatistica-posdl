# 03 — Conclusões de Probabilidade e Distribuições (`KAN-23`)

- **Ticket Principal (Jira):** [KAN-23 — Consolidar as conclusões da Seção 3](https://megamatic.atlassian.net/browse/KAN-23)
- **Tickets Consolidados da Trilha 3 (Probabilidade e Distribuições):**
  - [KAN-20 — Analisar distribuições de idade e despesas](https://megamatic.atlassian.net/browse/KAN-20)
  - [KAN-21 — Criar e interpretar QQ-plots](https://megamatic.atlassian.net/browse/KAN-21)
  - [KAN-22 — Implicações para os testes inferenciais](https://megamatic.atlassian.net/browse/KAN-22)
- **Notebook de Origem:** [`notebooks/03_probabilidade_distribuicoes.ipynb`](../../notebooks/03_probabilidade_distribuicoes.ipynb)
- **Fichamento Teórico:** [`notebooks/05_kan19_variaveis_aleatorias_distribuicoes.ipynb`](../../notebooks/05_kan19_variaveis_aleatorias_distribuicoes.ipynb) (KAN-19)
- **Base de Dados:** `data/processed/spaceship_titanic_clean.csv` — 8.693 passageiros × 22 colunas, 0 valores ausentes
- **Responsável:** Gustavo Menezes Gonçalves
- **Revisora:** Daniela Amaro

> **Escopo e cautela interpretativa.** As conclusões são **descritivas e observacionais**. Aderência a uma distribuição teórica não implica mecanismo gerador: indica apenas que o modelo é uma aproximação útil para resumir e testar os dados. Este documento complementa o fichamento da KAN-19, que produziu os histogramas e os ajustes (`fig_07` e `fig_08`); aqui se testa formalmente a aderência e se traduz o resultado na escolha dos testes da Seção 4.
>
> As referências entre colchetes indicam a **seção do notebook** em que está a célula correspondente, por exemplo [§5]. Os números de execução (`In [n]`) não são usados porque mudam a cada execução.

---

## 1. O que foi testado e em qual população [§3]

O erro mais comum em testes de aderência é testar a variável errada. `TotalSpend` **não é uma variável contínua**: é uma mistura *hurdle*, com uma decisão binária ("gastou ou não") e, condicionada a gastar, um valor positivo. Testar a variável completa contra uma lei contínua mede a mistura, não a forma dos gastos. Por isso as populações foram declaradas antes de qualquer teste:

| População | n | Zeros | Uso |
| :--- | ---: | ---: | :--- |
| `Age` (todos) | 8.693 | 178 (2,05%) | Aderência à Normal |
| `Age > 0` | 8.515 | 0 | Sensibilidade, sem figura |
| `TotalSpend` (todos) | 8.693 | 3.644 (41,92%) | Retrato da mistura |
| `log1p(TotalSpend) \| > 0` | 5.049 | 0 | Aderência à Normal na escala log |
| Gastos por serviço \| > 0 | 2.973 a 3.281 | 0 | Momentos apenas; sem teste individual |

## 2. Forma das distribuições [§3]

| População | Média | Desvio | Assimetria | Curtose (excesso) |
| :--- | ---: | ---: | ---: | ---: |
| `Age` (todos) | 28,78 | 14,35 | 0,43 | 0,16 |
| `Age > 0` | 29,38 | 13,88 | 0,54 | 0,20 |
| `TotalSpend` (todos) | US$ 1.447,46 | US$ 2.808,28 | 4,40 | 27,28 |
| `log1p(TotalSpend) \| > 0` | 7,34 | 0,95 | −0,19 | 4,93 |
| `RoomService \| > 0` | US$ 637,39 | US$ 995,60 | 4,07 | 27,91 |
| `FoodCourt \| > 0` | US$ 1.248,10 | US$ 2.460,11 | 4,42 | 28,76 |
| `ShoppingMall \| > 0` | US$ 496,93 | US$ 939,76 | 8,55 | 147,12 |
| `Spa \| > 0` | US$ 809,28 | US$ 1.717,21 | 4,86 | 32,82 |
| `VRDeck \| > 0` | US$ 840,05 | US$ 1.777,24 | 4,84 | 32,91 |

**Leitura.** A idade tem assimetria moderada e curtose próxima de zero: em forma, é a variável mais próxima de uma Normal. Já `TotalSpend` completo tem assimetria 4,40 e média 2,0 vezes maior que a mediana (US$ 717,00): a média não resume a variável. A transformação `log1p` nos positivos praticamente zera a assimetria (−0,19), mas **não** as caudas (curtose 4,93) — o log corrige o puxão à direita e revela que os gastos positivos são uma mistura de perfis.

## 3. Evidência visual: QQ-plots [§4]

**`Age` contra a Normal.** Na faixa central (quantis teóricos entre −1 e 1), **4.685 dos 5.935 pontos ficam abaixo da reta** — e não acima. A mediana observada (27 anos) é menor que a prevista pelo ajuste (28,8 anos): o miolo da distribuição real está em idades mais baixas do que a Normal desloca. À esquerda, um patamar horizontal em 0 anos marca o pico discreto dos 178 bebês e mantém os pontos **acima** da reta. Acima de 1, os pontos voltam a ficar **acima** (1.353 de 1.379), e o desenho fecha em S. O padrão combina **átomo em 0, discretização e concentração entre 20 e 40 anos** (55,3% dos passageiros, contra 51,3% previstos); não é de cauda pesada, como confirmam a curtose 0,16 e o W de 0,980.

**`log1p(TotalSpend)` contra a Normal.** O desvio mais forte está à esquerda: abaixo de −2,3, os pontos despencam quase na vertical, de 4 para 0,7, o que corresponde a gastos positivos mínimos (US$ 1 a US$ 30) muito mais numerosos do que o modelo prevê. No corpo, os pontos ficam levemente abaixo da reta; no trecho superior, acima; no extremo direito, voltam à reta. Esse S com perna vertical à esquerda é a assinatura da curtose 4,93.

Nenhum dos dois QQ-plots é prova isolada: eles orientam a leitura dos testes da seção seguinte.

## 4. Testes formais de aderência [§5]

As hipóteses são $H_0$: a variável segue a distribuição teórica indicada, contra $H_1$: não segue, com $\alpha = 0,05$. Foram aplicados dois testes com papéis distintos. O **Shapiro-Wilk** tem boa potência, mas o $p$-valor deixa de ser confiável acima de 5.000 observações — o SciPy emite aviso, e o W continua informativo. O **Kolmogorov-Smirnov com correção de Lilliefors** corrige o viés do KS quando média e desvio são estimados da amostra; reporta-se D, a maior distância entre as distribuições empírica e teórica.

| População | n | W | $p$ (Shapiro) | D | $p$ (Lilliefors) | Decisão |
| :--- | ---: | ---: | ---: | ---: | ---: | :--- |
| `Age` (todos) | 8.693 | 0,980 | $3{,}46 \times 10^{-33}$ | 0,076 | $2{,}50 \times 10^{-136}$ | Rejeita $H_0$ |
| `Age > 0` | 8.515 | 0,975 | $8{,}11 \times 10^{-36}$ | 0,085 | $1{,}45 \times 10^{-166}$ | Rejeita $H_0$ |
| `log1p(TotalSpend) \| > 0` | 5.049 | 0,891 | $8{,}57 \times 10^{-51}$ | 0,126 | $1{,}14 \times 10^{-222}$ | Rejeita $H_0$ |

**Leitura.** As três populações rejeitam $H_0$, como era esperado com $n$ entre 5 mil e 8,7 mil. O $p$-valor, portanto, não é o critério útil: ele mede se o desvio existe, não se ele importa. A decisão se apoia no **tamanho do desvio**:

- `Age` tem W de 0,980 e D de 0,076 — desvio **pequeno**. A Normal é aproximação de trabalho aceitável para o centro.
- `log1p(TotalSpend)` tem W de 0,891 e D de 0,126 — desvio **moderado a grande**. A Log-Normal descreve o corpo, mas não as duas caudas.

## 5. Sensibilidade: retirar o pico em `Age = 0` [§5.1]

A hipótese natural é que os 178 bebês sejam os responsáveis pela rejeição. O teste contraria a hipótese: ao restringir a `Age > 0`, o **W cai** de 0,980 para 0,975, o **D sobe** de 0,076 para 0,085 e a assimetria **aumenta** de 0,43 para 0,54. Retirar os zeros **piora** a aderência.

A explicação é que o pico em 0 ocupa uma região em que a Normal ajustada ainda tem densidade; ao removê-lo, sobra uma distribuição mais assimétrica e igualmente discreta. A rejeição **não** vem dos bebês: vem da **discretização** (80 valores inteiros) e da **concentração no centro**, que a curva teórica não reproduz. Consequência prática: não se deve "corrigir" a distribuição removendo crianças do recorte; declara-se a limitação e, em grupos pequenos, prefere-se o teste de postos.

## 6. Implicações para os testes inferenciais [§6]

| Variável | Modelo de referência | Teste indicado | Justificativa |
| :--- | :--- | :--- | :--- |
| `Age` | Normal aproximada (D = 0,076) | Média com $t$ de Welch; Mann-Whitney como salvaguarda | Assimetria moderada e $n$ grande sustentam a média; o teste de postos protege grupos pequenos |
| `TotalSpend` (todos) | Mistura *hurdle*: Bernoulli × Log-Normal | Levene → $t$ de Welch + Mann-Whitney | Heterocedasticidade severa e 41,92% de zeros: a média engana, mediana e postos são obrigatórios |
| `log1p(TotalSpend) \| > 0` | Log-Normal (corpo) com caudas pesadas | `log1p` na regressão linear, com erro-padrão HC3 | A transformação corrige a assimetria (−0,19); o HC3 entra pela heterocedasticidade dos resíduos, **não** pela curtose |
| Gastos por serviço | Log-Normal grosseira; assimetria 4,1 a 8,5 | Mann-Whitney ou Kruskal-Wallis; nunca $t$ de Student | Caudas muito longas mesmo entre quem gastou |
| Categóricas (`HomePlanet`, `CryoSleep`, `VIP`) | Bernoulli / multinomial | Qui-quadrado de Pearson, com Yates quando $df = 1$ | Normalidade não é pressuposto; o pressuposto é frequência esperada ≥ 5, atendido em 100% das células |

Essa tabela foi conferida contra `docs/conclusoes/04_testes_hipoteses_anova.md` e corresponde ao que a Seção 4 efetivamente executou: teste $t$ de Welch principal e Mann-Whitney complementar para gastos, ANOVA de Welch e Kruskal-Wallis para planetas, qui-quadrado para categóricas.

## 7. Limitações

1. **`Age` é discreta** (80 valores inteiros) e tem pico em zero. Nenhuma densidade contínua adere exatamente, e o QQ-plot mostra degraus por construção.
2. **`TotalSpend` é uma mistura.** Nenhum teste aplicado à variável completa descreve a forma dos gastos; a análise correta separa "quem gasta" de "quanto gasta".
3. **O $p$ do Shapiro é impreciso acima de 5.000 observações.** Ele é reportado por transparência, mas não sustenta nenhuma decisão.
4. **A curtose 4,93 dos gastos positivos não é corrigida pelo log.** A Log-Normal é modelo de trabalho, não descrição exata.
5. **Aderência não é causalidade.** Nada aqui autoriza afirmar que a idade ou o gasto *causam* o transporte.
6. **Normalidade de `Age` não é pré-requisito para usá-la como preditora.** A aderência aproximada à Normal descreve a variável isolada e sustenta a comparação de médias; regressão linear e logística não exigem preditoras normais. No modelo, o que se avalia é a especificação da relação e o comportamento dos resíduos.

## 8. Síntese para o cliente

- **A idade se comporta aproximadamente como uma Normal**, com desvio pequeno (W = 0,980; D = 0,076). É seguro usá-la como variável contínua, desde que se reconheça que a distribuição real tem um pico de bebês e valores inteiros.
- **O gasto a bordo não é uma variável só.** Quatro em cada dez passageiros não gastaram nada (41,92%); entre os que gastaram, a distribuição tem cauda longa dos dois lados. Relatar **mediana e proporção de gasto zero** é mais honesto do que relatar a média.
- **O logaritmo melhora muito a leitura dos gastos, mas não resolve tudo.** A assimetria cai de 4,40 para −0,19; as caudas continuam pesadas (curtose 4,93).
- **Os testes escolhidos na Seção 4 estão justificados pelos dados**, não por convenção: Welch e Mann-Whitney para gastos, qui-quadrado para categóricas, `log1p` com HC3 para heterocedasticidade na regressão.

---

*Documento produzido no âmbito do KAN-44, que repara as pendências de conteúdo apontadas pela auditoria de 08/11/2026.*
