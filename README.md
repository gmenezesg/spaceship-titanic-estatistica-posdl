# Spaceship Titanic — Análise Estatística (Pós-Graduação em Deep Learning - CIn/UFPE)

Repositório oficial do projeto prático da disciplina de **Estatística** da Pós-Graduação em Deep Learning (CIn/UFPE), dedicado à análise exploratória, inferência estatística, testes de hipóteses e modelagem sobre o conjunto de dados **Spaceship Titanic**.

- **URL Oficial do Repositório:** [https://github.com/gmenezesg/spaceship-titanic-estatistica-posdl](https://github.com/gmenezesg/spaceship-titanic-estatistica-posdl)
- **Painel de Gestão (Jira):** [https://megamatic.atlassian.net/jira/software/projects/KAN/boards](https://megamatic.atlassian.net/browse/KAN-4)

---

## Equipe

| Integrante | Papel na Governança |
| :--- | :--- |
| **Daniela** | Análise Estatística e Revisão Cruzada |
| **Gustavo** | Gestão do Repositório / Jira, Preparação de Dados e Análise Estatística |
| **Helton** | Análise Estatística e Revisão Técnica de Estrutura/Dados |
| **Luciana** | Análise Estatística e Revisão do Quadro de Gestão |
| **Renatta** | Análise Estatística e Revisão do Fluxo de PRs/Branches |

---

## Arquitetura de Diretórios

```text
spaceship-titanic-estatistica-posdl/
├── data/
│   ├── raw/              # Dados brutos originais (imutáveis) do Spaceship Titanic
│   └── processed/        # Dados limpos, tratados e prontos para análise/modelagem
├── docs/
│   └── conclusoes/       # Documentação metodológica, dicionário de dados, atas e sínteses
├── notebooks/            # Jupyter Notebooks numerados por etapa analítica
├── src/                  # Módulos e funções auxiliares reutilizáveis em Python
├── report/               # Relatório técnico final, figuras exportadas e apresentação
├── .gitignore            # Regras de exclusão de caches, checkpoints e arquivos temporários
├── LICENSE               # Licença MIT
├── README.md             # Documentação principal do repositório
└── requirements.txt      # Dependências e bibliotecas Python do ambiente
```

---

## Configuração do Ambiente Local

### 1. Clonar o repositório

```bash
# Via HTTPS
git clone https://github.com/gmenezesg/spaceship-titanic-estatistica-posdl.git
cd spaceship-titanic-estatistica-posdl

# Ou via SSH
git clone git@github.com:gmenezesg/spaceship-titanic-estatistica-posdl.git
cd spaceship-titanic-estatistica-posdl
```

### 2. Criar e ativar o ambiente virtual (Python 3.10+)

```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux / macOS
# .venv\Scripts\activate   # Windows
```

### 3. Instalar as dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Fluxo de Trabalho (Git & Governança)

1. **Padrão de Branches:** `tipo/nome-membro-descricao`
   - Exemplos: `feature/helton-descritiva-visual`, `docs/daniela-testes-hipoteses`, `chore/gustavo-estrutura-inicial`
2. **Padrão de Commits:** Mensagens em português no formato `[Ticket-ID] Descrição clara da alteração`
   - Exemplo: `[KAN-5] Configurar estrutura inicial de pastas e ambiente Python`
3. **Pull Requests:** Toda alteração na branch `main` deve ser integrada via Pull Request com revisão em pares.

---

## Licença

Distribuído sob a licença **MIT**. Consulte o arquivo [`LICENSE`](LICENSE) para mais informações.
