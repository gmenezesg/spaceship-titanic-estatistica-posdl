# Rule: Governança de Notebooks e Consolidação Obrigatória (`KAN-37`)

Esta regra garante que cada funcionalidade do Jira tenha como alvo seu próprio notebook e que a consolidação em `notebooks/00_projeto_final_estatistica.ipynb` seja rigorosamente cumprida.

## Diretrizes Obrigatórias

1. **Mapeamento Ticket $\rightarrow$ Notebook (`notebooks/consolidacao.json`):**
   - Toda alteração de análise ou código referente a um ticket do Jira (`KAN-10` a `KAN-34`) deve ser realizada **exclusivamente** no notebook de origem mapeado em `notebooks/consolidacao.json`.
   - Caso um novo notebook por ticket seja criado, ele deve ser registrado em `secoes` (`notebooks` e `mapeamento_tickets`) e em `mapa_tickets_notebooks` dentro de `notebooks/consolidacao.json`.

2. **Bloqueio de Edição Manual em `notebooks/00_projeto_final_estatistica.ipynb`:**
   - **JAMAIS edite `notebooks/00_projeto_final_estatistica.ipynb` diretamente** (não use `edit_file`, `write_file` ou scripts avulsos sobre ele).
   - O arquivo `notebooks/00_projeto_final_estatistica.ipynb` **só pode ser alterado pela Skill `consolidar-notebooks` / script `src/consolidar_notebooks.py`**.

3. **Chamada da Skill e Lembrete ao Final de Todo Ticket Jira:**
   - Ao finalizar a implementação de qualquer ticket do Jira:
     1. Ative e execute a Skill **`consolidar-notebooks`** (`python src/consolidar_notebooks.py --permitir-faltantes --forcar --executar`).
     2. **Lembre sempre o usuário** ao final da resposta para executar a Skill `consolidar-notebooks` / `src/consolidar_notebooks.py` antes do commit/PR final.
