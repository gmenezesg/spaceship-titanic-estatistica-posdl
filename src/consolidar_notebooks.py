#!/usr/bin/env python3
"""
Consolida os notebooks das trilhas em um único notebook final (KAN-37),
alinhado aos objetivos e critérios de avaliação de `docs/T3 Projeto Final Estatística PosDL.docx`.

REGRA DE OURO:
O arquivo `notebooks/00_projeto_final_estatistica.ipynb` é GERADO exclusivamente por
este script (ou pela skill `consolidar-notebooks`) a partir dos notebooks de cada
ticket/trilha mapeados em `notebooks/consolidacao.json`. Nunca edite o `00_` à mão.

Uso (a partir da raiz do repositório):

    # Consultar qual notebook/arquivo deve ser alterado para um ticket Jira
    python src/consolidar_notebooks.py --ticket KAN-19

    # Validar todos os mapeamentos de tickets Jira em notebooks/consolidacao.json
    python src/consolidar_notebooks.py --validar-mapa

    # Prévia com os notebooks que já existem na branch atual
    python src/consolidar_notebooks.py --permitir-faltantes --forcar --executar

    # Gerar e executar o notebook final oficial (quando todos os notebooks existirem)
    python src/consolidar_notebooks.py --forcar --executar
"""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from datetime import date
from pathlib import Path

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

RAIZ = Path(__file__).resolve().parent.parent
MANIFESTO_PADRAO = RAIZ / "notebooks" / "consolidacao.json"
TAG_PULAR = "pular-consolidacao"

# Padrões de caminho absoluto que quebram a reprodutibilidade em outra máquina.
PADRAO_CAMINHO_ABSOLUTO = re.compile(
    r"""["'](?:[A-Za-z]:[\\/]|/home/|/Users/|/mnt/|/content/drive/)"""
)

# Caminhos absolutos em textos de saída não vêm necessariamente entre aspas
# (ex.: "Diretório resolvido: /home/usuario/projeto/data").
PADRAO_CAMINHO_ABSOLUTO_TEXTO = re.compile(
    r"(?:(?<![A-Za-z0-9])[A-Za-z]:[\\/]|/home/|/Users/|/mnt/|/content/drive/)"
)

# Padrão de semente aleatória para auditoria de reprodutibilidade (KAN-37 / T3).
PADRAO_SEMENTE = re.compile(r"(?:seed\s*\(\s*42\s*\)|random_state\s*=\s*42)")

# Linhas administrativas de governança interna de PR/Jira que poluem a leitura objetiva do T3.
PADROES_LINHAS_BOILERPLATE = [
    re.compile(r"^\s*-\s*\*\*Notebook (?:Mestre Consolidado|da Trilha):\*\*.*$", re.IGNORECASE),
    re.compile(r"^\s*-\s*\*\*Responsável Principal.*:\*\*.*$", re.IGNORECASE),
    re.compile(r"^\s*-\s*\*\*Revisor(?:a)? Dedicad[oa].*:\*\*.*$", re.IGNORECASE),
    re.compile(r"^\s*\*\*Respons[aá]vel:\*\*.*$", re.IGNORECASE),
    re.compile(r"^\s*\*\*Revisor(?:a)?(?:\s+dedicad[oa])?:\*\*.*$", re.IGNORECASE),
    re.compile(r"^\s*\*\*Status:\*\*.*$", re.IGNORECASE),
    re.compile(r"^\s*\|\s*\*\*(?:Projeto|Ticket|Tickets|Prioridade|Responsável|Revisor|Revisora|Dependência|Dependências|Status)\*\*.*\|.*$", re.IGNORECASE),
]

# Subseções internas de controle de ticket que não agregam ao entregável acadêmico/cliente (T3).
PADRAO_SECOES_BOILERPLATE = re.compile(
    r"(?ms)^#{2,4}\s+(?:Checklist do ticket\b.*|8\.\s*Limite desta entrega e pr[oó]ximos passos\b.*|Por que a KAN-17 deve ser executada.*)(?=^#{1,3}\s+|\Z)"
)


def carregar_manifesto(caminho: Path) -> dict:
    with open(caminho, encoding="utf-8") as arquivo:
        manifesto = json.load(arquivo)
    if not manifesto.get("secoes"):
        raise ValueError(f"Manifesto sem seções: {caminho}")
    return manifesto


def validar_manifesto(manifesto: dict) -> tuple[bool, list[str], list[str]]:
    """Valida a integridade e completude do mapeamento de tickets Jira no manifesto."""
    erros: list[str] = []
    avisos: list[str] = []

    mapa_global = manifesto.get("mapa_tickets_notebooks", {})
    outros_tickets = manifesto.get("mapa_outros_tickets", {})
    tickets_secoes: dict[str, str] = {}

    for secao in manifesto.get("secoes", []):
        titulo_secao = secao.get("titulo", "<sem título>")
        tickets = secao.get("tickets", [])
        notebooks = secao.get("notebooks", [])
        mapeamento = secao.get("mapeamento_tickets", {})

        if not tickets:
            erros.append(f"Seção '{titulo_secao}' não possui tickets vinculados.")
        if not notebooks:
            erros.append(f"Seção '{titulo_secao}' não possui notebooks vinculados.")
        if not secao.get("objetivo_t3"):
            avisos.append(f"Seção '{titulo_secao}' não define 'objetivo_t3' (alinhamento com T3 docx).")

        for t in tickets:
            if t in tickets_secoes:
                erros.append(f"Ticket {t} duplicado entre '{tickets_secoes[t]}' e '{titulo_secao}'.")
            tickets_secoes[t] = titulo_secao

            if mapeamento and t not in mapeamento:
                erros.append(f"Ticket {t} listado na seção '{titulo_secao}', mas ausente em 'mapeamento_tickets'.")
            elif mapeamento and t in mapeamento:
                nb_map = mapeamento[t].get("notebook")
                if nb_map not in notebooks:
                    erros.append(
                        f"Ticket {t} aponta para '{nb_map}' em 'mapeamento_tickets', "
                        f"mas esse arquivo não consta em 'notebooks' da seção '{titulo_secao}'."
                    )
                if mapa_global and mapa_global.get(t) != nb_map:
                    erros.append(
                        f"Inconsistência para {t}: 'mapa_tickets_notebooks' tem '{mapa_global.get(t)}', "
                        f"mas a seção tem '{nb_map}'."
                    )

        for nb in notebooks:
            if mapeamento:
                usados = {info.get("notebook") for info in mapeamento.values()}
                if nb not in usados:
                    erros.append(f"Notebook '{nb}' na seção '{titulo_secao}' não está associado a nenhum ticket.")

    # Verifica cobertura de todos os 40 tickets operacionais do projeto (KAN-4 a KAN-43)
    todos_mapeados = set(tickets_secoes.keys()) | set(mapa_global.keys()) | set(outros_tickets.keys())
    esperados = {f"KAN-{i}" for i in range(4, 44)}
    faltantes_jira = sorted(esperados - todos_mapeados, key=lambda x: int(x.split("-")[1]))
    if faltantes_jira:
        erros.append(f"Tickets do Jira (KAN-4..KAN-43) sem mapeamento no manifesto: {', '.join(faltantes_jira)}")

    return len(erros) == 0, erros, avisos


def consultar_ticket(manifesto: dict, ticket: str) -> int:
    """Exibe informações detalhadas de mapeamento para um ticket específico do Jira."""
    ticket = ticket.strip().upper()
    saida_mestre = manifesto.get("saida", "notebooks/00_projeto_final_estatistica.ipynb")

    for secao in manifesto.get("secoes", []):
        mapeamento = secao.get("mapeamento_tickets", {})
        if ticket in mapeamento or ticket in secao.get("tickets", []):
            info = mapeamento.get(ticket, {})
            nb_alvo = info.get("notebook") or manifesto.get("mapa_tickets_notebooks", {}).get(ticket)
            resumo = info.get("resumo", "Tarefa analítica")
            extras = info.get("artefatos_extras", [])
            print(f"Ticket Jira      : {ticket} — {resumo}")
            print(f"Seção T3         : {secao.get('titulo')}")
            print(f"Notebook-Alvo    : {nb_alvo}")
            if extras:
                print(f"Artefatos Extras : {', '.join(extras)}")
            print(f"Notebook Mestre  : {saida_mestre} (NÃO EDITAR À MÃO)")
            print(
                "\nFluxo Obrigatório:\n"
                f"  1. Implemente as alterações exclusivamente em `{nb_alvo}`.\n"
                f"  2. Ao concluir o ticket {ticket}, consolide executando:\n"
                f"     python src/consolidar_notebooks.py --permitir-faltantes --forcar --executar"
            )
            return 0

    if ticket == manifesto.get("ticket_consolidacao", "KAN-37"):
        print(f"Ticket Jira      : {ticket} — Consolidação dos notebooks num notebook final")
        print(f"Script Oficial   : {manifesto.get('script_consolidador', 'src/consolidar_notebooks.py')}")
        print(f"Saída Gerada     : {saida_mestre}")
        return 0

    outros = manifesto.get("mapa_outros_tickets", {})
    if ticket in outros:
        info = outros[ticket]
        print(f"Ticket Jira      : {ticket} — {info.get('resumo')}")
        print(f"Tipo de Entrega  : {info.get('tipo')}")
        print(f"Arquivo-Alvo     : {info.get('alvo')}")
        if info.get("notebook_origem"):
            print(f"Notebook Base    : {info.get('notebook_origem')}")
        print(
            "\nLembrete: Caso qualquer ajuste seja feito no notebook base, "
            "execute a consolidação (`python src/consolidar_notebooks.py --permitir-faltantes --forcar --executar`)."
        )
        return 0

    print(f"ERRO: Ticket '{ticket}' não encontrado em {MANIFESTO_PADRAO.name}.", file=sys.stderr)
    return 1


def limpar_markdown_objetivo(texto: str) -> str:
    """
    Higieniza metadados burocráticos repetitivos (tabelas de governança de PR,
    checklists internos de ticket) para manter o notebook consolidado objetivo
    e focado nos entregáveis de `docs/T3 Projeto Final Estatística PosDL.docx`.
    """
    texto_limpo = PADRAO_SECOES_BOILERPLATE.sub("", texto)
    linhas_filtradas: list[str] = []
    em_tabela_governanca = False

    for linha in texto_limpo.splitlines():
        if any(p.match(linha) for p in PADROES_LINHAS_BOILERPLATE):
            if linha.strip().startswith("|"):
                em_tabela_governanca = True
            continue
        if em_tabela_governanca:
            # Pula cabeçalho vazio "| | |" ou separador "|---|---|" de tabela de governança
            if re.match(r"^\s*\|\s*(?:-+\s*\|\s*-+|)\s*\|\s*$", linha):
                continue
            em_tabela_governanca = False
        linhas_filtradas.append(linha)

    # Remove cabeçalho vazio "| | |\n|---|---|" que tenha sobrado sem linhas
    resultado = "\n".join(linhas_filtradas)
    resultado = re.sub(r"(?m)^\s*\|\s*\|\s*\|\s*\n\s*\|[-:\s|]+\|\s*\n?", "", resultado)
    # Comprime múltiplas quebras de linha ou divisores "---" consecutivos
    resultado = re.sub(r"(?:\n\s*---\s*\n){2,}", "\n\n---\n\n", resultado)
    resultado = re.sub(r"\n{3,}", "\n\n", resultado)
    return resultado.strip()


def normalizar_codigo_para_dedup(fonte: str) -> str:
    """Normaliza código ignorando linhas em branco e comentários decorativos para deduplicação."""
    linhas = []
    for linha in fonte.splitlines():
        s = linha.strip()
        if not s or s.startswith("# ==="):
            continue
        linhas.append(s)
    return "\n".join(linhas)


def registrar_caminho_absoluto(relatorio: dict, ocorrencia: str) -> None:
    """Registra um caminho absoluto evitando avisos duplicados no relatório."""
    if ocorrencia not in relatorio["caminhos_absolutos"]:
        relatorio["caminhos_absolutos"].append(ocorrencia)


def _juntar_texto(valor) -> str:
    """Converte campos de saída (str ou lista de str) em um único texto."""
    if isinstance(valor, list):
        return "".join(str(parte) for parte in valor)
    return str(valor or "")


def _texto_de_saida(saida) -> str:
    """Extrai o texto auditável de uma saída de célula do Jupyter."""
    tipo = saida.get("output_type")
    if tipo == "stream":
        return _juntar_texto(saida.get("text", ""))
    if tipo in ("execute_result", "display_data", "update_display_data"):
        dados = saida.get("data", {})
        return "\n".join(
            _juntar_texto(dados.get(chave, "")) for chave in ("text/plain", "text/html")
        )
    if tipo == "error":
        return _juntar_texto(saida.get("traceback", []))
    return ""


def auditar_caminhos_nas_saidas(celulas, relatorio: dict, rotulo: str) -> None:
    """Audita caminhos absolutos nas saídas das células (inclusive sem aspas)."""
    for celula in celulas:
        if getattr(celula, "cell_type", None) != "code":
            continue
        for saida in getattr(celula, "outputs", []) or []:
            for linha in _texto_de_saida(saida).splitlines():
                if PADRAO_CAMINHO_ABSOLUTO_TEXTO.search(linha):
                    registrar_caminho_absoluto(
                        relatorio, f"{rotulo} (saída): {linha.strip()}"
                    )


def celula_cabecalho_geral(manifesto: dict) -> nbformat.NotebookNode:
    linhas = [
        f"# {manifesto.get('titulo', 'Projeto Final')}",
        "",
        "> **Notebook Mestre Consolidado (`KAN-37`)** — Gerado automaticamente por "
        f"`src/consolidar_notebooks.py` em {date.today().strftime('%d/%m/%Y')}.  ",
        "> **Atenção:** **Não edite este arquivo diretamente.** Qualquer alteração deve ser "
        "feita no notebook específico do ticket Jira (mapeado em `notebooks/consolidacao.json`) "
        "seguida da execução da skill/script de consolidação.",
        "",
        "## Objetivo e Estrutura Analítica (`T3 Projeto Final Estatística PosDL`)",
        "",
        "Este estudo integra de ponta a ponta a análise estatística e probabilística do conjunto de dados "
        "**Spaceship Titanic**, estruturado de forma objetiva e reprodutível nas seguintes etapas:",
        "",
        "| Seção | Etapa Analítica | Tickets Jira | Notebooks de Origem |",
        "| :--- | :--- | :--- | :--- |",
    ]
    for idx, secao in enumerate(manifesto["secoes"], start=1):
        tickets = ", ".join(f"`{t}`" for t in secao.get("tickets", []))
        nbs = ", ".join(f"`{Path(n).name}`" for n in secao.get("notebooks", []))
        linhas.append(f"| **{idx}** | {secao['titulo']} | {tickets} | {nbs} |")
    return new_markdown_cell("\n".join(linhas))


def celula_cabecalho_secao(secao: dict, presentes: list[str], faltantes: list[str]) -> nbformat.NotebookNode:
    linhas = ["---", f"# {secao['titulo']}", ""]
    if secao.get("objetivo_t3"):
        linhas.append(f"**Objetivo Analítico (T3):** {secao['objetivo_t3']}  ")
    if secao.get("tickets"):
        links = [
            f"[{t}](https://megamatic.atlassian.net/browse/{t})" for t in secao["tickets"]
        ]
        linhas.append(f"**Tickets Jira:** {' · '.join(links)}  ")
    if presentes:
        linhas.append("**Notebooks Consolidados:** " + " · ".join(f"`{p}`" for p in presentes))
    if faltantes:
        linhas += [
            "",
            "> **Nota:** Seção parcialmente consolidada nesta prévia. Notebooks pendentes de merge: "
            + ", ".join(f"`{f}`" for f in faltantes),
        ]
    return new_markdown_cell("\n".join(linhas))


def copiar_celulas(
    caminho: Path,
    codigos_vistos: set[str],
    relatorio: dict,
    modo_objetivo: bool = True,
    preservar_saidas: bool = True,
) -> list:
    nb = nbformat.read(caminho, as_version=4)
    copiadas = []
    for celula in nb.cells:
        tags = celula.get("metadata", {}).get("tags", [])
        if TAG_PULAR in tags:
            relatorio["puladas_tag"] += 1
            continue

        if celula.cell_type == "code":
            fonte = celula.source.strip()
            if not fonte:
                continue
            chave_dedup = normalizar_codigo_para_dedup(fonte)
            if not chave_dedup or chave_dedup in codigos_vistos:
                relatorio["puladas_duplicadas"] += 1
                continue
            codigos_vistos.add(chave_dedup)

            for linha in fonte.splitlines():
                if PADRAO_CAMINHO_ABSOLUTO.search(linha):
                    registrar_caminho_absoluto(
                        relatorio, f"{caminho.name} (código): {linha.strip()}"
                    )
            if PADRAO_SEMENTE.search(fonte):
                relatorio["sementes_fixadas"] += 1

            nova_celula = new_code_cell(celula.source)
            if preservar_saidas and celula.get("outputs"):
                nova_celula.outputs = copy.deepcopy(celula.outputs)
                relatorio["contador_execucao"] += 1
                nova_celula.execution_count = relatorio["contador_execucao"]
            copiadas.append(nova_celula)
            relatorio["total_codigo"] += 1

        elif celula.cell_type == "markdown":
            texto = celula.source.strip()
            if not texto:
                continue
            if modo_objetivo:
                texto_limpo = limpar_markdown_objetivo(texto)
                if texto_limpo != texto:
                    relatorio["celulas_higienizadas"] += 1
                texto = texto_limpo
            if not texto or texto == "---":
                continue
            copiadas.append(new_markdown_cell(texto))
            relatorio["total_markdown"] += 1
        # células "raw" são descartadas: não fazem parte da análise

    if preservar_saidas:
        # As saídas copiadas também precisam ser auditadas: caminhos absolutos
        # podem aparecer em prints/DataFrames e quebrar a reprodutibilidade.
        auditar_caminhos_nas_saidas(copiadas, relatorio, caminho.name)

    relatorio["por_notebook"][caminho.name] = len(copiadas)
    return copiadas


def consolidar(
    manifesto: dict,
    permitir_faltantes: bool,
    modo_objetivo: bool = True,
    preservar_saidas: bool = True,
) -> tuple[nbformat.NotebookNode, dict]:
    relatorio = {
        "por_notebook": {},
        "faltantes": [],
        "puladas_tag": 0,
        "puladas_duplicadas": 0,
        "celulas_higienizadas": 0,
        "caminhos_absolutos": [],
        "sementes_fixadas": 0,
        "total_codigo": 0,
        "total_markdown": 0,
        "contador_execucao": 0,
    }

    presentes_totais = []
    for secao in manifesto["secoes"]:
        for relativo in secao["notebooks"]:
            if (RAIZ / relativo).exists():
                presentes_totais.append(relativo)
            else:
                relatorio["faltantes"].append(relativo)

    if not presentes_totais:
        raise FileNotFoundError(
            "Nenhum dos notebooks de origem listados no manifesto foi encontrado em disco. "
            "Operação abortada para proteger o notebook consolidado."
        )

    if relatorio["faltantes"] and not permitir_faltantes:
        lista = "\n  - ".join(relatorio["faltantes"])
        raise FileNotFoundError(
            "Notebooks do manifesto não encontrados:\n  - " + lista +
            "\nUse --permitir-faltantes para gerar uma consolidação parcial com os notebooks já disponíveis."
        )

    celulas = [celula_cabecalho_geral(manifesto)]
    codigos_vistos: set[str] = set()

    for secao in manifesto["secoes"]:
        presentes = [r for r in secao["notebooks"] if (RAIZ / r).exists()]
        faltantes = [r for r in secao["notebooks"] if r not in presentes]
        celulas.append(celula_cabecalho_secao(secao, presentes, faltantes))
        for relativo in presentes:
            celulas += copiar_celulas(
                RAIZ / relativo,
                codigos_vistos,
                relatorio,
                modo_objetivo=modo_objetivo,
                preservar_saidas=preservar_saidas,
            )

    nb = new_notebook(cells=celulas)
    nb.metadata["kernelspec"] = {"display_name": "Python 3", "language": "python", "name": "python3"}
    nb.metadata["language_info"] = {"name": "python"}
    return nb, relatorio


def executar(nb: nbformat.NotebookNode, pasta_trabalho: Path, timeout: int) -> None:
    from nbclient import NotebookClient

    cliente = NotebookClient(
        nb,
        timeout=timeout,
        kernel_name="python3",
        resources={"metadata": {"path": str(pasta_trabalho)}},
    )
    cliente.execute()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Consolida os notebooks das trilhas em um único notebook final (KAN-37 / T3)."
    )
    parser.add_argument("--manifesto", type=Path, default=MANIFESTO_PADRAO,
                        help="arquivo JSON com o mapeamento das seções e tickets")
    parser.add_argument("--saida", type=Path, default=None,
                        help="notebook de saída (padrão: o definido no manifesto)")
    parser.add_argument("--forcar", action="store_true",
                        help="sobrescreve o notebook de saída se ele já existir")
    parser.add_argument("--executar", action="store_true",
                        help="executa o notebook final do início ao fim (Restart & Run All) e salva as saídas")
    parser.add_argument("--limpar-saidas", action="store_true",
                        help="descarta as saídas pré-existentes quando --executar não é informado")
    parser.add_argument("--permitir-faltantes", action="store_true",
                        help="gera mesmo se algum notebook do manifesto ainda não existir na branch atual")
    parser.add_argument("--manter-boilerplate", action="store_true",
                        help="mantém tabelas administrativas de governança de tickets sem higienização")
    parser.add_argument("--validar-mapa", action="store_true",
                        help="apenas valida a completude do mapeamento de tickets Jira no manifesto")
    parser.add_argument("--ticket", type=str, default=None,
                        help="consulta o notebook/artefato alvo para um ticket Jira específico (ex: KAN-19)")
    parser.add_argument("--timeout", type=int, default=600,
                        help="tempo máximo por célula ao executar, em segundos")
    args = parser.parse_args()

    manifesto = carregar_manifesto(args.manifesto)

    if args.ticket:
        return consultar_ticket(manifesto, args.ticket)

    ok_mapa, erros_mapa, avisos_mapa = validar_manifesto(manifesto)
    if args.validar_mapa:
        if erros_mapa:
            print("ERRO na validação do manifesto:", file=sys.stderr)
            for e in erros_mapa:
                print(f"  - {e}", file=sys.stderr)
            return 1
        print(f"Manifesto '{args.manifesto.name}' validado com sucesso!")
        print(f"  - Seções analíticas T3 : {len(manifesto.get('secoes', []))}")
        print(f"  - Tickets de notebook  : {len(manifesto.get('mapa_tickets_notebooks', {}))}")
        print(f"  - Outros tickets Jira  : {len(manifesto.get('mapa_outros_tickets', {}))}")
        for a in avisos_mapa:
            print(f"  AVISO: {a}")
        return 0

    if not ok_mapa:
        print("ERRO de integridade no manifesto de consolidação:", file=sys.stderr)
        for e in erros_mapa:
            print(f"  - {e}", file=sys.stderr)
        return 1

    saida = args.saida or (RAIZ / manifesto["saida"])
    saida = saida if saida.is_absolute() else (Path.cwd() / saida)

    origens = {(RAIZ / r).resolve() for s in manifesto["secoes"] for r in s["notebooks"]}
    if saida.resolve() in origens:
        print(f"ERRO: a saída {saida.name} também é um notebook de origem.", file=sys.stderr)
        return 1
    if saida.exists() and not args.forcar:
        print(f"ERRO: {saida} já existe. Use --forcar para sobrescrever.", file=sys.stderr)
        return 1

    preservar_saidas = not args.limpar_saidas and not args.executar
    try:
        nb, relatorio = consolidar(
            manifesto,
            permitir_faltantes=args.permitir_faltantes,
            modo_objetivo=not args.manter_boilerplate,
            preservar_saidas=preservar_saidas,
        )
    except FileNotFoundError as erro:
        print(f"ERRO: {erro}", file=sys.stderr)
        return 1

    print("=== Relatório de Consolidação (KAN-37 / T3) ===")
    print("Células copiadas por notebook:")
    for nome, quantidade in relatorio["por_notebook"].items():
        print(f"  {nome:<48} {quantidade:>3}")
    print(f"Total de células (Código / Markdown interpretativo): {relatorio['total_codigo']} / {relatorio['total_markdown']}")
    print(f"Puladas pela tag '{TAG_PULAR}': {relatorio['puladas_tag']}")
    print(f"Puladas por código duplicado: {relatorio['puladas_duplicadas']}")
    print(f"Células higienizadas (modo objetivo T3): {relatorio['celulas_higienizadas']}")

    # Auditoria de conformidade com o T3
    if relatorio["total_markdown"] < relatorio["total_codigo"]:
        print(
            "AVISO T3: Há menos células interpretativas (Markdown) do que células de código. "
            "Lembre-se de interpretar todos os resultados para o cliente."
        )
    if relatorio["sementes_fixadas"] == 0:
        print("AVISO T3: Nenhuma fixação explícita de semente aleatória (seed=42) detectada.")
    if relatorio["faltantes"]:
        print("AVISO: Notebooks ainda não disponíveis nesta branch (seções marcadas como parciais):")
        for faltante in relatorio["faltantes"]:
            print(f"  - {faltante}")

    if args.executar:
        print("Executando o notebook do início ao fim (Restart & Run All)...")
        try:
            executar(nb, saida.parent, args.timeout)
        except Exception as erro:  # noqa: BLE001 - relata qualquer falha de célula
            print(f"ERRO na execução: {erro}", file=sys.stderr)
            return 1
        print("Execução concluída sem erros.")
        # Audita as saídas geradas pela execução (prints, DataFrames etc.).
        auditar_caminhos_nas_saidas(nb.cells, relatorio, "notebook final")

    if relatorio["caminhos_absolutos"]:
        print("AVISO: Possíveis caminhos absolutos (quebram a reprodutibilidade):")
        for ocorrencia in relatorio["caminhos_absolutos"]:
            print(f"  - {ocorrencia}")

    saida.parent.mkdir(parents=True, exist_ok=True)
    nbformat.write(nb, saida)
    caminho_exibicao = saida.relative_to(RAIZ) if saida.is_relative_to(RAIZ) else saida
    print(f"Notebook consolidado salvo com sucesso em: {caminho_exibicao}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
