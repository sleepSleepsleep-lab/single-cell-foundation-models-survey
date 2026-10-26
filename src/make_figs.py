# -*- coding: utf-8 -*-
"""Generate all report figures (300 dpi PNG) with a consistent editorial style."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Circle, Polygon
from matplotlib.lines import Line2D
import numpy as np

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = [
    "Microsoft YaHei", "SimHei", "PingFang SC",
    "Noto Sans CJK SC", "Source Han Sans SC", "DejaVu Sans",
]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["figure.facecolor"] = "#FBFAF7"
plt.rcParams["savefig.facecolor"] = "#FBFAF7"

OUT = "figs"
os.makedirs(OUT, exist_ok=True)

NAVY = "#1F3A5F"
TEAL = "#2A7F8F"
AMBER = "#C0803A"
BRICK = "#A5484A"
SAGE = "#5B7F5E"
PLUM = "#6B4C7A"
GRAY = "#8A94A6"
LIGHT = "#E8EDF3"
INK = "#22303F"

CLS_COLOR = {"A": NAVY, "B": TEAL, "C": AMBER, "D": SAGE, "E": BRICK, "F": PLUM}


def box(ax, x, y, w, h, fc="#FFFFFF", ec=GRAY, lw=0.8, r=0.03, alpha=1.0, z=2):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                       facecolor=fc, edgecolor=ec, linewidth=lw, alpha=alpha, zorder=z)
    ax.add_patch(p)
    return p


def arrow(ax, x1, y1, x2, y2, color=GRAY, lw=1.0, style="-|>", ls="-", ms=8, z=3):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style,
                                 mutation_scale=ms, color=color, linewidth=lw,
                                 linestyle=ls, zorder=z,
                                 shrinkA=0, shrinkB=0))


# ----------------------------------------------------------------------------- Fig 1
def fig1():
    fig = plt.figure(figsize=(6.4, 3.95))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 10.55); ax.set_ylim(1.02, 6.95); ax.axis("off")

    bands = [
        ("数据层", "模型吃什么", "#EDF1F6", [
            ("P1", "规模幻觉", "数据翻十倍\n下游增益趋零"),
            ("P2", "噪声与批次", "模型学到的是\n平台而非生物学"),
            ("P3", "数据泄漏", "零样本成绩\n被预训练污染抬高"),
            ("P4", "长尾与偏移", "稀有类型、跨物种\n跨 panel 失效"),
        ]),
        ("表示层", "模型怎么读", "#F3EFE6", [
            ("P5", "词表与顺序", "基因没有顺序\n词表不能通用"),
            ("P6", "值的离散化", "分箱丢幅值\n排序丢绝对量"),
            ("P7", "语境缺失", "细胞被当成孤岛\n空间与邻接被抹掉"),
        ]),
        ("目标层", "模型学什么", "#EEF3EF", [
            ("P8", "重建≠理解", "注意力不等于\n基因调控网络"),
            ("P9", "扰动与因果", "打不过加法基线\n真实交互仅 4.2%"),
            ("P10", "生成与多模态", "全转录组生成\n与跨模态对齐仍早"),
        ]),
        ("适配与评价", "模型怎么用、怎么判", "#F6ECEC", [
            ("P11", "适配成本", "微调贵、超参敏感\n零样本不敌基线"),
            ("P12", "评测失焦", "指标与生物学脱节\n排行榜不可比"),
        ]),
    ]

    y0 = 6.08
    band_h = 1.22
    for bi, (name, sub, bg, items) in enumerate(bands):
        top = y0 - bi * band_h
        ax.add_patch(Rectangle((0.12, top - 1.10), 9.60, 1.10, facecolor=bg,
                               edgecolor="none", zorder=1))
        ax.text(0.28, top - 0.26, name, fontsize=8.6, color=INK, fontweight="bold", va="top")
        ax.text(0.28, top - 0.55, sub, fontsize=6.2, color="#5D6B7A", va="top")

        n = len(items)
        x_start, x_end = 1.66, 9.56
        gap = 0.10
        if n == 2:
            x_end = 7.10
        w = (x_end - x_start - gap * (n - 1)) / n
        for i, (pid, title, desc) in enumerate(items):
            x = x_start + i * (w + gap)
            box(ax, x, top - 1.00, w, 0.80, fc="#FFFFFF", ec="#C9D2DE", lw=0.6, r=0.04)
            ax.text(x + 0.10, top - 0.26, pid, fontsize=6.8, color=TEAL, fontweight="bold")
            ax.text(x + 0.50, top - 0.26, title, fontsize=7.2, color=INK, fontweight="bold")
            ax.text(x + 0.10, top - 0.50, desc, fontsize=5.9, color="#4E5C6B", va="top", linespacing=1.3)

    ax.text(7.34, 2.18, "这 12 个问题不是并列清单：\n修好一层，代价会出现在下一层。",
            fontsize=6.3, color="#7A4E50", va="top", linespacing=1.7)

    # right-side flow arrow
    arrow(ax, 9.82, 6.02, 9.82, 1.30, color="#9AA6B5", lw=1.0, ms=9)
    ax.text(9.97, 3.66, "问题沿管线向下游传递", rotation=90, fontsize=6.0,
            color="#5D6B7A", ha="center", va="center")

    ax.text(0.12, 6.86, "单细胞大模型的 12 个可验证问题", fontsize=11.2, color=NAVY,
            fontweight="bold", va="top")
    ax.text(0.12, 6.54, "按「数据 → 表示 → 目标 → 适配与评价」四层归置；箭头表示上游问题会把代价推给下游",
            fontsize=6.3, color="#5D6B7A", va="top")

    fig.savefig(os.path.join(OUT, "fig1_problem_map.png"), dpi=300)
    plt.close(fig)


# ----------------------------------------------------------------------------- Fig 2
def fig2():
    fig = plt.figure(figsize=(6.4, 3.75))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 10); ax.set_ylim(0.62, 6.65); ax.axis("off")

    ax.text(0.12, 6.52, "按「建模单元 × 学习信号」得到的六个架构大类", fontsize=11.0,
            color=NAVY, fontweight="bold", va="top")
    ax.text(0.12, 6.22, "同一个主干（Transformer / RetNet / Mamba）可以出现在任何一类；分类看的是它把什么当作第一性对象、用什么信号学习",
            fontsize=6.0, color="#5D6B7A", va="top")

    box(ax, 0.12, 3.20, 1.24, 0.68, fc=NAVY, ec=NAVY, r=0.05)
    ax.text(0.74, 3.68, "scFM", fontsize=9.6, color="white", ha="center", fontweight="bold")
    ax.text(0.74, 3.38, "单细胞基础模型", fontsize=6.2, color="#DCE5EF", ha="center")

    rows = [
        ("A", "掩码基因序列", "看一半，猜一半", "scBERT · Geneformer · GeneCompass\nNicheformer · UCE · CellFM · scPRINT", NAVY),
        ("B", "自回归基因序列", "顺着往下写", "scGPT · TranscriptFormer · scMulan", TEAL),
        ("C", "连续谱编解码", "压成向量，再还原", "scFoundation · xTrimoGene · CellVQ · CAPTAIN", AMBER),
        ("D", "细胞集合模型", "细胞看细胞", "CellPLM · State · tGPT · Tahoe-x1", SAGE),
        ("E", "状态分布模型", "学分布，不学点", "Lingshu-Cell · AlphaCell · CellOS · scDifformer", BRICK),
        ("F", "语言接口模型", "把细胞翻译成人话", "Cell2Sentence · GenePT · LangCell · CellWhisperer", PLUM),
    ]
    y_top, row_h = 5.40, 0.86
    for i, (k, name, tag, models, color) in enumerate(rows):
        y = y_top - i * row_h
        ax.plot([1.36, 1.52], [3.54, y + 0.28], color="#C3CBD6", lw=0.8, zorder=1)
        ax.plot([1.52, 1.64], [y + 0.28, y + 0.28], color="#C3CBD6", lw=0.8, zorder=1)
        box(ax, 1.64, y, 0.40, 0.56, fc=color, ec=color, r=0.06)
        ax.text(1.84, y + 0.28, k, fontsize=10.5, color="white", ha="center", va="center", fontweight="bold")
        ax.text(2.16, y + 0.40, name, fontsize=8.2, color=INK, fontweight="bold", va="center")
        ax.text(2.16, y + 0.14, tag, fontsize=6.2, color=color, va="center")
        box(ax, 4.10, y, 5.72, 0.56, fc="#FFFFFF", ec="#D6DDE6", r=0.04)
        ax.text(4.24, y + 0.28, models, fontsize=6.2, color="#3D4B5C", va="center", linespacing=1.5)

    ax.text(0.12, 0.30, "注：分类依据是「一次前向传播里第一性对象是什么」与「监督信号从哪里来」，不是主干网络；跨类混血（如 RegFormer = A 类目标 + Mamba 主干）见 §3.7。",
            fontsize=5.7, color="#6B7887", va="center")

    fig.savefig(os.path.join(OUT, "fig2_taxonomy.png"), dpi=300)
    plt.close(fig)


# ----------------------------------------------------------------------------- Fig 3
def fig3():
    fig = plt.figure(figsize=(6.4, 3.05))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 10); ax.set_ylim(0.55, 5.15); ax.axis("off")

    ax.text(0.12, 5.02, "表达值怎么变成 token：一条「保真度 / 兼容性」的取舍光谱", fontsize=10.6,
            color=NAVY, fontweight="bold", va="top")

    xs = [1.25, 2.72, 4.19, 5.66, 7.13, 8.60]
    labels = ["秩\n(rank)", "硬分箱\n(hard bin)", "软分箱\n(soft bin)", "连续投影\n(continuous)", "分布参数\n(ZINB/ZTP)", "细胞级量化\n(VQ)"]
    models = ["Geneformer\nNicheformer\nscMulan", "scBERT (7)\nscGPT (51)\nscMulan (10)", "scFoundation\nCellVQ\nState (10)", "CellFM\nCellPLM\nCAPTAIN", "scPRINT\nTranscriptFormer", "CellVQ\nRVQ / CellTok"]
    colors = ["#7C8FA6", "#5E7FA6", "#3E6E92", "#2A7F8F", "#2F6E63", "#6B4C7A"]
    losses = ["丢绝对幅值", "丢序与幅值", "保留序，近似幅值", "保留幅值，怕噪声", "保留完整分布", "面向生成与压缩"]

    arrow(ax, 0.70, 2.95, 9.45, 2.95, color="#B9C3CF", lw=1.2, ms=9)
    for i, x in enumerate(xs):
        ax.add_patch(Circle((x, 2.95), 0.12, facecolor=colors[i], edgecolor="white", lw=1.2, zorder=5))
        ax.text(x, 3.38, labels[i], fontsize=6.6, color=INK, ha="center", va="bottom", fontweight="bold", linespacing=1.3)
        ax.text(x, 2.55, losses[i], fontsize=5.8, color="#6B7887", ha="center", va="top")
        ax.text(x, 2.05, models[i], fontsize=5.6, color=colors[i], ha="center", va="top", linespacing=1.4)

    arrow(ax, 0.70, 4.38, 9.45, 4.38, color=TEAL, lw=0.9, ms=8)
    ax.text(0.70, 4.54, "信息保真度更高 →", fontsize=6.2, color=TEAL, ha="left", va="bottom")
    arrow(ax, 9.45, 4.04, 0.70, 4.04, color=AMBER, lw=0.9, ms=8)
    ax.text(9.45, 4.16, "← 更易接入 LLM 词表与生成接口", fontsize=6.2, color=AMBER, ha="right", va="bottom")

    ax.text(0.12, 0.72, "左端把表达压成序，右端把表达压成分布或码字；越往右信息越完整，但与离散词表、交叉熵目标的距离越远。",
            fontsize=5.9, color="#6B7887", va="center")

    fig.savefig(os.path.join(OUT, "fig3_tokenizer_spectrum.png"), dpi=300)
    plt.close(fig)


# ----------------------------------------------------------------------------- Fig 4
def fig4():
    probs = ["P1 规模幻觉", "P2 噪声与批次", "P3 数据泄漏", "P4 长尾与偏移",
             "P5 词表与顺序", "P6 值的离散化", "P7 语境缺失",
             "P8 重建≠理解", "P9 扰动与因果", "P10 生成与多模态",
             "P11 适配成本", "P12 评测失焦"]
    cls = ["A 掩码\n基因序列", "B 自回归\n基因序列", "C 连续谱\n编解码", "D 细胞\n集合", "E 状态\n分布", "F 语言\n接口"]
    M = np.array([
        [1, 0, 2, 0, 1, 0],
        [2, 1, 2, 3, 2, 0],
        [0, 0, 0, 0, 0, 0],
        [1, 1, 2, 1, 1, 1],
        [3, 1, 1, 0, 0, 2],
        [2, 2, 3, 2, 2, 0],
        [0, 0, 0, 3, 1, 0],
        [2, 1, 0, 0, 0, 1],
        [1, 2, 1, 3, 3, 0],
        [1, 3, 3, 2, 3, 1],
        [3, 2, 2, 3, 1, 3],
        [1, 1, 1, 1, 2, 2],
    ])
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list(
        "cov", ["#F5F2EC", "#DCE5EE", "#9DB9D1", "#2F5E8C"])
    fig = plt.figure(figsize=(6.4, 4.25))
    ax = fig.add_axes([0.225, 0.10, 0.60, 0.75])
    ax.imshow(M, cmap=cmap, vmin=0, vmax=3, aspect="auto")
    ax.set_xticks(range(len(cls))); ax.set_xticklabels(cls, fontsize=6.4)
    ax.set_yticks(range(len(probs))); ax.set_yticklabels(probs, fontsize=6.6)
    ax.tick_params(length=0)
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.set_xticks(np.arange(-.5, len(cls), 1), minor=True)
    ax.set_yticks(np.arange(-.5, len(probs), 1), minor=True)
    ax.grid(which="minor", color="#FBFAF7", linewidth=2.2)
    ax.tick_params(which="minor", length=0)

    sizes = {1: 16, 2: 55, 3: 135}
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            v = M[i, j]
            if v:
                ax.scatter([j], [i], s=sizes[v], marker="o",
                           color="white" if v >= 2 else "#63727F",
                           edgecolor="none", zorder=5)

    # P3 row: not an architecture problem
    ax.add_patch(Rectangle((-0.5, 1.5), 6, 1, facecolor="none", edgecolor="#B08A6A",
                           hatch="///", linewidth=0, alpha=0.55, zorder=4))
    ax.text(2.5, 2.0, "无架构解：只能靠数据审计与时间切分", fontsize=6.8,
            color="#7A4E50", ha="center", va="center", zorder=6,
            bbox=dict(facecolor="#F7F3EC", edgecolor="none", pad=2.0, alpha=0.92))

    fig.text(0.03, 0.955, "问题 × 架构：哪一类真正回应了哪个问题", fontsize=10.2, color=NAVY,
             fontweight="bold", va="top")
    fig.text(0.03, 0.905, "圆点越大 = 该类的核心设计越直接地针对该问题；空白 = 该类在该问题上没有结构性优势",
             fontsize=6.1, color="#5D6B7A", va="top")

    cax = fig.add_axes([0.865, 0.24, 0.013, 0.46])
    cb = matplotlib.colorbar.ColorbarBase(cax, cmap=cmap, norm=matplotlib.colors.Normalize(0, 3),
                                          orientation="vertical", ticks=[0, 1, 2, 3])
    cb.ax.set_yticklabels(["无", "间接", "部分", "核心"], fontsize=6)
    cb.outline.set_visible(False)
    cb.ax.tick_params(length=0)

    fig.savefig(os.path.join(OUT, "fig4_coverage.png"), dpi=300)
    plt.close(fig)


# ----------------------------------------------------------------------------- Fig 5
def fig5():
    fig = plt.figure(figsize=(6.4, 3.75))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 10); ax.set_ylim(0, 6.0); ax.axis("off")

    ax.text(0.12, 5.88, "从任务出发的选型路径", fontsize=10.6, color=NAVY, fontweight="bold", va="top")
    ax.text(0.12, 5.58, "先判断任务落在哪一层，再看该层的结构性代价你是否能接受——而不是先问「哪个模型最强」",
            fontsize=6.1, color="#5D6B7A", va="top")

    box(ax, 0.30, 2.68, 1.20, 0.62, fc=NAVY, ec=NAVY, r=0.05)
    ax.text(0.90, 2.99, "任务", fontsize=9, color="white", ha="center", va="center", fontweight="bold")

    items = [
        ("注释 / 检索", "A 类为主，D 类补语境", "CellFM、Geneformer、SCimilarity", NAVY, 4.70),
        ("批次整合", "先基线，再考虑 scFM", "Harmony / scVI → scGPT、Geneformer", TEAL, 3.90),
        ("跨物种 / 跨平台", "词表无关的基因身份", "UCE、TranscriptFormer、GeneCompass", AMBER, 3.10),
        ("扰动 / 虚拟细胞", "集合分布或状态转移", "State、Lingshu-Cell、AlphaCell", BRICK, 2.30),
        ("生成 / 补全", "谱级生成模型", "scFoundation、scMulan、CAPTAIN", SAGE, 1.50),
        ("GRN / 可解释", "先验注入 + 因果验证", "scPRINT、RegFormer、GeneCompass", PLUM, 0.70),
    ]
    # bracket
    ax.plot([1.50, 1.64], [2.99, 2.99], color="#C3CBD6", lw=0.8, zorder=1)
    ax.plot([1.64, 1.64], [0.94, 4.94], color="#C3CBD6", lw=0.8, zorder=1)
    for label, judge, rec, color, y in items:
        cy = y + 0.22
        ax.plot([1.64, 1.82], [cy, cy], color="#C3CBD6", lw=0.8, zorder=1)
        box(ax, 1.82, y, 1.40, 0.44, fc="#FFFFFF", ec=color, lw=0.9, r=0.04)
        ax.text(2.52, cy, label, fontsize=7.0, color=INK, ha="center", va="center", fontweight="bold")
        arrow(ax, 3.24, cy, 3.44, cy, color=color, lw=0.8, ms=7)
        ax.text(3.52, cy + 0.10, judge, fontsize=6.3, color=color, va="center")
        ax.text(3.52, cy - 0.12, rec, fontsize=6.0, color="#4E5C6B", va="center")

    ax.text(0.12, 0.12, "注：① 任何任务都应先跑强基线（HVG、Harmony、scVI、逻辑回归、additive）；② A 类在零样本上最容易被简单基线追平，微调后才有稳定优势。",
            fontsize=5.7, color="#6B7887", va="center")

    fig.savefig(os.path.join(OUT, "fig5_decision.png"), dpi=300)
    plt.close(fig)


# ----------------------------------------------------------------------------- Fig 6
def fig6():
    # (name, time, class, dy, label?)
    models = [
        ("scBERT", 2021.95, "A", 0.22, True), ("tGPT", 2022.45, "D", 0, False),
        ("Geneformer", 2022.80, "A", 0.22, True), ("scGPT", 2023.30, "B", 0.22, True),
        ("scFoundation", 2023.40, "C", 0.22, True), ("GenePT", 2023.70, "F", 0.22, True),
        ("Cell2Sentence", 2023.74, "F", 0, False), ("xTrimoGene", 2023.88, "C", 0, False),
        ("scMulan", 2024.08, "B", 0, False), ("CellPLM", 2024.25, "D", 0.22, True),
        ("scPRINT", 2024.35, "A", 0, False), ("Nicheformer", 2024.55, "A", 0, False),
        ("GeneCompass", 2024.78, "A", 0, False), ("SCimilarity", 2024.90, "A", 0, False),
        ("TranscriptFormer", 2025.30, "B", 0.22, True), ("CellFM", 2025.40, "A", 0.22, False),
        ("State", 2025.50, "D", 0.22, True), ("UCE", 2025.80, "A", 0.22, False),
        ("CellVQ", 2025.90, "C", 0, False), ("AlphaCell", 2026.22, "E", 0.22, True),
        ("CAPTAIN", 2026.40, "C", 0.22, True), ("RegFormer", 2026.50, "A", 0.22, True),
        ("scDifformer", 2026.55, "E", 0, False), ("CellOS", 2026.62, "E", 0, False),
        ("Lingshu-Cell", 2026.70, "E", 0.55, True),
    ]
    lanes = {"A": 5.75, "B": 4.75, "C": 3.75, "D": 2.75, "E": 1.75, "F": 0.75}
    lane_names = {"A": "A 掩码基因序列", "B": "B 自回归序列", "C": "C 连续谱编解码",
                  "D": "D 细胞集合", "E": "E 状态分布", "F": "F 语言接口"}
    fig = plt.figure(figsize=(6.4, 3.95))
    ax = fig.add_axes([0.195, 0.12, 0.775, 0.715])

    ax.axvspan(2026.05, 2026.95, color="#F7EEEB", zorder=0)
    for k, y in lanes.items():
        ax.axhline(y, color="#E1E6ED", lw=0.8, zorder=0)
    for yr in (2022, 2023, 2024, 2025, 2026):
        ax.axvline(yr, color="#EEF1F5", lw=0.7, zorder=0)

    for name, x, k, dy, show in models:
        y = lanes[k]
        ax.scatter([x], [y], s=26, color=CLS_COLOR[k], zorder=4, edgecolor="white", linewidth=0.6)
        if show:
            ax.annotate(name, (x, y), xytext=(x + (0.0 if name != "Lingshu-Cell" else -0.18), y + dy), fontsize=6.4, color="#33404F",
                        ha="center", va="bottom",
                        arrowprops=dict(arrowstyle="-", color="#C3CBD6", lw=0.35, shrinkA=0, shrinkB=0.5))

    ax.set_xlim(2021.62, 2026.95)
    ax.set_ylim(-0.20, 6.30)
    ax.set_yticks([lanes[k] for k in "ABCDEF"])
    ax.set_yticklabels([lane_names[k] for k in "ABCDEF"], fontsize=6.8)
    for i, k in enumerate("ABCDEF"):
        ax.get_yticklabels()[i].set_color(CLS_COLOR[k])
    ax.set_xticks([2022, 2023, 2024, 2025, 2026])
    ax.set_xticklabels(["2022", "2023", "2024", "2025", "2026"], fontsize=6.8)
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.tick_params(length=0, colors="#5D6B7A")
    ax.set_title("六个大类的时间分布：2026 年的新增几乎都在 E 类（状态分布）",
                 fontsize=10.0, color=NAVY, fontweight="bold", loc="left", pad=8)
    fig.text(0.195, 0.02, "每个圆点 = 一个模型首次公开；仅标注各阶段代表，完整清单与规格见 §4.1。",
             fontsize=6.2, color="#6B7887")

    fig.savefig(os.path.join(OUT, "fig6_timeline.png"), dpi=300)
    plt.close(fig)


for f in (fig1, fig2, fig3, fig4, fig5, fig6):
    f()
print("done")
