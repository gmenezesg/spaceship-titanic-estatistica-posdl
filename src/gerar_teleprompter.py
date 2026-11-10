"""Gera o teleprompter em PDF a partir do roteiro em Markdown.

Uso:
    python src/gerar_teleprompter.py
    python src/gerar_teleprompter.py --preview /tmp/opencode/teleprompter

Entrada : docs/apresentacao/teleprompter_apresentacao.md
Saída   : report/teleprompter_apresentacao.pdf (A4 retrato, uma página por slide)

O Markdown usa um formato fixo:
    ## NN · m:ss · Título      -> início de uma página
    > rubrica                  -> indicação de palco (não falada)
    [PAUSA] / [APONTE] ...     -> marcação de cena (não falada)
    demais linhas              -> fala, uma linha por grupo de respiração
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties
from matplotlib.patches import FancyBboxPatch, Rectangle

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "docs" / "apresentacao" / "teleprompter_apresentacao.md"
OUT = ROOT / "report" / "teleprompter_apresentacao.pdf"

PAGE_W, PAGE_H = 8.27, 11.69  # A4 retrato, polegadas
MARGIN = 0.55
TEXT_W = PAGE_W - 2 * MARGIN

INK = "#152238"
TEAL = "#0F766E"
TEAL_SOFT = "#E8F5F2"
CORAL = "#C2410C"
GRAY = "#52606D"
MUTED = "#8A97A8"
BORDER = "#DCE4EE"
BG = "#FCFDFF"

plt.rcParams.update(
    {
        "font.family": ["Lato", "DejaVu Sans"],
        "text.parse_math": False,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    }
)

HEADER = re.compile(r"^##\s+(\d{2})\s+·\s+([\d:]+)\s+·\s+(.+)$")
SIZES = (21.0, 20.0, 19.0, 18.0, 17.0, 16.0, 15.0, 14.0, 13.0, 12.0, 11.0)


@dataclass
class Section:
    num: str
    time: str
    title: str
    lines: list[str]

    @property
    def is_slide(self) -> bool:
        return 1 <= int(self.num) <= 18

    @property
    def kicker(self) -> str:
        if self.is_slide:
            return f"SLIDE {self.num} / 18"
        return "COMO USAR" if self.num == "00" else "COLA DE EMERGÊNCIA"


@dataclass
class Item:
    kind: str  # speech | cue | direction
    text: str
    height: float
    gap_before: float


def parse(path: Path) -> list[Section]:
    sections: list[Section] = []
    current: Section | None = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        match = HEADER.match(raw)
        if match:
            current = Section(match.group(1), match.group(2), match.group(3).strip(), [])
            sections.append(current)
        elif current is not None and raw.strip() != "---":
            current.lines.append(raw)
    return sections


class Wrapper:
    """Mede e quebra linhas em polegadas, com as métricas reais da fonte."""

    def __init__(self) -> None:
        self._fig = Figure(figsize=(1, 1), dpi=72)
        self._renderer = FigureCanvasAgg(self._fig).get_renderer()

    def width(self, text: str, size: float, weight: str = "normal", style: str = "normal") -> float:
        prop = FontProperties(family=["Lato", "DejaVu Sans", "sans-serif"], size=size, weight=weight, style=style)
        return self._renderer.get_text_width_height_descent(text, prop, False)[0] / 72.0

    def wrap(self, text: str, size: float, max_w: float, weight: str = "normal", style: str = "normal") -> list[str]:
        words = text.split()
        if not words:
            return [""]
        lines: list[str] = []
        current = words[0]
        for word in words[1:]:
            candidate = f"{current} {word}"
            if self.width(candidate, size, weight, style) <= max_w:
                current = candidate
            else:
                lines.append(current)
                current = word
        lines.append(current)
        # evita órfão de uma palavra na última linha (ex.: um número sozinho)
        if len(lines) > 1 and len(lines[-1].split()) == 1 and len(lines[-2].split()) > 2:
            previous = lines[-2].split()
            lines[-1] = f"{previous[-1]} {lines[-1]}"
            lines[-2] = " ".join(previous[:-1])
        return lines


def layout(section: Section, size: float, wrap: Wrapper) -> list[Item]:
    items: list[Item] = []
    pending_gap = 0.0
    for raw in section.lines:
        line = raw.rstrip()
        if not line.strip():
            pending_gap = max(pending_gap, 0.10)
            continue
        if line.startswith(">"):
            text = line.lstrip("> ").strip()
            for part in wrap.wrap(text, 10.5, TEXT_W - 0.16, style="italic"):
                items.append(Item("direction", part, 10.5 * 1.32 / 72, pending_gap))
                pending_gap = 0.0
            pending_gap = 0.08
            continue
        if line.startswith("["):
            items.append(Item("cue", line, 11.5 * 1.32 / 72, max(pending_gap, 0.06)))
            pending_gap = 0.10
            continue
        for part in wrap.wrap(line, size, TEXT_W):
            items.append(Item("speech", part, size * 1.30 / 72, pending_gap))
            pending_gap = 0.0
    return items


def total_height(items: list[Item]) -> float:
    return sum(item.gap_before + item.height for item in items)


def pick_layout(section: Section, available: float, wrap: Wrapper) -> tuple[float, list[Item]]:
    for size in SIZES:
        items = layout(section, size, wrap)
        if total_height(items) <= available:
            return size, items
    return SIZES[-1], layout(section, SIZES[-1], wrap)


def draw_page(fig: Figure, section: Section, wrap: Wrapper, next_label: str) -> None:
    fig.patch.set_facecolor(BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, PAGE_W)
    ax.set_ylim(PAGE_H, 0)  # y cresce para baixo
    ax.axis("off")

    ax.text(MARGIN, 0.44, section.kicker, fontsize=8.5, color=TEAL, fontweight="bold", va="top")
    pill_x, pill_w = PAGE_W - MARGIN - 0.72, 0.72
    ax.add_patch(
        FancyBboxPatch(
            (pill_x, 0.30),
            pill_w,
            0.28,
            boxstyle="round,pad=0,rounding_size=0.14",
            facecolor=TEAL_SOFT,
            edgecolor="none",
            zorder=3,
        )
    )
    ax.text(pill_x + pill_w / 2, 0.44, section.time, ha="center", va="center", fontsize=10.5, color=TEAL, fontweight="bold", zorder=4)

    title_lines = wrap.wrap(section.title, 24, TEXT_W, weight="bold")
    y = 0.80
    for line in title_lines:
        ax.text(MARGIN, y, line, fontsize=24, color=INK, fontweight="bold", va="top")
        y += 24 * 1.16 / 72
    divider_y = 0.80 + len(title_lines) * 24 * 1.16 / 72 + 0.20
    ax.plot([MARGIN, PAGE_W - MARGIN], [divider_y, divider_y], color=BORDER, lw=0.9)

    text_top = divider_y + 0.26
    size, items = pick_layout(section, 11.10 - text_top, wrap)

    y = text_top
    for item in items:
        y += item.gap_before
        if item.kind == "cue":
            ax.add_patch(Rectangle((MARGIN, y + 0.02), 0.045, item.height - 0.05, facecolor=CORAL, edgecolor="none"))
            ax.text(MARGIN + 0.15, y, item.text, fontsize=11.5, color=CORAL, fontweight="bold", va="top")
        elif item.kind == "direction":
            ax.add_patch(Rectangle((MARGIN, y + 0.02), 0.03, item.height - 0.05, facecolor=BORDER, edgecolor="none"))
            ax.text(MARGIN + 0.14, y, item.text, fontsize=10.5, color=GRAY, style="italic", va="top")
        else:
            ax.text(MARGIN, y, item.text, fontsize=size, color=INK, va="top")
        y += item.height

    if y < 10.45:
        ax.text(MARGIN, 10.62, next_label, fontsize=9.5, color=MUTED, va="top", style="italic")

    ax.plot([MARGIN, PAGE_W - MARGIN], [11.30, 11.30], color=BORDER, lw=0.7)
    ax.text(MARGIN, 11.40, "Teleprompter · Spaceship Titanic · CIn/UFPE", fontsize=7.8, color=MUTED, va="top")
    ax.text(PAGE_W - MARGIN, 11.40, "associação ≠ causalidade", fontsize=7.8, color=MUTED, va="top", ha="right")


def main() -> None:
    parser = argparse.ArgumentParser(description="Gera o teleprompter em PDF (A4 retrato).")
    parser.add_argument("--preview", type=Path, default=None, help="Diretório opcional para PNGs de conferência.")
    args = parser.parse_args()

    sections = parse(SRC)
    if not sections:
        raise SystemExit(f"Nenhuma seção encontrada em {SRC}")

    wrap = Wrapper()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    if args.preview:
        args.preview.mkdir(parents=True, exist_ok=True)

    with PdfPages(OUT) as pdf:
        pdf.infodict().update(
            {
                "Title": "Teleprompter — Apresentação Final (Spaceship Titanic)",
                "Author": "Gustavo Menezes, Helton Gomes, Luciana Almeida, Daniela Amaro e Renatta",
                "Subject": "Roteiro de fala por slide — Projeto Final de Estatística — CIn/UFPE",
                "Keywords": "teleprompter, apresentação, estatística, Spaceship Titanic",
            }
        )
        for index, section in enumerate(sections, 1):
            fig = plt.figure(figsize=(PAGE_W, PAGE_H), dpi=72)
            if index < len(sections):
                nxt = sections[index]
                next_label = f"→  A seguir: {nxt.num} · {nxt.title}" if nxt.is_slide else "→  Fim · perguntas"
            else:
                next_label = "→  Fim · perguntas"
            draw_page(fig, section, wrap, next_label)
            if args.preview:
                fig.savefig(args.preview / f"page_{index:02d}.png", dpi=110, facecolor=fig.get_facecolor())
            pdf.savefig(fig, facecolor=fig.get_facecolor())
            plt.close(fig)

    print(f"PDF gerado: {OUT.relative_to(ROOT)} ({len(sections)} páginas, {OUT.stat().st_size / 1e6:.2f} MB)")


if __name__ == "__main__":
    main()
