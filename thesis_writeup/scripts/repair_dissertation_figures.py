from __future__ import annotations

import json
import math
import os
import shutil
import textwrap
import zipfile
from pathlib import Path
from tempfile import NamedTemporaryFile

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, Rectangle
from lxml import etree
from PIL import Image, ImageDraw, ImageOps


ROOT = Path(r"C:\Users\lby\Downloads\v2")
THESIS = ROOT / "thesis_writeup"
DOCX = Path(os.environ.get("DISSERTATION_DOCX", THESIS / "dissertation_final.docx"))
QA_ROOT = THESIS / "qa_outputs" / "figure_repair_20260527"
BACKUP = THESIS / "archive_old_versions_20260527_figure_repair" / "dissertation_final_before_figure_repair.docx"

EMU_PER_INCH = 914400

BLUE_BG = "#dbeafb"
GREEN_BG = "#dcefd8"
YELLOW_BG = "#fff2cc"
PURPLE_BG = "#eadcf6"
NODE_BG = "#f5f5f5"
BORDER = "#555555"
BLUE_BORDER = "#5b87c7"
GREEN_BORDER = "#7ab36d"
YELLOW_BORDER = "#d6b656"
PURPLE_BORDER = "#9a69b5"
TEXT = "#222222"
REAL = "#7fa6d8"
FAKE = "#d89a6a"
MODEL = "#9bc58a"
BASELINE = "#b8b8b8"
ACCENT = "#c9a552"
TFIDF = "#4E79A7"
WBERT = "#F28E2B"
UBERT = "#B6C7E5"
WROB = "#59A14F"
MAJ = "#9EA3A8"
GRID = "#D9D9D9"
FAKE_RED = "#E15759"


MEDIA_TO_FIG = {
    "image1.png": "logo",
    "image2.png": "fig_3_1",
    "image3.png": "fig_3_2",
    "image4.png": "fig_3_3",
    "image5.png": "fig_4_1",
    "image6.png": "fig_4_2",
    "image7.png": "fig_5_1",
    "image14.png": "fig_6_1",
    "image15.png": "fig_6_2",
    "image16.png": "fig_6_3",
    "image8.png": "fig_6_4",
    "image13.png": "fig_a_1",
}


def configure() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 8.8,
            "axes.titlesize": 11,
            "axes.labelsize": 10,
            "xtick.labelsize": 8.8,
            "ytick.labelsize": 8.8,
            "legend.fontsize": 8.5,
            "savefig.dpi": 360,
            "figure.dpi": 140,
            "axes.edgecolor": "#222222",
        }
    )


def wrap(text: str, width: int) -> str:
    return "\n".join(textwrap.wrap(text, width=width, break_long_words=False))


def save(fig, path: Path, caption: str | None = None, bottom: float = 0.05) -> None:
    if caption:
        fig.text(0.5, bottom, caption, ha="center", va="bottom", fontsize=11.2, family="DejaVu Serif")
    fig.savefig(path, bbox_inches="tight", facecolor="white", pad_inches=0.08)
    plt.close(fig)
    trim_whitespace(path, padding=30)


def trim_whitespace(path: Path, padding: int = 30) -> None:
    im = Image.open(path).convert("RGB")
    gray = ImageOps.grayscale(im)
    mask = gray.point(lambda p: 255 if p < 248 else 0)
    bbox = mask.getbbox()
    if not bbox:
        return
    l, t, r, b = bbox
    l = max(0, l - padding)
    t = max(0, t - padding)
    r = min(im.width, r + padding)
    b = min(im.height, b + padding)
    im.crop((l, t, r, b)).save(path, quality=95)


def setup_canvas(figsize=(6.4, 4.1)):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    return fig, ax


def rect(ax, x, y, w, h, text="", fc=NODE_BG, ec=BORDER, fs=7.2, bold=False, lw=0.9):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec, linewidth=lw))
    if text:
        ax.text(
            x + w / 2,
            y + h / 2,
            text,
            ha="center",
            va="center",
            fontsize=fs,
            color=TEXT,
            fontweight="bold" if bold else "normal",
            linespacing=1.12,
        )


def band(ax, y, h, label, fc, ec):
    rect(ax, 0.02, y, 0.96, h, "", fc=fc, ec=ec, lw=0.8)
    ax.text(
        0.035,
        y + h - 0.018,
        label,
        ha="left",
        va="top",
        fontsize=7.4,
        fontweight="bold",
        bbox={"facecolor": fc, "edgecolor": "none", "pad": 1.0},
        zorder=5,
    )


def arrow(ax, start, end, lw=0.85, dashed=False):
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=8.5,
            linewidth=lw,
            color="black",
            linestyle=(0, (2, 2)) if dashed else "solid",
            shrinkA=0,
            shrinkB=0,
        )
    )


def ortho(ax, points, lw=0.85):
    for p1, p2 in zip(points[:-2], points[1:-1]):
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color="black", linewidth=lw)
    arrow(ax, points[-2], points[-1], lw=lw)


def add_labels(ax, bars, decimals=3, size=7.2, pad=0.012):
    ymin, ymax = ax.get_ylim()
    off = (ymax - ymin) * pad
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + off, f"{h:.{decimals}f}", ha="center", va="bottom", fontsize=size)


def make_logo(out: Path) -> None:
    src = THESIS / "dissertation_planning" / "assets" / "galway_wordmark_cropped_from_sample.png"
    im = Image.open(src).convert("RGBA")
    im = im.resize((1515, 540), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (1515, 540), "white")
    canvas.alpha_composite(im)
    canvas.convert("RGB").save(out, quality=95)
    trim_whitespace(out, padding=28)


def fig_3_1(out: Path) -> None:
    fig, ax = setup_canvas((6.2, 4.25))
    band(ax, 0.76, 0.17, "Data Preparation Phase", BLUE_BG, BLUE_BORDER)
    band(ax, 0.44, 0.32, "Training and Selection Phase", GREEN_BG, GREEN_BORDER)
    band(ax, 0.14, 0.30, "Evaluation Phase", YELLOW_BG, YELLOW_BORDER)
    rect(ax, 0.07, 0.80, 0.17, 0.075, "LIAR\nDataset", PURPLE_BG, PURPLE_BORDER)
    rect(ax, 0.31, 0.80, 0.20, 0.075, "Binary Label\nMapping")
    rect(ax, 0.58, 0.80, 0.22, 0.075, "Fixed Train / Valid /\nTest Splits")
    arrow(ax, (0.24, 0.837), (0.31, 0.837))
    arrow(ax, (0.51, 0.837), (0.58, 0.837))
    rect(ax, 0.30, 0.575, 0.40, 0.10, "Model Training on LIAR\nTF-IDF | BERT | Weighted BERT\nRoBERTa | Weighted RoBERTa", fs=6.9)
    ortho(ax, [(0.69, 0.80), (0.69, 0.735), (0.50, 0.735), (0.50, 0.675)])
    rect(ax, 0.34, 0.445, 0.32, 0.07, "Select Checkpoint by\nValidation Macro-F1")
    arrow(ax, (0.50, 0.575), (0.50, 0.515))
    rect(ax, 0.12, 0.305, 0.23, 0.08, "LIAR Test\nEvaluation")
    rect(ax, 0.39, 0.305, 0.23, 0.08, "FakeNewsNet Title\nTransfer")
    rect(ax, 0.66, 0.305, 0.23, 0.08, "Majority-Class\nBaseline")
    ortho(ax, [(0.43, 0.445), (0.43, 0.415), (0.24, 0.415), (0.24, 0.385)])
    arrow(ax, (0.50, 0.445), (0.50, 0.385))
    ortho(ax, [(0.57, 0.445), (0.57, 0.415), (0.78, 0.415), (0.78, 0.385)])
    rect(ax, 0.35, 0.17, 0.30, 0.08, "Compare Accuracy,\nMacro-F1 and Recall")
    ortho(ax, [(0.24, 0.305), (0.24, 0.278), (0.42, 0.278), (0.42, 0.25)])
    arrow(ax, (0.50, 0.305), (0.50, 0.25))
    ortho(ax, [(0.78, 0.305), (0.78, 0.278), (0.58, 0.278), (0.58, 0.25)])
    save(fig, out, "Figure 3.1: Overall experimental pipeline for cross-dataset fake news detection.")


def fig_3_2(out: Path) -> None:
    fig = plt.figure(figsize=(6.6, 4.45))
    ax = fig.add_axes([0.045, 0.23, 0.91, 0.69])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    band(ax, 0.64, 0.30, "Binary Label Mapping", BLUE_BG, BLUE_BORDER)
    rect(ax, 0.10, 0.79, 0.24, 0.08, "true / mostly-true\nhalf-true", fs=6.9)
    rect(ax, 0.42, 0.79, 0.18, 0.08, "REAL", PURPLE_BG, PURPLE_BORDER, bold=True)
    rect(ax, 0.10, 0.67, 0.24, 0.08, "barely-true / false\npants-fire", fs=6.9)
    rect(ax, 0.42, 0.67, 0.18, 0.08, "FAKE", PURPLE_BG, PURPLE_BORDER, bold=True)
    arrow(ax, (0.34, 0.83), (0.42, 0.83))
    arrow(ax, (0.34, 0.71), (0.42, 0.71))
    rect(ax, 0.68, 0.735, 0.22, 0.10, "Binary task used\nfor all experiments", fs=6.8)
    chart1 = fig.add_axes([0.09, 0.30, 0.38, 0.27])
    chart2 = fig.add_axes([0.56, 0.30, 0.38, 0.27])
    x = np.arange(3)
    w = 0.34
    chart1.bar(x - w / 2, [5752, 668, 714], w, color=REAL, edgecolor=BORDER, linewidth=0.4, label="REAL")
    chart1.bar(x + w / 2, [4488, 616, 553], w, color=FAKE, edgecolor=BORDER, linewidth=0.4, label="FAKE")
    chart1.set_title("LIAR counts", fontsize=8.2, fontweight="bold")
    chart1.set_xticks(x, ["Train", "Valid", "Test"])
    chart1.set_ylabel("Rows")
    chart1.set_ylim(0, 6500)
    chart1.grid(axis="y", alpha=0.25)
    chart1.legend(frameon=False, fontsize=6.5, loc="upper right")
    chart2.bar(x - w / 2, [624, 16817, 17441], w, color=REAL, edgecolor=BORDER, linewidth=0.4, label="REAL")
    chart2.bar(x + w / 2, [432, 5323, 5755], w, color=FAKE, edgecolor=BORDER, linewidth=0.4, label="FAKE")
    chart2.set_title("FakeNewsNet title counts", fontsize=8.2, fontweight="bold")
    chart2.set_xticks(x, ["PolitiFact", "GossipCop", "Combined"])
    chart2.set_ylim(0, 19000)
    chart2.grid(axis="y", alpha=0.25)
    chart2.legend(frameon=False, fontsize=6.5, loc="upper right")
    save(fig, out, "Figure 3.2: Binary label mapping and class distribution across LIAR and FakeNewsNet.")


def fig_3_3(out: Path) -> None:
    fig, ax = setup_canvas((6.2, 4.05))
    band(ax, 0.72, 0.19, "Seed Phase", BLUE_BG, BLUE_BORDER)
    band(ax, 0.37, 0.35, "Training Phase", GREEN_BG, GREEN_BORDER)
    band(ax, 0.14, 0.23, "Reporting Phase", YELLOW_BG, YELLOW_BORDER)
    rect(ax, 0.13, 0.79, 0.42, 0.06, "Seeds: 42, 52, 62, 72, 82", PURPLE_BG, PURPLE_BORDER)
    rect(ax, 0.23, 0.585, 0.26, 0.08, "Train on\nLIAR train")
    rect(ax, 0.58, 0.585, 0.26, 0.08, "Select by validation\nMacro-F1")
    arrow(ax, (0.34, 0.79), (0.34, 0.69))
    arrow(ax, (0.49, 0.625), (0.58, 0.625))
    rect(ax, 0.20, 0.445, 0.28, 0.08, "Evaluate on\nLIAR test")
    rect(ax, 0.58, 0.445, 0.28, 0.08, "Evaluate on\nFakeNewsNet titles")
    arrow(ax, (0.36, 0.585), (0.36, 0.525))
    arrow(ax, (0.71, 0.585), (0.71, 0.525))
    rect(ax, 0.35, 0.22, 0.30, 0.08, "Report mean +/-\nstandard deviation")
    ortho(ax, [(0.34, 0.445), (0.34, 0.335), (0.43, 0.335), (0.43, 0.30)])
    ortho(ax, [(0.72, 0.445), (0.72, 0.335), (0.57, 0.335), (0.57, 0.30)])
    save(fig, out, "Figure 3.3: Five-seed transformer training and evaluation protocol.")


def grouped_bar(out: Path, caption: str, labels, series, colors, ylabel, ylim, note=None) -> None:
    fig = plt.figure(figsize=(6.25, 4.25))
    ax = fig.add_axes([0.12, 0.29, 0.82, 0.56])
    x = np.arange(len(labels))
    width = min(0.72 / len(series), 0.34)
    offsets = np.linspace(-width * (len(series) - 1) / 2, width * (len(series) - 1) / 2, len(series))
    for (name, values), color, off in zip(series, colors, offsets):
        bars = ax.bar(x + off, values, width, label=name, color=color, edgecolor=BORDER, linewidth=0.5)
        add_labels(ax, bars, size=6.9)
    ax.set_ylabel(ylabel)
    ax.set_ylim(*ylim)
    ax.set_xticks(x, [wrap(str(l), 12) for l in labels])
    ax.grid(axis="y", alpha=0.28)
    ax.set_axisbelow(True)
    ax.legend(frameon=True, fontsize=7.2, loc="upper center", bbox_to_anchor=(0.5, 1.13), ncol=len(series))
    for spine in ax.spines.values():
        spine.set_linewidth(0.7)
    if note:
        fig.text(0.12, 0.19, note, ha="left", va="center", fontsize=6.8, color="#555555")
    save(fig, out, caption)


def fig_4_1(out: Path) -> None:
    grouped_bar(
        out,
        "Figure 4.1: LIAR in-domain performance comparison across local baselines.",
        ["TF-IDF", "BERT", "RoBERTa", "Weighted BERT", "Weighted RoBERTa"],
        [("Accuracy", np.array([0.6235, 0.6425, 0.6504, 0.6412, 0.6522])), ("Macro-F1", np.array([0.6005, 0.6231, 0.6262, 0.6322, 0.6396]))],
        [REAL, MODEL],
        "Score",
        (0.55, 0.69),
        "Transformer values are five-seed means where available; TF-IDF is deterministic.",
    )


def fig_4_2(out: Path) -> None:
    grouped_bar(
        out,
        "Figure 4.2: REAL and FAKE recall trade-off on the LIAR test set.",
        ["TF-IDF", "RoBERTa", "Weighted BERT", "Weighted RoBERTa"],
        [("REAL recall", np.array([0.7661, 0.8025, 0.7048, 0.7443])), ("FAKE recall", np.array([0.4394, 0.4539, 0.5591, 0.5335]))],
        [REAL, FAKE],
        "Recall",
        (0.0, 0.92),
    )


def fig_5_1(out: Path) -> None:
    fig, ax = setup_canvas((6.1, 4.05))
    band(ax, 0.73, 0.17, "Error Pattern Summary", BLUE_BG, BLUE_BORDER)
    band(ax, 0.22, 0.51, "", GREEN_BG, GREEN_BORDER)
    ax.text(0.08, 0.675, "Qualitative Error Types", ha="left", va="center",
            fontsize=8.8, fontweight="bold",
            bbox={"boxstyle": "square,pad=0.12", "facecolor": GREEN_BG, "edgecolor": "none"})
    rect(ax, 0.34, 0.78, 0.32, 0.07, "Remaining LIAR\nerror patterns", PURPLE_BG, PURPLE_BORDER)
    items = [
        (0.07, 0.49, 0.20, 0.08, "Numeric claims", 7.5),
        (0.39, 0.49, 0.22, 0.08, "Label-boundary\nambiguity", 7.3),
        (0.70, 0.49, 0.24, 0.08, "Context-dependent\nstatements", 6.7),
        (0.21, 0.31, 0.20, 0.08, "Short statements", 7.5),
        (0.60, 0.31, 0.20, 0.08, "Ambiguous wording", 7.5),
    ]
    for x, y, w, h, txt, fs in items:
        rect(ax, x, y, w, h, txt, fs=fs)

    # Branch lines use gap columns and stop at box borders, so no line crosses label text.
    bus_y = 0.625
    lower_bus_y = 0.445
    ax.plot([0.50, 0.50], [0.78, bus_y], color="black", lw=1.0)
    ax.plot([0.17, 0.82], [bus_y, bus_y], color="black", lw=1.0)
    for x, y_top in [(0.17, 0.57), (0.50, 0.57), (0.82, 0.57)]:
        ax.annotate("", xy=(x, y_top), xytext=(x, bus_y),
                    arrowprops={"arrowstyle": "-|>", "lw": 1.0, "color": "black",
                                "shrinkA": 0, "shrinkB": 0, "mutation_scale": 8})
    for x, y_top in [(0.31, 0.39), (0.70, 0.39)]:
        ax.plot([x, x], [bus_y, lower_bus_y], color="black", lw=1.0)
        ax.annotate("", xy=(x, y_top), xytext=(x, lower_bus_y),
                    arrowprops={"arrowstyle": "-|>", "lw": 1.0, "color": "black",
                                "shrinkA": 0, "shrinkB": 0, "mutation_scale": 8})
    rect(ax, 0.13, 0.13, 0.74, 0.075, "Observed from representative saved errors,\nnot automatic full-test classification.", YELLOW_BG, YELLOW_BORDER, fs=6.7)
    save(fig, out, "Figure 5.1: Qualitative taxonomy of recurring LIAR error patterns.")


def fig_6_1(out: Path) -> None:
    models = ["TF-IDF", "Weighted BERT", "Weighted RoBERTa", "Unweighted BERT\n(control)"]
    liar = np.array([0.6005, 0.6322, 0.6396, 0.6231])
    fnn = np.array([0.4745, 0.2682, 0.2358, 0.2806])
    fig, ax = plt.subplots(figsize=(6.3, 3.85))
    fig.subplots_adjust(left=0.10, right=0.965, top=0.80, bottom=0.30)
    centers = np.array([0.0, 1.8])
    width = 0.17
    offsets = np.array([-1.5, -0.5, 0.5, 1.5]) * width
    for i, (model, color, hatch) in enumerate(zip(models, [TFIDF, WBERT, WROB, UBERT], ["", "", "", "///"])):
        bars = ax.bar(centers + offsets[i], [liar[i], fnn[i]], width=width, label=model, color=color, edgecolor=BORDER, linewidth=0.55, hatch=hatch)
        add_labels(ax, bars, size=6.7)
    ax.hlines(0.4292, centers[1] - 0.45, centers[1] + 0.45, colors="#666666", linestyles="--", linewidth=1.0)
    ax.text(centers[1] + 0.49, 0.4292, "Majority\n0.429", ha="left", va="center", fontsize=7.2)
    ax.set_xticks(centers, ["LIAR\n(in-domain)", "FakeNewsNet combined\n(strict transfer)"])
    ax.set_ylabel("Macro-F1")
    ax.set_ylim(0, 0.70)
    ax.grid(axis="y", color=GRID, linewidth=0.65)
    ax.set_axisbelow(True)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.18), ncol=2, frameon=True, fontsize=7.6)
    save(fig, out, "Figure 6.1: Macro-F1 on LIAR and FakeNewsNet combined titles.", bottom=0.045)


def fig_6_2(out: Path) -> None:
    real = np.array([1.0000, 0.4766, 0.0747, 0.0890, 0.0372])
    fake = np.array([0.0000, 0.5682, 0.9564, 0.9467, 0.9827])
    order = ["Always-REAL", "TF-IDF", "Weighted BERT", "Unweighted BERT", "Weighted RoBERTa"]
    fig, ax = plt.subplots(figsize=(6.35, 3.9))
    fig.subplots_adjust(left=0.09, right=0.975, top=0.79, bottom=0.32)
    x = np.arange(len(order))
    width = 0.33
    ax.axvspan(1.5, 3.5, color=YELLOW_BG, alpha=0.45, zorder=0)
    b1 = ax.bar(x - width / 2, real, width=width, label="REAL recall", color=TFIDF, edgecolor=BORDER, linewidth=0.55)
    b2 = ax.bar(x + width / 2, fake, width=width, label="FAKE recall", color=FAKE_RED, edgecolor=BORDER, linewidth=0.55)
    add_labels(ax, b1, size=6.5)
    add_labels(ax, b2, size=6.5)
    ax.text(3.85, 0.50, "Balanced target:\nboth recalls near 0.50", ha="center", va="center", fontsize=7.0, bbox={"boxstyle": "round,pad=0.22", "facecolor": "white", "edgecolor": "#999999", "linewidth": 0.6})
    ax.set_xticks(x, [wrap(m, 11) for m in order])
    ax.set_ylabel("Recall")
    ax.set_ylim(0, 1.08)
    ax.grid(axis="y", color=GRID, linewidth=0.65)
    ax.set_axisbelow(True)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.15), ncol=2, frameon=True, fontsize=7.6)
    save(fig, out, "Figure 6.2: Class-level recall on FakeNewsNet combined titles.", bottom=0.045)


def fig_6_3(out: Path) -> None:
    order = ["Always-REAL", "TF-IDF", "Weighted BERT", "Unweighted BERT", "Weighted RoBERTa"]
    accuracy = np.array([0.7519, 0.4993, 0.2935, 0.3018, 0.2718])
    macro = np.array([0.4292, 0.4745, 0.2682, 0.2806, 0.2358])
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.35, 3.75))
    fig.subplots_adjust(left=0.075, right=0.975, top=0.83, bottom=0.33, wspace=0.30)
    for ax, title, values, ylim in [(ax1, "Accuracy", accuracy, (0, 0.85)), (ax2, "Macro-F1", macro, (0, 0.55))]:
        x = np.arange(len(order))
        bars = ax.bar(x, values, color=[MAJ, TFIDF, WBERT, UBERT, WROB], edgecolor=BORDER, linewidth=0.55)
        bars[3].set_hatch("///")
        add_labels(ax, bars, size=6.3)
        ax.set_title(title, fontweight="bold", pad=6)
        ax.set_ylim(*ylim)
        ax.set_xticks(x, ["Always-\nREAL", "TF-IDF", "W.\nBERT", "U.\nBERT", "W.\nRoBERTa"])
        ax.tick_params(axis="x", labelsize=7.4)
        ax.grid(axis="y", color=GRID, linewidth=0.65)
        ax.set_axisbelow(True)
    save(fig, out, "Figure 6.3: Majority baseline comparison on FakeNewsNet combined titles.", bottom=0.045)


def fig_6_4(out: Path) -> None:
    fig, ax = plt.subplots(figsize=(5.25, 5.25))
    fig.subplots_adjust(left=0.15, right=0.97, top=0.85, bottom=0.26)
    ax.fill_between([0, 0.18], 0.82, 1.04, color="#FCE8DD", alpha=0.55, zorder=0)
    ax.text(0.02, 0.84, "FAKE-heavy\ntransfer bias", ha="left", va="bottom", fontsize=7.7, color="#8A3A22")
    ax.plot([0, 1], [0, 1], linestyle="--", color="#8C8C8C", linewidth=0.9, alpha=0.85, zorder=1)
    ax.text(0.70, 0.76, "balanced recall", rotation=45, color="#666666", fontsize=7.0, ha="center", va="center")
    points = [("Always-REAL", 1.0000, 0.0000, MAJ, ""), ("TF-IDF", 0.4766, 0.5682, TFIDF, ""), ("Weighted BERT", 0.0747, 0.9564, WBERT, ""), ("Unweighted BERT", 0.0890, 0.9467, UBERT, "///"), ("Weighted RoBERTa", 0.0372, 0.9827, WROB, "")]
    handles = []
    for label, x, y, color, hatch in points:
        handles.append(ax.scatter([x], [y], s=82, color=color, alpha=0.88, edgecolor=BORDER, linewidth=0.65, hatch=hatch, label=label, zorder=3))
    ax.text(0.50, 0.535, "TF-IDF", fontsize=7.6, ha="left", va="top")
    ax.text(0.88, 0.08, "Always-REAL", fontsize=7.4, ha="right", va="bottom")
    ax.text(0.32, 0.93, "Transformer cluster:\nhigh FAKE recall,\nlow REAL recall", fontsize=7.0, ha="left", va="top", bbox={"boxstyle": "round,pad=0.23", "facecolor": "white", "edgecolor": "#C9C9C9", "linewidth": 0.55})
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.15), ncol=3, frameon=False, fontsize=6.7, handletextpad=0.3, columnspacing=0.7)
    ax.set_xlabel("REAL recall")
    ax.set_ylabel("FAKE recall")
    ax.set_xlim(-0.03, 1.03)
    ax.set_ylim(-0.03, 1.03)
    ax.set_aspect("equal", adjustable="box")
    ax.grid(color=GRID, linewidth=0.6)
    ax.tick_params(labelsize=8.2)
    ax.set_title("Prediction bias under strict transfer", fontweight="bold", fontsize=10.5, pad=7)
    save(fig, out, "Figure 6.4: Prediction bias under strict transfer.", bottom=0.045)


def fig_a_1(out: Path) -> None:
    fig, ax = setup_canvas((6.2, 4.05))
    band(ax, 0.72, 0.18, "Workspace Phase", BLUE_BG, BLUE_BORDER)
    band(ax, 0.34, 0.38, "Experiment Artefact Phase", GREEN_BG, GREEN_BORDER)
    band(ax, 0.14, 0.20, "Thesis Reporting Phase", YELLOW_BG, YELLOW_BORDER)
    rect(ax, 0.38, 0.78, 0.24, 0.07, "Project\nworkspace", PURPLE_BG, PURPLE_BORDER)
    rect(ax, 0.08, 0.49, 0.22, 0.12, "data/\nLIAR splits\nFakeNewsNet titles")
    rect(ax, 0.39, 0.49, 0.22, 0.12, "notebooks /\nscripts\nseed sweeps")
    rect(ax, 0.70, 0.49, 0.22, 0.12, "results/\nCSV, MD,\nfigures")
    # Keep the branch line well below the phase title text.
    ortho(ax, [(0.50, 0.78), (0.50, 0.66), (0.19, 0.66), (0.19, 0.61)])
    arrow(ax, (0.50, 0.78), (0.50, 0.61))
    ortho(ax, [(0.50, 0.78), (0.50, 0.66), (0.81, 0.66), (0.81, 0.61)])
    rect(ax, 0.18, 0.22, 0.64, 0.08, "Dissertation numbers trace back to saved result artefacts.")
    ortho(ax, [(0.19, 0.49), (0.19, 0.34), (0.38, 0.34), (0.38, 0.30)])
    arrow(ax, (0.50, 0.49), (0.50, 0.30))
    ortho(ax, [(0.81, 0.49), (0.81, 0.34), (0.62, 0.34), (0.62, 0.30)])
    save(fig, out, "Figure A.1: Reproducible experiment file structure and output artefacts.")


def generated_paths(round_dir: Path) -> dict[str, Path]:
    return {key: round_dir / "generated" / f"{key}.png" for key in MEDIA_TO_FIG.values()}


def generate_all(round_dir: Path) -> dict[str, Path]:
    configure()
    gen = round_dir / "generated"
    gen.mkdir(parents=True, exist_ok=True)
    paths = generated_paths(round_dir)
    make_logo(paths["logo"])
    fig_3_1(paths["fig_3_1"])
    fig_3_2(paths["fig_3_2"])
    fig_3_3(paths["fig_3_3"])
    fig_4_1(paths["fig_4_1"])
    fig_4_2(paths["fig_4_2"])
    fig_5_1(paths["fig_5_1"])
    fig_6_1(paths["fig_6_1"])
    fig_6_2(paths["fig_6_2"])
    fig_6_3(paths["fig_6_3"])
    fig_6_4(paths["fig_6_4"])
    fig_a_1(paths["fig_a_1"])
    return paths


def image_metrics(path: Path, extent: dict | None = None) -> dict:
    im = Image.open(path).convert("RGB")
    w, h = im.size
    gray = ImageOps.grayscale(im)
    mask = gray.point(lambda p: 255 if p < 248 else 0)
    bbox = mask.getbbox()
    margins = None
    content_ratio = 0.0
    if bbox:
        l, t, r, b = bbox
        margins = {"left": l, "top": t, "right": w - r, "bottom": h - b}
        content_ratio = ((r - l) * (b - t)) / (w * h)
    issues = []
    if margins:
        for side, value in margins.items():
            if value < 12:
                issues.append(f"tight {side} margin ({value}px)")
        if margins["top"] > h * 0.10:
            issues.append(f"excess top whitespace ({margins['top']}px)")
        if margins["bottom"] > h * 0.10:
            issues.append(f"excess bottom whitespace ({margins['bottom']}px)")
    if extent and extent.get("width_in"):
        dpi = w / extent["width_in"]
        if dpi < 180:
            issues.append(f"low effective dpi ({dpi:.0f})")
    else:
        dpi = None
    return {
        "pixels": [w, h],
        "margins": margins,
        "content_ratio": round(content_ratio, 3),
        "effective_dpi": round(dpi, 1) if dpi else None,
        "issues": issues,
    }


def extract_inventory(docx: Path, round_dir: Path) -> list[dict]:
    out = round_dir / "extracted"
    out.mkdir(parents=True, exist_ok=True)
    records = []
    with zipfile.ZipFile(docx) as z:
        used = used_media_paths(z)
        for name in sorted(used):
            media = Path(name).name
            data = z.read(name)
            path = out / media
            path.write_bytes(data)
            rec = {"media": media, "path": str(path)}
            rec.update(image_metrics(path))
            records.append(rec)
    make_contact_sheet(records, round_dir / "contact_sheet.png")
    (round_dir / "figure_audit.json").write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    return records


def used_media_paths(z: zipfile.ZipFile) -> set[str]:
    rel_ns = "http://schemas.openxmlformats.org/package/2006/relationships"
    doc = z.read("word/document.xml").decode("utf-8", errors="replace")
    rels_root = etree.fromstring(z.read("word/_rels/document.xml.rels"))
    used_rids = set()
    for token in ('r:embed="', 'r:link="'):
        start = 0
        while True:
            idx = doc.find(token, start)
            if idx == -1:
                break
            idx += len(token)
            end = doc.find('"', idx)
            if end == -1:
                break
            used_rids.add(doc[idx:end])
            start = end + 1
    used = set()
    for rel in rels_root.findall(f"{{{rel_ns}}}Relationship"):
        rid = rel.get("Id")
        target = rel.get("Target", "")
        if rid in used_rids and target.startswith("media/"):
            used.add("word/" + target)
    return used


def make_contact_sheet(records: list[dict], path: Path) -> None:
    cells = []
    for rec in records:
        im = Image.open(rec["path"]).convert("RGB")
        im.thumbnail((440, 250), Image.Resampling.LANCZOS)
        cell = Image.new("RGB", (480, 335), "white")
        cell.paste(im, ((480 - im.width) // 2, 10))
        d = ImageDraw.Draw(cell)
        issue_text = "; ".join(rec.get("issues", [])) or "no structural issue"
        d.multiline_text((12, 270), f"{rec['media']}  {rec.get('pixels')}\nDPI {rec.get('effective_dpi')}  {issue_text[:90]}", fill=(0, 0, 0), spacing=3)
        cells.append(cell)
    cols = 2
    rows = math.ceil(len(cells) / cols)
    sheet = Image.new("RGB", (cols * 480, rows * 335), (245, 245, 245))
    for i, cell in enumerate(cells):
        sheet.paste(cell, ((i % cols) * 480, (i // cols) * 335))
    sheet.save(path, quality=95)


def replace_media(docx: Path, generated: dict[str, Path]) -> None:
    if not BACKUP.exists():
        BACKUP.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(docx, BACKUP)
    replacements = {f"word/media/{media}": generated[key] for media, key in MEDIA_TO_FIG.items()}
    with NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
        tmp_path = Path(tmp.name)
    try:
        with zipfile.ZipFile(docx, "r") as zin, zipfile.ZipFile(tmp_path, "w", compression=zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                if item.filename in replacements:
                    zout.writestr(item, replacements[item.filename].read_bytes())
                else:
                    zout.writestr(item, zin.read(item.filename))
        shutil.move(str(tmp_path), docx)
    finally:
        if tmp_path.exists():
            tmp_path.unlink()


def remove_orphan_media(docx: Path) -> tuple[int, int]:
    rel_ns = "http://schemas.openxmlformats.org/package/2006/relationships"
    with zipfile.ZipFile(docx, "r") as zin:
        used = used_media_paths(zin)
        rels_root = etree.fromstring(zin.read("word/_rels/document.xml.rels"))
        removed_rels = 0
        for rel in list(rels_root.findall(f"{{{rel_ns}}}Relationship")):
            target = rel.get("Target", "")
            full = "word/" + target if target.startswith("media/") else None
            if full and full not in used:
                rel.getparent().remove(rel)
                removed_rels += 1
        rels_bytes = etree.tostring(rels_root, xml_declaration=True, encoding="UTF-8", standalone=True)
        removed_media = 0
        with NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            tmp_path = Path(tmp.name)
        try:
            with zipfile.ZipFile(tmp_path, "w", compression=zipfile.ZIP_DEFLATED) as zout:
                for item in zin.infolist():
                    if item.filename.startswith("word/media/") and item.filename not in used:
                        removed_media += 1
                        continue
                    if item.filename == "word/_rels/document.xml.rels":
                        zout.writestr(item, rels_bytes)
                    else:
                        zout.writestr(item, zin.read(item.filename))
            shutil.move(str(tmp_path), docx)
        finally:
            if tmp_path.exists():
                tmp_path.unlink()
    return removed_media, removed_rels


def round_run(round_no: int) -> dict:
    round_dir = QA_ROOT / f"round{round_no}"
    round_dir.mkdir(parents=True, exist_ok=True)
    before = extract_inventory(DOCX, round_dir / "before")
    generated = generate_all(round_dir)
    gen_records = []
    for media, key in MEDIA_TO_FIG.items():
        rec = {"media": media, "generated_key": key, "path": str(generated[key])}
        rec.update(image_metrics(generated[key]))
        gen_records.append(rec)
    make_contact_sheet(gen_records, round_dir / "generated_contact_sheet.png")
    replace_media(DOCX, generated)
    removed_media, removed_rels = remove_orphan_media(DOCX)
    after = extract_inventory(DOCX, round_dir / "after")
    summary = {
        "round": round_no,
        "before_issue_count": sum(len(r["issues"]) for r in before),
        "generated_issue_count": sum(len(r["issues"]) for r in gen_records),
        "after_issue_count": sum(len(r["issues"]) for r in after),
        "before_contact_sheet": str(round_dir / "before" / "contact_sheet.png"),
        "generated_contact_sheet": str(round_dir / "generated_contact_sheet.png"),
        "after_contact_sheet": str(round_dir / "after" / "contact_sheet.png"),
        "removed_orphan_media": removed_media,
        "removed_orphan_relationships": removed_rels,
    }
    (round_dir / "round_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--round", type=int, required=True)
    args = parser.parse_args()
    print(json.dumps(round_run(args.round), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
