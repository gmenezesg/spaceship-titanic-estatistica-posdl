# Guia de Contribuição e Governança Git (`KAN-6`)

Este documento formaliza o fluxo de trabalho com Git e GitHub para o projeto **Spaceship Titanic — Estatística (Pós-Graduação em Deep Learning - CIn/UFPE)**, garantindo rastreabilidade com o Jira, integridade da branch `main` e revisão em pares.

---

## 1. Regras de Proteção da Branch `main`

- A branch `main` representa a versão estável e auditável do projeto.
- **Push direto bloqueado:** Nenhuma alteração deve ser enviada diretamente para a `main`.
- **Pull Request obrigatório:** Toda entrega deve vir de uma branch de trabalho via Pull Request (PR).
- **Revisão em Pares (Peer Review):** Cada PR exige pelo menos **1 aprovação (`Approve`)** do revisor dedicado definido no card do Jira antes do merge.

---

## 2. Convenção de Nomenclatura de Branches

Formato obrigatório:
```text
<tipo>/<nome-membro>-<descricao-curta>
```

### Tipos permitidos:
| Prefixo (`tipo`) | Uso | Exemplo |
| :--- | :--- | :--- |
| `feature/` | Análises estatísticas, notebooks, scripts e visualizações | `feature/helton-descritiva-visual` |
| `docs/` | Documentação, dicionário de dados, atas e conclusões | `docs/daniela-testes-hipoteses` |
| `fix/` | Correções em notebooks, cálculos, gráficos ou textos | `fix/luciana-ajuste-intervalo-confianca` |
| `chore/` | Configuração de ambiente, estrutura e governança | `chore/gustavo-regras-git` |
| `report/` | Consolidação do relatório técnico final | `report/renatta-revisao-relatorio` |

**Regras adicionais:**
- Usar apenas letras minúsculas, sem acentos ou espaços, separando palavras por hífen (`-`).

---

## 3. Convenção de Mensagens de Commit

Todas as mensagens de commit devem ser escritas em **português** e iniciar com o identificador do ticket do Jira entre colchetes:

```text
[Ticket-ID] Descrição clara da alteração
```

### Exemplos válidos:
- `[KAN-6] Padronizar fluxo de branches, commits e pull requests`
- `[KAN-10] Criar dicionário de dados e tipagem das variáveis no notebook 01`
- `[KAN-15] Implementar análise descritiva e boxplots de gastos a bordo`

---

## 4. Fluxo Passo a Passo para Entregas (Pull Request)

1. **Atualizar a branch `main` local:**
   ```bash
   git checkout main
   git pull origin main
   ```
2. **Criar a branch da tarefa:**
   ```bash
   git checkout -b tipo/seu-nome-descricao-curta
   ```
3. **Realizar as alterações e commitar com a referência do Jira:**
   ```bash
   git add .
   git commit -m "[KAN-XX] Descrição clara da alteração"
   ```
4. **Enviar a branch para o GitHub:**
   ```bash
   git push -u origin tipo/seu-nome-descricao-curta
   ```
5. **Abrir o Pull Request:**
   - Pelo GitHub Web ou via CLI (`gh pr create`).
   - Preencher o template de PR, vincular o ticket `KAN-XX` e atribuir o **Revisor Dedicado** conforme indicado na seção de Governança do card no Jira.
6. **Revisão e Merge:**
   - Após a aprovação pelo revisor dedicado, realizar o merge (`Squash and merge` ou `Merge pull request`) para a `main`.

---

## 5. Consolidação Obrigatória Antes do PR

O notebook final [`notebooks/00_projeto_final_estatistica.ipynb`](notebooks/00_projeto_final_estatistica.ipynb) é **gerado automaticamente** e **nunca deve ser editado à mão**. Antes de abrir ou atualizar um Pull Request:

1. **Implemente a alteração apenas no notebook de origem do ticket.** Consulte o mapeamento com:
   ```bash
   python src/consolidar_notebooks.py --ticket KAN-XX
   ```
2. **Valide o manifesto de tickets e notebooks:**
   ```bash
   python src/consolidar_notebooks.py --validar-mapa
   ```
3. **Consolide e execute o notebook final do início ao fim:**
   ```bash
   python src/consolidar_notebooks.py --permitir-faltantes --forcar --executar
   ```
   Na entrega final, quando todos os notebooks das trilhas estiverem presentes, remova `--permitir-faltantes`:
   ```bash
   python src/consolidar_notebooks.py --forcar --executar
   ```
4. **Confira o relatório de conformidade:** zero erros de execução, zero caminhos absolutos nas células e nas saídas, semente fixada (`seed(42)` / `random_state=42`) e toda saída acompanhada de interpretação em Markdown.

Consulte o passo a passo completo em [`docs/guia_consolidacao.md`](docs/guia_consolidacao.md) e as regras em [`.agents/skills/consolidar-notebooks/SKILL.md`](.agents/skills/consolidar-notebooks/SKILL.md).
