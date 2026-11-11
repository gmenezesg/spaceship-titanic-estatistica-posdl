# Teleprompter — Apresentação Final (Spaceship Titanic)

**Uso:** este é o texto falado, slide por slide, para leitura em tela ou impressão. As seções
`## 01` a `## 18` correspondem, cada uma, a um slide de `report/apresentacao_final.pdf` e a uma
página do PDF gerado por `src/gerar_teleprompter.py`; as seções `00` e `19` são páginas de apoio.

- **Duração-alvo:** 12 min 40 s de fala + 20 s de margem (13 min de bloco, 2 min para perguntas).
- **Ritmo:** 100 a 110 palavras por minuto. As quebras de linha são grupos de respiração.
- **Regra de ouro:** “associação”, nunca “causa”; “no teste”, não “no modelo em geral”.
- **Fonte dos números:** notebook consolidado e `docs/conclusoes/01` a `06`.

---

## 00 · 0:00 · Como usar este teleprompter

> Esta página não é falada.

Cada página corresponde a um slide do deck.
Avance os dois juntos: slide na tela, página aqui.

As linhas foram quebradas em grupos de respiração.
Leia um grupo, respire, leia o próximo.

[PAUSA] significa um segundo de silêncio.
Não preencha a pausa: ela dá peso ao número.

Números: diga devagar e repita o principal uma vez.
“81,47%” merece meio segundo antes e depois.

Se perder o lugar, olhe o título no topo
e o último número dito.
O slide na tela mostra a mesma informação.

Orçamento por slide
01 0:35 · 02 0:45 · 03 0:45 · 04 0:50 · 05 0:35 · 06 0:55
07 0:50 · 08 0:50 · 09 0:45 · 10 0:50 · 11 0:35 · 12 0:40
13 0:50 · 14 0:35 · 15 0:40 · 16 0:45 · 17 0:30 · 18 0:25

Três regras que não se quebram
Diga “associação”, nunca “causa”.
Diga “no teste”, não “no modelo em geral”.
Diga “apoio à triagem”, nunca “decisão automática”.

---

## 01 · 0:35 · Abertura

> Objetivo: situar o problema e o cliente. Olhe para a banca, não para a tela.

Boa noite.
[PAUSA]
Nosso projeto analisa o incidente da Spaceship Titanic.
A nave atravessou uma anomalia espaço-temporal
e metade dos 8.693 passageiros foi transportada
para outra dimensão.
[PAUSA]
Nosso cliente é o comando de resgate.
Ele precisa saber quem estava mais exposto
e prever quem foi transportado.
[APONTE] para a linha de base do slide
Vou mostrar o que os dados dizem —
e o que eles não autorizam dizer.

---

## 02 · 0:45 · A resposta em 30 segundos

> Objetivo: entregar a conclusão antes do método. Aponte para cada cartão ao citá-lo.

Em trinta segundos.
[PAUSA]
A taxa global é de 50,36%: 4.378 pessoas.
[APONTE] primeiro cartão
O criossono separa os grupos com a maior diferença:
81,47% contra 32,82% dos acordados.
[APONTE] segundo cartão
Origem e deck contam a mesma história
por caminhos diferentes.
E o modelo acerta 77,9% no teste,
com ROC-AUC de 0,862.
[PAUSA]
Três números, uma mensagem:
o confinamento é o sinal mais forte,
e o gasto engana.

---

## 03 · 0:45 · O incidente, o cliente e a pergunta

> Objetivo: deixar claro que existem duas perguntas e um limite metodológico.

O problema tem duas perguntas.
[PAUSA]
A primeira é entender:
quais perfis estavam mais expostos ao teletransporte?
Isso orienta apuração, comunicação às famílias
e revisão de protocolos.
[PAUSA]
A segunda é prever:
quais passageiros da base não rotulada foram transportados?
Isso prioriza busca e reconstrução de registros.
[PAUSA]
O desenho é observacional.
Não vamos afirmar causalidade em nenhum momento.

---

## 04 · 0:50 · De 14 para 22 variáveis, sem perder passageiros

> Objetivo: mostrar que o saneamento protegeu a amostra. Aponte para a faixa de decisões.

A base chegou com 1,91% das células ausentes
e 24% das linhas incompletas.
[PAUSA]
A saída óbvia — apagar linhas —
jogaria fora quase um quarto da amostra.
[PAUSA]
Optamos por um pipeline em dez etapas:
primeiro regras de negócio, depois estatística.
Criossono e criança implicam gasto zero.
Cabine e planeta são recuperados pelo grupo de viagem.
[PAUSA]
Resultado: 8.693 por 22, zero ausentes,
nenhuma linha descartada, nenhum outlier removido.
[APONTE] faixa inferior do slide
Impacto máximo da imputação: 0,77 ponto percentual.

---

## 05 · 0:35 · Cinco perguntas, cinco camadas de evidência

> Objetivo: dar o mapa da apresentação em 30 segundos.

O fio condutor são cinco camadas de evidência.
[PAUSA]
Descrever; entender a forma das distribuições;
testar; relacionar e prever; recomendar.
[PAUSA]
Cada camada responde a uma pergunta
e prepara a seguinte.
E nenhum número é citado sem a seção de origem.

---

## 06 · 0:55 · O confinamento é o sinal mais forte

> Objetivo: provar que criossono é a associação mais forte. Aponte para 81,47% antes de falar.

O achado mais forte da análise.
[PAUSA]
81,47% dos passageiros em criossono
foram transportados.
[APONTE] 81,47%
Entre os acordados, 32,82%.
[PAUSA]
Quase 49 pontos percentuais de diferença:
a maior do conjunto.
[PAUSA]
O V de Cramér é 0,467 — associação muito forte.
O qui-quadrado é 1.897,71, com p menor que 0,001.
[PAUSA]
Na prática, é o primeiro corte da triagem.

---

## 07 · 0:50 · Origem e deck contam a mesma história

> Objetivo: mostrar a segunda pista e desarmar a leitura de que origem “causa” transporte.

A segunda pista é a origem.
[PAUSA]
Europa tem 66,05%. Marte, 52,44%. Terra, 42,33%.
[PAUSA]
Mas atenção ao mecanismo aparente:
72,6% dos europeus ocupam os decks B e C —
justamente os de maior taxa.
[PAUSA]
Os decks B e C têm 72,95% e 68,07% de transporte.
O deck E, onde estão os terráqueos, fica em 36,05%.
[PAUSA]
Origem e deck são a mesma história
contada de dois jeitos.
Não podemos dizer que um causa o outro.
[PAUSA]
Por isso a recomendação é analisar os dois juntos.

---

## 08 · 0:50 · O gasto é uma pista falsa — ou quase isso

> Objetivo: impedir a leitura causal do gasto. Aponte para 41,92% e para as medianas.

Aqui está a pista falsa.
[PAUSA]
41,92% não gastaram nada a bordo.
[APONTE] 41,92%
A mediana dos transportados é zero.
A dos não transportados, 907 dólares.
[PAUSA]
Entre os não transportados, só 18% têm gasto zero.
Parece que gastar menos aumenta a chance de transporte.
Mas não é isso: quem está em criossono não consome.
[PAUSA]
O gasto acompanha o confinamento;
não protege contra ele.
[PAUSA]
Quem lê a média em vez da mediana erra duas vezes.

---

## 09 · 0:45 · A forma da distribuição define o teste

> Objetivo: justificar a escolha dos testes pela forma, não por formalidade.

Por que testar a forma? Porque ela define o teste.
[PAUSA]
A idade é aproximadamente Normal:
W de 0,980 e D de 0,076 — desvio pequeno.
Média e teste t são defensáveis.
[PAUSA]
O gasto é uma mistura: primeiro “gastou ou não”,
depois “quanto gastou”.
Testar a variável completa mediria a mistura,
não a forma dos gastos.
[PAUSA]
Nos positivos, o log zera a assimetria,
mas a curtose fica em 4,93: as caudas continuam pesadas.
[PAUSA]
Por isso: média para idade; mediana e testes robustos
para gasto.

---

## 10 · 0:50 · As diferenças resistem ao teste

> Objetivo: separar significância de relevância. Aponte para a linha do VIP.

Agora separamos sinal de ruído.
[PAUSA]
Criossono: V de 0,467. Planeta: 0,197.
VIP: 0,037 — significativo, mas irrelevante na prática.
[PAUSA]
É o exemplo perfeito de que p-valor pequeno
não significa efeito grande.
[PAUSA]
Para gasto, Levene rejeitou a homocedasticidade.
Trocamos Student por Welch:
t de 18,94, d de 0,407.
[PAUSA]
Entre planetas, a ANOVA de Welch deu F de 407,57
e eta-quadrado de 0,171 — efeito grande.
[PAUSA]
O pós-hoc mostra Europa acima da Terra
em 2.768 dólares por passageiro.

---

## 11 · 0:35 · Significância não é relevância

> Objetivo: fazer a banca olhar o tamanho do efeito, não só o p-valor.

Significância não é relevância.
[PAUSA]
O gráfico ordena o tamanho do efeito.
Criossono está muito acima do limite de associação forte.
Planeta fica no moderado. VIP quase encosta no zero.
[PAUSA]
Com 8.693 casos, quase tudo fica significativo.
O que decide a recomendação é a magnitude.
[PAUSA]
É por isso que o relatório discute tamanho de efeito
em todas as seções.

---

## 12 · 0:40 · Quem consome um serviço tende a consumir outros

> Objetivo: mostrar as correlações e o alerta de multicolinearidade.

As correlações mais fortes são de cada gasto
com o total — esperado, porque o total é a soma.
[PAUSA]
Entre serviços, Spearman chega a 0,52:
quem usa um serviço tende a usar outros.
[PAUSA]
Já idade e tamanho do grupo têm relação negativa,
mas fraca: menos 0,18.
[PAUSA]
E há um alerta: origem e deck se sobrepõem.
O VIF de Europa chega a 7,98 no treino.
[PAUSA]
Por isso os coeficientes do modelo exigem cautela.

---

## 13 · 0:50 · Um apoio à triagem, não uma sentença

> Objetivo: entregar as métricas sem exagerar o papel do modelo.

O modelo é uma regressão logística,
com limiar de 0,5 fixado antes do teste.
[PAUSA]
No teste, acerta 77,9%,
com ROC-AUC de 0,862 e F1 de 0,784.
[PAUSA]
São 25,5 pontos percentuais acima do melhor baseline,
que acerta 52,4% no teste.
[PAUSA]
Recall de 0,796:
o modelo encontra quase oito em cada dez transportados.
A precisão é 0,772; a especificidade, 0,761.
[PAUSA]
É um apoio à triagem; não substitui a decisão humana.

---

## 14 · 0:35 · O que o modelo aprendeu, ajustado pelas demais variáveis

> Objetivo: ler os Odds Ratios como associações ajustadas. Aponte para Europa e criossono.

Olhando o modelo ajustado.
[PAUSA]
Europa tem OR de 3,97. Criossono, 3,21.
[PAUSA]
Isso já desconta gasto, deck e as demais variáveis.
[PAUSA]
Do outro lado, Spa, RoomService e deck G
ficam abaixo de 1.
[PAUSA]
O pseudo-R² de McFadden é 0,311 no treino.
[PAUSA]
São associações ajustadas, não causas.

---

## 15 · 0:40 · Três achados que respondem à pergunta

> Objetivo: consolidar a resposta em três cartões. Sem números novos.

Três achados respondem à pergunta.
[PAUSA]
Criossono: 81,47% contra 32,82%, com V de 0,467.
[PAUSA]
Origem e deck: Europa 66,05%, Terra 42,33%,
e 72,6% dos europeus nos decks B e C.
[PAUSA]
Gasto: 41,92% não gastaram nada,
e a mediana é zero contra 907 dólares.
[PAUSA]
Nenhum desses achados autoriza afirmar causalidade.

---

## 16 · 0:45 · O que o cliente pode fazer com isso

> Objetivo: fechar com ações, em ordem de prioridade. Fale devagar: é a parte mais prática.

Quatro ações, em ordem de prioridade.
[PAUSA]
Primeira: priorizar a inspeção das cápsulas de criossono.
É a associação mais forte e a mais acionável.
[PAUSA]
Segunda: investigar a diferença por origem,
cruzada com deck e classe.
[PAUSA]
Terceira: abandonar o gasto como proxy de presença.
[PAUSA]
Quarta: usar o modelo como triagem, com revisão humana,
e recalibrar o limiar pelo custo do erro.
[PAUSA]
O próximo passo é validar por grupo de viagem
antes de qualquer uso real.

---

## 17 · 0:30 · O que este estudo não permite afirmar

> Objetivo: declarar as limitações sem enfraquecer o resultado.

O que este estudo não permite.
[PAUSA]
Associação não é causa.
A divisão é única, sem intervalo de incerteza.
A separação é por passageiro, não por grupo de viagem —
o que pode deixar a avaliação otimista.
[PAUSA]
A imputação pela moda atinge 2,1% a 2,5% das categóricas.
E há multicolinearidade entre origem e deck.
[PAUSA]
A cautela define o que o trabalho autoriza recomendar.

---

## 18 · 0:25 · Encerramento

> Objetivo: fechar a narrativa e abrir para perguntas. Não acrescente números novos.

Metade da nave foi transportada.
O criossono é o sinal mais forte;
origem e deck contam a mesma história;
e o gasto não é um bom atalho.
[PAUSA]
O modelo ajuda a triar; não substitui o juízo humano.
[PAUSA]
Obrigado. Ficamos à disposição para as perguntas.

---

## 19 · 0:00 · Cola de emergência

> Esta página não é falada. Use se a banca interromper ou se o tempo apertar.

Versão de 60 segundos
Metade dos 8.693 passageiros foi transportada.
O criossono é o sinal mais forte: 81,47% contra 32,82%.
Origem e deck contam a mesma história: Europa 66,05%,
Terra 42,33%.
O gasto engana: 41,92% não gastaram nada.
O modelo acerta 77,9% e serve como triagem, não sentença.

Respostas curtas
Por que não apagar linhas? Perderíamos 24% da amostra.
A imputação distorce? No máximo 0,77 p.p. nas taxas.
Por que Welch? Levene rejeitou a homocedasticidade.
Por que não 90% de acurácia? As variáveis não capturam tudo.
Por que limiar 0,5? Fixado antes do teste, para não otimizar.
Isso é causal? Não. Todo o desenho é observacional.
Qual a maior limitação? A divisão única e por passageiro.
O que fariam com mais tempo? Validação por grupo de viagem.

Números de bolso
Global: 50,36% · Criossono: 81,47% × 32,82%
Planetas: 66,05% / 52,44% / 42,33%
Sem gasto: 41,92% · Medianas: US$ 0 × US$ 907
Criossono: χ² 1.897,71 · V 0,467
Gasto: t 18,94 · d 0,407 · Δ US$ 1.120,74
Modelo: 77,9% · ROC-AUC 0,862 · F1 0,784

Nunca diga
“Isso prova que o criossono causa o transporte.”
“O modelo decide quem foi transportado.”
“Acurácia de 90%.”
