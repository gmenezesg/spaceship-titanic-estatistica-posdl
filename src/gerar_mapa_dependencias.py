#!/usr/bin/env python3
"""
Gerador Automatizado do Mapa de Dependências, Estados e Responsáveis do Jira (Projeto KAN).

Este script gera:
1. docs/mapa_dependencias_jira.png (Imagem em alta resolução 200 DPI)
2. docs/mapa_dependencias_jira.mmd (DSL Mermaid.js para GitHub, Draw.io, Lucidchart, Mermaid Live. Use a extensão https://marketplace.visualstudio.com/items?itemName=MermaidChart.vscode-mermaid-chart para visualizar o arquivo .md)
3. docs/mapa_dependencias_jira.dot (DSL Graphviz DOT para Draw.io, Graphviz, Gephi)

Uso:
    python src/gerar_mapa_dependencias.py
"""

from pathlib import Path
import textwrap
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

TICKETS_JIRA = {'KAN-4': {'summary': 'Preparar criação do repositório GitHub',
           'status': 'Concluído',
           'assignee': 'Gustavo',
           'resp': 'Gustavo',
           'rev': 'Todos os membros (Confirmação de Acesso)',
           'deps': []},
 'KAN-5': {'summary': 'Configurar estrutura inicial do repositório',
           'status': 'Concluído',
           'assignee': 'Helton',
           'resp': 'Gustavo',
           'rev': 'Helton',
           'deps': ['KAN-4']},
 'KAN-6': {'summary': 'Definir fluxo de branches, commits e pull requests',
           'status': 'Concluído',
           'assignee': 'Gustavo',
           'resp': 'Gustavo',
           'rev': 'Renatta',
           'deps': ['KAN-5']},
 'KAN-7': {'summary': 'Criar e configurar o projeto Jira',
           'status': 'Concluído',
           'assignee': 'Gustavo',
           'resp': 'Gustavo',
           'rev': 'Luciana',
           'deps': []},
 'KAN-8': {'summary': 'Importar e validar os cards no Jira',
           'status': 'Concluído',
           'assignee': 'Gustavo',
           'resp': 'Gustavo',
           'rev': 'Daniela',
           'deps': ['KAN-7']},
 'KAN-9': {'summary': 'Preparar a Reunião 1 de 25 de outubro',
           'status': 'Cancelado',
           'assignee': 'Gustavo',
           'resp': 'Gustavo',
           'rev': 'Todos os membros',
           'deps': ['KAN-6', 'KAN-8']},
 'KAN-10': {'summary': 'Criar inventário e dicionário de dados',
            'status': 'Concluído',
            'assignee': 'Helton',
            'resp': 'Gustavo',
            'rev': 'Helton',
            'deps': ['KAN-9']},
 'KAN-11': {'summary': 'Analisar valores ausentes e duplicados',
            'status': 'Concluído',
            'assignee': 'Helton',
            'resp': 'Gustavo',
            'rev': 'Helton',
            'deps': ['KAN-10']},
 'KAN-12': {'summary': 'Criar variáveis derivadas do Spaceship Titanic',
            'status': 'Concluído',
            'assignee': 'Helton',
            'resp': 'Gustavo',
            'rev': 'Helton',
            'deps': ['KAN-11']},
 'KAN-13': {'summary': 'Publicar conclusões de preparação em Markdown',
            'status': 'A fazer',
            'assignee': 'Gustavo',
            'resp': 'Gustavo',
            'rev': 'Helton',
            'deps': ['KAN-12']},
 'KAN-14': {'summary': 'Produzir resumos de variáveis categóricas',
            'status': 'A fazer',
            'assignee': 'Helton',
            'resp': 'Helton',
            'rev': 'Luciana',
            'deps': ['KAN-12']},
 'KAN-15': {'summary': 'Produzir resumos de variáveis quantitativas',
            'status': 'Concluído',
            'assignee': 'Helton',
            'resp': 'Helton',
            'rev': 'Luciana',
            'deps': ['KAN-12']},
 'KAN-16': {'summary': 'Criar gráficos descritivos candidatos ao relatório',
            'status': 'Em Progresso',
            'assignee': 'Helton',
            'resp': 'Helton',
            'rev': 'Luciana',
            'deps': ['KAN-14', 'KAN-15']},
 'KAN-17': {'summary': 'Documentar valores extremos sem remoção automática',
            'status': 'Concluído',
            'assignee': 'Helton',
            'resp': 'Helton',
            'rev': 'Luciana',
            'deps': ['KAN-15']},
 'KAN-18': {'summary': 'Publicar conclusões descritivas em Markdown',
            'status': 'A fazer',
            'assignee': 'Helton',
            'resp': 'Helton',
            'rev': 'Luciana',
            'deps': ['KAN-16', 'KAN-17']},
 'KAN-19': {'summary': 'Estudar variáveis aleatórias e distribuições',
            'status': 'A fazer',
            'assignee': 'Luciana',
            'resp': 'Luciana',
            'rev': 'Daniela',
            'deps': ['KAN-9']},
 'KAN-20': {'summary': 'Analisar distribuições de idade e despesas',
            'status': 'A fazer',
            'assignee': 'Luciana',
            'resp': 'Luciana',
            'rev': 'Daniela',
            'deps': ['KAN-12', 'KAN-19']},
 'KAN-21': {'summary': 'Criar e interpretar QQ-plots',
            'status': 'A fazer',
            'assignee': 'Luciana',
            'resp': 'Luciana',
            'rev': 'Daniela',
            'deps': ['KAN-20']},
 'KAN-22': {'summary': 'Relacionar distribuições com a escolha dos testes inferenciais',
            'status': 'A fazer',
            'assignee': 'Luciana',
            'resp': 'Luciana',
            'rev': 'Daniela',
            'deps': ['KAN-21']},
 'KAN-23': {'summary': 'Publicar conclusões de distribuições em Markdown',
            'status': 'A fazer',
            'assignee': 'Luciana',
            'resp': 'Luciana',
            'rev': 'Daniela',
            'deps': ['KAN-22']},
 'KAN-24': {'summary': 'Definir hipóteses estatísticas antes dos testes',
            'status': 'In Review',
            'assignee': 'Daniela',
            'resp': 'Daniela',
            'rev': 'Renatta',
            'deps': ['KAN-12']},
 'KAN-25': {'summary': 'Testar associação entre variáveis categóricas',
            'status': 'In Review',
            'assignee': 'Daniela',
            'resp': 'Daniela',
            'rev': 'Renatta',
            'deps': ['KAN-24']},
 'KAN-26': {'summary': 'Comparar TotalSpend por Transported',
            'status': 'In Review',
            'assignee': 'Daniela',
            'resp': 'Daniela',
            'rev': 'Renatta',
            'deps': ['KAN-22', 'KAN-24']},
 'KAN-27': {'summary': 'Comparar TotalSpend entre planetas de origem',
            'status': 'A fazer',
            'assignee': 'Daniela',
            'resp': 'Daniela',
            'rev': 'Renatta',
            'deps': ['KAN-22', 'KAN-24']},
 'KAN-28': {'summary': 'Criar tabela-resumo dos testes de hipóteses',
            'status': 'A fazer',
            'assignee': 'Daniela',
            'resp': 'Daniela',
            'rev': 'Renatta',
            'deps': ['KAN-25', 'KAN-26', 'KAN-27']},
 'KAN-29': {'summary': 'Publicar conclusões dos testes em Markdown',
            'status': 'A fazer',
            'assignee': 'Daniela',
            'resp': 'Daniela',
            'rev': 'Renatta',
            'deps': ['KAN-28']},
 'KAN-30': {'summary': 'Analisar correlações e diagramas de dispersão',
            'status': 'A fazer',
            'assignee': 'Renatta',
            'resp': 'Renatta',
            'rev': 'Gustavo',
            'deps': ['KAN-12']},
 'KAN-31': {'summary': 'Desenvolver regressão linear para TotalSpend',
            'status': 'A fazer',
            'assignee': 'Renatta',
            'resp': 'Renatta',
            'rev': 'Gustavo',
            'deps': ['KAN-30']},
 'KAN-32': {'summary': 'Criar baseline para classificação de Transported',
            'status': 'A fazer',
            'assignee': 'Renatta',
            'resp': 'Renatta',
            'rev': 'Gustavo',
            'deps': ['KAN-12']},
 'KAN-33': {'summary': 'Desenvolver regressão logística para Transported',
            'status': 'A fazer',
            'assignee': 'Renatta',
            'resp': 'Renatta',
            'rev': 'Gustavo',
            'deps': ['KAN-32']},
 'KAN-34': {'summary': 'Avaliar e interpretar o modelo logístico',
            'status': 'A fazer',
            'assignee': 'Renatta',
            'resp': 'Renatta',
            'rev': 'Gustavo',
            'deps': ['KAN-33']},
 'KAN-35': {'summary': 'Publicar conclusões de correlação e regressões',
            'status': 'A fazer',
            'assignee': 'Renatta',
            'resp': 'Renatta',
            'rev': 'Gustavo',
            'deps': ['KAN-34', 'KAN-31']},
 'KAN-36': {'summary': 'Preparar apresentações cruzadas da Reunião 2',
            'status': 'A fazer',
            'assignee': 'Gustavo',
            'resp': 'Todos (Coordenação: Gustavo)',
            'rev': 'Pares de Revisão Cruzada',
            'deps': ['KAN-13', 'KAN-18', 'KAN-23', 'KAN-29', 'KAN-35']},
 'KAN-37': {'summary': 'Consolidar os notebooks num notebook final',
            'status': 'A fazer',
            'assignee': 'Gustavo',
            'resp': 'Gustavo',
            'rev': 'Todos os membros',
            'deps': ['KAN-36']},
 'KAN-38': {'summary': 'Selecionar tabelas e gráficos do relatório',
            'status': 'A fazer',
            'assignee': 'Helton',
            'resp': 'Helton',
            'rev': 'Luciana e Daniela',
            'deps': ['KAN-36']},
 'KAN-39': {'summary': 'Consolidar texto técnico do relatório',
            'status': 'A fazer',
            'assignee': 'Daniela',
            'resp': 'Daniela e Renatta',
            'rev': 'Luciana e Gustavo',
            'deps': ['KAN-37', 'KAN-38']},
 'KAN-40': {'summary': 'Rever coerência metodológica do relatório',
            'status': 'A fazer',
            'assignee': 'Luciana',
            'resp': 'Luciana',
            'rev': 'Daniela e Renatta',
            'deps': ['KAN-39']},
 'KAN-41': {'summary': 'Executar validação numérica cruzada',
            'status': 'A fazer',
            'assignee': 'Daniela',
            'resp': 'Todos (Coordenação: Daniela)',
            'rev': 'Todos os membros',
            'deps': ['KAN-40']},
 'KAN-42': {'summary': 'Gerar e rever o PDF final',
            'status': 'A fazer',
            'assignee': 'Renatta',
            'resp': 'Renatta',
            'rev': 'Todos os membros',
            'deps': ['KAN-41']},
 'KAN-43': {'summary': 'Preparar pacote final de entrega',
            'status': 'A fazer',
            'assignee': 'Gustavo',
            'resp': 'Gustavo',
            'rev': 'Todos os membros',
            'deps': ['KAN-42']}}

POSICOES = {
    # Fase 1: Governança GitHub & Jira
    'KAN-4':  (1.0, 15.6),
    'KAN-7':  (3.0, 15.6),
    'KAN-5':  (1.0, 14.2),
    'KAN-8':  (3.0, 14.2),
    'KAN-6':  (1.0, 12.8),
    'KAN-9':  (3.0, 12.8),
    # Fase 2: Preparação de Dados (Notebook 01) + Base Teórica
    'KAN-10': (1.3, 11.1),
    'KAN-19': (3.0, 11.1),
    'KAN-11': (1.3,  9.8),
    'KAN-12': (1.3,  8.5),
    # Fase 3: 5 Trilhas Analíticas Paralelas
    'KAN-13': (0.0,  6.3),
    'KAN-14': (1.0,  6.3),
    'KAN-15': (1.0,  4.9),
    'KAN-16': (1.0,  3.5),
    'KAN-17': (1.0,  2.1),
    'KAN-18': (1.0,  0.7),
    'KAN-20': (2.0,  6.3),
    'KAN-21': (2.0,  4.9),
    'KAN-22': (2.0,  3.5),
    'KAN-23': (2.0,  0.7),
    'KAN-24': (3.0,  6.3),
    'KAN-25': (3.0,  4.9),
    'KAN-26': (3.0,  3.5),
    'KAN-27': (3.0,  2.1),
    'KAN-28': (3.0,  0.7),
    'KAN-29': (3.0, -0.7),
    'KAN-30': (4.0,  6.3),
    'KAN-31': (4.0,  4.9),
    'KAN-32': (4.0,  3.5),
    'KAN-33': (4.0,  2.1),
    'KAN-34': (4.0,  0.7),
    'KAN-35': (4.0, -0.7),
    # Fase 4: Consolidação, Revisão Cruzada e Relatório Final
    'KAN-36': (2.0, -2.4),
    'KAN-37': (1.2, -3.8),
    'KAN-38': (2.8, -3.8),
    'KAN-39': (0.0, -5.3),
    'KAN-40': (1.0, -5.3),
    'KAN-41': (2.0, -5.3),
    'KAN-42': (3.0, -5.3),
    'KAN-43': (4.0, -5.3),
}


def gerar_png(docs_dir: Path) -> Path:
    status_styles = {
        'Concluído':    {'bg': '#E6F4EA', 'border': '#1E8E3E', 'badge_bg': '#1E8E3E', 'badge_fg': '#FFFFFF', 'label': 'CONCLUÍDO'},
        'In Review':    {'bg': '#FEF7E0', 'border': '#F29900', 'badge_bg': '#F29900', 'badge_fg': '#FFFFFF', 'label': 'EM REVISÃO (PR)'},
        'Em Progresso': {'bg': '#E8F0FE', 'border': '#1967D2', 'badge_bg': '#1967D2', 'badge_fg': '#FFFFFF', 'label': 'EM PROGRESSO'},
        'A fazer':      {'bg': '#F8FAFC', 'border': '#64748B', 'badge_bg': '#475569', 'badge_fg': '#FFFFFF', 'label': 'A FAZER'},
        'Cancelado':    {'bg': '#F1F5F9', 'border': '#94A3B8', 'badge_bg': '#94A3B8', 'badge_fg': '#FFFFFF', 'label': 'CANCELADO'},
    }
    person_colors = {
        'Gustavo': '#2563EB',
        'Helton':  '#0D9488',
        'Luciana': '#7C3AED',
        'Daniela': '#DB2777',
        'Renatta': '#EA580C',
    }

    fig, ax = plt.subplots(figsize=(26, 31), dpi=200)
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')

    bands = [
        (12.1, 16.4, '#EFF6FF', 'FASE 1 — GOVERNANÇA (GITHUB, JIRA E ALINHAMENTO)'),
        (7.8,  11.9, '#F0FDF4', 'FASE 2 — PREPARAÇÃO DE DADOS (NOTEBOOK 01) E BASE DE DISTRIBUIÇÕES'),
        (-1.4,  7.6, '#FFFBEB', 'FASE 3 — TRILHAS ANALÍTICAS PARALELAS (PREPARAÇÃO, DESCRITIVA, DISTRIBUIÇÕES, HIPÓTESES E REGRESSÕES)'),
        (-6.0, -1.6, '#FDF2F8', 'FASE 4 — REUNIÃO 2, CONSOLIDAÇÃO TÉCNICA, VALIDAÇÃO CRUZADA E ENTREGA FINAL'),
    ]
    for ymin, ymax, bcolor, btitle in bands:
        rect = FancyBboxPatch(
            (-0.55, ymin), 5.1, ymax - ymin,
            boxstyle="round,pad=0.08,rounding_size=0.12",
            facecolor=bcolor, edgecolor='#CBD5E1', linewidth=1.5, alpha=0.65, zorder=0
        )
        ax.add_patch(rect)
        ax.text(-0.48, ymax - 0.12, btitle, fontsize=11.5, fontweight='bold', color='#1E293B', ha='left', va='top', zorder=1)

    track_headers = [
        (0.0, 'Trilha 0: Preparação\n(Gustavo)', '#2563EB'),
        (1.0, 'Trilha 1: Descritiva\n(Helton)', '#0D9488'),
        (2.0, 'Trilha 2: Distribuições\n(Luciana)', '#7C3AED'),
        (3.0, 'Trilha 3: Hipóteses\n(Daniela)', '#DB2777'),
        (4.0, 'Trilha 4: Regressões\n(Renatta)', '#EA580C'),
    ]
    for tx, tlabel, tcol in track_headers:
        ax.text(
            tx, 7.22, tlabel, fontsize=10.2, fontweight='bold', color=tcol, ha='center', va='top',
            bbox=dict(boxstyle='round,pad=0.26', facecolor='#FFFFFF', edgecolor=tcol, lw=1.5, alpha=0.95), zorder=2
        )

    box_w, box_h = 0.82, 0.92
    for target_key, info in TICKETS_JIRA.items():
        x2, y2 = POSICOES[target_key]
        for src_key in info['deps']:
            x1, y1 = POSICOES[src_key]
            dx, dy = x2 - x1, y2 - y1
            if src_key == 'KAN-12' and target_key == 'KAN-15':
                start, end, rad = (x1 - box_w / 4, y1 - box_h / 2), (x2 - box_w / 2, y2), 0.28
            elif src_key == 'KAN-12' and target_key == 'KAN-32':
                start, end, rad = (x1 + box_w / 2, y1 - 0.15), (x2 - box_w / 2, y2 + 0.1), -0.15
            elif abs(dy) < 0.1 and dx > 0:
                start, end, rad = (x1 + box_w / 2, y1), (x2 - box_w / 2, y2), 0.0
            elif abs(dx) < 0.05:
                if abs(dy) > 1.8:
                    start, end, rad = (x1 + box_w / 2, y1), (x2 + box_w / 2, y2), -0.35
                else:
                    start, end, rad = (x1, y1 - box_h / 2), (x2, y2 + box_h / 2), 0.0
            else:
                start, end, rad = (x1, y1 - box_h / 2), (x2, y2 + box_h / 2), (0.12 if dx > 0 else -0.12)

            edge_color = '#0284C7' if src_key == 'KAN-12' else ('#7C3AED' if target_key == 'KAN-36' else '#475569')
            lw = 1.9 if src_key == 'KAN-12' else 1.6
            arrow = FancyArrowPatch(
                start, end, connectionstyle=f"arc3,rad={rad}",
                arrowstyle="-|>,head_length=7,head_width=4.5",
                color=edge_color, linewidth=lw, alpha=0.80, zorder=2
            )
            ax.add_patch(arrow)

    for key, info in TICKETS_JIRA.items():
        cx, cy = POSICOES[key]
        st = status_styles.get(info['status'], status_styles['A fazer'])
        x0, y0 = cx - box_w / 2, cy - box_h / 2
        linestyle = '--' if info['status'] == 'Cancelado' else '-'
        card = FancyBboxPatch(
            (x0, y0), box_w, box_h, boxstyle="round,pad=0.02,rounding_size=0.06",
            facecolor=st['bg'], edgecolor=st['border'], linewidth=2.3, linestyle=linestyle, zorder=3
        )
        ax.add_patch(card)
        ax.text(x0 + 0.03, y0 + box_h - 0.12, key, fontsize=10.5, fontweight='bold', color='#0F172A', ha='left', va='center', zorder=4)
        ax.text(
            x0 + box_w - 0.03, y0 + box_h - 0.12, st['label'], fontsize=7.2, fontweight='bold', color=st['badge_fg'],
            ha='right', va='center', bbox=dict(boxstyle='round,pad=0.22', facecolor=st['badge_bg'], edgecolor='none'), zorder=4
        )
        wrapped_summary = "\n".join(textwrap.wrap(info['summary'], width=28))
        ax.text(cx, cy + 0.04, wrapped_summary, fontsize=8.6, fontweight='bold', color='#1E293B', ha='center', va='center', zorder=4)

        assignee_name = info['assignee']
        p_col = person_colors.get(assignee_name, '#334155')
        rev_short = info['rev'].split('(')[0].strip()
        if len(rev_short) > 16:
            rev_short = rev_short[:15] + '…'
        ax.text(x0 + 0.03, y0 + 0.11, f"Atual: {assignee_name}", fontsize=7.8, fontweight='bold', color=p_col, ha='left', va='center', zorder=4)
        ax.text(x0 + box_w - 0.03, y0 + 0.11, f"Rev: {rev_short}", fontsize=7.3, color='#475569', ha='right', va='center', zorder=4)

    ax.text(2.0, 18.05, "MAPA DE DEPENDÊNCIAS, ESTADOS E RESPONSÁVEIS — JIRA (PROJETO KAN)", fontsize=18, fontweight='bold', color='#0F172A', ha='center', va='center')
    ax.text(2.0, 17.62, "Spaceship Titanic — Estatística (Pós-Graduação em Deep Learning - CIn/UFPE)", fontsize=12, color='#475569', ha='center', va='center')

    ax.set_xlim(-0.65, 4.65)
    ax.set_ylim(-6.2, 18.4)
    ax.axis('off')
    plt.tight_layout()
    out_file = docs_dir / "mapa_dependencias_jira.png"
    plt.savefig(out_file, dpi=200, bbox_inches='tight')
    plt.close(fig)
    return out_file


def _mmd_node(key: str) -> str:
    info = TICKETS_JIRA[key]
    status_map = {
        'Concluído': ('CONCLUÍDO', 'concluido'),
        'In Review': ('EM REVISÃO', 'revisao'),
        'Em Progresso': ('EM PROGRESSO', 'progresso'),
        'A fazer': ('A FAZER', 'afazer'),
        'Cancelado': ('CANCELADO', 'cancelado'),
    }
    badge, cls = status_map.get(info['status'], ('A FAZER', 'afazer'))
    rev_short = info['rev'].split('(')[0].strip()
    return (
        f'{key}["<b>{key}</b> [{badge}]<br/>'
        f'{info["summary"]}<br/>'
        f'<i>Atual: {info["assignee"]} | Rev: {rev_short}</i>"]:::{cls}'
    )


def gerar_mmd(docs_dir: Path) -> str:
    lines = [
        "flowchart TD",
        "    %% =====================================================================",
        "    %% MAPA DE DEPENDÊNCIAS, ESTADOS E RESPONSÁVEIS — JIRA (PROJETO KAN)",
        "    %% Compatível com: GitHub Markdown, Draw.io (Arrange > Insert > Mermaid),",
        "    %% Lucidchart, Mermaid Live Editor (https://mermaid.live) e VS Code.",
        "    %% =====================================================================",
        "",
        "    classDef concluido fill:#E6F4EA,stroke:#1E8E3E,stroke-width:2.5px,color:#0F172A;",
        "    classDef revisao fill:#FEF7E0,stroke:#F29900,stroke-width:2.5px,color:#0F172A;",
        "    classDef progresso fill:#E8F0FE,stroke:#1967D2,stroke-width:2.5px,color:#0F172A;",
        "    classDef afazer fill:#F8FAFC,stroke:#64748B,stroke-width:1.8px,color:#0F172A;",
        "    classDef cancelado fill:#F1F5F9,stroke:#94A3B8,stroke-width:1.8px,stroke-dasharray: 5 5,color:#64748B;",
        "",
        '    subgraph FASE1["FASE 1 — Governança (GitHub, Jira e Alinhamento)"]',
    ]
    for k in ['KAN-4', 'KAN-5', 'KAN-6', 'KAN-7', 'KAN-8', 'KAN-9']:
        lines.append(f"        {_mmd_node(k)}")
    lines += [
        "    end",
        "",
        '    subgraph FASE2["FASE 2 — Preparação de Dados (Notebook 01) e Base Teórica"]',
    ]
    for k in ['KAN-10', 'KAN-11', 'KAN-12', 'KAN-19']:
        lines.append(f"        {_mmd_node(k)}")
    lines += [
        "    end",
        "",
        '    subgraph FASE3["FASE 3 — Trilhas Analíticas Paralelas"]',
        '        subgraph T0["Trilha 0: Preparação (Gustavo)"]',
        f"            {_mmd_node('KAN-13')}",
        "        end",
        '        subgraph T1["Trilha 1: Estatística Descritiva (Helton)"]',
    ]
    for k in ['KAN-14', 'KAN-15', 'KAN-16', 'KAN-17', 'KAN-18']:
        lines.append(f"            {_mmd_node(k)}")
    lines += [
        "        end",
        '        subgraph T2["Trilha 2: Distribuições e QQ-Plots (Luciana)"]',
    ]
    for k in ['KAN-20', 'KAN-21', 'KAN-22', 'KAN-23']:
        lines.append(f"            {_mmd_node(k)}")
    lines += [
        "        end",
        '        subgraph T3["Trilha 3: Testes de Hipóteses (Daniela)"]',
    ]
    for k in ['KAN-24', 'KAN-25', 'KAN-26', 'KAN-27', 'KAN-28', 'KAN-29']:
        lines.append(f"            {_mmd_node(k)}")
    lines += [
        "        end",
        '        subgraph T4["Trilha 4: Correlação e Regressões (Renatta)"]',
    ]
    for k in ['KAN-30', 'KAN-31', 'KAN-32', 'KAN-33', 'KAN-34', 'KAN-35']:
        lines.append(f"            {_mmd_node(k)}")
    lines += [
        "        end",
        "    end",
        "",
        '    subgraph FASE4["FASE 4 — Consolidação, Validação Cruzada e Entrega Final"]',
    ]
    for k in ['KAN-36', 'KAN-37', 'KAN-38', 'KAN-39', 'KAN-40', 'KAN-41', 'KAN-42', 'KAN-43']:
        lines.append(f"        {_mmd_node(k)}")
    lines += [
        "    end",
        "",
        "    %% Arestas de Dependência (Origem --> Destino)",
    ]
    for target_key, info in TICKETS_JIRA.items():
        for src_key in info['deps']:
            lines.append(f"    {src_key} --> {target_key}")

    content = "\n".join(lines) + "\n"
    (docs_dir / "mapa_dependencias_jira.mmd").write_text(content, encoding="utf-8")
    return content


def gerar_dot(docs_dir: Path) -> Path:
    dot_styles = {
        'Concluído': ('CONCLUÍDO', '#E6F4EA', '#1E8E3E', 'rounded,filled'),
        'In Review': ('EM REVISÃO', '#FEF7E0', '#F29900', 'rounded,filled'),
        'Em Progresso': ('EM PROGRESSO', '#E8F0FE', '#1967D2', 'rounded,filled'),
        'A fazer': ('A FAZER', '#F8FAFC', '#64748B', 'rounded,filled'),
        'Cancelado': ('CANCELADO', '#F1F5F9', '#94A3B8', 'rounded,filled,dashed'),
    }
    lines = [
        "digraph JiraDependencyMap {",
        "    rankdir=TB;",
        "    splines=ortho;",
        "    nodesep=0.45;",
        "    ranksep=0.65;",
        '    fontname="Helvetica";',
        '    node [shape=box, style="rounded,filled", fontname="Helvetica", fontsize=10, margin="0.18,0.12", penwidth=2.0];',
        '    edge [color="#475569", penwidth=1.4, arrowsize=0.8];',
        "",
    ]
    for key, info in TICKETS_JIRA.items():
        badge, fill, border, style = dot_styles.get(info['status'], dot_styles['A fazer'])
        rev_short = info['rev'].split('(')[0].strip()
        label = f"{key} [{badge}]\\n{info['summary']}\\nAtual: {info['assignee']} | Rev: {rev_short}"
        lines.append(f'    "{key}" [label="{label}", fillcolor="{fill}", color="{border}", style="{style}"];')
    lines.append("")
    for target_key, info in TICKETS_JIRA.items():
        for src_key in info['deps']:
            lines.append(f'    "{src_key}" -> "{target_key}";')
    lines.append("}\n")
    out_file = docs_dir / "mapa_dependencias_jira.dot"
    out_file.write_text("\n".join(lines), encoding="utf-8")
    return out_file


def gerar_md(docs_dir: Path, mmd_content: str) -> Path:
    rows = []
    for key, info in TICKETS_JIRA.items():
        deps_str = ", ".join(f"`{d}`" for d in info['deps']) if info['deps'] else "—"
        rows.append(
            f"| [`{key}`](https://megamatic.atlassian.net/browse/{key}) "
            f"| {info['summary']} "
            f"| **{info['status']}** "
            f"| {info['assignee']} "
            f"| {info['resp']} "
            f"| {info['rev']} "
            f"| {deps_str} |"
        )
    table_body = "\n".join(rows)
    md_content = f"""# Mapa de Dependências, Estados e Responsáveis — Jira (`KAN`)

Este documento consolida a arquitetura de dependências (DAG), o estado atual e a governança de responsáveis/revisores dos **40 tickets operacionais (`KAN-4` a `KAN-43`)** do projeto **Spaceship Titanic — Estatística (CIn/UFPE)**.

- **Painel Oficial no Jira:** [https://megamatic.atlassian.net/jira/software/projects/KAN/boards](https://megamatic.atlassian.net/jira/software/projects/KAN/boards)
- **Arquivos DSL Open-Source para Edição e Visualização:**
  - **Mermaid.js DSL (`.mmd`):** [`docs/mapa_dependencias_jira.mmd`](mapa_dependencias_jira.mmd) *(compatível nativamente com GitHub, Draw.io / diagrams.net, Lucidchart, Mermaid Live Editor, Notion e VS Code)*
  - **Graphviz DOT DSL (`.dot`):** [`docs/mapa_dependencias_jira.dot`](mapa_dependencias_jira.dot) *(compatível com Graphviz, Draw.io, Gephi e WebGraphviz)*
  - **Gerador Automatizado em Python:** [`src/gerar_mapa_dependencias.py`](../src/gerar_mapa_dependencias.py) *(regenera `.png`, `.mmd` e `.dot` com um único comando)*

---

## 1. Visualização Gráfica de Alta Resolução (PNG)

![Mapa de Dependências do Jira](mapa_dependencias_jira.png)

---

## 2. Diagrama Interativo em Mermaid.js (Renderização Nativa GitHub)

O bloco abaixo utiliza a DSL **Mermaid (`flowchart TD`)** e é renderizado interativamente pelo próprio GitHub.

```mermaid
{mmd_content.rstrip()}
```

---

## 3. Como Atualizar ou Importar em Ferramentas Visuais (Draw.io, Lucidchart, Mermaid)

### Opção A — Atualizar via Script Python (Recomendado)
1. Edite o estado (`status`) ou responsável (`assignee`) do ticket no dicionário `TICKETS_JIRA` dentro de [`src/gerar_mapa_dependencias.py`](../src/gerar_mapa_dependencias.py).
2. Execute na raiz do repositório:
   ```bash
   python src/gerar_mapa_dependencias.py
   ```
   O script atualizará automaticamente a imagem `docs/mapa_dependencias_jira.png` e os arquivos DSL `docs/mapa_dependencias_jira.mmd` e `docs/mapa_dependencias_jira.dot`.

### Opção B — Importar no Draw.io (`app.diagrams.net`)
1. Abra o [Draw.io (diagrams.net)](https://app.diagrams.net/).
2. No menu superior, clique em **Arrange (Organizar) $\\rightarrow$ Insert (Inserir) $\\rightarrow$ Advanced (Avançado) $\\rightarrow$ Mermaid...** (ou **From Text / DOT**).
3. Cole o conteúdo de [`docs/mapa_dependencias_jira.mmd`](mapa_dependencias_jira.mmd) (para Mermaid) ou [`docs/mapa_dependencias_jira.dot`](mapa_dependencias_jira.dot) (para Graphviz DOT) e clique em **Insert**. Todos os blocos e conectores serão convertidos em objetos editáveis!

### Opção C — Editar no Mermaid Live Editor ou Lucidchart
- **Mermaid Live Editor:** Acesse [https://mermaid.live](https://mermaid.live) e cole o conteúdo de [`docs/mapa_dependencias_jira.mmd`](mapa_dependencias_jira.mmd). Para mudar a cor/estado de um ticket, basta trocar o sufixo da classe no final do nó:
  - `:::concluido` (Verde)
  - `:::revisao` (Laranja / Em Revisão)
  - `:::progresso` (Azul / Em Progresso)
  - `:::afazer` (Cinza / A Fazer)
  - `:::cancelado` (Tracejado / Cancelado)
- **Lucidchart:** Clique em **Insert $\\rightarrow$ Mermaid** e cole o conteúdo de [`docs/mapa_dependencias_jira.mmd`](mapa_dependencias_jira.mmd).

---

## 4. Tabela Completa de Rastreabilidade dos Tickets (`KAN-4` a `KAN-43`)

| Ticket | Resumo da Tarefa | Estado Atual | Assignee Atual (Jira) | Responsável Principal | Revisor Dedicado | Dependências Diretas |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
{table_body}
"""
    out_file = docs_dir / "mapa_dependencias_jira.md"
    out_file.write_text(md_content, encoding="utf-8")
    return out_file


if __name__ == "__main__":
    root_dir = Path(__file__).resolve().parent.parent
    docs_dir = root_dir / "docs"
    out_png = gerar_png(docs_dir)
    mmd_str = gerar_mmd(docs_dir)
    out_dot = gerar_dot(docs_dir)
    out_md = gerar_md(docs_dir, mmd_str)
    print(f"Arquivos gerados com sucesso em: {docs_dir}")
