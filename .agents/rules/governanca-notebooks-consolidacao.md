# Rule: Governança de Notebooks e Consolidação Sob Demanda (`KAN-37`)

Esta regra define:
1. **Conformidade preventiva obrigatória em todos os commits/PRs** dos notebooks de origem para garantir que a consolidação final ocorra de uma só vez e sem falhas;
2. **Execução da consolidação (`notebooks/00_projeto_final_estatistica.ipynb`) exclusivamente sob demanda** no encerramento do projeto (`KAN-37` / `KAN-43`) ou quando solicitada explicitamente pelo usuário, por meio da Skill [`consolidar-notebooks`](../skills/consolidar-notebooks/SKILL.md).

## 1. Conformidade Obrigatória em Todos os Commits (Preparação para Consolidação Única)

Para garantir que a consolidação final ocorra de uma só vez e sem conflitos ou retrabalho, **todo commit e PR de qualquer ticket Jira (`KAN-4` a `KAN-43`)** deve cumprir rigorosamente:

1. **Isolamento Estrito por Notebook de Origem (`notebooks/consolidacao.json`):**
   - Toda alteração de análise ou código referente a um ticket do Jira deve ser realizada **exclusivamente** no notebook ou artefato de origem mapeado em [`notebooks/consolidacao.json`](../../notebooks/consolidacao.json) (`python src/consolidar_notebooks.py --ticket KAN-XX`).
   - Caso um novo notebook seja criado para um ticket, registre-o em `secoes` (`notebooks` e `mapeamento_tickets`) e em `mapa_tickets_notebooks` dentro de `notebooks/consolidacao.json`, validando com:
     ```bash
     python src/consolidar_notebooks.py --validar-mapa
     ```
   - Notebooks das Seções 2 a 5 devem ler apenas `data/processed/spaceship_titanic_clean.csv`, sem repetir o pipeline de limpeza da Seção 1 (`notebooks/01_preparacao_dados.ipynb`).

2. **Proibição de Edição ou Commit de `notebooks/00_projeto_final_estatistica.ipynb` nas Trilhas:**
   - **JAMAIS edite `notebooks/00_projeto_final_estatistica.ipynb` manualmente** (`edit_file`, `write_file` ou scripts avulsos).
   - **NÃO inclua alterações em `notebooks/00_projeto_final_estatistica.ipynb` nos commits/PRs de tickets individuais das trilhas**, evitando conflitos de merge e inclusão prematura de seções em andamento.

3. **Checklist de Prontidão para Consolidação em Cada Notebook de Origem:**
   - **Zero caminhos absolutos** tanto no código-fonte quanto nas saídas renderizadas (`prints`, logs ou tabelas não devem exibir `/home/...`, `/Users/...`, `C:\...` — use sempre caminhos relativos à raiz do projeto);
   - **Semente aleatória fixada** (`np.random.seed(42)` / `random_state=42`);
   - **Execução limpa (*Restart & Run All*)** validada no próprio notebook de origem do ticket antes do commit;
   - **Clareza e objetividade T3:** toda saída numérica, tabela ou gráfico deve possuir interpretação imediata em Markdown voltada ao cliente;
   - **Teste opcional sem alterar o `00_`:** se desejar testar a compatibilidade com o consolidador durante o desenvolvimento, gere apenas um arquivo temporário ignorado pelo Git:
     ```bash
     python src/consolidar_notebooks.py --permitir-faltantes --forcar --saida notebooks/_previa_consolidado.ipynb
     ```

---

## 2. Consolidação Oficial Exclusivamente Sob Demanda (`consolidar-notebooks`)

1. **Não Execute Automaticamente a Cada Ticket:**
   - Agentes **NÃO** devem sobrescrever `notebooks/00_projeto_final_estatistica.ipynb` automaticamente ao final de tickets comuns.
2. **Quando Acionar a Skill `consolidar-notebooks`:**
   - Acione a Skill **[`consolidar-notebooks`](../skills/consolidar-notebooks/SKILL.md)** **apenas sob demanda**, isto é:
     - Quando o usuário solicitar explicitamente a consolidação do notebook final; ou
     - Na execução do ticket final de consolidação/entrega do projeto (`KAN-37` / `KAN-43`), gerando e validando de uma só vez o `notebooks/00_projeto_final_estatistica.ipynb` completo:
       ```bash
       python src/consolidar_notebooks.py --forcar --executar
       ```
