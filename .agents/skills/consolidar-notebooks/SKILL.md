---
name: consolidar-notebooks
description: >-
  Use this skill whenever implementing, finishing, or validating any Jira ticket (KAN-XX)
  in the Spaceship Titanic project, or when the user asks to consolidate notebooks into
  notebooks/00_projeto_final_estatistica.ipynb. Enforces that each Jira ticket targets only
  its own source notebook mapped in notebooks/consolidacao.json, executes src/consolidar_notebooks.py
  aligned with docs/T3 Projeto Final Estatística PosDL.docx, and reminds the user to run consolidation
  at the end of every Jira ticket implementation.
---

# Skill: Consolidação Oficial de Notebooks (`consolidar-notebooks`)

Esta skill garante que o arquivo principal [`notebooks/00_projeto_final_estatistica.ipynb`](../../../notebooks/00_projeto_final_estatistica.ipynb) seja **exclusivamente gerado e atualizado** pelo script [`src/consolidar_notebooks.py`](../../../src/consolidar_notebooks.py) a partir do manifesto [`notebooks/consolidacao.json`](../../../notebooks/consolidacao.json), mantendo total objetividade e conformidade com `docs/T3 Projeto Final Estatística PosDL.docx`.

## Regras Invioláveis

1. **Proibição de Edição Direta:** **NUNCA** edite `notebooks/00_projeto_final_estatistica.ipynb` manualmente ou diretamente. Toda implementação de ticket Jira (`KAN-XX`) deve ocorrer exclusivamente no notebook de origem mapeado em `notebooks/consolidacao.json`.
2. **Execução e Lembrete ao Final de Todo Ticket Jira:** Sempre que concluir a implementação de qualquer ticket do Jira, execute os passos abaixo e **lembre explicitamente o usuário** de rodar esta skill/script antes de finalizar a entrega.

---

## Procedimento Passo a Passo

### Passo 1: Identificar e Validar o Mapeamento do Ticket Jira
Antes ou logo após implementar um ticket `KAN-XX`, consulte e valide o manifesto `notebooks/consolidacao.json`:

```bash
python src/consolidar_notebooks.py --ticket KAN-XX
python src/consolidar_notebooks.py --validar-mapa
```

- Se um novo notebook específico foi criado para o ticket, atualize `notebooks/consolidacao.json` (em `secoes[].notebooks`, `secoes[].mapeamento_tickets` e `mapa_tickets_notebooks`) e rode `--validar-mapa` novamente até obter código de saída `0`.

### Passo 2: Executar a Consolidação e Verificação Ponta a Ponta (*Restart & Run All*)
Gere e execute o notebook consolidado oficial `notebooks/00_projeto_final_estatistica.ipynb`:

```bash
# Durante o desenvolvimento das trilhas (quando nem todas as branches foram mescladas):
python src/consolidar_notebooks.py --permitir-faltantes --forcar --executar

# Na entrega final (KAN-37 / KAN-43, exigindo 100% dos notebooks presentes):
python src/consolidar_notebooks.py --forcar --executar
```

### Passo 3: Auditar o Relatório de Conformidade T3
Verifique na saída do comando se todos os critérios de `docs/T3 Projeto Final Estatística PosDL.docx` foram atendidos:
- **Zero erros de execução** em kernel limpo (`Restart & Run All`);
- **Zero caminhos absolutos** detectados (`AVISO: Possíveis caminhos absolutos` não deve aparecer);
- **Semente aleatória fixada** (`np.random.seed(42)` / `random_state=42`);
- **Objetividade e interpretação:** toda saída de código/gráfico possui célula Markdown interpretativa orientada ao cliente, e metadados burocráticos repetitivos foram higienizados.

### Passo 4: Emitir Lembrete Obrigatório ao Usuário
Ao finalizar qualquer tarefa vinculada a um ticket do Jira, inclua obrigatoriamente na sua resposta final ao usuário um bloco de lembrete como:

> **Lembrete de Consolidação (`KAN-37`):** O arquivo `notebooks/00_projeto_final_estatistica.ipynb` é gerado automaticamente e não deve ser editado à mão. Certifique-se de executar a skill **`consolidar-notebooks`** (`python src/consolidar_notebooks.py --permitir-faltantes --forcar --executar`) ao final da implementação deste ticket antes de abrir/atualizar o Pull Request.
