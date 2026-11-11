"""Gera o PDF do Roteiro de Compartilhamento de Conhecimento e Ata da Reunião 2 (KAN-36).

Produz um documento diagramado em formato A4 com fluxo vertical dinâmico,
medição precisa de fontes e ausência absoluta de sobreposição de textos ou blocos.

Uso:
    python src/gerar_pdf_reuniao_02.py
    python src/gerar_pdf_reuniao_02.py --preview /tmp/preview_pdf
"""

from __future__ import annotations

import argparse
import shutil
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
OUT_REPORT = ROOT / "report" / "roteiro_compartilhamento_reuniao_02.pdf"
OUT_DOCS = ROOT / "docs" / "ata_reuniao_02.pdf"

# Dimensões da folha A4 em polegadas
PAGE_W, PAGE_H = 8.27, 11.69
MARGIN_X = 0.55
CONTENT_W = PAGE_W - 2 * MARGIN_X  # 7.17 in

# Paleta de Cores Institucional
NAVY = "#0B1B33"
NAVY_LIGHT = "#162D50"
TEAL = "#0F766E"
TEAL_ACCENT = "#2EC4B6"
TEAL_BG = "#F0FDF4"
TEAL_BORDER = "#86EFAC"
AMBER_BG = "#FFFBEB"
AMBER_BORDER = "#FCD34D"
CORAL = "#C2410C"
BG_PAGE = "#FFFFFF"
TEXT_MAIN = "#0F172A"
TEXT_MUTED = "#334155"
BORDER_CARD = "#CBD5E1"
CARD_BG = "#F8FAFC"

plt.rcParams.update(
    {
        "font.family": ["DejaVu Sans", "sans-serif"],
        "text.parse_math": False,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    }
)


class TextWrapper:
    """Mede e quebra linhas de texto em polegadas usando as métricas reais da fonte."""

    def __init__(self) -> None:
        self._fig = Figure(figsize=(1, 1), dpi=72)
        self._renderer = FigureCanvasAgg(self._fig).get_renderer()

    def width(self, text: str, size: float, weight: str = "normal", style: str = "normal") -> float:
        prop = FontProperties(family=["DejaVu Sans", "sans-serif"], size=size, weight=weight, style=style)
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
        return lines


WRAPPER = TextWrapper()


@dataclass
class CardItem:
    label: str
    text: str


@dataclass
class CardSpec:
    title: str
    items: list[CardItem]
    layout_mode: str = "block"  # "block" ou "table"
    bg_color: str = CARD_BG
    border_color: str = BORDER_CARD
    accent_color: str = TEAL
    title_color: str = TEAL
    col1_w: float = 2.05  # Largura fixa da coluna de label em layout de tabela


class PageLayoutManager:
    """Gerencia a renderização de uma página A4 com posicionamento vertical dinâmico e sem sobreposições."""

    def __init__(self, page_num: int, total_pages: int, title: str, subtitle: str, badge: str = ""):
        self.page_num = page_num
        self.total_pages = total_pages
        self.title = title
        self.subtitle = subtitle
        self.badge = badge

        self.fig = plt.figure(figsize=(PAGE_W, PAGE_H), dpi=300)
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.fig.patch.set_facecolor(BG_PAGE)
        self.ax.set_facecolor(BG_PAGE)
        self.ax.set_xlim(0, PAGE_W)
        self.ax.set_ylim(0, PAGE_H)
        self.ax.axis("off")

        self.header_height = 1.42
        self.content_top = PAGE_H - self.header_height - 0.20  # ~10.07 in
        self.content_bottom = 0.58  # 0.58 in
        self.usable_height = self.content_top - self.content_bottom  # ~9.49 in

        self._draw_header()
        self._draw_footer()

    def _draw_header(self):
        # 1. Fundo do cabeçalho
        self.ax.add_patch(
            Rectangle((0, PAGE_H - self.header_height), PAGE_W, self.header_height, facecolor=NAVY, edgecolor="none", zorder=1)
        )
        self.ax.add_patch(
            Rectangle((0, PAGE_H - self.header_height - 0.04), PAGE_W, 0.04, facecolor=TEAL_ACCENT, edgecolor="none", zorder=2)
        )

        # 2. Linha 1 do Header: Identificação Institucional e Badge
        self.ax.text(
            MARGIN_X,
            PAGE_H - 0.36,
            "CIn / UFPE · PROJETO FINAL DE ESTATÍSTICA",
            fontsize=8.2,
            fontweight="bold",
            color=TEAL_ACCENT,
            zorder=3,
        )

        if self.badge:
            # Badge posicionado no canto superior direito, alinhado à margem
            badge_w = WRAPPER.width(self.badge, 7.5, weight="bold") + 0.35
            badge_x = PAGE_W - MARGIN_X - badge_w
            badge_y = PAGE_H - 0.48
            badge_h = 0.28

            self.ax.add_patch(
                FancyBboxPatch(
                    (badge_x, badge_y),
                    badge_w,
                    badge_h,
                    boxstyle="round,pad=0.02,rounding_size=0.06",
                    facecolor=NAVY_LIGHT,
                    edgecolor=TEAL_ACCENT,
                    linewidth=0.8,
                    zorder=3,
                )
            )
            self.ax.text(
                badge_x + badge_w / 2.0,
                badge_y + badge_h / 2.0,
                self.badge,
                fontsize=7.5,
                fontweight="bold",
                color="#FFFFFF",
                ha="center",
                va="center",
                zorder=4,
            )

        # 3. Linha 2 do Header: Título Principal (ocupa toda a largura útil, sem colisão)
        title_lines = WRAPPER.wrap(self.title, 12.0, CONTENT_W, weight="bold")
        title_y = PAGE_H - 0.76
        for line in title_lines:
            self.ax.text(
                MARGIN_X,
                title_y,
                line,
                fontsize=12.0,
                fontweight="bold",
                color="#FFFFFF",
                zorder=3,
            )
            title_y -= 0.22

        # 4. Linha 3 do Header: Subtítulo / Metadados
        sub_lines = WRAPPER.wrap(self.subtitle, 8.5, CONTENT_W)
        sub_y = PAGE_H - 1.18
        for line in sub_lines:
            self.ax.text(
                MARGIN_X,
                sub_y,
                line,
                fontsize=8.5,
                color="#E2E8F0",
                zorder=3,
            )
            sub_y -= 0.17

    def _draw_footer(self):
        self.ax.add_patch(Rectangle((MARGIN_X, 0.48), CONTENT_W, 0.015, facecolor=BORDER_CARD, edgecolor="none", zorder=1))
        self.ax.text(
            MARGIN_X,
            0.30,
            "Ticket Jira KAN-36 · Roteiro de Nivelamento e Ata da Reunião 2",
            fontsize=7.5,
            color=TEXT_MUTED,
            zorder=2,
        )
        self.ax.text(
            PAGE_W - MARGIN_X,
            0.30,
            f"Página {self.page_num} de {self.total_pages}",
            fontsize=7.5,
            fontweight="bold",
            color=NAVY,
            ha="right",
            zorder=2,
        )

    def calculate_card_height(self, card: CardSpec) -> float:
        """Calcula a altura estrita necessária para conter o card com margem de segurança."""
        title_h = 0.40
        padding_bottom = 0.22

        if card.layout_mode == "table":
            # Tabela em 2 colunas com limites rigorosos
            content_h = 0.0
            col2_w = CONTENT_W - card.col1_w - 0.90
            for it in card.items:
                lbl_lines = WRAPPER.wrap(it.label, 8.0, card.col1_w - 0.15, weight="bold")
                val_lines = WRAPPER.wrap(it.text, 7.8, col2_w)
                row_lines = max(len(lbl_lines), len(val_lines))
                row_h = row_lines * 0.17 + 0.10
                content_h += row_h
            return title_h + content_h + padding_bottom

        else:
            # Modo Bloco: Título do item + linhas de texto recuadas
            content_h = 0.0
            text_w = CONTENT_W - 0.60
            for it in card.items:
                if it.label:
                    item_h = 0.18  # Altura da linha do label
                    val_lines = WRAPPER.wrap(it.text, 7.8, text_w - 0.25)
                    item_h += len(val_lines) * 0.16 + 0.08  # Linhas do texto + espaçamento
                else:
                    val_lines = WRAPPER.wrap(it.text, 7.8, text_w)
                    item_h = len(val_lines) * 0.16 + 0.08
                content_h += item_h
            return title_h + content_h + padding_bottom

    def render_cards(self, cards: list[CardSpec]):
        """Renderiza os cards distribuindo o espaço vertical sem sobreposições."""
        heights = [self.calculate_card_height(c) for c in cards]
        total_cards_h = sum(heights)

        num_cards = len(cards)
        remaining_space = self.usable_height - total_cards_h

        # Calcula o gap proporcional entre os cards
        if num_cards > 1:
            raw_gap = remaining_space / (num_cards - 1)
            gap = max(0.12, min(raw_gap, 0.45))
        else:
            gap = 0.0

        current_y = self.content_top

        for card, card_h in zip(cards, heights):
            card_top = current_y
            card_bottom = card_top - card_h
            self._render_single_card(card, MARGIN_X, card_bottom, CONTENT_W, card_h)
            current_y = card_bottom - gap

    def _render_single_card(self, card: CardSpec, x: float, y: float, w: float, h: float):
        # 1. Fundo do Card com cantos arredondados
        self.ax.add_patch(
            FancyBboxPatch(
                (x, y),
                w,
                h,
                boxstyle="round,pad=0.02,rounding_size=0.08",
                facecolor=card.bg_color,
                edgecolor=card.border_color,
                linewidth=1.0,
                zorder=2,
            )
        )

        # 2. Barra de destaque no topo do card
        if card.accent_color:
            self.ax.add_patch(
                FancyBboxPatch(
                    (x, y + h - 0.045),
                    w,
                    0.045,
                    boxstyle="round,pad=0.01,rounding_size=0.03",
                    facecolor=card.accent_color,
                    edgecolor="none",
                    zorder=3,
                )
            )

        # 3. Título do Card
        self.ax.text(
            x + 0.20,
            y + h - 0.24,
            card.title.upper(),
            fontsize=8.5,
            fontweight="bold",
            color=card.title_color,
            zorder=4,
        )

        # 4. Renderização dos Itens
        curr_y = y + h - 0.46

        if card.layout_mode == "table":
            col2_x = x + 0.20 + card.col1_w + 0.15
            col2_w = w - card.col1_w - 0.90

            for idx, it in enumerate(card.items):
                lbl_lines = WRAPPER.wrap(it.label, 8.0, card.col1_w - 0.15, weight="bold")
                val_lines = WRAPPER.wrap(it.text, 7.8, col2_w)
                row_lines = max(len(lbl_lines), len(val_lines))
                row_h = row_lines * 0.17 + 0.10

                # Renderiza Label na Coluna 1
                lbl_y = curr_y
                for line in lbl_lines:
                    self.ax.text(x + 0.20, lbl_y, line, fontsize=8.0, fontweight="bold", color=TEXT_MAIN, zorder=4)
                    lbl_y -= 0.165

                # Renderiza Valor na Coluna 2
                val_y = curr_y
                for line in val_lines:
                    self.ax.text(col2_x, val_y, line, fontsize=7.8, color=TEXT_MUTED, zorder=4)
                    val_y -= 0.165

                # Linha divisória sutil (exceto na última linha)
                if idx < len(card.items) - 1:
                    div_y = curr_y - row_h + 0.05
                    self.ax.plot([x + 0.20, x + w - 0.20], [div_y, div_y], color=BORDER_CARD, linewidth=0.5, linestyle=":", zorder=3)

                curr_y -= row_h

        else:
            # Modo Bloco: Título com bullet + descrição recuada
            text_w = w - 0.60
            for it in card.items:
                if it.label:
                    # Linha do Label
                    self.ax.text(x + 0.20, curr_y, f"▸ {it.label}", fontsize=8.2, fontweight="bold", color=TEXT_MAIN, zorder=4)
                    curr_y -= 0.17

                    # Linhas de Texto com Recuo
                    val_lines = WRAPPER.wrap(it.text, 7.8, text_w - 0.25)
                    for line in val_lines:
                        self.ax.text(x + 0.38, curr_y, line, fontsize=7.8, color=TEXT_MUTED, zorder=4)
                        curr_y -= 0.155
                    curr_y -= 0.08
                else:
                    val_lines = WRAPPER.wrap(it.text, 7.8, text_w)
                    for line in val_lines:
                        self.ax.text(x + 0.22, curr_y, line, fontsize=7.8, color=TEXT_MUTED, zorder=4)
                        curr_y -= 0.155
                    curr_y -= 0.08


def make_page_1(total_pages: int) -> PageLayoutManager:
    p = PageLayoutManager(
        1,
        total_pages,
        "Roteiro de Nivelamento & Apresentações Cruzadas",
        "Reunião 2 · 31/10/2026 · Domínio Integral do Projeto e Eliminação de Silos",
        "KAN-36 · REUNIÃO 2",
    )

    cards = [
        CardSpec(
            title="1. Visão de Negócio & Alinhamento Estratégico",
            items=[
                CardItem("Objetivo Acadêmico", "Integrar o conteúdo de Estatística Avançada para IA de forma aplicada no Spaceship Titanic."),
                CardItem("Eliminação de Silos", "Garantir que todos os 5 membros dominem 100% da metodologia, dados e conclusões de todas as trilhas."),
                CardItem("Problema Analítico", "Determinar fatores sociodemográficos, espaciais e de consumo associados ao transporte (Transported)."),
                CardItem("Critérios de Avaliação", "Observância dos pesos: 30% Qualidade Técnica, 50% Clareza/Objetividade e 20% Reprodutibilidade."),
                CardItem("Postura com a Banca", "Nenhum número citado sem seção de origem. Clareza sobre a distinção entre associação e causalidade."),
            ],
            accent_color=TEAL,
        ),
        CardSpec(
            title="2. Dinâmica de Validação Cruzada (Apresentações Espelho)",
            items=[
                CardItem("Formato da Apresentação", "O autor resume o capítulo em até 5 min nos 4 eixos: Pergunta, Método, Números e Limitações."),
                CardItem("Papel do Revisor Dedicado", "O revisor reexplica o capítulo do colega com suas próprias palavras perante o grupo."),
                CardItem("Par 1 (Capítulo 1)", "Preparação de Dados: Gustavo Menezes apresenta  |  Helton reexplica e valida."),
                CardItem("Par 2 (Capítulo 2)", "Estatística Descritiva: Helton apresenta  |  Luciana reexplica e valida."),
                CardItem("Par 3 (Capítulo 3)", "Probabilidade e Distribuições: Luciana apresenta  |  Daniela reexplica e valida."),
                CardItem("Par 4 (Capítulo 4)", "Testes de Hipóteses e ANOVA: Daniela apresenta  |  Renatta reexplica e valida."),
                CardItem("Par 5 (Capítulo 5)", "Correlação e Modelagem Preditiva: Renatta apresenta  |  Gustavo Menezes reexplica e valida."),
            ],
            bg_color=TEAL_BG,
            border_color=TEAL_BORDER,
            title_color=TEAL,
            accent_color=TEAL_ACCENT,
        ),
        CardSpec(
            title="3. Compromisso da Equipe e Pré-Requisitos de Homologação",
            items=[
                CardItem("Quórum Pleno", "Participação confirmada dos 5 integrantes: Gustavo, Helton, Luciana, Daniela e Renatta."),
                CardItem("Reprodutibilidade Estrita", "Fixação de seed(42), ausência de caminhos absolutos e execução Restart & Run All limpa."),
                CardItem("Critério de Aprovação", "Reunião concluída apenas com validação e aceite consensual dos 5 capítulos."),
            ],
            accent_color=CORAL,
        ),
    ]

    p.render_cards(cards)
    return p


def make_page_chapter(
    page_num: int,
    total_pages: int,
    chapter_num: int,
    title: str,
    author: str,
    reviewer: str,
    notebook: str,
    cards: list[CardSpec],
) -> PageLayoutManager:
    p = PageLayoutManager(
        page_num,
        total_pages,
        f"Capítulo {chapter_num} · {title}",
        f"Apresentador: {author}   |   Revisor Dedicado: {reviewer}",
        f"TRILHA {chapter_num - 1} · {notebook}",
    )
    p.render_cards(cards)
    return p


def make_page_summary(total_pages: int) -> PageLayoutManager:
    p = PageLayoutManager(
        7,
        total_pages,
        "Síntese Executiva & Tabela de Bolso de Números Canônicos",
        "Compêndio Rápido de Fatos e Números Inquestionáveis para a Apresentação",
        "SÍNTESE EXECUTIVA",
    )

    cards = [
        CardSpec(
            title="1. Tabela de Bolso: Números Canônicos Inquestionáveis",
            layout_mode="table",
            items=[
                CardItem("Amostra Total", "8.693 passageiros (sem perda de registros; 22 colunas após engenharia de dados)."),
                CardItem("Taxa Global Transporte", "50,36% (4.378 transportados / 4.315 não-transportados) — classes equilibradas."),
                CardItem("Efeito Criossono", "81,47% em estase vs 32,82% acordados (χ² = 1.897,71; V de Cramér = 0,467)."),
                CardItem("Origem Planetária", "Europa 66,05% | Marte 52,44% | Terra 42,33% (χ² = 338,82; V de Cramér = 0,197)."),
                CardItem("Despesas Nulas", "41,92% da tripulação com US$ 0 (mediana transportados US$ 0; não-transp. US$ 907)."),
                CardItem("Aderência Idade", "Shapiro-Wilk W = 0,980 (KS D = 0,076) — aproximadamente normal no corpo central."),
                CardItem("Despesas por Origem", "ANOVA de Welch F = 407,57 (η² = 0,171); pós-hoc Games-Howell p < 10⁻⁶ para todos os pares."),
                CardItem("Regressão Logística", "Acurácia 77,9% (+27,5 p.p. sobre baseline); ROC-AUC 0,862; F1-Score 78,4%."),
            ],
            bg_color=TEAL_BG,
            border_color=TEAL_BORDER,
            title_color=TEAL,
            accent_color=TEAL,
            col1_w=2.00,
        ),
        CardSpec(
            title="2. As Três Diretrizes Centrais para o Tomador de Decisão",
            items=[
                CardItem("1. Foco em Criossono", "Priorizar auditoria técnica das cápsulas de estase; o isolamento físico ou energético é crítico."),
                CardItem("2. Estrutura e Origem", "Investigar conveses superiores (B e C) onde Europa concentra alta taxa de transporte."),
                CardItem("3. Desmistificar Gasto", "Gasto alto não protege passageiros; reflete apenas circulação ativa em decks inferiores."),
                CardItem("Cautela Metodológica", "Estudo estritamente observacional: correlação sólida não constitui nexo de causa direta."),
            ],
            accent_color=NAVY_LIGHT,
        ),
    ]

    p.render_cards(cards)
    return p


def make_page_signatures(total_pages: int) -> PageLayoutManager:
    p = PageLayoutManager(
        8,
        total_pages,
        "Homologação Final, Checklist de Domínio & Assinatura da Ata",
        "Registro Oficial de Conclusão da Reunião 2 e Liberação para o Fechamento do Projeto",
        "HOMOLOGAÇÃO KAN-36",
    )

    cards = [
        CardSpec(
            title="1. Checklist de Domínio Analítico Individual dos 5 Integrantes",
            layout_mode="table",
            items=[
                CardItem("Gustavo Menezes", "Demonstrou domínio de preparação, imputações sem bias e modelo logístico preditivo."),
                CardItem("Helton", "Demonstrou domínio de estatística descritiva, zero-inflação e preparação de dados."),
                CardItem("Luciana", "Demonstrou domínio de distribuições, testes de aderência e análise exploratória visual."),
                CardItem("Daniela", "Demonstrou domínio de testes de hipóteses, ANOVA de Welch e teoria de probabilidade."),
                CardItem("Renatta", "Demonstrou domínio de correlação de Spearman, regressões e testes inferenciais."),
            ],
            bg_color=CARD_BG,
            accent_color=TEAL,
            col1_w=1.80,
        ),
        CardSpec(
            title="2. Deliberação Coletiva e Autorização de Próximos Passos",
            items=[
                CardItem("Parecer Técnico", "Os cinco membros da equipe foram aprovados com louvor na dinâmica de validação cruzada."),
                CardItem("Eliminação de Silos", "Constatada capacidade de defesa integral de qualquer capítulo por qualquer membro perante a banca."),
                CardItem("Autorização KAN-37", "Liberada a consolidação oficial dos notebooks para geração de 00_projeto_final_estatistica.ipynb."),
                CardItem("Autorização Relatório", "Liberada a finalização da redação do relatório técnico final (KAN-39 a KAN-42)."),
            ],
            bg_color=TEAL_BG,
            border_color=TEAL_BORDER,
            accent_color=TEAL_ACCENT,
        ),
        CardSpec(
            title="3. Assinatura Formal da Ata da Reunião 2",
            items=[
                CardItem("Data e Local", "Recife/PE, 31 de outubro de 2026 — Sessão Virtual Síncrona."),
                CardItem("Assinaturas", "Gustavo Menezes Gonçalves (Coordenação) · Helton · Luciana · Daniela · Renatta."),
            ],
            accent_color=CORAL,
        ),
    ]

    p.render_cards(cards)
    return p


def generate_all_pages(preview_dir: Path | None = None):
    total_pages = 8
    pages: list[PageLayoutManager] = []

    # Página 1: Abertura
    pages.append(make_page_1(total_pages))

    # Página 2: Capítulo 1 (Gustavo / Helton)
    pages.append(
        make_page_chapter(
            2,
            total_pages,
            1,
            "Preparação, Limpeza e Engenharia de Atributos",
            "Gustavo Menezes Gonçalves",
            "Helton",
            "01_preparacao_dados.ipynb",
            [
                CardSpec(
                    title="1. Pergunta Central & Contexto dos Dados",
                    items=[
                        CardItem("Pergunta", "Como transformar uma base com nulos e texto em formato analítico sem criar distorções ou data leakage?"),
                        CardItem("Escopo Amostral", "8.693 passageiros da nave com 14 colunas brutas heterogêneas."),
                    ],
                    accent_color=TEAL,
                ),
                CardSpec(
                    title="2. Metodologia & Decisões Técnicas",
                    items=[
                        CardItem("Imputação Controlada", "Moda para categóricas e mediana para numéricas, testando sensibilidade populacional."),
                        CardItem("Engenharia de Variáveis", "Extração de GroupId, GroupSize e IsAlone de PassengerId; Deck, CabinNum e Side de Cabin."),
                        CardItem("Métricas de Consumo", "Soma vetorial TotalSpend das 5 comodidades pagas e criação da flag binária HasSpended."),
                        CardItem("Governança de Outliers", "Nenhum passageiro extremo de consumo descartado; preservação da integridade da tripulação."),
                    ],
                    accent_color=NAVY_LIGHT,
                ),
                CardSpec(
                    title="3. Números Canônicos & Evidências Empíricas",
                    items=[
                        CardItem("Integridade Final", "8.693 registros limpos com 22 colunas enriquecidas e exatamente zero nulos."),
                        CardItem("Teste de Sensibilidade", "Desvio máximo entre proporções pré e pós-imputação foi de apenas 0,64 ponto percentual."),
                        CardItem("Consistência Física", "100% dos passageiros em criossono possuem despesa estritamente igual a US$ 0,00."),
                        CardItem("Viajantes Solitários", "55,30% dos passageiros viajavam desacompanhados (IsAlone = True)."),
                    ],
                    bg_color=TEAL_BG,
                    border_color=TEAL_BORDER,
                    accent_color=TEAL_ACCENT,
                ),
                CardSpec(
                    title="4. Desafio para o Revisor Dedicado (Helton) & Limitações",
                    items=[
                        CardItem("Pergunta de Desafio", "Por que não descartamos simplesmente as linhas que possuíam valores ausentes?"),
                        CardItem("Resposta do Revisor", "O descarte eliminaria ~2.000 passageiros (quase 25% da base), introduzindo viés de seleção grave."),
                        CardItem("Ponto de Cautela", "Toda imputação deve aprender estritamente com os dados de treino para evitar data leakage."),
                    ],
                    bg_color=AMBER_BG,
                    border_color=AMBER_BORDER,
                    title_color=CORAL,
                    accent_color=CORAL,
                ),
            ],
        )
    )

    # Página 3: Capítulo 2 (Helton / Luciana)
    pages.append(
        make_page_chapter(
            3,
            total_pages,
            2,
            "Estatística Descritiva e Análise Visual",
            "Helton",
            "Luciana",
            "02_estatistica_descritiva.ipynb",
            [
                CardSpec(
                    title="1. Pergunta Central & Contexto Descritivo",
                    items=[
                        CardItem("Pergunta", "Quais são os perfis sociodemográficos e padrões de consumo associados ao transporte?"),
                        CardItem("Escopo Analítico", "Análise univariada, bivariada e detecção de assimetrias estruturais nas despesas."),
                    ],
                    accent_color=TEAL,
                ),
                CardSpec(
                    title="2. Metodologia & Técnicas Exploratórias",
                    items=[
                        CardItem("Medidas de Resumo", "Cálculo de tendência central, dispersão, IQR, assimetria (skewness) e curtose."),
                        CardItem("Tabelas Cruzadas", "Estratificação das taxas de transporte por planeta de origem, convés e criossono."),
                        CardItem("Detecção de Zero-Inflação", "Identificação de massa de probabilidade pontual em despesas nulas."),
                        CardItem("Visualização Rigorosa", "Histogramas com densidade KDE, boxplots comparativos e barras estratificadas."),
                    ],
                    accent_color=NAVY_LIGHT,
                ),
                CardSpec(
                    title="3. Números Canônicos & Evidências Empíricas",
                    items=[
                        CardItem("Taxa Global de Transporte", "50,36% dos passageiros transportados (4.378 de 8.693)."),
                        CardItem("Impacto do Criossono", "81,47% em criossono foram transportados contra apenas 32,82% dos acordados (+48,65 p.p.)."),
                        CardItem("Origem Planetária", "Europa 66,05% (1.439/2.179) | Marte 52,44% (930/1.773) | Terra 42,33% (1.987/4.693)."),
                        CardItem("Zero-Inflação em Despesas", "41,92% com gasto nulo. Mediana dos transportados US$ 0 vs US$ 907 dos não-transportados."),
                        CardItem("Assimetria de Gastos", "Assimetria severa de 4,40; média global de US$ 1.480 distorcida pela cauda superior."),
                    ],
                    bg_color=TEAL_BG,
                    border_color=TEAL_BORDER,
                    accent_color=TEAL_ACCENT,
                ),
                CardSpec(
                    title="4. Desafio para a Revisora Dedicada (Luciana) & Limitações",
                    items=[
                        CardItem("Pergunta de Desafio", "Por que é proibido usar a média aritmética para comparar os gastos entre os grupos?"),
                        CardItem("Resposta da Revisora", "Porque a presença de 41,92% de zeros e cauda pesada faz a média mentir; a mediana é a medida honesta."),
                        CardItem("Padrão nos Conveses", "Decks superiores B e C abrigam passageiros de Europa e têm transporte superior a 70%."),
                    ],
                    bg_color=AMBER_BG,
                    border_color=AMBER_BORDER,
                    title_color=CORAL,
                    accent_color=CORAL,
                ),
            ],
        )
    )

    # Página 4: Capítulo 3 (Luciana / Daniela)
    pages.append(
        make_page_chapter(
            4,
            total_pages,
            3,
            "Teoria de Probabilidade e Distribuições",
            "Luciana",
            "Daniela",
            "03_probabilidade_distribuicoes.ipynb",
            [
                CardSpec(
                    title="1. Pergunta Central & Justificativa Teórica",
                    items=[
                        CardItem("Pergunta", "As variáveis quantitativas (Age e TotalSpend) aderem a distribuições teóricas Normal ou Log-Normal?"),
                        CardItem("Relevância Prática", "A forma das distribuições dita a escolha entre testes paramétricos clássicos ou métodos robustos."),
                    ],
                    accent_color=TEAL,
                ),
                CardSpec(
                    title="2. Metodologia & Tríade Probatória",
                    items=[
                        CardItem("Inspeção de Densidade", "Gráficos de densidade empírica vs gaussiana e Quantile-Quantile Plots (QQ-plots)."),
                        CardItem("Testes Formais", "Aplicação combinada de Shapiro-Wilk (quantis amostrais) e Kolmogorov-Smirnov (distribuição acumulada)."),
                        CardItem("Transformações", "Investigação da transformação logarítmica log(1 + x) para estabilização de variância."),
                        CardItem("Orientação Inferencial", "Avaliação de premissas de homocedasticidade e normalidade residual."),
                    ],
                    accent_color=NAVY_LIGHT,
                ),
                CardSpec(
                    title="3. Números Canônicos & Evidências Empíricas",
                    items=[
                        CardItem("Idade (Age)", "Shapiro-Wilk W = 0,980 (p < 10⁻¹⁵); Kolmogorov-Smirnov D = 0,076."),
                        CardItem("Diagnóstico de Idade", "Comportamento aproximadamente normal no corpo central, com leve truncamento em crianças e idosos."),
                        CardItem("Gastos (log1p TotalSpend)", "Shapiro-Wilk W = 0,891 (p < 10⁻¹⁵); Kolmogorov-Smirnov D = 0,126; curtose de 4,93."),
                        CardItem("Diagnóstico de Gastos", "Distribuição bimodal mista (massa pontual de zeros de 41,92% + cauda pesada assimétrica)."),
                        CardItem("Implicação Direta", "Rejeição categórica de testes t de Student clássicos e de ANOVA clássica de Fisher."),
                    ],
                    bg_color=TEAL_BG,
                    border_color=TEAL_BORDER,
                    accent_color=TEAL_ACCENT,
                ),
                CardSpec(
                    title="4. Desafio para a Revisora Dedicada (Daniela) & Limitações",
                    items=[
                        CardItem("Pergunta de Desafio", "Se o p-valor de Shapiro-Wilk rejeita a normalidade de Age, por que a consideramos aproximadamente normal?"),
                        CardItem("Resposta da Revisora", "Com n=8.693, o teste tem potência máxima e rejeita desvios ínfimos; W=0,980 prova forte aderência prática."),
                        CardItem("Ponto de Cautela", "TotalSpend não pode ser tratada como Log-Normal pura por causa da concentração em zero."),
                    ],
                    bg_color=AMBER_BG,
                    border_color=AMBER_BORDER,
                    title_color=CORAL,
                    accent_color=CORAL,
                ),
            ],
        )
    )

    # Página 5: Capítulo 4 (Daniela / Renatta)
    pages.append(
        make_page_chapter(
            5,
            total_pages,
            4,
            "Testes de Hipóteses, Comparações e ANOVA",
            "Daniela",
            "Renatta",
            "04_testes_hipoteses_anova.ipynb",
            [
                CardSpec(
                    title="1. Pergunta Central & Formulação Inferencial",
                    items=[
                        CardItem("Pergunta", "As discrepâncias de transporte e consumo são estatisticamente significativas ou mero ruído amostral?"),
                        CardItem("Tamanho de Efeito", "Determinar a magnitude prática das associações além da mera significância estatística (p-valor)."),
                    ],
                    accent_color=TEAL,
                ),
                CardSpec(
                    title="2. Metodologia Estatística Rigorosa",
                    items=[
                        CardItem("Independência Categórica", "Testes Qui-Quadrado de Pearson (χ²) acompanhados do coeficiente V de Cramér."),
                        CardItem("Comparação de Duas Médias", "Teste t de Welch para variâncias heterogêneas e tamanho de efeito d de Cohen."),
                        CardItem("Comparação de Três Grupos", "ANOVA de Welch (F) após Levene acusar heterocedasticidade severa (razão de variâncias > 37x)."),
                        CardItem("Pós-hoc Robusto", "Teste pareado de Games-Howell para controle de erro Tipo I sob variâncias desiguais."),
                    ],
                    accent_color=NAVY_LIGHT,
                ),
                CardSpec(
                    title="3. Números Canônicos & Evidências Empíricas",
                    items=[
                        CardItem("Associação Criossono", "χ² = 1.897,71 (gl = 1, p < 10⁻¹⁵); V de Cramér = 0,467 (associação extremamente forte)."),
                        CardItem("Associação Planeta", "χ² = 338,82 (gl = 2, p < 10⁻¹⁵); V de Cramér = 0,197 (associação moderada a substancial)."),
                        CardItem("Associação Convés", "χ² = 389,01 (gl = 7, p < 10⁻¹⁵); V de Cramér = 0,212."),
                        CardItem("Teste t de Welch", "t = 18,94 (p < 10⁻¹⁵); d de Cohen = 0,407 (não-transportados consumiram significativamente mais)."),
                        CardItem("ANOVA de Welch (Origem)", "F = 407,57 (p < 10⁻¹⁵); η² = 0,171 (17,1% da variação de consumo explicada pelo planeta natal)."),
                        CardItem("Pós-hoc Games-Howell", "Europa gasta expressivamente mais que Terra e Marte (p < 10⁻⁶ para todas as comparações)."),
                    ],
                    bg_color=TEAL_BG,
                    border_color=TEAL_BORDER,
                    accent_color=TEAL_ACCENT,
                ),
                CardSpec(
                    title="4. Desafio para a Revisora Dedicada (Renatta) & Limitações",
                    items=[
                        CardItem("Pergunta de Desafio", "Por que não adotar a ANOVA clássica de Fisher para comparar os gastos dos planetas?"),
                        CardItem("Resposta da Revisora", "A razão de variâncias passa de 37x; a ANOVA clássica inflaria os erros falso-positivos (Tipo I)."),
                        CardItem("Magnitude Prática", "O V de Cramér comprova que Criossono tem associação mais de duas vezes superior a Planeta."),
                    ],
                    bg_color=AMBER_BG,
                    border_color=AMBER_BORDER,
                    title_color=CORAL,
                    accent_color=CORAL,
                ),
            ],
        )
    )

    # Página 6: Capítulo 5 (Renatta / Gustavo)
    pages.append(
        make_page_chapter(
            6,
            total_pages,
            5,
            "Correlação, Regressões e Modelo Preditivo",
            "Renatta",
            "Gustavo Menezes Gonçalves",
            "05_correlacao_regressoes.ipynb",
            [
                CardSpec(
                    title="1. Pergunta Central & Modelagem Estatística",
                    items=[
                        CardItem("Pergunta", "Como as variáveis se correlacionam e qual o poder de um modelo logístico interpretável para triagem?"),
                        CardItem("Compromisso Ético", "Definir os limites de aplicabilidade preditiva: apoio à triagem vs decisão automática."),
                    ],
                    accent_color=TEAL,
                ),
                CardSpec(
                    title="2. Metodologia de Modelagem & Validação",
                    items=[
                        CardItem("Correlação Não-Linear", "Matriz de Spearman avaliando associações monotônicas sem exigir normalidade."),
                        CardItem("Regressão Múltipla OLS", "Ajuste linear em log1p(TotalSpend) para identificar determinantes socioeconômicos de consumo."),
                        CardItem("Regressão Logística", "Divisão 80/20 estratificada (seed 42), padronização e One-Hot Encoding."),
                        CardItem("Métricas de Desempenho", "Acurácia, ROC-AUC, Precision-Recall AUC, F1-Score, Sensibilidade e Especificidade."),
                    ],
                    accent_color=NAVY_LIGHT,
                ),
                CardSpec(
                    title="3. Números Canônicos & Evidências Empíricas",
                    items=[
                        CardItem("Regressão Linear Gastos", "R² = 0,314 (Idade, conveses superiores B/C e Europa explicam 31,4% do gasto a bordo)."),
                        CardItem("Acurácia do Modelo", "77,9% no conjunto de teste (+27,5 p.p. superior à regra ingênua de 50,36%)."),
                        CardItem("Capacidade Discriminativa", "ROC-AUC = 0,862 | Precision-Recall AUC = 0,880."),
                        CardItem("Equilíbrio de Classes", "Precisão = 77,2% | Sensibilidade (Recall) = 79,6% | F1-Score = 78,4% | Especificidade = 76,1%."),
                        CardItem("Odds Ratios", "CryoSleep multiplica em > 8,5x as chances de transporte; gastos em Spa/VRDeck reduzem a chance."),
                    ],
                    bg_color=TEAL_BG,
                    border_color=TEAL_BORDER,
                    accent_color=TEAL_ACCENT,
                ),
                CardSpec(
                    title="4. Desafio para o Revisor Dedicado (Gustavo) & Limitações",
                    items=[
                        CardItem("Pergunta de Desafio", "Este modelo logístico pode ser utilizado para automação de decisões de resgate?"),
                        CardItem("Resposta do Revisor", "Não. A acurácia de 77,9% gera 22% de erros; ele serve para priorização e triagem investigativa."),
                        CardItem("Ponto de Cautela", "O limiar de decisão foi fixado a priori em 0,5 para evitar data snooping e otimização espúria."),
                    ],
                    bg_color=AMBER_BG,
                    border_color=AMBER_BORDER,
                    title_color=CORAL,
                    accent_color=CORAL,
                ),
            ],
        )
    )

    # Página 7: Síntese e Tabela de Bolso
    pages.append(make_page_summary(total_pages))

    # Página 8: Homologação e Assinaturas
    pages.append(make_page_signatures(total_pages))

    # Salva o PDF consolidado
    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    OUT_DOCS.parent.mkdir(parents=True, exist_ok=True)

    with PdfPages(OUT_REPORT) as pdf:
        for idx, page in enumerate(pages):
            pdf.savefig(page.fig)
            if preview_dir:
                preview_path = preview_dir / f"page_{idx + 1:02d}.png"
                page.fig.savefig(preview_path, dpi=150)
            plt.close(page.fig)

    shutil.copyfile(OUT_REPORT, OUT_DOCS)
    print(f"Sucesso! {total_pages} páginas geradas sem sobreposição em:\n - {OUT_REPORT}\n - {OUT_DOCS}")
    if preview_dir:
        print(f"Previews em PNG salvos em: {preview_dir}")


def main():
    parser = argparse.ArgumentParser(description="Gera o PDF de alinhamento KAN-36.")
    parser.add_argument("--preview", type=Path, default=None, help="Diretório para salvar imagens PNG de preview.")
    args = parser.parse_args()

    generate_all_pages(preview_dir=args.preview)


if __name__ == "__main__":
    main()
