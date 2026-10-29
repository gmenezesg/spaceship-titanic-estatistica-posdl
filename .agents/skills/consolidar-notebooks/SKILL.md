---
name: consolidar-notebooks
description: >-
  On-demand skill to consolidate source notebooks into notebooks/00_projeto_final_estatistica.ipynb
  at the end of the project (KAN-37 / KAN-43) or ONLY when explicitly requested by the user,
  and to audit commit readiness across source notebooks. Do NOT run automatically on every Jira ticket.
---

# Skill Sob Demanda: Consolidação Oficial de Notebooks (`consolidar-notebooks`)

Esta skill aplica sob demanda a regra [`.agents/rules/governanca-notebooks-consolidacao.md`](../../rules/governanca-notebooks-consolidacao.md) para gerar e auditar o arquivo principal [`notebooks/00_projeto_final_estatistica.ipynb`](../../../notebooks/00_projeto_final_estatistica.ipynb) exclusivamente através do script [`src/consolidar_notebooks.py`](../../../src/consolidar_notebooks.py) e do manifesto [`notebooks/consolidacao.json`](../../../notebooks/consolidacao.json).

## Quando Invocar Esta Skill (Apenas Sob Demanda)

1. **Execução Estritamente Sob Demanda:**
   - **NÃO** execute a geração de `notebooks/00_projeto_final_estatistica.ipynb` automaticamente ao final de cada ticket Jira das trilhas analíticas.
   - Invocação permitida **somente** quando:
     - O usuário pedir explicitamente para rodar a consolidação ou auditar a prontidão para consolidação; ou
     - O trabalho estiver na etapa final de consolidação do projeto (`KAN-37` / `KAN-43`), quando todos os notebooks das trilhas já estiverem prontos e conformes para consolidação única.
2. **Conformidade Contínua nos Commits das Trilhas:**
   - Embora o `00_projeto_final_estatistica.ipynb` só seja gerado sob demanda no final do projeto, **todos os commits de cada ticket (`KAN-XX`) devem ser entregues 100% conformes** (isolados no próprio notebook de origem, sem caminhos absolutos no código ou nos outputs, com `seed(42)` fixada e validados via `--validar-mapa` ou prévia descartável) para que a consolidação final ocorra de uma só vez e sem erros.

---

## Procedimento Passo a Passo

### Modo A: Verificação Preventiva de Conformidade (Sem Alterar o `00_`)
Para validar que um commit/PR de trilha está pronto para a futura consolidação final sem modificar `notebooks/00_projeto_final_estatistica.ipynb`:

```bash
# 1. Consultar o mapeamento exato do ticket e validar integridade do manifesto:
python src/consolidar_notebooks.py --ticket KAN-XX
python src/consolidar_notebooks.py --validar-mapa

# 2. (Opcional) Testar a consolidação em arquivo temporário ignorado pelo Git (_previa*.ipynb):
python src/consolidar_notebooks.py --permitir-faltantes --forcar --executar --saida notebooks/_previa_consolidado.ipynb
rm -f notebooks/_previa_consolidado.ipynb
```

### Modo B: Consolidação Oficial Sob Demanda (Final do Projeto — `KAN-37` / `KAN-43`)
Quando solicitado explicitamente pelo usuário ou no fechamento do projeto (`KAN-37`):

```bash
# 1. Validar que todos os tickets e notebooks estão corretamente mapeados:
python src/consolidar_notebooks.py --validar-mapa

# 2. Consolidar e executar de uma só vez todos os notebooks em kernel limpo (Restart & Run All):
python src/consolidar_notebooks.py --forcar --executar

# (Caso o usuário peça explicitamente uma consolidação parcial antes de todas as trilhas existirem):
python src/consolidar_notebooks.py --permitir-faltantes --forcar --executar
```

### Auditoria do Relatório de Conformidade T3
Verifique na saída do script se todos os critérios de `docs/T3 Projeto Final Estatística PosDL.docx` foram atendidos:
- **Zero erros de execução** em kernel limpo (`Restart & Run All`);
- **Zero caminhos absolutos** no código e nas saídas (`AVISO: Possíveis caminhos absolutos` não deve aparecer);
- **Semente aleatória fixada** (`np.random.seed(42)` / `random_state=42`);
- **Objetividade e interpretação:** toda saída de código/gráfico possui célula Markdown interpretativa orientada ao cliente, e metadados burocráticos repetitivos foram higienizados.
