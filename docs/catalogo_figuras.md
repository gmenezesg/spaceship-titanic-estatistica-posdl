# Catálogo de Figuras e Tabelas do Relatório Final (`KAN-38`)

- **Ticket Principal (Jira):** [KAN-38 — Selecionar tabelas e gráficos do relatório](https://megamatic.atlassian.net/browse/KAN-38)
- **Tickets de Origem:** [KAN-14](https://megamatic.atlassian.net/browse/KAN-14) · [KAN-15](https://megamatic.atlassian.net/browse/KAN-15) · [KAN-16](https://megamatic.atlassian.net/browse/KAN-16) · [KAN-17](https://megamatic.atlassian.net/browse/KAN-17) · [KAN-18](https://megamatic.atlassian.net/browse/KAN-18) · [KAN-19](https://megamatic.atlassian.net/browse/KAN-19)
- **Pasta Oficial:** `report/figures/`
- **Documento de Referência:** [`docs/conclusoes/02_descritiva_visual.md`](conclusoes/02_descritiva_visual.md)
- **Base de Dados:** `data/processed/spaceship_titanic_clean.csv` — 8.693 passageiros × 22 colunas, 0 valores ausentes
- **Responsável:** Helton Gomes Soares de Lima · **Revisoras:** Luciana Almeida e Daniela
- **Status:** 8 figuras selecionadas e exportadas (faixa de 8 a 12 do Jira atendida) e 4 tabelas selecionadas, das quais 3 já estão publicadas em notebook e 1 depende da KAN-15.

> **Convenção.** Os arquivos seguem o padrão `fig_XX_nome_descritivo.png`, com `XX` em dois dígitos, nome em minúsculas, sem acentos e sem espaços. Todas as figuras têm **300 DPI**, pelo menos 1.700 px de largura e legenda autossuficiente (a imagem deve ser compreensível sem o texto ao redor). Os títulos embutidos nas imagens não trazem numeração: a numeração existe apenas neste catálogo e no documento do relatório.

---

## 1. Figuras Selecionadas

| Arquivo | Figura | Legenda formal | Seção do relatório | Origem | Dimensões | DPI |
| :--- | :---: | :--- | :--- | :--- | ---: | ---: |
| [`fig_01_transporte_por_planeta.png`](../report/figures/fig_01_transporte_por_planeta.png) | 1 | Taxa de transporte por planeta de origem (n = 8.693). Europa 66,05%, Marte 52,44% e Terra 42,33%; linha tracejada = taxa global de 50,36%. | 2.1 Perfil demográfico | notebook 02, célula 11 (`2598f142`, KAN-16) | 2.075 × 1.373 | 300 |
| [`fig_02_transporte_por_criossono.png`](../report/figures/fig_02_transporte_por_criossono.png) | 2 | Taxa de transporte por estado de criossono: 81,47% entre os passageiros em criossono contra 32,82% entre os acordados. | 2.3 Relação com `Transported` | notebook 02, célula 12 (`dfdd436d`, KAN-16) | 1.775 × 1.374 | 300 |
| [`fig_03_idade_distribuicao.png`](../report/figures/fig_03_idade_distribuicao.png) | 3 | Distribuição da idade dos passageiros (n = 8.693), com média de 28,8 anos e mediana de 27; 9,3% têm até 12 anos. | 2.1 Perfil demográfico | notebook 02, célula 13 (`9e54921e`, KAN-16) | 2.375 × 1.318 | 300 |
| [`fig_04_gasto_por_transporte.png`](../report/figures/fig_04_gasto_por_transporte.png) | 4 | Gasto total a bordo (US$) por desfecho, em escala symlog: mediana zero entre transportados (65,5% sem consumo) e US$ 907,00 entre não transportados. | 2.3 Relação com `Transported` | notebook 02, célula 14 (`f48f6c2b`, KAN-16) | 2.079 × 1.442 | 300 |
| [`fig_05_gasto_por_planeta.png`](../report/figures/fig_05_gasto_por_planeta.png) | 5 | Gasto total a bordo (US$) por planeta de origem: medianas de US$ 1.914,00 (Europa), US$ 950,00 (Marte) e US$ 705,00 (Terra). | 2.2 Consumo e gastos | notebook 02, célula 14 (`f48f6c2b`, KAN-16) | 2.379 × 1.442 | 300 |
| [`fig_06_passageiros_por_deck.png`](../report/figures/fig_06_passageiros_por_deck.png) | 6 | Passageiros por deck da cabine e taxa de transporte; os decks F e G concentram 62,76% da amostra e o deck T (n = 5) está sinalizado como amostra insuficiente. | 2.1 Perfil demográfico | notebook 02, célula 15 (`7165bedf`, KAN-16) | 2.676 × 1.470 | 300 |
| [`fig_07_idade_normal_ajustada.png`](../report/figures/fig_07_idade_normal_ajustada.png) | 7 | Idade observada × Normal ajustada (μ = 28,8 anos; σ = 14,4): a curva acompanha o centro da distribuição e subestima as caudas, sobretudo a concentração em idade 0. | 3. Probabilidade e distribuições | notebook 05, célula 14 (`eee78901`, KAN-19) | 2.341 × 990 | 300 |
| [`fig_08_gasto_zero_e_log_normal.png`](../report/figures/fig_08_gasto_zero_e_log_normal.png) | 8 | Painel esquerdo: proporção de passageiros com gasto zero por rubrica e no total (41,9%). Painel direito: gasto positivo em escala logarítmica com Log-Normal ajustada (ln: μ = 7,33; σ = 0,96). | 3. Probabilidade e distribuições | notebook 05, célula 17 (`830812c4`, KAN-19) | 3.575 × 1.049 | 300 |

### 1.1. Legendas completas para o relatório

**Figura 1 — Taxa de transporte por planeta de origem.**
Barras 100% empilhadas com a proporção de passageiros transportados em cada planeta; a linha tracejada marca a taxa global de 50,36% e o número entre parênteses é o tamanho da categoria. Passageiros de Europa foram os mais transportados (66,05%) e os da Terra, os menos (42,33%). A figura descreve associação, não efeito: a origem está entrelaçada com o deck da cabine.

**Figura 2 — Taxa de transporte por criossono.**
Mesma construção da Figura 1, aplicada ao estado durante a viagem. A diferença de 48,7 pontos percentuais (81,47% contra 32,82%) é a maior associação categórica observada no conjunto de dados.

**Figura 3 — Distribuição da idade.**
Histograma com intervalos de 2 anos e curva de densidade estimada (KDE). A distribuição é aproximadamente simétrica (assimetria 0,43), concentrada entre 20 e 37 anos, com pico visível em idade 0 (bebês) e 9,3% de crianças de até 12 anos.

**Figura 4 — Gasto total a bordo por desfecho.**
Boxplots de `TotalSpend` em escala symlog (linear perto de zero, logarítmica acima), com mediana, média (losango) e valores extremos preservados. Entre os transportados, a mediana é zero e 65,5% não consumiram nada; entre os não transportados, 18,0% têm gasto zero e a mediana é de US$ 907,00. A linha tracejada marca o limite global de US$ 3.610,00 definido na KAN-17.

**Figura 5 — Gasto total a bordo por planeta de origem.**
Boxplots de `TotalSpend` por planeta, com a mesma construção da Figura 4. Europa concentra os maiores gastos (mediana de US$ 1.914,00) apesar de ter a maior proporção de passageiros sem consumo (48,1%). Os pontos acima do bigode são valores extremos mantidos na base.

**Figura 6 — Passageiros por deck da cabine e taxa de transporte.**
Barras empilhadas com o número absoluto de passageiros por deck e a taxa de transporte anotada em cada barra. Os decks F (32,99%) e G (29,77%) concentram 62,76% da amostra; B (72,95%) e C (68,07%) têm as maiores taxas. O deck T, com 5 passageiros, aparece marcado como amostra insuficiente.

**Figura 7 — Idade observada × Normal ajustada.**
Histograma da idade com intervalos de 2 anos, sobreposto à densidade da Normal de mesma média e mesmo desvio padrão (μ = 28,8; σ = 14,4), acompanhado de uma tabela de frequências observadas versus previstas. A Normal reproduz razoavelmente o centro da distribuição (média ± 1 desvio e faixa de 20 a 40 anos), mas erra as caudas: prevê massa em idades negativas e subestima a concentração de bebês em idade 0. Conclusão prática: a idade não deve ser tratada como Normal em testes que dependam desse pressuposto.

**Figura 8 — Proporção de gasto zero e gasto positivo em escala logarítmica.**
Painel esquerdo: proporção de passageiros com gasto zero em cada uma das cinco rubricas (62% a 66%) e no total (41,9%), mostrando que "quem gasta" e "quanto gasta" são perguntas distintas. Painel direito: histograma de `ln(TotalSpend)` entre os 5.049 passageiros com gasto positivo, com a Log-Normal ajustada (μ = 7,33; σ = 0,96). O formato de sino apoia a Log-Normal como modelo de trabalho, mas o pico estreito em torno de 800 unidades monetárias revela uma mistura de populações que o modelo não captura.

---

## 2. Tabelas Selecionadas

| Tabela | Conteúdo | Seção do relatório | Origem | Status |
| :--- | :--- | :--- | :--- | :--- |
| **T1** | Composição da amostra nas 7 variáveis categóricas (n e %), com `Transported` no topo | 2.1 Perfil demográfico | notebook 02, célula 03 (`6b742183`, KAN-14) | Publicada |
| **T2** | Resumo das 5 rubricas de gasto: % de zeros, mediana, média, assimetria e coeficiente de variação | 2.2 Consumo e gastos | KAN-15 (resumos quantitativos) | Prevista |
| **T3** | Ranking das categorias com n ≥ 30 mais afastadas da taxa global de transporte | 2.3 Relação com `Transported` | notebook 02, célula 05 (`2aae6bb8`, KAN-14) | Publicada |
| **T4** | Gasto total por desfecho e por planeta: n, % de zeros, mediana e média | 2.2 e 2.3 | notebook 02, célula 14 (`f48f6c2b`, KAN-16) | Publicada |

> **Sobre a T2.** A tabela depende do notebook da KAN-15, ainda não publicado no repositório; até lá, o conteúdo equivalente pode ser reproduzido a partir das colunas de gasto da base tratada. As tabelas entram no relatório numeradas como **T1** a **T4**; qualquer tabela nova passa a ser **T5** em diante, sem renumerar as anteriores.

---

## 3. Regras de Nomenclatura e de Legenda

1. **Arquivo:** `fig_XX_nome_descritivo.png`, com `XX` em dois dígitos, minúsculas, sem acentos, sem espaços e no máximo 40 caracteres.
2. **Numeração:** define a ordem de citação no relatório, não a ordem de geração. Uma figura renumerada deve ser renomeada no notebook de origem, neste catálogo e no documento que a cita.
3. **Legenda:** começa com o número da figura, nomeia o que é medido, informa o tamanho da amostra e a estatística citada; nunca depende de siglas não explicadas.
4. **Padrão técnico:** 300 DPI, fundo branco, eixos com unidade, legenda explícita e paleta legível em preto e branco.
5. **Proibição:** caminhos absolutos em legendas, em links ou nas saídas dos notebooks.

---

## 4. Como Regenerar as Figuras

A partir da raiz do projeto, com o ambiente do repositório ativo:

```bash
# fig_01 a fig_06
jupyter nbconvert --to notebook --execute --inplace notebooks/02_estatistica_descritiva.ipynb

# fig_07 e fig_08
jupyter nbconvert --to notebook --execute --inplace notebooks/05_kan19_variaveis_aleatorias_distribuicoes.ipynb
```

As figuras são gravadas em `report/figures/` pelas chamadas `salvar(...)` (notebook 02) e `fig.savefig(...)` (notebook 05). No notebook 02, a célula 16 audita DPI e dimensões das figuras que ele mesmo gera; no notebook 05, a exportação usa `dpi=300` e `bbox_inches="tight"`.

---

## 5. Escopo Fechado

A seleção está fechada em **8 figuras**, o que atende à faixa de 8 a 12 do Jira e cabe no relatório de 10 a 15 páginas. Nenhuma figura adicional será exportada nesta fase; se alguma lacuna aparecer na revisão cruzada (KAN-40), a nova figura entra como `fig_09` ou superior e é registrada nesta tabela.

---

## 6. Checklist de Aceitação (`KAN-38`)

- [x] 8 figuras em `report/figures/`, todas com prefixo `fig_XX` (faixa de 8 a 12 do Jira atendida).
- [x] Todas a 300 DPI, com pelo menos 1.700 px de largura.
- [x] Títulos embutidos nas imagens sem numeração: a numeração vive apenas neste catálogo e no relatório.
- [x] Nenhuma figura órfã: cada arquivo aparece neste catálogo e é citado em um documento Markdown.
- [x] `docs/conclusoes/02_descritiva_visual.md` e notebook 02 usando exatamente os novos nomes.
- [x] Zero caminhos absolutos nos documentos e nas saídas dos notebooks.
- [ ] Revisão final de legendas e de enquadramento pela dupla Luciana e Daniela.
