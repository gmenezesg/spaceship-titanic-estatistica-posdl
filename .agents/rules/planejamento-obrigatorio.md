# Rule: Planejamento Obrigatório Antes de Qualquer Tarefa

Todo agente operando neste repositório deve **planejar antes de executar qualquer tarefa**.

## Diretrizes Obrigatórias

1. **Investigação Prévia:** Antes de criar, modificar ou remover qualquer arquivo, leia os artefatos relevantes, identifique o ticket Jira associado (`KAN-XX`) e consulte seu mapeamento em `notebooks/consolidacao.json` (`python src/consolidar_notebooks.py --ticket KAN-XX`).
2. **Alinhamento com o T3:** Verifique como a tarefa atende aos objetivos de `docs/T3 Projeto Final Estatística PosDL.docx` (qualidade técnica 30%, clareza e objetividade 50%, organização e reprodutibilidade do notebook 20%).
3. **Plano Explícito:** Formule e apresente um plano de ação objetivo contendo:
   - Escopo e ticket Jira (`KAN-XX`);
   - Arquivo(s) de origem que serão criados ou editados (garantindo que `notebooks/00_projeto_final_estatistica.ipynb` não seja editado manualmente);
   - Etapas de implementação e verificação;
   - Etapa final de consolidação via Skill `consolidar-notebooks` (`src/consolidar_notebooks.py`).
