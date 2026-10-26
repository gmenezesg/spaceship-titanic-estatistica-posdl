# Guia de Consolidação dos Notebooks (KAN-37)

O notebook final `notebooks/00_projeto_final_estatistica.ipynb` é **gerado automaticamente** pelo script `src/consolidar_notebooks.py`, a partir dos notebooks de cada trilha, na ordem definida em `notebooks/consolidacao.json`.

## Regras

1. **Cada trilha trabalha no seu notebook** e lê apenas a base tratada `data/processed/spaceship_titanic_clean.csv`. Nenhum notebook de trilha repete a preparação dos dados.
2. **Ninguém edita o `00_` à mão.** Para corrigir algo, edite o notebook de origem e rode o script de novo.
3. **A ordem das seções** fica no manifesto `notebooks/consolidacao.json`. Para incluir, remover ou reordenar um notebook, altere só esse arquivo.

## Como usar

Na raiz do repositório, com o ambiente virtual ativo:

| Objetivo | Comando |
|---|---|
| Prévia com os notebooks que já existem (não toca no `00_`) | `python src/consolidar_notebooks.py --permitir-faltantes --saida notebooks/_previa_consolidado.ipynb` |
| Prévia executada do início ao fim | o comando acima com `--executar` |
| Gerar o notebook final oficial | `python src/consolidar_notebooks.py --forcar --executar` |

Arquivos de prévia (`_previa_consolidado.ipynb`) servem só para conferência e **não devem ser commitados**.

## O que o script garante

- **Ordem fixa e rastreável:** cada seção recebe um cabeçalho com título, tickets do Jira e notebooks de origem.
- **Sem duplicação:** células de código idênticas a uma já incluída (como imports repetidos) são puladas automaticamente.
- **Exclusão explícita:** células marcadas com a tag `pular-consolidacao` não entram no notebook final. Use para rascunhos ou blocos de configuração que só fazem sentido no notebook da trilha. No Jupyter, a tag é adicionada pelo menu de metadados da célula; no VS Code, pelo botão `...` da célula, em "Add Cell Tag".
- **Reprodutibilidade:** o script avisa quando encontra caminhos absolutos (`C:\...`, `/home/...`) e, com `--executar`, roda o notebook inteiro em um kernel limpo, equivalente a "Restart & Run All". Se alguma célula falhar, o notebook não é salvo.
- **Segurança:** o script recusa sobrescrever o `00_` sem `--forcar` e recusa gerar o oficial se faltar algum notebook do manifesto, a menos que se use `--permitir-faltantes`.

## Pré-requisito de migração (uma vez)

Hoje a preparação dos dados (KAN-10, 11 e 12) está escrita diretamente no `00_projeto_final_estatistica.ipynb`. Para que o `00_` passe a ser gerado, esse conteúdo vira a primeira seção, com o nome que o Jira já prevê:

```bash
git mv notebooks/00_projeto_final_estatistica.ipynb notebooks/01_preparacao_dados.ipynb
python src/consolidar_notebooks.py --permitir-faltantes --executar
```

O segundo comando recria o `00_` a partir do `01_` e dos demais notebooks disponíveis.
