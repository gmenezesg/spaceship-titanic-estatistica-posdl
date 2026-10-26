# Rule: Padrão de Criação e Manutenção de Rules e Skills Multi-Agente

Toda criação ou atualização de **Rules** e **Skills** neste repositório deve seguir o princípio de **Fonte Única da Verdade (*Single Source of Truth*)** em [`.agents/`](../.agents/) e [`AGENTS.md`](../../AGENTS.md), garantindo compatibilidade integral entre **Linux, macOS e Windows** e zero duplicação de conteúdo entre agentes.

## Diretrizes Obrigatórias

1. **Fonte Única da Verdade (`.agents/`):**
   - **Novas Rules:** Devem ter seu conteúdo completo escrito **exclusivamente** em `.agents/rules/<nome-da-rule>.md`.
   - **Novas Skills:** Devem ter seu conteúdo completo escrito **exclusivamente** em `.agents/skills/<nome-da-skill>/SKILL.md` (com frontmatter YAML contendo `name` e `description`).
   - **Proibição de Duplicação:** Nunca copie o texto completo de rules ou skills para dentro de `.claude/`, `.cursor/`, `.opencode/`, `.github/`, `CLAUDE.md`, `GEMINI.md` ou `.windsurfrules`.

2. **Compatibilidade Multiplataforma (Linux, macOS e Windows):**
   - **Evite Symlinks (`ln -s`):** Não utilize links simbólicos do sistema operacional para rules/skills, pois no Windows (sem Modo de Desenvolvedor e `core.symlinks=true`) o Git converte symlinks em arquivos de texto plano contendo apenas o caminho relativo, quebrando a leitura pelos agentes.
   - **Use Stubs de Referência (`@caminho`):** Para agentes que exigem arquivos em diretórios próprios, crie apenas *stubs* mínimos contendo a diretiva `@caminho` apontando para `.agents/`:
     - **Cursor (`.cursor/rules/<nome-da-rule>.mdc`):** Crie apenas o cabeçalho YAML (`description`, `globs: "**/*"`, `alwaysApply: true`) seguido de `@.agents/rules/<nome-da-rule>.md`.
     - **Claude Code (`CLAUDE.md` e `.claude/commands/<nome-da-skill>.md`):** Adicione apenas a linha `@.agents/rules/<nome-da-rule>.md` (ou `@.agents/skills/<nome-da-skill>/SKILL.md`) para importação automática de contexto.
     - **Antigravity (`GEMINI.md`), Windsurf (`.windsurfrules`) e GitHub Copilot (`.github/copilot-instructions.md`):** Adicione apenas a referência de uma linha apontando para o novo arquivo em `.agents/rules/` ou `.agents/skills/`.
     - **OpenCode / Codex:** Leem `AGENTS.md` e `.agents/` nativamente (não crie pasta `.opencode/`).

3. **Checklist ao Criar ou Editar uma Rule ou Skill:**
   - [ ] Criar/editar o arquivo canônico em `.agents/rules/<nome>.md` ou `.agents/skills/<nome>/SKILL.md`;
   - [ ] Registrar a referência na lista de fontes de `AGENTS.md`;
   - [ ] Adicionar a linha `@.agents/...` nos stubs `CLAUDE.md`, `GEMINI.md`, `.windsurfrules`, `.github/copilot-instructions.md` e (para rules) criar o stub de 6 linhas em `.cursor/rules/<nome>.mdc`.
