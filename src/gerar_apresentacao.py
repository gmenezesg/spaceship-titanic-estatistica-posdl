"""Gera o PDF de apresentação final (16:9) do projeto Spaceship Titanic.

Uso:
    python src/gerar_apresentacao.py
    python src/gerar_apresentacao.py --preview /tmp/opencode/deck

O PDF é gravado em report/apresentacao_final.pdf. As figuras vêm de
report/figures/ e os números canônicos de docs/conclusoes/01 a 06.
"""

from __future__ import annotations

import argparse
import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager as fm
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "report" / "figures"
OUT = ROOT / "report" / "apresentacao_final.pdf"

# ---------------------------------------------------------------------------
# Identidade visual
# ---------------------------------------------------------------------------
W, H = 13.333, 7.5
NAVY = "#0B1B33"
NAVY_2 = "#13294B"
TEAL = "#2EC4B6"
TEAL_DARK = "#16867C"
CORAL = "#FF6B6B"
GOLD = "#F4B942"
INK = "#152238"
GRAY = "#5D6B80"
MUTED = "#8492A6"
BORDER = "#DCE4EE"
OFFWHITE = "#F7F9FC"
WHITE = "#FFFFFF"
LIGHT_TEAL = "#E6F7F5"
LIGHT_CORAL = "#FFEDEC"
LIGHT_GOLD = "#FFF5DE"

for _font in ("Lato", "Lato Semibold", "Lato Black", "DejaVu Sans"):
    try:
        fm.findfont(_font, fallback_to_default=False)
    except Exception:
        pass

plt.rcParams.update(
    {
        "font.family": ["Lato", "DejaVu Sans"],
        "font.size": 12,
        "text.color": INK,
        "axes.edgecolor": BORDER,
        "axes.labelcolor": INK,
        "xtick.color": GRAY,
        "ytick.color": GRAY,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
    }
)

RNG = np.random.default_rng(42)


# ---------------------------------------------------------------------------
# Helpers de desenho
# ---------------------------------------------------------------------------
def new_slide(bg: str = OFFWHITE):
    fig = plt.figure(figsize=(W, H))
    fig.patch.set_facecolor(bg)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.set_facecolor(bg)
    ax.axis("off")
    return fig, ax


def text(
    ax,
    x,
    y,
    s,
    size=14,
    color=INK,
    weight="normal",
    ha="left",
    va="top",
    wrap=None,
    lh=1.25,
    z=10,
    **kw,
):
    if wrap:
        s = "\n".join(textwrap.wrap(s, width=wrap))
    return ax.text(
        x,
        y,
        s,
        fontsize=size,
        color=color,
        fontweight=weight,
        ha=ha,
        va=va,
        linespacing=lh,
        zorder=z,
        **kw,
    )


def card(ax, x, y, w, h, fc=WHITE, ec=BORDER, lw=1.0, r=0.14, shadow=True, alpha=1.0, z=2):
    if shadow:
        ax.add_patch(
            FancyBboxPatch(
                (x + 0.035, y - 0.045),
                w,
                h,
                boxstyle=f"round,pad=0,rounding_size={r}",
                linewidth=0,
                facecolor=NAVY,
                alpha=0.06,
                zorder=z - 1,
            )
        )
    ax.add_patch(
        FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle=f"round,pad=0,rounding_size={r}",
            linewidth=lw,
            edgecolor=ec,
            facecolor=fc,
            alpha=alpha,
            zorder=z,
        )
    )


def pill(ax, x, y, w, h, label, fc=LIGHT_TEAL, tc=TEAL_DARK, size=10.5, weight="bold"):
    card(ax, x, y, w, h, fc=fc, ec="none", r=h / 2, shadow=False, z=4)
    text(ax, x + w / 2, y + h / 2, label, size=size, color=tc, weight=weight, ha="center", va="center", z=6)


def header(ax, kicker, title, subtitle=None, dark=False):
    fg = WHITE if dark else INK
    sub = "#C7D4E6" if dark else GRAY
    ax.add_patch(Rectangle((0.68, 6.52), 0.075, 0.58, color=TEAL, zorder=5))
    text(ax, 0.86, 7.08, kicker.upper(), size=9.5, color=TEAL, weight="bold", z=6)
    text(ax, 0.86, 6.92, title, size=28, color=fg, weight="bold", va="top", z=6)
    if subtitle:
        text(ax, 0.88, 6.38, subtitle, size=12.5, color=sub, z=6)


def footer(ax, n, dark=False, total=18):
    fg = "#AFC0D6" if dark else MUTED
    line = "#2B4162" if dark else BORDER
    ax.plot([0.68, W - 0.68], [0.56, 0.56], color=line, lw=0.8, zorder=4)
    text(
        ax,
        0.68,
        0.36,
        "Spaceship Titanic  ·  Análise Estatística  ·  CIn/UFPE",
        size=8.5,
        color=fg,
        z=5,
    )
    text(ax, W - 0.68, 0.36, f"{n:02d} / {total}", size=8.5, color=fg, ha="right", z=5)


def stars(ax, n=150, alpha=0.7):
    xs = RNG.uniform(0, W, n)
    ys = RNG.uniform(0, H, n)
    sizes = RNG.uniform(0.4, 2.8, n)
    ax.scatter(xs, ys, s=sizes, c=WHITE, alpha=alpha, linewidths=0, zorder=1)


def gradient(ax, bottom=NAVY, top=NAVY_2):
    cmap = LinearSegmentedColormap.from_list("bg", [bottom, top])
    grad = np.linspace(0, 1, 256).reshape(-1, 1)
    ax.imshow(grad, extent=(0, W, 0, H), origin="lower", aspect="auto", cmap=cmap, zorder=0)


def add_image(ax, name, x, y, w, h, z=3):
    path = FIG / name
    im = Image.open(path)
    iw, ih = im.size
    ar = iw / ih
    if w / h > ar:
        h2 = h
        w2 = h * ar
        x2 = x + (w - w2) / 2
        y2 = y
    else:
        w2 = w
        h2 = w / ar
        x2 = x
        y2 = y + (h - h2) / 2
    ax.imshow(im, extent=(x2, x2 + w2, y2, y2 + h2), aspect="auto", zorder=z)


def metric_card(ax, x, y, w, h, value, label, note="", accent=TEAL, value_size=38):
    card(ax, x, y, w, h, fc=WHITE, ec=BORDER, r=0.16)
    ax.add_patch(Rectangle((x, y + h - 0.09), w, 0.09, color=accent, zorder=4))
    text(ax, x + 0.22, y + h - 0.28, value, size=value_size, color=accent, weight="bold", z=6)
    text(ax, x + 0.22, y + h - 0.88, label, size=11, color=INK, weight="bold", wrap=int(w * 11), z=6)
    if note:
        text(ax, x + 0.22, y + 0.22, note, size=9, color=GRAY, wrap=int(w * 12), z=6)


# ---------------------------------------------------------------------------
# Slides
# ---------------------------------------------------------------------------
def slide_01_cover(fig, ax, n):
    gradient(ax, "#081426", "#122A4D")
    stars(ax, 180, 0.75)
    for r, a in ((3.5, 0.10), (2.5, 0.16), (1.55, 0.24)):
        ax.add_patch(Circle((11.35, 1.15), r, fill=False, ec=TEAL, lw=1.1, alpha=a, zorder=2))
    ax.add_patch(Circle((11.35, 1.15), 0.17, color=TEAL, alpha=0.9, zorder=3))
    ax.add_patch(Circle((12.05, 3.05), 0.07, color=GOLD, alpha=0.9, zorder=3))
    ax.add_patch(Circle((9.95, 2.6), 0.05, color=CORAL, alpha=0.9, zorder=3))

    text(ax, 0.78, 6.82, "TRABALHO FINAL  ·  ESTATÍSTICA AVANÇADA  ·  CIn/UFPE", size=10.5, color=TEAL, weight="bold")
    ax.add_patch(Rectangle((0.78, 5.78), 0.09, 0.78, color=CORAL, zorder=5))
    text(ax, 1.02, 6.52, "Spaceship Titanic", size=44, color=WHITE, weight="bold", va="top")
    text(
        ax,
        1.04,
        4.98,
        "O que distingue quem foi transportado —\ne o que os dados permitem recomendar",
        size=20,
        color="#DDE7F3",
        va="top",
        lh=1.35,
    )

    labels = [("8.693", "passageiros"), ("6", "etapas analíticas"), ("1", "modelo de triagem")]
    x = 1.04
    for value, label in labels:
        card(ax, x, 2.62, 2.42, 0.82, fc="#142D50", ec="#28476F", r=0.12, shadow=False, z=4)
        text(ax, x + 0.2, 2.98, value, size=21, color=TEAL, weight="bold", z=6)
        text(ax, x + 1.0, 3.0, label, size=10, color="#C7D4E6", z=6)
        x += 2.62

    text(ax, 0.8, 1.42, "Gustavo Menezes  ·  Helton Gomes  ·  Luciana Almeida  ·  Daniela Amaro  ·  Renatta", size=11, color="#E8EEF6")
    text(ax, 0.8, 1.06, "Novembro de 2026  ·  Pós-Graduação em Deep Learning", size=9.5, color="#9FB2CA")
    text(ax, W - 0.78, 6.82, "50,36% transportados", size=10, color=TEAL, weight="bold", ha="right")


def slide_02_summary(fig, ax, n):
    header(ax, "Resumo executivo", "A resposta em 30 segundos", "Três números que organizam toda a apresentação")
    metric_card(ax, 0.68, 4.28, 3.88, 1.72, "50,36%", "dos passageiros foram transportados", "4.378 de 8.693 — alvo equilibrado", TEAL)
    metric_card(ax, 4.73, 4.28, 3.88, 1.72, "81,47%", "em criossono vs. 32,82% acordados", "diferença de 48,65 p.p.", CORAL, 36)
    metric_card(ax, 8.78, 4.28, 3.88, 1.72, "77,9%", "de acurácia no teste", "ROC-AUC 0,862 · F1 0,784", GOLD)

    card(ax, 0.68, 2.46, 11.98, 1.28, fc=NAVY, ec="none", r=0.16)
    ax.add_patch(Rectangle((0.68, 2.46), 0.09, 1.28, color=TEAL, zorder=5))
    text(
        ax,
        1.02,
        3.34,
        "Criossono é o sinal mais forte. Origem e deck contam a mesma história por caminhos diferentes.",
        size=15,
        color=WHITE,
        weight="bold",
        z=6,
    )
    text(
        ax,
        1.02,
        2.86,
        "O gasto engana: 41,92% não gastaram nada e a mediana dos transportados é zero. O modelo apoia a triagem — não decide sozinho.",
        size=11,
        color="#C7D4E6",
        z=6,
    )
    text(ax, 0.7, 1.72, "Leitura de 60 segundos", size=9.5, color=TEAL_DARK, weight="bold")
    text(
        ax,
        0.7,
        1.38,
        "Metade da amostra foi transportada; o confinamento em criossono separa os grupos com a maior magnitude observada.",
        size=11.5,
        color=GRAY,
        wrap=108,
    )
    footer(ax, n)


def slide_03_problem(fig, ax, n):
    header(ax, "Contexto", "O incidente, o cliente e a pergunta", "Por que esta análise existe")
    text(ax, 0.7, 5.72, "A nave atravessou uma anomalia espaço-temporal.", size=16, color=INK, weight="bold")
    text(
        ax,
        0.7,
        5.28,
        "Metade dos 8.693 passageiros foi transportada para outra dimensão. Os registros de bordo "
        "sobreviveram, mas chegaram incompletos: quem estava a bordo, onde dormia, quanto consumiu e "
        "em que estado viajava.",
        size=12,
        color=GRAY,
        wrap=63,
        lh=1.35,
    )
    text(ax, 0.7, 3.64, "O cliente", size=9.5, color=TEAL_DARK, weight="bold")
    text(ax, 0.7, 3.32, "Comando de Operações Espaciais e equipe de resgate", size=14, color=INK, weight="bold", wrap=48)

    card(ax, 0.7, 1.34, 5.7, 1.58, fc=LIGHT_TEAL, ec="none", r=0.14)
    text(ax, 0.94, 2.62, "1  ENTENDER", size=9.5, color=TEAL_DARK, weight="bold")
    text(ax, 0.94, 2.34, "Quais perfis estavam mais expostos ao teletransporte?", size=11.5, color=INK, wrap=44)
    text(ax, 0.94, 1.72, "Apurar responsabilidades, comunicar famílias e revisar protocolos.", size=9.5, color=GRAY, wrap=52)

    card(ax, 6.68, 1.34, 5.98, 1.58, fc=LIGHT_GOLD, ec="none", r=0.14)
    text(ax, 6.92, 2.62, "2  PREVER", size=9.5, color="#9A6B00", weight="bold")
    text(ax, 6.92, 2.34, "Quais passageiros da base não rotulada foram transportados?", size=11.5, color=INK, wrap=46)
    text(ax, 6.92, 1.72, "Priorizar busca e reconstrução de registros.", size=9.5, color=GRAY, wrap=52)

    text(ax, 6.6, 5.72, "A pergunta analítica", size=9.5, color=TEAL_DARK, weight="bold")
    card(ax, 6.6, 3.32, 6.06, 2.22, fc=NAVY, ec="none", r=0.16)
    text(
        ax,
        6.92,
        5.06,
        "“Quais características estão associadas ao desfecho, qual é a magnitude dessas associações "
        "e quão bem elas permitem prever quem foi transportado?”",
        size=13,
        color=WHITE,
        wrap=47,
        lh=1.4,
        z=6,
    )
    text(ax, 6.92, 3.58, "Desenho observacional  ·  sem afirmação causal", size=9.5, color=TEAL, weight="bold", z=6)
    footer(ax, n)


def slide_04_data(fig, ax, n):
    header(ax, "Dados", "De 14 para 22 variáveis, sem perder passageiros", "Saneamento e engenharia de atributos")
    stats = [
        ("8.693 × 14", "base bruta de treino"),
        ("1,91%", "células ausentes"),
        ("24,01%", "linhas incompletas"),
        ("842", "células recuperadas por regra"),
    ]
    x = 0.68
    for value, label in stats:
        card(ax, x, 4.98, 2.86, 1.02, fc=WHITE, ec=BORDER, r=0.12)
        text(ax, x + 0.18, 5.66, value, size=19, color=TEAL_DARK, weight="bold")
        text(ax, x + 0.18, 5.28, label, size=9, color=GRAY, wrap=30)
        x += 3.02

    text(ax, 0.7, 4.42, "Pipeline em 10 etapas", size=9.5, color=TEAL_DARK, weight="bold")
    steps = [
        ("1", "Base bruta", "14 colunas e 2.324\ncélulas ausentes"),
        ("2", "Regras de negócio", "criossono e criança\nimplicam gasto zero"),
        ("3", "Imputação", "mediana e moda\ncondicionais"),
        ("4", "Atributos", "8 variáveis\nderivadas"),
        ("5", "Base analítica", "8.693 × 22\n0 ausentes"),
    ]
    x = 0.68
    for i, (num, title, desc) in enumerate(steps):
        fc = NAVY if i == 4 else WHITE
        tc = WHITE if i == 4 else INK
        sc = "#C7D4E6" if i == 4 else GRAY
        card(ax, x, 2.52, 2.22, 1.48, fc=fc, ec="none" if i == 4 else BORDER, r=0.14)
        ax.add_patch(Circle((x + 0.38, 3.68), 0.19, color=TEAL, zorder=5))
        text(ax, x + 0.38, 3.68, num, size=9, color=WHITE, weight="bold", ha="center", va="center", z=6)
        text(ax, x + 0.68, 3.74, title, size=10, color=tc, weight="bold", va="center", z=6)
        text(ax, x + 0.18, 3.36, desc, size=8.4, color=sc, va="top", z=6, lh=1.3)
        if i < 4:
            ax.annotate(
                "",
                xy=(x + 2.3, 3.26),
                xytext=(x + 2.12, 3.26),
                arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=1.4),
                zorder=6,
            )
        x += 2.4

    card(ax, 0.68, 1.02, 11.96, 1.02, fc=LIGHT_TEAL, ec="none", r=0.14)
    text(ax, 0.94, 1.78, "Decisões que protegem a análise", size=9, color=TEAL_DARK, weight="bold")
    text(
        ax,
        0.94,
        1.48,
        "Nenhum outlier removido  ·  nenhuma linha descartada  ·  parâmetros estimados só no treino  ·  impacto máximo da imputação: 0,77 p.p.",
        size=10.5,
        color=INK,
    )
    footer(ax, n)


def slide_05_method(fig, ax, n):
    header(ax, "Método", "Cinco perguntas, cinco camadas de evidência", "O fio condutor da análise")
    cols = [
        ("01", "DESCREVER", "Quem são os passageiros e o que os distingue?", "Proporções, medianas e figuras", TEAL),
        ("02", "ENTENDER A FORMA", "As distribuições permitem os testes que queremos?", "Shapiro-Wilk, Lilliefors e QQ-plots", GOLD),
        ("03", "TESTAR", "As diferenças resistem à incerteza?", "Qui-quadrado, Welch, ANOVA e pós-hoc", CORAL),
        ("04", "RELACIONAR E PREVER", "O que se mantém no conjunto e com qual desempenho?", "Correlações, ORs e regressão logística", "#7C6FD6"),
        ("05", "RECOMENDAR", "O que o cliente pode fazer com isso?", "Triagem, priorização e cautela", TEAL_DARK),
    ]
    x = 0.68
    for num, title, question, tech, color in cols:
        card(ax, x, 1.42, 2.22, 4.72, fc=WHITE, ec=BORDER, r=0.16)
        ax.add_patch(Rectangle((x, 5.95), 2.22, 0.19, color=color, zorder=4))
        text(ax, x + 0.18, 5.54, num, size=10, color=color, weight="bold")
        text(ax, x + 0.18, 5.18, title, size=9.5, color=INK, weight="bold", wrap=20)
        text(ax, x + 0.18, 4.42, question, size=10.2, color=INK, wrap=24, lh=1.32)
        text(ax, x + 0.18, 3.64, "COMO", size=8.2, color=MUTED, weight="bold")
        text(ax, x + 0.18, 3.34, tech, size=8.8, color=GRAY, wrap=26, lh=1.3)
        x += 2.4
    text(ax, 0.7, 1.02, "Regra de ouro: nenhum número é citado sem a seção de origem.", size=10, color=GRAY)
    footer(ax, n)


def slide_06_cryo(fig, ax, n):
    header(ax, "Achado 01", "O confinamento é o sinal mais forte", "Criossono × transporte")
    text(ax, 0.7, 5.7, "81,47%", size=44, color=CORAL, weight="bold")
    text(ax, 0.72, 5.04, "dos passageiros em criossono\nforam transportados", size=12, color=INK, weight="bold", lh=1.25)
    text(ax, 0.72, 4.38, "32,82%", size=30, color=GRAY, weight="bold")
    text(ax, 2.48, 4.16, "dos acordados", size=10.5, color=GRAY, va="center")

    card(ax, 0.7, 2.72, 5.1, 1.06, fc=LIGHT_CORAL, ec="none", r=0.14)
    text(ax, 0.94, 3.52, "48,65 p.p.", size=17, color=CORAL, weight="bold")
    text(ax, 0.94, 3.12, "de diferença — a maior do conjunto", size=9.5, color=INK)

    text(ax, 0.72, 2.28, "V de Cramér = 0,467", size=11, color=INK, weight="bold")
    text(ax, 0.72, 1.96, "associação muito forte", size=9.5, color=GRAY)
    text(ax, 0.72, 1.56, "χ² = 1.897,71  ·  p < 0,001", size=9.5, color=GRAY)

    card(ax, 6.1, 1.06, 6.56, 5.64, fc=WHITE, ec=BORDER, r=0.16)
    add_image(ax, "fig_02_transporte_por_criossono.png", 6.34, 1.5, 6.08, 4.78)
    text(ax, 6.34, 1.22, "Taxa de transporte por estado de criossono (n = 8.693)", size=8.5, color=MUTED)
    text(ax, 0.7, 0.93, "Fonte: Seção 2, figura 2 do relatório.", size=8.2, color=MUTED)
    footer(ax, n)


def slide_07_origin(fig, ax, n):
    header(ax, "Achado 02", "Origem e deck contam a mesma história", "Taxas por planeta e por deck da cabine")
    chips = [("Europa", "66,05%", TEAL_DARK), ("Marte", "52,44%", GOLD), ("Terra", "42,33%", GRAY)]
    x = 0.7
    for name, value, color in chips:
        pill(ax, x, 5.64, 2.16, 0.46, f"{name}  {value}", fc=WHITE, tc=color, size=10.5)
        x += 2.27

    card(ax, 0.68, 1.78, 5.86, 3.72, fc=WHITE, ec=BORDER, r=0.14)
    add_image(ax, "fig_01_transporte_por_planeta.png", 0.86, 1.96, 5.5, 3.1)
    text(ax, 0.86, 1.9, "Taxa por planeta de origem", size=8.4, color=MUTED)

    card(ax, 6.78, 1.78, 5.86, 3.72, fc=WHITE, ec=BORDER, r=0.14)
    add_image(ax, "fig_06_passageiros_por_deck.png", 6.96, 1.96, 5.5, 3.1)
    text(ax, 6.96, 1.9, "Passageiros e taxa por deck da cabine", size=8.4, color=MUTED)

    card(ax, 0.68, 0.96, 11.96, 0.62, fc=LIGHT_GOLD, ec="none", r=0.12)
    text(
        ax,
        0.92,
        1.27,
        "72,6% dos europeus ocupam os decks B e C — os mesmos de maior taxa. Origem e localização física estão entrelaçadas.",
        size=10.5,
        color=INK,
        weight="bold",
        va="center",
    )
    footer(ax, n)


def slide_08_spend(fig, ax, n):
    header(ax, "Achado 03", "O gasto é uma pista falsa — ou quase isso", "Consumo, zero-inflação e o efeito do criossono")
    card(ax, 0.68, 1.2, 6.3, 4.92, fc=WHITE, ec=BORDER, r=0.16)
    add_image(ax, "fig_04_gasto_por_transporte.png", 0.9, 1.42, 5.86, 4.4)
    text(ax, 0.9, 1.34, "Gasto total por desfecho (escala symlog)", size=8.4, color=MUTED)

    text(ax, 7.28, 6.08, "41,92%", size=40, color=CORAL, weight="bold")
    text(ax, 7.3, 5.44, "não gastaram nada a bordo", size=11, color=INK, weight="bold")
    text(ax, 7.3, 4.92, "Mediana de gasto", size=8.8, color=MUTED, weight="bold")
    text(ax, 7.3, 4.58, "US$ 0,00", size=22, color=TEAL_DARK, weight="bold")
    text(ax, 8.82, 4.64, "transportados", size=9, color=GRAY)
    text(ax, 7.3, 4.06, "US$ 907,00", size=22, color=INK, weight="bold")
    text(ax, 9.32, 4.12, "não transportados", size=9, color=GRAY)

    card(ax, 7.28, 2.3, 5.32, 1.38, fc=LIGHT_CORAL, ec="none", r=0.14)
    text(ax, 7.52, 3.36, "Cuidado com a leitura causal", size=9.5, color=CORAL, weight="bold")
    text(
        ax,
        7.52,
        3.04,
        "Quem está em criossono não consome. O gasto acompanha o confinamento, não protege contra ele.",
        size=10,
        color=INK,
        wrap=52,
    )
    text(ax, 7.3, 1.92, "Assimetria 4,40  ·  65,5% dos transportados com gasto zero", size=9, color=GRAY)
    text(ax, 7.3, 0.98, "Fonte: Seções 2 e 4.", size=8.2, color=MUTED)
    footer(ax, n)


def slide_09_probability(fig, ax, n):
    header(ax, "Probabilidade", "A forma da distribuição define o teste", "Idade ≈ Normal; gasto positivo ≈ Log-Normal com caudas pesadas")
    card(ax, 0.68, 1.2, 7.3, 4.78, fc=WHITE, ec=BORDER, r=0.16)
    add_image(ax, "fig_07_idade_normal_ajustada.png", 0.9, 2.45, 6.86, 2.95)
    text(ax, 0.9, 2.2, "Idade observada contra a Normal ajustada", size=8.4, color=MUTED)
    text(ax, 0.92, 1.9, "LEITURA", size=7.6, color=TEAL_DARK, weight="bold")
    text(
        ax,
        0.92,
        1.67,
        "O miolo está em idades mais baixas do que a Normal desloca; o pico em 0 são 178 bebês.",
        size=8.4,
        color=GRAY,
        wrap=94,
    )

    text(ax, 8.24, 5.98, "Age", size=11, color=TEAL_DARK, weight="bold")
    text(ax, 8.24, 5.56, "W = 0,980  ·  D = 0,076", size=13, color=INK, weight="bold")
    text(ax, 8.24, 5.18, "desvio pequeno: média e teste t são defensáveis", size=9.2, color=GRAY, wrap=36)

    text(ax, 8.24, 4.46, "log1p(TotalSpend)", size=11, color=CORAL, weight="bold")
    text(ax, 8.24, 4.04, "W = 0,891  ·  D = 0,126", size=13, color=INK, weight="bold")
    text(ax, 8.24, 3.66, "assimetria cai de 4,40 para −0,19", size=9.2, color=GRAY, wrap=36)
    text(ax, 8.24, 3.24, "mas a curtose 4,93 mantém as caudas pesadas", size=9.2, color=GRAY, wrap=36)

    card(ax, 8.18, 1.84, 4.46, 1.08, fc=LIGHT_TEAL, ec="none", r=0.12)
    text(ax, 8.42, 2.64, "Implicação prática", size=8.8, color=TEAL_DARK, weight="bold")
    text(ax, 8.42, 2.34, "Média para idade; mediana, proporção de zeros e testes robustos para gasto.", size=9.5, color=INK, wrap=48)
    text(ax, 8.24, 1.32, "Shapiro-Wilk e Kolmogorov-Smirnov (Lilliefors), α = 0,05.", size=8.2, color=MUTED, wrap=50)
    footer(ax, n)


def slide_10_tests(fig, ax, n):
    header(ax, "Testes de hipóteses", "As diferenças resistem ao teste", "H0 de independência ou igualdade; α = 0,05")
    x0, y0 = 0.68, 5.18
    widths = [2.28, 2.34, 1.72, 1.18, 1.86, 2.62]
    headers = ["Relação", "Teste", "Estatística", "p-valor", "Tamanho do efeito", "Leitura"]
    rows = [
        ("Criossono × transporte", "Qui-quadrado", "χ² = 1.897,71", "< 0,001", "V = 0,467", "muito forte"),
        ("Planeta × transporte", "Qui-quadrado", "χ² = 338,82", "< 0,001", "V = 0,197", "moderada"),
        ("VIP × transporte", "Qui-quadrado (Yates)", "χ² = 12,07", "0,0005", "V = 0,037", "desprezível"),
        ("Gasto × transporte", "t de Welch", "t = 18,94", "< 0,001", "d = 0,407", "moderado"),
        ("Gasto × planeta", "ANOVA de Welch", "F = 407,57", "< 0,001", "η² = 0,171", "grande"),
    ]
    row_h = 0.55
    ax.add_patch(Rectangle((x0, y0 - 0.08), sum(widths), 0.54, color=NAVY, zorder=3))
    x = x0
    for w, htxt in zip(widths, headers):
        text(ax, x + 0.12, y0 + 0.19, htxt, size=8.4, color=WHITE, weight="bold", va="center", z=6)
        x += w
    for i, row in enumerate(rows):
        y = y0 - 0.68 - i * row_h
        fc = WHITE if i % 2 == 0 else "#F1F5FA"
        ax.add_patch(Rectangle((x0, y - 0.02), sum(widths), row_h, facecolor=fc, edgecolor="none", zorder=2))
        x = x0
        for j, (w, val) in enumerate(zip(widths, row)):
            color = INK
            weight = "normal"
            if j == 4:
                color = TEAL_DARK if i < 2 else (CORAL if i == 2 else GOLD)
                weight = "bold"
            if j == 5:
                color = GRAY
            text(ax, x + 0.12, y + 0.28, val, size=8.3, color=color, weight=weight, va="center", z=6, wrap=int(w * 15))
            x += w
    ax.plot([x0, x0 + sum(widths)], [y0 - 0.78 - 4 * row_h, y0 - 0.78 - 4 * row_h], color=BORDER, lw=0.8)

    card(ax, 0.68, 1.14, 5.86, 0.82, fc=LIGHT_CORAL, ec="none", r=0.12)
    text(ax, 0.92, 1.72, "p-valor não é tamanho de efeito", size=8.8, color=CORAL, weight="bold")
    text(ax, 0.92, 1.42, "VIP é significativo (p = 0,0005), mas V = 0,037: irrelevante na prática.", size=9.2, color=INK, wrap=64)

    card(ax, 6.78, 1.14, 5.86, 0.82, fc=LIGHT_TEAL, ec="none", r=0.12)
    text(ax, 7.02, 1.72, "Pressupostos verificados", size=8.8, color=TEAL_DARK, weight="bold")
    text(ax, 7.02, 1.42, "Levene rejeitou homocedasticidade: Welch e Games-Howell no lugar de Student e Tukey.", size=9.2, color=INK, wrap=64)
    text(ax, 0.7, 0.98, "Fonte: Seção 4. Valores exatos e IC 95% no documento de conclusões.", size=8.2, color=MUTED)
    footer(ax, n)


def slide_11_effect(fig, ax, n):
    header(ax, "Leitura estatística", "Significância não é relevância", "Tamanho do efeito: onde a diferença importa de verdade")
    axc = fig.add_axes([1.42 / W, 1.62 / H, 5.66 / W, 4.1 / H], zorder=5)
    axc.set_facecolor(WHITE)
    labels = ["Criossono", "Planeta", "VIP"]
    vals = [0.467, 0.197, 0.037]
    colors = [CORAL, GOLD, GRAY]
    bars = axc.barh(labels[::-1], vals[::-1], color=colors[::-1], height=0.48)
    for b, v in zip(bars, vals[::-1]):
        axc.text(v + 0.012, b.get_y() + b.get_height() / 2, f"{v:.3f}".replace(".", ","), va="center", fontsize=11, color=INK, fontweight="bold")
    for t, lab in ((0.1, "fraco"), (0.3, "moderado"), (0.5, "forte")):
        axc.axvline(t, color=BORDER, lw=1, ls="--", zorder=1)
        axc.text(t, 2.46, lab, ha="center", va="bottom", fontsize=7.5, color=MUTED)
    axc.set_xlim(0, 0.56)
    axc.set_ylim(-0.5, 2.5)
    axc.set_xlabel("V de Cramér", fontsize=9, color=GRAY)
    axc.tick_params(axis="both", labelsize=10)
    for s in ("top", "right"):
        axc.spines[s].set_visible(False)
    axc.grid(axis="x", color="#EEF2F7", lw=0.8)
    axc.set_axisbelow(True)
    axc.set_title("Associações categóricas", fontsize=10.5, color=INK, fontweight="bold", loc="left", pad=10)

    card(ax, 7.5, 4.56, 5.14, 1.2, fc=WHITE, ec=BORDER, r=0.14)
    text(ax, 7.74, 5.46, "d de Cohen = 0,407", size=14, color=TEAL_DARK, weight="bold")
    text(ax, 7.74, 5.1, "Gasto × transporte: efeito moderado, com +US$ 1.120,74.", size=9.2, color=GRAY, wrap=54)
    card(ax, 7.5, 3.2, 5.14, 1.2, fc=WHITE, ec=BORDER, r=0.14)
    text(ax, 7.74, 4.1, "η² = 0,171", size=14, color=GOLD, weight="bold")
    text(ax, 7.74, 3.74, "Origem explica 17,1% da variância do gasto: efeito grande.", size=9.2, color=GRAY, wrap=54)
    card(ax, 7.5, 1.44, 5.14, 1.5, fc=LIGHT_CORAL, ec="none", r=0.14)
    text(ax, 7.74, 2.66, "A lição do VIP", size=8.8, color=CORAL, weight="bold")
    text(ax, 7.74, 2.34, "χ² significativo (p = 0,0005), V = 0,037. Com n grande, quase tudo fica significativo — o que importa é a magnitude.", size=9.2, color=INK, wrap=52)
    footer(ax, n)


def slide_12_correlation(fig, ax, n):
    header(ax, "Correlação", "Quem consome um serviço tende a consumir outros", "Pearson e Spearman lado a lado")
    card(ax, 0.68, 1.12, 5.36, 5.0, fc=WHITE, ec=BORDER, r=0.16)
    add_image(ax, "kan30_heatmap_spearman.png", 0.86, 1.32, 5.0, 4.4)
    text(ax, 0.86, 1.26, "Matriz de Spearman — 8 variáveis quantitativas", size=8.2, color=MUTED)

    text(ax, 6.34, 5.84, "0,67", size=25, color=TEAL_DARK, weight="bold")
    text(ax, 7.22, 5.92, "FoodCourt × TotalSpend", size=10.5, color=INK, weight="bold")
    text(ax, 7.22, 5.6, "a maior correlação — esperada, pois o total é a soma", size=9, color=GRAY, wrap=44)

    text(ax, 6.34, 4.98, "0,52", size=25, color=GOLD, weight="bold")
    text(ax, 7.22, 5.06, "FoodCourt × VRDeck", size=10.5, color=INK, weight="bold")
    text(ax, 7.22, 4.74, "uso combinado de serviços; Spearman supera Pearson", size=9, color=GRAY, wrap=44)

    text(ax, 6.34, 4.12, "−0,18", size=25, color=CORAL, weight="bold")
    text(ax, 7.22, 4.2, "Age × GroupSize", size=10.5, color=INK, weight="bold")
    text(ax, 7.22, 3.88, "a relação negativa mais forte, ainda assim fraca", size=9, color=GRAY, wrap=44)

    card(ax, 6.28, 1.72, 6.36, 1.26, fc=LIGHT_GOLD, ec="none", r=0.14)
    text(ax, 6.52, 2.8, "Cuidado com multicolinearidade", size=9, color="#9A6B00", weight="bold")
    text(
        ax,
        6.52,
        2.5,
        "HomePlanet e CabinDeck se sobrepõem: 72,6% dos europeus estão nos decks B/C e o deck G é 100% Terra. "
        "O VIF de Europa chega a 7,98 no treino.",
        size=9.6,
        color=INK,
        wrap=72,
        lh=1.35,
    )
    text(ax, 6.34, 0.94, "Fonte: Seção 5, KAN-30.", size=8.2, color=MUTED)
    footer(ax, n)


def slide_13_model(fig, ax, n):
    header(ax, "Modelo preditivo", "Um apoio à triagem, não uma sentença", "Regressão logística com limiar 0,5 fixado a priori")
    metrics = [
        ("77,9%", "acurácia", TEAL_DARK),
        ("0,862", "ROC-AUC", TEAL_DARK),
        ("0,784", "F1", GOLD),
        ("+25,5 p.p.", "sobre o baseline", CORAL),
    ]
    x = 0.68
    for value, label, color in metrics:
        card(ax, x, 5.06, 2.86, 1.12, fc=WHITE, ec=BORDER, r=0.13)
        text(ax, x + 0.18, 5.78, value, size=24, color=color, weight="bold")
        text(ax, x + 0.18, 5.34, label, size=9.5, color=GRAY)
        x += 3.02

    card(ax, 0.68, 1.2, 7.24, 3.7, fc=WHITE, ec=BORDER, r=0.14)
    add_image(ax, "kan34_curvas_roc_pr.png", 0.86, 1.44, 6.88, 3.1)
    text(ax, 0.86, 1.34, "Curvas ROC e Precision-Recall no conjunto de teste", size=8.2, color=MUTED)

    card(ax, 8.14, 1.2, 4.5, 3.7, fc=WHITE, ec=BORDER, r=0.14)
    add_image(ax, "kan34_matriz_confusao.png", 8.3, 1.6, 4.18, 2.9)
    text(ax, 8.3, 1.34, "Matriz de confusão — 1.739 passageiros", size=8.2, color=MUTED)

    text(ax, 0.7, 0.94, "Teste: 20% da base (1.739 passageiros), divisão estratificada, random_state = 42.", size=8.2, color=MUTED)
    footer(ax, n)


def slide_14_odds(fig, ax, n):
    header(ax, "Interpretação do modelo", "O que o modelo aprendeu, ajustado pelas demais variáveis", "Odds Ratios com IC 95% — associações, não causas")
    axc = fig.add_axes([1.55 / W, 1.62 / H, 5.95 / W, 4.26 / H], zorder=5)
    axc.set_facecolor(WHITE)
    labels = [
        "Europa",
        "Criossono",
        "FoodCourt",
        "Marte",
        "ShoppingMall",
        "CabinSide P",
        "RoomService",
        "Deck G",
        "Spa",
    ]
    vals = [3.97, 3.21, 1.48, 1.40, 1.24, 0.60, 0.55, 0.53, 0.48]
    colors = [TEAL_DARK if v >= 1 else CORAL for v in vals]
    bars = axc.barh(labels[::-1], vals[::-1], color=colors[::-1], height=0.56)
    for b, v in zip(bars, vals[::-1]):
        shown = f"{v:.2f}".replace(".", ",")
        axc.text(v + 0.07, b.get_y() + b.get_height() / 2, shown, va="center", fontsize=9, color=INK, fontweight="bold")
    axc.axvline(1, color=INK, lw=1.2, ls="--")
    axc.set_xlim(0, 4.55)
    axc.set_xlabel("Odds Ratio (escala linear; 1 = sem associação)", fontsize=8.8, color=GRAY)
    axc.tick_params(axis="both", labelsize=8.8)
    for s in ("top", "right"):
        axc.spines[s].set_visible(False)
    axc.grid(axis="x", color="#EEF2F7", lw=0.8)
    axc.set_axisbelow(True)
    text(
        ax,
        1.55,
        1.02,
        "Referências: Terra, acordado, deck F, lado S; gastos por 1 DP de log1p.",
        size=7.5,
        color=MUTED,
    )

    text(ax, 7.72, 5.86, "Como ler", size=9.5, color=TEAL_DARK, weight="bold")
    text(ax, 7.72, 5.54, "OR > 1 aumenta a chance de transporte; OR < 1 reduz.", size=9.6, color=GRAY, wrap=46)
    card(ax, 7.68, 3.86, 4.98, 1.38, fc=LIGHT_TEAL, ec="none", r=0.14)
    text(ax, 7.92, 4.94, "Criossono: OR = 3,21", size=10, color=TEAL_DARK, weight="bold")
    text(ax, 7.92, 4.6, "Chance 3,2× maior, já descontando gastos, origem, deck e demais variáveis.", size=9.2, color=INK, wrap=50)
    card(ax, 7.68, 2.34, 4.98, 1.34, fc=LIGHT_GOLD, ec="none", r=0.14)
    text(ax, 7.92, 3.38, "Europa: OR = 3,97", size=10, color="#9A6B00", weight="bold")
    text(ax, 7.92, 3.04, "Associação estimada dentro dos decks em que os planetas coexistem.", size=9.2, color=INK, wrap=50)
    text(ax, 7.72, 1.66, "Pseudo-R² de McFadden = 0,311 no treino.", size=8.8, color=GRAY)
    text(ax, 7.72, 1.3, "Fonte: Seção 5, KAN-33/34.", size=8.2, color=MUTED)
    footer(ax, n)


def slide_15_conclusions(fig, ax, n):
    header(ax, "Conclusões", "Três achados que respondem à pergunta", "O que os dados sustentam — e com qual força")
    items = [
        ("01", "Criossono", "81,47%", "vs. 32,82% dos acordados", "V = 0,467 · associação muito forte", CORAL),
        ("02", "Origem e deck", "66,05%", "Europa; Terra fica em 42,33%", "72,6% dos europeus nos decks B/C", GOLD),
        ("03", "Gasto", "41,92%", "não gastaram nada", "medianas: US$ 0 e US$ 907", TEAL_DARK),
    ]
    x = 0.68
    for num, title, value, desc, detail, color in items:
        card(ax, x, 1.66, 3.88, 4.36, fc=WHITE, ec=BORDER, r=0.16)
        ax.add_patch(Rectangle((x, 5.83), 3.88, 0.19, color=color, zorder=4))
        text(ax, x + 0.24, 5.44, num, size=9.5, color=color, weight="bold")
        text(ax, x + 0.24, 5.0, title, size=14, color=INK, weight="bold", wrap=22)
        text(ax, x + 0.24, 4.04, value, size=30, color=color, weight="bold")
        text(ax, x + 0.24, 3.5, desc, size=9.6, color=GRAY, wrap=28)
        ax.plot([x + 0.24, x + 3.62], [3.16, 3.16], color=BORDER, lw=1)
        text(ax, x + 0.24, 2.86, detail, size=9, color=INK, wrap=30, lh=1.35)
        x += 3.02
    text(ax, 0.7, 1.16, "Todas as leituras são observacionais. Nenhum achado autoriza afirmar causalidade.", size=10, color=GRAY)
    footer(ax, n)


def slide_16_recommendations(fig, ax, n):
    header(ax, "Recomendações", "O que o cliente pode fazer com isso", "Quatro ações práticas, em ordem de prioridade")
    recs = [
        ("1", "Priorizar a inspeção das cápsulas de criossono", "É a associação mais forte e a mais acionável: 81,47% vs. 32,82%.", CORAL),
        ("2", "Investigar a diferença por origem, cruzada com deck e classe", "Origem e localização física se sobrepõem; não usar origem isolada.", GOLD),
        ("3", "Abandonar o gasto como proxy de presença ou importância", "41,92% não gastaram nada; usar cabine, grupo e criossono.", TEAL_DARK),
        ("4", "Usar o modelo como triagem, com revisão humana", "Recall 0,796 e limiar 0,5 fixado a priori; recalibrar pelo custo do erro.", "#7C6FD6"),
    ]
    positions = [(0.68, 3.7), (6.72, 3.7), (0.68, 1.3), (6.72, 1.3)]
    for (x, y), (num, title, desc, color) in zip(positions, recs):
        card(ax, x, y, 5.92, 2.14, fc=WHITE, ec=BORDER, r=0.16)
        ax.add_patch(Circle((x + 0.46, y + 1.66), 0.25, color=color, zorder=5))
        text(ax, x + 0.46, y + 1.66, num, size=10.5, color=WHITE, weight="bold", ha="center", va="center", z=6)
        text(ax, x + 0.86, y + 1.84, title, size=11.2, color=INK, weight="bold", wrap=44)
        ax.plot([x + 0.24, x + 5.68], [y + 0.98, y + 0.98], color=BORDER, lw=1)
        text(ax, x + 0.24, y + 0.8, "POR QUÊ", size=7.4, color=MUTED, weight="bold")
        text(ax, x + 0.24, y + 0.58, desc, size=9.3, color=GRAY, wrap=62)
    text(ax, 0.7, 0.94, "Próximo passo operacional: validar o modelo em uma divisão por grupo de viagem antes de qualquer uso real.", size=8.6, color=MUTED, wrap=140)
    footer(ax, n)


def slide_17_limits(fig, ax, n):
    header(ax, "Limitações", "O que este estudo não permite afirmar", "Transparência metodológica para a banca")
    text(ax, 0.72, 5.72, "Limitações", size=9.5, color=CORAL, weight="bold")
    limits = [
        ("Associação não é causa", "O desenho é observacional e não isola mecanismos."),
        ("Divisão única de treino e teste", "Sem intervalo de incerteza para as métricas."),
        ("Divisão por passageiro, não por grupo", "Famílias podem aparecer dos dois lados; avaliação possivelmente otimista."),
        ("Imputação pela moda", "2,1% a 2,5% das categóricas; impacto máximo de 0,77 p.p."),
        ("Multicolinearidade", "HomePlanet_Europa com VIF de 7,98: coeficientes exigem cautela."),
    ]
    y = 5.28
    for title, desc in limits:
        ax.add_patch(Circle((0.82, y + 0.1), 0.055, color=CORAL, zorder=5))
        text(ax, 1.02, y + 0.24, title, size=10.2, color=INK, weight="bold")
        text(ax, 1.02, y - 0.04, desc, size=9.1, color=GRAY, wrap=58)
        y -= 0.82

    text(ax, 7.04, 5.72, "Próximos passos", size=9.5, color=TEAL_DARK, weight="bold")
    steps = [
        ("Validação por grupo de viagem", "Reavaliar o modelo com GroupKFold ou divisão por família."),
        ("Intervalos de confiança", "Bootstrap para acurácia, ROC-AUC e F1."),
        ("Recalibrar o limiar", "Definir o custo relativo de falso positivo e falso negativo."),
        ("Aprofundar origem × deck", "Modelo hierárquico ou análise estratificada por deck."),
    ]
    y = 5.28
    for i, (title, desc) in enumerate(steps, 1):
        ax.add_patch(Circle((7.14, y + 0.1), 0.19, color=TEAL, zorder=5))
        text(ax, 7.14, y + 0.1, str(i), size=9, color=WHITE, weight="bold", ha="center", va="center", z=6)
        text(ax, 7.48, y + 0.24, title, size=10.2, color=INK, weight="bold")
        text(ax, 7.48, y - 0.04, desc, size=9.1, color=GRAY, wrap=52)
        y -= 0.92
    text(ax, 0.7, 0.94, "A cautela não enfraquece o trabalho: define o que ele autoriza recomendar.", size=9.5, color=GRAY, weight="bold")
    footer(ax, n)


def slide_18_closing(fig, ax, n):
    gradient(ax, "#081426", "#122A4D")
    stars(ax, 170, 0.7)
    for r, a in ((3.2, 0.10), (2.2, 0.16)):
        ax.add_patch(Circle((11.5, 1.3), r, fill=False, ec=TEAL, lw=1.1, alpha=a, zorder=2))
    ax.add_patch(Circle((11.5, 1.3), 0.14, color=TEAL, alpha=0.9, zorder=3))

    text(ax, 0.8, 6.5, "OBRIGADO", size=11, color=TEAL, weight="bold")
    text(ax, 0.8, 5.96, "O que levamos desta análise", size=30, color=WHITE, weight="bold")
    text(
        ax,
        0.82,
        4.96,
        "Metade da nave foi transportada. O criossono é o sinal mais forte, a origem e o deck "
        "contam a mesma história, e o gasto não é um bom atalho. O modelo ajuda a triar — não substitui o juízo humano.",
        size=14,
        color="#DDE7F3",
        wrap=64,
        lh=1.45,
    )

    facts = [("81,47%", "criossono"), ("66,05%", "Europa"), ("77,9%", "acurácia")]
    x = 0.82
    for value, label in facts:
        card(ax, x, 2.2, 2.34, 0.98, fc="#142D50", ec="#28476F", r=0.12, shadow=False)
        text(ax, x + 0.18, 2.9, value, size=19, color=TEAL, weight="bold")
        text(ax, x + 0.2, 2.42, label, size=8.8, color="#C7D4E6")
        x += 2.52

    text(ax, 0.82, 1.62, "Perguntas?", size=20, color=WHITE, weight="bold")
    text(ax, 0.82, 0.78, "Gustavo Menezes  ·  Helton Gomes  ·  Luciana Almeida  ·  Daniela Amaro  ·  Renatta", size=9.5, color="#9FB2CA")
    text(ax, W - 0.8, 0.78, "CIn/UFPE  ·  2026", size=9.5, color="#9FB2CA", ha="right")


SLIDES = [
    slide_01_cover,
    slide_02_summary,
    slide_03_problem,
    slide_04_data,
    slide_05_method,
    slide_06_cryo,
    slide_07_origin,
    slide_08_spend,
    slide_09_probability,
    slide_10_tests,
    slide_11_effect,
    slide_12_correlation,
    slide_13_model,
    slide_14_odds,
    slide_15_conclusions,
    slide_16_recommendations,
    slide_17_limits,
    slide_18_closing,
]


def main():
    parser = argparse.ArgumentParser(description="Gera o PDF de apresentação final (16:9).")
    parser.add_argument("--preview", type=Path, default=None, help="Diretório opcional para PNGs de conferência.")
    args = parser.parse_args()

    if args.preview:
        args.preview.mkdir(parents=True, exist_ok=True)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    total = len(SLIDES)
    with PdfPages(OUT) as pdf:
        pdf.infodict().update(
            {
                "Title": "Spaceship Titanic — Apresentação Final",
                "Author": "Gustavo Menezes, Helton Gomes, Luciana Almeida, Daniela Amaro e Renatta",
                "Subject": "Projeto Final de Estatística Avançada — CIn/UFPE",
                "Keywords": "estatística, Spaceship Titanic, regressão logística, testes de hipóteses",
            }
        )
        for i, builder in enumerate(SLIDES, 1):
            fig, ax = new_slide()
            builder(fig, ax, i)
            if args.preview:
                fig.savefig(args.preview / f"slide_{i:02d}.png", dpi=110, facecolor=fig.get_facecolor())
            pdf.savefig(fig, facecolor=fig.get_facecolor())
            plt.close(fig)

    print(f"PDF gerado: {OUT.relative_to(ROOT)} ({total} slides, {OUT.stat().st_size / 1e6:.2f} MB)")


if __name__ == "__main__":
    main()
