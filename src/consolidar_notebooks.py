"""
Consolida os notebooks das trilhas em um único notebook final (KAN-37).

O notebook final é GERADO por este script a partir dos notebooks de cada trilha,
na ordem definida em `notebooks/consolidacao.json`. Ninguém precisa editá-lo à
mão: para corrigir algo, edite o notebook de origem e rode o script de novo.

Uso (a partir da raiz do repositório):

    # Gera o notebook final (recusa sobrescrever um arquivo existente)
    python src/consolidar_notebooks.py

    # Regenera, sobrescrevendo o notebook final
    python src/consolidar_notebooks.py --forcar

    # Gera e executa de ponta a ponta ("Restart & Run All"), salvando as saídas
    python src/consolidar_notebooks.py --forcar --executar

    # Prévia com os notebooks que já existem, em outro arquivo
    python src/consolidar_notebooks.py --permitir-faltantes --saida notebooks/_previa_consolidado.ipynb

O que o script faz:
  1. Lê o manifesto (ordem das seções e notebooks de origem).
  2. Para cada seção, insere um cabeçalho com título, tickets e arquivos de origem.
  3. Copia as células de cada notebook, sem saídas e sem contadores de execução.
  4. Pula células marcadas com a tag `pular-consolidacao`, para o autor excluir
     blocos que não devem ir para a entrega (rascunhos, configuração repetida).
  5. Pula células de código idênticas a uma já incluída, como imports repetidos.
  6. Verifica caminhos absolutos no código (critério de aceitação da KAN-37).
  7. Opcionalmente executa o notebook final do início ao fim.

Requisitos: nbformat e nbclient (instalados com o pacote `jupyter` do requirements.txt).
"""

from __future__ import annotations

import argparse
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


def carregar_manifesto(caminho: Path) -> dict:
    with open(caminho, encoding="utf-8") as arquivo:
        manifesto = json.load(arquivo)
    if not manifesto.get("secoes"):
        raise ValueError(f"Manifesto sem seções: {caminho}")
    return manifesto


def celula_cabecalho_geral(manifesto: dict) -> nbformat.NotebookNode:
    linhas = [
        f"# {manifesto.get('titulo', 'Projeto Final')}",
        "",
        "> **Notebook gerado automaticamente** por `src/consolidar_notebooks.py` "
        f"em {date.today().strftime('%d/%m/%Y')}. **Não edite este arquivo:** "
        "corrija o notebook de origem indicado em cada seção e rode o script novamente.",
        "",
        "## Sumário",
        "",
    ]
    for secao in manifesto["secoes"]:
        tickets = ", ".join(secao.get("tickets", []))
        linhas.append(f"- **{secao['titulo']}**" + (f" ({tickets})" if tickets else ""))
    return new_markdown_cell("\n".join(linhas))


def celula_cabecalho_secao(secao: dict, presentes: list[str], faltantes: list[str]) -> nbformat.NotebookNode:
    linhas = ["---", f"# {secao['titulo']}", ""]
    if secao.get("tickets"):
        links = [
            f"[{t}](https://megamatic.atlassian.net/browse/{t})" for t in secao["tickets"]
        ]
        linhas.append(f"**Tickets:** {' · '.join(links)}  ")
    if presentes:
        linhas.append("**Origem:** " + " · ".join(f"`{p}`" for p in presentes))
    if faltantes:
        linhas += [
            "",
            "> **Seção incompleta nesta geração.** Notebooks ainda não disponíveis: "
            + ", ".join(f"`{f}`" for f in faltantes),
        ]
    return new_markdown_cell("\n".join(linhas))


def copiar_celulas(caminho: Path, codigos_vistos: set[str], relatorio: dict) -> list:
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
            if fonte in codigos_vistos:
                relatorio["puladas_duplicadas"] += 1
                continue
            codigos_vistos.add(fonte)
            for numero, linha in enumerate(fonte.splitlines(), start=1):
                if PADRAO_CAMINHO_ABSOLUTO.search(linha):
                    relatorio["caminhos_absolutos"].append(f"{caminho.name}: {linha.strip()}")
            copiadas.append(new_code_cell(celula.source))
        elif celula.cell_type == "markdown":
            copiadas.append(new_markdown_cell(celula.source))
        # células "raw" são descartadas: não fazem parte da análise

    relatorio["por_notebook"][caminho.name] = len(copiadas)
    return copiadas


def consolidar(manifesto: dict, permitir_faltantes: bool) -> tuple[nbformat.NotebookNode, dict]:
    relatorio = {
        "por_notebook": {},
        "faltantes": [],
        "puladas_tag": 0,
        "puladas_duplicadas": 0,
        "caminhos_absolutos": [],
    }

    # Verifica antes de gerar qualquer coisa
    for secao in manifesto["secoes"]:
        for relativo in secao["notebooks"]:
            if not (RAIZ / relativo).exists():
                relatorio["faltantes"].append(relativo)
    if relatorio["faltantes"] and not permitir_faltantes:
        lista = "\n  - ".join(relatorio["faltantes"])
        raise FileNotFoundError(
            "Notebooks do manifesto não encontrados:\n  - " + lista +
            "\nUse --permitir-faltantes para gerar uma prévia com o que existe."
        )

    celulas = [celula_cabecalho_geral(manifesto)]
    codigos_vistos: set[str] = set()

    for secao in manifesto["secoes"]:
        presentes = [r for r in secao["notebooks"] if (RAIZ / r).exists()]
        faltantes = [r for r in secao["notebooks"] if r not in presentes]
        celulas.append(celula_cabecalho_secao(secao, presentes, faltantes))
        for relativo in presentes:
            celulas += copiar_celulas(RAIZ / relativo, codigos_vistos, relatorio)

    nb = new_notebook(cells=celulas)
    nb.metadata["kernelspec"] = {"display_name": "Python 3", "language": "python", "name": "python3"}
    nb.metadata["language_info"] = {"name": "python"}
    return nb, relatorio


def executar(nb: nbformat.NotebookNode, pasta_trabalho: Path, timeout: int) -> None:
    from nbclient import NotebookClient

    cliente = NotebookClient(
        nb, timeout=timeout, kernel_name="python3",
        resources={"metadata": {"path": str(pasta_trabalho)}},
    )
    cliente.execute()


def main() -> int:
    parser = argparse.ArgumentParser(description="Consolida os notebooks das trilhas (KAN-37).")
    parser.add_argument("--manifesto", type=Path, default=MANIFESTO_PADRAO,
                        help="arquivo JSON com a ordem das seções")
    parser.add_argument("--saida", type=Path, default=None,
                        help="notebook de saída (padrão: o definido no manifesto)")
    parser.add_argument("--forcar", action="store_true",
                        help="sobrescreve o notebook de saída se ele já existir")
    parser.add_argument("--executar", action="store_true",
                        help="executa o notebook final do início ao fim e salva as saídas")
    parser.add_argument("--permitir-faltantes", action="store_true",
                        help="gera mesmo se algum notebook do manifesto ainda não existir")
    parser.add_argument("--timeout", type=int, default=600,
                        help="tempo máximo por célula ao executar, em segundos")
    args = parser.parse_args()

    manifesto = carregar_manifesto(args.manifesto)
    saida = args.saida or (RAIZ / manifesto["saida"])
    saida = saida if saida.is_absolute() else (Path.cwd() / saida)

    origens = {(RAIZ / r).resolve() for s in manifesto["secoes"] for r in s["notebooks"]}
    if saida.resolve() in origens:
        print(f"ERRO: a saída {saida.name} também é um notebook de origem.", file=sys.stderr)
        return 1
    if saida.exists() and not args.forcar:
        print(f"ERRO: {saida} já existe. Use --forcar para sobrescrever.", file=sys.stderr)
        return 1

    try:
        nb, relatorio = consolidar(manifesto, args.permitir_faltantes)
    except FileNotFoundError as erro:
        print(f"ERRO: {erro}", file=sys.stderr)
        return 1

    print("Células copiadas por notebook:")
    for nome, quantidade in relatorio["por_notebook"].items():
        print(f"  {nome:<45} {quantidade:>3}")
    print(f"Puladas pela tag '{TAG_PULAR}': {relatorio['puladas_tag']}")
    print(f"Puladas por serem código idêntico a outra célula: {relatorio['puladas_duplicadas']}")
    if relatorio["faltantes"]:
        print("AVISO: notebooks ausentes (seções marcadas como incompletas):")
        for faltante in relatorio["faltantes"]:
            print(f"  - {faltante}")
    if relatorio["caminhos_absolutos"]:
        print("AVISO: possíveis caminhos absolutos (quebram a reprodutibilidade):")
        for ocorrencia in relatorio["caminhos_absolutos"]:
            print(f"  - {ocorrencia}")

    if args.executar:
        print("Executando o notebook do início ao fim...")
        try:
            executar(nb, saida.parent, args.timeout)
        except Exception as erro:  # noqa: BLE001 - relata qualquer falha de célula
            print(f"ERRO na execução: {erro}", file=sys.stderr)
            return 1
        print("Execução concluída sem erros.")

    saida.parent.mkdir(parents=True, exist_ok=True)
    nbformat.write(nb, saida)
    print(f"Notebook consolidado salvo em: {saida.relative_to(RAIZ) if saida.is_relative_to(RAIZ) else saida}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
