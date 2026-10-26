# -*- coding: utf-8 -*-
"""Build the 16:9 presentation deck for the report (v2, tighter layouts)."""
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from lxml import etree

NAVY = RGBColor(0x1F, 0x3A, 0x5F)
BLUE = RGBColor(0x2E, 0x5C, 0x8A)
AMBER = RGBColor(0xC0, 0x80, 0x3A)
BRICK = RGBColor(0xA5, 0x48, 0x4A)
SAGE = RGBColor(0x5B, 0x7F, 0x5E)
PLUM = RGBColor(0x6B, 0x4C, 0x7A)
INK = RGBColor(0x22, 0x30, 0x3F)
GRAY = RGBColor(0x5D, 0x6B, 0x7A)
LIGHTGRAY = RGBColor(0x8A, 0x94, 0xA6)
PAPER = RGBColor(0xF7, 0xF5, 0xF1)
CARD = RGBColor(0xF5, 0xF7, 0xFA)
CREAM = RGBColor(0xF4, 0xF1, 0xEC)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LINE = RGBColor(0xD5, 0xDC, 0xE6)

FONT = "微软雅黑"
W, H = 13.333, 7.5
ML = 0.78
CW = W - 2 * ML


def set_font(run, size=14, bold=False, color=INK, font=FONT):
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = font
    rPr = run._r.get_or_add_rPr()
    ea = rPr.find(qn("a:ea"))
    if ea is None:
        ea = etree.SubElement(rPr, qn("a:ea"))
    ea.set("typeface", font)


def add_text(slide, x, y, w, h, text, size=14, bold=False, color=INK,
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, line=1.15):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    p = tf.paragraphs[0]
    p.alignment = align
    p.line_spacing = line
    r = p.add_run()
    r.text = text
    set_font(r, size, bold, color)
    return box


def add_multi(slide, x, y, w, h, paras, anchor=MSO_ANCHOR.TOP, align=PP_ALIGN.LEFT):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    for i, part in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = part.get("align", align)
        p.line_spacing = part.get("line", 1.22)
        if part.get("space_before"):
            p.space_before = Pt(part["space_before"])
        if part.get("space_after") is not None:
            p.space_after = Pt(part["space_after"])
        r = p.add_run()
        r.text = part["text"]
        set_font(r, part.get("size", 12), part.get("bold", False), part.get("color", INK))
    return box


def rect(slide, x, y, w, h, fill=None, line_color=None, line_w=0.75,
         shape=MSO_SHAPE.RECTANGLE, radius=None):
    s = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is None:
        s.fill.background()
    else:
        s.fill.solid()
        s.fill.fore_color.rgb = fill
    if line_color is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line_color
        s.line.width = Pt(line_w)
    el = s._element
    style = el.find(qn("p:style"))
    if style is not None:
        el.remove(style)
    if radius is not None and shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        try:
            s.adjustments[0] = radius
        except Exception:
            pass
    return s


def header(slide, kicker, title):
    add_text(slide, ML, 0.40, CW, 0.28, kicker, 10.5, True, AMBER)
    add_text(slide, ML, 0.66, CW, 0.70, title, 26, True, NAVY)
    rect(slide, ML, 1.46, CW, 0.012, fill=LINE)


def footer(slide, page):
    rect(slide, ML, 7.04, CW, 0.006, fill=LINE)
    add_text(slide, ML, 7.11, 8.0, 0.24, "单细胞大模型：问题、方案与架构", 8.5, False, LIGHTGRAY)
    add_text(slide, W - ML - 0.8, 7.11, 0.8, 0.24, f"{page:02d}", 8.5, True, LIGHTGRAY,
             align=PP_ALIGN.RIGHT)


def new_slide(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])


def picture_fit(slide, path, x, y, w, h):
    from PIL import Image
    iw, ih = Image.open(path).size
    ratio = min(w / iw, h / ih)
    nw, nh = iw * ratio, ih * ratio
    slide.shapes.add_picture(path, Inches(x + (w - nw) / 2), Inches(y + (h - nh) / 2),
                             width=Inches(nw), height=Inches(nh))


def chips(slide, y, items, color, size=10.5, h=0.40, x0=ML, maxw=None):
    maxw = maxw or (W - ML)
    x = x0
    for m in items:
        tw = max(1.05, 0.118 * len(m) + 0.36)
        if x + tw > maxw:
            x = x0
            y += h + 0.12
        rect(slide, x, y, tw, h, fill=WHITE, line_color=color, line_w=1.0,
             shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.2)
        add_text(slide, x + 0.06, y + 0.08, tw - 0.12, 0.24, m, size, True, color,
                 align=PP_ALIGN.CENTER)
        x += tw + 0.10
    return y + h


# --------------------------------------------------------------------------- components
def class_slide(prs, page, tag, title, blocks, models, color, fit, avoid, verdict, strip):
    s = new_slide(prs)
    header(s, tag, title)
    n = len(blocks)
    gap = 0.18
    w = (CW - gap * (n - 1)) / n
    for i, (h, body) in enumerate(blocks):
        x = ML + i * (w + gap)
        rect(s, x, 1.62, w, 1.52, fill=CARD)
        rect(s, x, 1.62, w, 0.05, fill=color)
        add_text(s, x + 0.20, 1.76, w - 0.4, 0.24, h, 9.5, True, color)
        add_text(s, x + 0.20, 2.02, w - 0.4, 1.0, body, 9.8, False, GRAY, line=1.38)

    add_text(s, ML, 3.34, 1.8, 0.24, "代表模型", 9, True, AMBER)
    chips(s, 3.56, models, color, size=10, h=0.38)

    rect(s, ML, 4.28, CW, 0.55, fill=WHITE, line_color=LINE, line_w=0.75)
    add_text(s, ML + 0.18, 4.40, 1.1, 0.24, "变体谱", 8.6, True, color)
    add_text(s, ML + 1.30, 4.38, CW - 1.5, 0.32, strip, 9.6, False, GRAY)

    rect(s, ML, 5.08, CW, 0.72, fill=CREAM)
    rect(s, ML, 5.08, 0.05, 0.72, fill=AMBER)
    add_text(s, ML + 0.20, 5.18, 5.6, 0.22, "适用", 8.6, True, SAGE)
    add_text(s, ML + 0.80, 5.17, 5.0, 0.55, fit, 9.2, False, RGBColor(0x3D, 0x4B, 0x5C), line=1.3)
    add_text(s, ML + 6.45, 5.18, 5.6, 0.22, "不适用", 8.6, True, BRICK)
    add_text(s, ML + 7.30, 5.17, 4.2, 0.55, avoid, 9.2, False, RGBColor(0x3D, 0x4B, 0x5C), line=1.3)

    add_text(s, ML, 6.12, CW, 0.3, "一句话：" + verdict, 11, True, color)
    footer(s, page)


def duo_panel(slide, x, y, w, h, tag, title, rows, models, color, verdict):
    rect(slide, x, y, w, h, fill=CARD)
    rect(slide, x, y, w, 0.06, fill=color)
    add_text(slide, x + 0.24, y + 0.14, w - 0.48, 0.22, tag, 9.0, True, color)
    add_text(slide, x + 0.24, y + 0.38, w - 0.48, 0.32, title, 14.5, True, INK)

    yy = y + 0.84
    for label, body in rows:
        lines = body.split("\n") if isinstance(body, str) else list(body)
        add_text(slide, x + 0.24, yy, 0.82, 0.22, label, 8.2, True, LIGHTGRAY)
        box = slide.shapes.add_textbox(Inches(x + 1.08), Inches(yy - 0.03),
                                       Inches(w - 1.32), Inches(1.9))
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = 0; tf.margin_right = 0; tf.margin_top = 0; tf.margin_bottom = 0
        for j, line in enumerate(lines):
            para = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
            para.line_spacing = 1.28
            r = para.add_run(); r.text = line
            set_font(r, 9.4, False, GRAY)
        yy += max(0.29, len(lines) * 0.205 + 0.09)

    add_text(slide, x + 0.24, y + 3.10, w - 0.48, 0.5, verdict, 9.2, True, color, line=1.3)
    add_text(slide, x + 0.24, y + 3.66, w - 0.48, 0.28, " · ".join(models), 9.0, True, color)


def duo_slide(prs, page, title, left, right, bottom):
    s = new_slide(prs)
    header(s, "02  ·  架构分类", title)
    w = CW / 2 - 0.12
    duo_panel(s, ML, 1.60, w, 4.40, *left)
    duo_panel(s, ML + w + 0.24, 1.60, w, 4.40, *right)
    rect(s, ML, 6.22, CW, 0.62, fill=CREAM)
    rect(s, ML, 6.22, 0.05, 0.62, fill=AMBER)
    add_text(s, ML + 0.22, 6.38, CW - 0.44, 0.35, bottom, 10.2, True, RGBColor(0x7A, 0x4E, 0x50))
    footer(s, page)


def models_slide(prs, page, kicker, title, models, color):
    s = new_slide(prs)
    header(s, kicker, title)
    n = len(models)
    gap = 0.14
    w = (CW - gap * (n - 1)) / n
    for i, (name, role, spec, design, cost, verdict) in enumerate(models):
        x = ML + i * (w + gap)
        rect(s, x, 1.60, w, 5.12, fill=CARD)
        rect(s, x, 1.60, w, 0.06, fill=color)
        add_text(s, x + 0.18, 1.74, w - 0.36, 0.30, name, 13, True, color)
        add_text(s, x + 0.18, 2.06, w - 0.36, 0.24, role, 8.4, True, LIGHTGRAY)
        add_text(s, x + 0.18, 2.34, w - 0.36, 0.24, spec, 8.4, True, AMBER)
        add_text(s, x + 0.18, 2.68, w - 0.36, 0.20, "独特设计", 7.8, True, LIGHTGRAY)
        add_text(s, x + 0.18, 2.90, w - 0.36, 1.55, design, 9.0, False, INK, line=1.34)
        add_text(s, x + 0.18, 4.52, w - 0.36, 0.20, "代价", 7.8, True, BRICK)
        add_text(s, x + 0.18, 4.74, w - 0.36, 1.0, cost, 9.0, False, GRAY, line=1.34)
        add_text(s, x + 0.18, 5.94, w - 0.36, 0.55, verdict, 8.6, True, color, line=1.3)
    footer(s, page)


def slide_cover(prs):
    s = new_slide(prs)
    rect(s, 0, 0, W, 0.10, fill=NAVY)
    add_text(s, ML, 1.92, 9.0, 0.3, "RESEARCH REPORT  ·  2026", 11, True, AMBER)
    add_text(s, ML, 2.16, 11.8, 0.85, "单细胞大模型", 46, True, NAVY)
    add_text(s, ML, 2.98, 11.8, 0.75, "问题、方案与架构", 36, True, BLUE)
    rect(s, ML, 3.92, 2.6, 0.05, fill=AMBER)
    add_text(s, ML, 4.14, 11.4, 0.4, "十二个可验证问题 · 六个架构大类 · 二十七个模型的设计取舍",
             16, False, RGBColor(0x3D, 0x4B, 0x5C))
    add_text(s, ML, 4.60, 11.4, 0.35, "从“把 BERT 搬到细胞”到“用分布预测干预”：一次以代价为中心的技术盘点",
             11, False, GRAY)

    rect(s, ML, 6.10, CW, 0.008, fill=LINE)
    add_text(s, ML, 6.28, 4.0, 0.28, "汇报版 v1.0", 10, True, NAVY)
    add_text(s, ML, 6.58, 5.0, 0.28, "2026 年 10 月 26 日", 10, False, GRAY)
    add_text(s, W - ML - 4.4, 6.58, 4.4, 0.28, "资料截至 2026-10 · 厂商口径单独标注", 9, False, LIGHTGRAY,
             align=PP_ALIGN.RIGHT)


def slide_map(prs, page):
    s = new_slide(prs)
    header(s, "00  ·  报告地图", "四个部分，回答两个问题")
    items = [
        ("01", "问题", "12 个可验证的问题，分四层\n机理 · 证据 · 解法 · 判据", NAVY),
        ("02", "架构", "6 个架构大类，按建模单元 × 学习信号划分\n每类给出归纳偏置与共同天花板", BLUE),
        ("03", "模型", "27 款模型的独特设计与代价\n一张速查表 + 逐模型点评", AMBER),
        ("04", "判断", "13 项独立评测的结论\n5 条趋势判断 + 3 组建议", BRICK),
    ]
    for i, (num, title, body, color) in enumerate(items):
        x = ML + (i % 2) * (CW / 2 + 0.12)
        y = 1.78 + (i // 2) * 2.30
        w = CW / 2 - 0.12
        rect(s, x, y, w, 2.05, fill=CARD)
        rect(s, x, y, w, 0.05, fill=color)
        add_text(s, x + 0.24, y + 0.24, 0.9, 0.45, num, 21, True, color)
        add_text(s, x + 0.95, y + 0.28, w - 1.1, 0.35, title, 16, True, INK)
        add_text(s, x + 0.24, y + 0.92, w - 0.5, 1.0, body, 11.5, False, GRAY, line=1.5)
    footer(s, page)


def slide_theses(prs, page):
    s = new_slide(prs)
    header(s, "00  ·  核心判断", "六条判断，先看结论")
    rows = [
        ("01", "问题是分层的", "修好一层，代价会以另一种形式出现在下一层。", NAVY),
        ("02", "最硬的问题不在模型侧", "泄漏、饱和、噪声，都是数据与评测制度问题。", BLUE),
        ("03", "六个大类 = 两组坐标的可行组合", "建模单元 × 学习信号；主干是正交选择。", AMBER),
        ("04", "每一类都有结构性代价", "没有免费午餐：丢幅值、丢序、丢分辨率、丢可解释。", SAGE),
        ("05", "2026 的主线是换监督信号", "从“重建表达”转向“预测干预后的分布”。", BRICK),
        ("06", "评测仍停在重建指标", "与“干预正确性”错位，是最大的方法论缺口。", PLUM),
    ]
    y = 1.76
    for num, head, body, color in rows:
        rect(s, ML, y, 0.44, 0.44, fill=color, shape=MSO_SHAPE.OVAL)
        add_text(s, ML, y + 0.10, 0.44, 0.24, num, 9.5, True, WHITE, align=PP_ALIGN.CENTER)
        add_text(s, ML + 0.64, y + 0.03, 3.55, 0.38, head, 15, True, INK)
        add_text(s, ML + 4.20, y + 0.05, CW - 4.20, 0.38, body, 12.2, False, GRAY)
        y += 0.84
    footer(s, page)


def slide_problem_overview(prs, page):
    s = new_slide(prs)
    header(s, "01  ·  问题图谱", "十二个问题，四层管线")
    layers = [
        ("数据层", "模型吃什么", NAVY, [
            ("P1", "规模幻觉", "数据翻十倍，下游增益趋零"),
            ("P2", "噪声与批次", "学到的是平台，不是生物学"),
            ("P3", "数据泄漏", "零样本成绩被预训练污染"),
            ("P4", "长尾与偏移", "稀有类型、跨物种失效"),
        ]),
        ("表示层", "模型怎么读", AMBER, [
            ("P5", "词表与顺序", "基因没有顺序，词表不通用"),
            ("P6", "值的离散化", "分箱丢幅值，排序丢绝对量"),
            ("P7", "语境缺失", "细胞被当成孤岛"),
        ]),
        ("目标层", "模型学什么", SAGE, [
            ("P8", "重建≠理解", "注意力不等于基因调控网络"),
            ("P9", "扰动与因果", "打不过加法基线，真实交互 4.2%"),
            ("P10", "生成与多模态", "全谱生成与跨模态对齐仍早"),
        ]),
        ("适配与评价", "怎么用、怎么判", BRICK, [
            ("P11", "适配成本", "微调贵、超参敏感、许可分裂"),
            ("P12", "评测失焦", "指标与生物学脱节"),
        ]),
    ]
    y = 1.62
    for name, sub, color, items in layers:
        h = 1.18
        rect(s, ML, y, CW, h, fill=PAPER)
        add_text(s, ML + 0.18, y + 0.18, 1.4, 0.3, name, 12.5, True, INK)
        add_text(s, ML + 0.18, y + 0.52, 1.4, 0.5, sub, 9, False, GRAY, line=1.2)
        n = len(items)
        x0 = ML + 1.62
        avail = CW - 1.68
        gap = 0.10
        w = (avail - gap * (n - 1)) / n
        for i, (pid, title, desc) in enumerate(items):
            x = x0 + i * (w + gap)
            rect(s, x, y + 0.10, w, h - 0.20, fill=WHITE, line_color=LINE, line_w=0.75)
            add_text(s, x + 0.12, y + 0.18, 0.45, 0.25, pid, 8.5, True, color)
            add_text(s, x + 0.52, y + 0.18, w - 0.6, 0.25, title, 10.2, True, INK)
            add_text(s, x + 0.12, y + 0.52, w - 0.2, 0.5, desc, 8.4, False, GRAY, line=1.25)
        y += h + 0.10
    add_text(s, ML, 6.72, CW, 0.25,
             "这 12 个问题不是并列清单：修好一层，代价会出现在下一层。",
             9.5, True, AMBER)
    footer(s, page)


def slide_layer(prs, page, kicker, title, cards, note, verdicts, banner):
    s = new_slide(prs)
    header(s, kicker, title)
    n = len(cards)
    gap = 0.16
    w = (CW - gap * (n - 1)) / n
    for i, (tag, head, body, color) in enumerate(cards):
        x = ML + i * (w + gap)
        rect(s, x, 1.64, w, 3.20, fill=CARD)
        rect(s, x, 1.64, w, 0.06, fill=color)
        add_text(s, x + 0.18, 1.80, 0.8, 0.26, tag, 9.5, True, color)
        add_text(s, x + 0.18, 2.06, w - 0.36, 0.5, head, 13.2, True, INK, line=1.2)
        add_text(s, x + 0.18, 2.62, w - 0.36, 1.05, body, 9.4, False, GRAY, line=1.4)
        rect(s, x + 0.18, 3.66, w - 0.36, 0.008, fill=LINE)
        add_text(s, x + 0.18, 3.74, 0.6, 0.2, "判据", 7.8, True, AMBER)
        add_text(s, x + 0.60, 3.72, w - 0.76, 0.95, verdicts[i], 8.4, False, RGBColor(0x3D, 0x4B, 0x5C), line=1.3)
    add_text(s, ML, 5.12, CW, 0.55, note, 9.6, False, RGBColor(0x3D, 0x4B, 0x5C), line=1.4)
    rect(s, ML, 5.86, CW, 0.72, fill=CREAM)
    rect(s, ML, 5.86, 0.05, 0.72, fill=AMBER)
    add_text(s, ML + 0.22, 6.04, CW - 0.44, 0.45, "核心矛盾：" + banner, 10.8, True, RGBColor(0x7A, 0x4E, 0x50))
    footer(s, page)


def slide_taxonomy(prs, page):
    s = new_slide(prs)
    header(s, "02  ·  架构分类", "六个大类：建模单元 × 学习信号")
    picture_fit(s, "figs/fig2_taxonomy.png", ML - 0.1, 1.56, 7.9, 5.25)
    x = ML + 8.15
    w = W - ML - x
    add_text(s, x, 1.70, w, 0.26, "两个坐标", 11, True, NAVY)
    add_text(s, x, 2.00, w, 1.1,
             "横轴：第一性对象是什么——基因、细胞、表达谱、状态分布、语言。",
             9.8, False, GRAY, line=1.45)
    add_text(s, x, 2.78, w, 1.1,
             "纵轴：监督从哪里来——掩码重建、似然生成、对齐、隐空间预测。",
             9.8, False, GRAY, line=1.45)
    rect(s, x, 3.62, w, 0.008, fill=LINE)
    add_text(s, x, 3.76, w, 0.26, "主干是正交维度", 11, True, NAVY)
    add_text(s, x, 4.06, w, 1.6,
             "Performer / RetNet / Mamba / Flowformer 只决定“能读多长、多快”，不决定“学什么”。同一个 Mamba 可以出现在 A 类与 E 类。",
             9.8, False, GRAY, line=1.45)
    footer(s, page)


def slide_reality(prs, page):
    s = new_slide(prs)
    header(s, "04  ·  现实检验", "三项被确认的负面结论，四项仍然成立的优势")
    neg = [
        ("零样本不敌基线", "Geneformer ASW 0.38–0.52；\nPBMC 上 L1 逻辑回归胜 scBERT"),
        ("扰动打不过 additive", "Norman 双扰动上所有模型误差\n高于“两个单扰动相加”"),
        ("排名随数据集翻转", "scEval 8 类任务 × 10 个模型：\n没有任何模型全面领先"),
    ]
    w = (CW - 0.5) / 3
    for i, (h, body) in enumerate(neg):
        x = ML + i * (w + 0.25)
        rect(s, x, 1.64, w, 1.95, fill=CARD)
        rect(s, x, 1.64, w, 0.05, fill=BRICK)
        add_text(s, x + 0.20, 1.82, w - 0.4, 0.28, h, 12.5, True, BRICK)
        add_text(s, x + 0.20, 2.20, w - 0.36, 1.2, body, 9.4, False, GRAY, line=1.4)

    add_text(s, ML, 3.90, CW, 0.28, "但四条优势仍然成立", 12.5, True, NAVY)
    pos = [
        ("微调后 OOD 泛化", "样本越少，优势越明显"),
        ("嵌入可作特征", "优于均值与随机嵌入"),
        ("预训练确有贡献", "去预训练显著变差"),
        ("域匹配 > 规模", "Replogle 线性模型胜通用大模型"),
    ]
    for i, (h, body) in enumerate(pos):
        x = ML + i * (CW / 4 + 0.02)
        add_text(s, x, 4.28, CW / 4 - 0.08, 0.24, "● " + h, 10, True, SAGE)
        add_text(s, x + 0.22, 4.58, CW / 4 - 0.28, 0.7, body, 9, False, GRAY, line=1.35)

    rect(s, ML, 5.55, CW, 0.95, fill=CREAM)
    rect(s, ML, 5.55, 0.05, 0.95, fill=AMBER)
    add_text(s, ML + 0.22, 5.70, CW - 0.44, 0.68,
             "结论：scFM 不是“无用”，而是“被误用”。当成开箱即用的通用智能会失望；当成高质量初始化 + 迁移学习起点，它已在多个场景证明价值。",
             10.2, False, RGBColor(0x3D, 0x4B, 0x5C), line=1.45)
    footer(s, page)


def slide_theses5(prs, page):
    s = new_slide(prs)
    header(s, "05  ·  判断", "2026–2028：五条可观察的判断")
    rows = [
        ("数据", "观测 atlas 接近饱和，扰动数据决定上限", "扰动数据成本、跨实验室标准", NAVY),
        ("目标", "从重建转向分布/转移，集合级损失成为标配", "新论文是否默认报告分布指标", BLUE),
        ("表示", "词表无关的基因身份成为默认", "新模型是否还依赖固定词表", AMBER),
        ("架构", "通用底座 + 领域适配器，不会有一个主干通吃", "是否出现模型卡与适配器市场", SAGE),
        ("评测", "从排行榜转向“能否替代一次实验”", "VCC 是否成为年度惯例", BRICK),
    ]
    y = 1.72
    for tag, text, signal, c in rows:
        rect(s, ML, y, 1.10, 0.62, fill=c)
        add_text(s, ML, y + 0.17, 1.10, 0.28, tag, 11.5, True, WHITE, align=PP_ALIGN.CENTER)
        add_text(s, ML + 1.30, y + 0.06, 6.4, 0.5, text, 13, True, INK, line=1.25)
        add_text(s, ML + 7.85, y + 0.16, CW - 7.85, 0.4, "信号：" + signal, 9.2, False, GRAY)
        y += 0.92
    footer(s, page)


def slide_advice(prs, page):
    s = new_slide(prs)
    header(s, "05  ·  建议", "三条值得走的路，一条不建议的路")
    cols = [
        ("做数据", "高质量扰动数据的生产成本、元数据标准化、跨实验室去重，是最难被追平的壁垒。", NAVY),
        ("做目标", "分布级损失、因果识别、可识别性约束，才是 P8–P10 的真正解法。", BLUE),
        ("做评测", "时间切分、逐细胞审计、任务化指标、失败案例披露——不产生引用，但决定判断力。", AMBER),
    ]
    w = (CW - 0.3) / 3
    for i, (h, body, c) in enumerate(cols):
        x = ML + i * (w + 0.15)
        rect(s, x, 1.64, w, 2.45, fill=CARD)
        rect(s, x, 1.64, w, 0.05, fill=c)
        add_text(s, x + 0.22, 1.84, w - 0.44, 0.32, h, 15.5, True, c)
        add_text(s, x + 0.22, 2.26, w - 0.44, 1.65, body, 10.2, False, GRAY, line=1.45)

    rect(s, ML, 4.38, CW, 0.80, fill=RGBColor(0xF6, 0xEC, 0xEC))
    rect(s, ML, 4.38, 0.05, 0.80, fill=BRICK)
    add_text(s, ML + 0.20, 4.52, 1.4, 0.26, "不建议", 9.5, True, BRICK)
    add_text(s, ML + 1.35, 4.50, CW - 1.55, 0.55,
             "再训一个同质的大模型。除非你有别人没有的数据，或者别人没有的算力栈。",
             11, False, RGBColor(0x3D, 0x4B, 0x5C))

    add_text(s, ML, 5.55, CW, 0.28, "如果只有一句话", 9.8, True, AMBER)
    add_text(s, ML, 5.86, CW, 0.9,
             "先用强基线把任务做到 80 分，再问 scFM 能不能把最后 20 分补上。\n补不上，不是模型不好，是任务不需要它。",
             15, True, NAVY, line=1.45)
    footer(s, page)


def slide_end(prs):
    s = new_slide(prs)
    rect(s, 0, 0, W, H, fill=NAVY)
    add_text(s, ML, 2.55, 11.0, 0.32, "THANK YOU", 11, True, AMBER)
    add_text(s, ML, 2.95, 11.0, 0.85, "讨论与提问", 42, True, WHITE)
    rect(s, ML, 4.02, 2.2, 0.05, fill=AMBER)
    add_text(s, ML, 4.28, 10.5, 0.55,
             "报告全文：单细胞大模型_问题与架构_调研报告（DOCX / PDF，50 页）",
             11.5, False, RGBColor(0xD8, 0xE2, 0xEC))
    add_text(s, ML, 6.55, 10.5, 0.28, "2026 年 10 月 26 日", 9.5, False, RGBColor(0xA9, 0xB8, 0xC9))


# --------------------------------------------------------------------------- build

def slide_adaptation(prs, page):
    s = new_slide(prs)
    header(s, "01  ·  问题 · 适配与评价", "模型怎么用、怎么判：最后一公里")
    cards = [
        ("P11", "适配成本", "预训练要数十张 GPU；微调对种子与超参敏感。许可四分五裂：Apache / MIT / GPL / CC BY-NC-ND / 无 LICENSE。", BLUE, "10% 标注的增益 / 单卡可跑"),
        ("P12", "评测失焦", "MSE 被近零差异基因稀释；benchmark 饱和、排行榜不可比。饱和是“可识别性失败”，不是能力到顶。", BRICK, "预注册 + 盲测 + 复现包"),
    ]
    w = 3.78
    for i, (tag, head, body, color, verdict) in enumerate(cards):
        x = ML + i * (w + 0.22)
        rect(s, x, 1.62, w, 3.20, fill=CARD)
        rect(s, x, 1.62, w, 0.06, fill=color)
        add_text(s, x + 0.18, 1.78, 0.8, 0.24, tag, 9.2, True, color)
        add_text(s, x + 0.18, 2.04, w - 0.36, 0.45, head, 13.2, True, INK)
        add_text(s, x + 0.18, 2.58, w - 0.36, 1.15, body, 9.4, False, GRAY, line=1.4)
        rect(s, x + 0.18, 3.72, w - 0.36, 0.008, fill=LINE)
        add_text(s, x + 0.18, 3.80, 0.6, 0.2, "判据", 7.8, True, AMBER)
        add_text(s, x + 0.60, 3.78, w - 0.76, 0.9, verdict, 8.6, False, RGBColor(0x3D, 0x4B, 0x5C), line=1.3)

    x0 = 9.10
    add_text(s, x0, 1.66, 3.4, 0.28, "一条向下游传导的因果链", 10, True, AMBER)
    chain = [("数据", "6 类问题", NAVY), ("表示", "3 类问题", AMBER), ("目标", "3 类问题", SAGE),
             ("适配", "1 类问题", BLUE), ("评价", "1 类问题", BRICK)]
    y = 2.02
    for i, (name, sub, c) in enumerate(chain):
        rect(s, x0, y, 1.30, 0.56, fill=c)
        add_text(s, x0, y + 0.16, 1.30, 0.26, name, 11, True, WHITE, align=PP_ALIGN.CENTER)
        if i < len(chain) - 1:
            add_text(s, x0 + 0.42, y + 0.58, 0.5, 0.22, "↓", 11, True, LIGHTGRAY, align=PP_ALIGN.CENTER)
        y += 0.82
    add_text(s, x0, 6.18, 3.35, 0.5, "修好一层，代价会以另一种形式出现在下一层。", 9.4, True, RGBColor(0x7A, 0x4E, 0x50), line=1.35)
    footer(s, page)


def build():
    prs = Presentation()
    prs.slide_width = Inches(W)
    prs.slide_height = Inches(H)

    slide_cover(prs)
    slide_map(prs, 2)
    slide_theses(prs, 3)
    slide_problem_overview(prs, 4)

    slide_layer(prs, 5, "01  ·  问题 · 数据层", "模型吃什么：四个问题决定上限", [
        ("P1", "规模幻觉", "语料从 3,000 万涨到 3.9 亿，但下游增益在 1%–10% 数据处就停了。没有可用的数据 scaling law。", NAVY),
        ("P2", "噪声与批次", "零值二义、双细胞、环境 RNA；批次效应与生物效应同量级。ASW 好看，整合可能已经失败。", BLUE),
        ("P3", "数据泄漏", "PBMC 3k 有 80.4%、人胰岛 77.0% 的细胞与预训练语料重叠。唯一没有架构解的问题。", BRICK),
        ("P4", "长尾与偏移", "总体准确率 97.5%，稀有类召回仍系统性失败。HVG 与截断恰好丢掉低表达标记。", AMBER),
    ], "只有 P2 有真正的架构解（显式协变量、噪声建模、集合损失）；其余三个只能靠数据工程与评测制度。",
        ["下游指标 vs token 数曲线", "两组对照 + 噪声注入", "截止日 + 逐细胞指纹", "per-class recall"],
        "模型在拟合测量，而不是拟合生物学。")

    slide_layer(prs, 6, "01  ·  问题 · 表示层", "模型怎么读：三个被低估的设计选择", [
        ("P5", "词表与顺序", "基因没有自然顺序，词表随物种与平台变化。四种解法：位置嵌入、秩、蛋白身份、调控先验。", NAVY),
        ("P6", "值的离散化", "分箱丢幅值、丢序、边界不可迁移。实测排序：soft binning > 连续 ≈ log 分箱 > 硬分箱。", BLUE),
        ("P7", "语境缺失", "解离测序把组织打散成独立细胞，而生物学发生在细胞之间。空间与邻域信息被完全抹掉。", SAGE),
    ], "表示层进步最快：蛋白语言模型让基因身份不再依赖固定词表；软分箱与分布头让表达值不再被硬边界切断。",
        ["能否嵌入未见基因/物种", "跨数据集 + DE 端误差", "去坐标后性能掉多少"],
        "为了兼容词表与语言模型，牺牲了定量信息。")

    slide_layer(prs, 7, "01  ·  问题 · 目标层", "模型学什么：三个错位的奖励函数", [
        ("P8", "重建 ≠ 理解", "掩码重建的最优解是学共表达，不是学调控。注意力权重是路由，不是因果。", NAVY),
        ("P9", "扰动与因果", "Norman 双扰动上，所有模型误差都高于 additive 基线。真实交互仅 4.2%。", BRICK),
        ("P10", "生成与多模态", "全转录组生成要同时建模两万个相关维度与零膨胀；多模态数据少、缺失普遍。", AMBER),
    ], "目标层的问题必须换损失，不能换主干：把 Transformer 换成 Mamba、把 12 层加到 40 层，都不会让模型从“重建”转向“预测干预”。",
        ["与 ChIP/Perturb-seq 重叠", "DES/PDS + 未见扰动", "分布距离 + DE 保真"],
        "奖励函数在奖励复述，而不是奖励干预。")

    slide_adaptation(prs, 8)

    slide_taxonomy(prs, 9)

    class_slide(prs, 10, "02  ·  A 类", "掩码基因序列：看一半，猜一半", [
        ("定义", "基因 token 序列 + 掩码重建；BERT 配方可原样复用。"),
        ("归纳偏置", "共表达即语法：两个基因总一起出现，就能互相推断。"),
        ("结构性代价", "只奖励“重建自己”，不奖励“干预正确”。"),
    ], ["scBERT", "Geneformer", "GeneCompass", "Nicheformer", "UCE", "CellFM", "scPRINT", "RegFormer"],
        NAVY, "注释、检索、基因功能、数据稀缺时的迁移起点", "扰动预测、生成、跨物种定量",
        "A 类的竞争史，就是一部 tokenizer 迭代史。",
        "硬分箱（scBERT）→ 秩（Geneformer）→ 连续（CellFM）→ 软分箱（State）→ 蛋白身份（UCE）→ 分布头（scPRINT）")

    duo_slide(prs, 11, "四类结构，四种代价",
              ("B 类 · 自回归基因序列", "顺着往下写", [
                  ("定义", "p(x)=∏ p(g,c | 前序)；训练信号是似然，不是重建。"),
                  ("能力", "条件生成、计数分布、不确定性。"),
                  ("代表", "scGPT：块状掩码，让“敲除”变成一次前向。\nTranscriptFormer：ZTP 计数头 + 247k 跨物种词表。\nscMulan：元数据即 prompt。"),
                  ("代价", "推理逐 token；基因顺序人为；对分布外过度自信。"),
              ], ["scGPT", "TranscriptFormer", "scMulan"], BLUE,
               "它把“生成”变成可计算的目标，但顺序是人为的。"),
              ("C 类 · 连续谱编解码", "压成向量，再还原", [
                  ("定义", "z=E(x)，x̂=D(z)；显式建模“整谱”。"),
                  ("能力", "去噪、补全、跨平台、跨模态。"),
                  ("代表", "scFoundation：只编码非零位，90% 的零不进注意力。\nCellVQ：细胞压成 2^16 码本整数。\nCAPTAIN：蛋白 query 去读 RNA。"),
                  ("代价", "固定基因数；MSE 被高表达主导。"),
              ], ["scFoundation", "xTrimoGene", "CellVQ", "CAPTAIN"], AMBER,
               "它把“整谱”变成可压缩对象，但基因关系被压进一个向量。"),
              "B 类与 C 类的共同点：都换了损失函数；区别是换似然，还是换重建目标。")

    duo_slide(prs, 12, "另外两类：换建模单元",
              ("D 类 · 细胞集合", "细胞看细胞", [
                  ("定义", "细胞为 token，同一张切片或同一组扰动里的细胞互相注意。"),
                  ("机制", "线性注意力 / 集合编码器 / 下一细胞预测。"),
                  ("代表", "CellPLM：切片内 Flowformer + 16 分量高斯混合。\nState：256 个细胞的集合，MMD/能量距离。\ntGPT：细胞序列当文本。"),
                  ("代价", "基因关系被压平；推理需邻域；集合丢分辨率。"),
              ], ["CellPLM", "State", "tGPT", "Tahoe-x1"], SAGE,
               "它把“语境”带进模型，但丢掉了单基因分辨率。"),
              ("E 类 · 状态分布", "学分布，不学点", [
                  ("定义", "学 p(x_t | x_0, c)：扩散去噪、流匹配速度场、JEPA 隐空间预测。"),
                  ("机制", "不再复述输入，而是建模状态转移。"),
                  ("代表", "Lingshu-Cell：掩码离散扩散 + 条件生成。\nAlphaCell：OT-CFM 在 32×128 隐流形上建模转移。\nCellOS：JEPA 双视角 + 12B MoE。"),
                  ("代价", "采样慢；可解释性弱；评测没跟上。"),
              ], ["Lingshu-Cell", "AlphaCell", "CellOS", "scDifformer"], BRICK,
               "它把“干预”变成分布搬运，但还没学会解释自己。"),
              "D 类与 E 类的共同点：都换了建模单元；区别是建模细胞集合，还是建模状态分布。")

    class_slide(prs, 13, "02  ·  F 类与主干", "语言接口，以及一个正交维度", [
        ("F 类：定义", "把细胞与语言放进同一坐标系：序列化、文本嵌入、对比对齐。"),
        ("F 类：代价", "读得到“是什么”，读不到“多少”。"),
        ("主干：正交维度", "Performer / RetNet / Mamba 只决定“能读多长、多快”。"),
    ], ["Cell2Sentence", "GenePT", "LangCell", "CellWhisperer", "Transformer", "Performer", "RetNet", "Mamba"],
        PLUM, "冷启动、自然语言检索、零样本注释", "扰动预测、剂量响应、精细定量",
        "语言是入口，不是终点。",
        "文本序列化（Cell2Sentence）→ 文本嵌入（GenePT）→ 对比对齐（CellWhisperer / LangCell）")

    models_slide(prs, 14, "03  ·  模型亮点 · A 类", "三个定义了范式的模型", [
        ("scBERT", "2021 · 腾讯 AI Lab", "110 万细胞 · 参数未公开",
         "用 gene2vec 替代位置编码；\nPerformer 把 16,907 长度的注意力降到线性。\n\n首次证明 BERT 可行。",
         "200 维偏窄、词表封闭；\nPBMC 上不敌逻辑回归。",
         "历史意义 > 实用价值"),
        ("Geneformer", "2022 · Gladstone", "2,990 万细胞 · 10M 参数",
         "秩编码：除中位表达再排序，把管家基因压后、转录因子顶前。\n\n10M 参数，单卡可跑。",
         "丢绝对幅值；dropout 让整条排名平移；截断丢尾部。",
         "第一个证明“迁移学习有效”"),
        ("GeneCompass", "2024 · 中科院", "1.02 亿细胞 · >100M 参数",
         "四类先验拼成 3,841 维再投影：GRN、启动子、基因家族、共表达。\n\n人鼠同源映射 + 物种 token。",
         "首层参数大；先验质量决定上限；仓库无 LICENSE。",
         "少数做了湿实验闭环的模型"),
    ], NAVY)

    models_slide(prs, 15, "03  ·  模型亮点 · B/C 类", "三个把“生成”做进架构的模型", [
        ("scGPT", "2023 · 多伦多/Vector", "1,030 万细胞 · 53M 参数",
         "块状掩码：待预测基因只能看已知基因。\n\n于是“敲除”= 把该基因设为未知，一次前向完成。",
         "每细胞分箱边界漂移；1,200 HVG 限制覆盖；零样本不敌基线。",
         "生态最完整的模型之一"),
        ("TranscriptFormer", "2025 · CZI", "1.12 亿 / 12 物种 · 444M",
         "基因 softmax + 零截断泊松；计数以 log1p 进入注意力分数。\n\n12 物种、247,388 词表、ESM-2 蛋白身份。",
         "输出头很宽；自回归推理慢；随机排列需靠打乱训练。",
         "生成式 + 跨物种结合得最好"),
        ("scFoundation", "2023 · 清华/百图", "5,000 万细胞 · 100M 参数",
         "非对称编解码：只编码非零位（约 10%），解码全谱。\n\nT/S 深度 token + 软分箱 + 30% 掩码 MSE。",
         "固定 19,264 基因；MSE 被高表达主导；scaling 只在 loss 上成立。",
         "最务实的稀疏设计"),
    ], AMBER)

    models_slide(prs, 16, "03  ·  模型亮点 · 四类极致", "四个在不同维度上做到极致的模型", [
        ("UCE", "2023 · Stanford", "3,600 万 / 8 物种 · 650M",
         "没有基因词表：ESM-2 蛋白嵌入即身份。\n\n按表达加权抽 1,024 基因，零样本嵌入未见物种。",
         "抽样随机；嵌入表巨大；二分类目标丢幅值。",
         "通用坐标系的最佳代表"),
        ("CellFM", "2025 · 中山大学/华为", "1.02 亿细胞 · 800M 参数",
         "8 亿参数、40 层 ERetNet、2,048 基因、连续标量。\n\nMindSpore + 32 张昇腾 910。",
         "单物种；参数与下游增益未解耦；许可为 Other。",
         "国产算力栈的可行性证明"),
        ("State", "2025 · Arc Institute", "1.67 亿 + 1 亿扰动细胞",
         "不预测单个细胞，预测 256 个细胞的集合分布。\n\nSE 学表征、ST 学变换，MMD/能量距离做损失。",
         "非商用；集合丢单细胞分辨率；依赖扰动数据。",
         "第一个把分布损失做成主流"),
        ("CellPLM", "2024 · ICLR", "1,140 万细胞 · 82.4M",
         "细胞为 token：切片内细胞互相注意。\n\n16 分量高斯混合；批次标签只进解码器。",
         "基因关系被压平；推理需邻域；位置编码实现有落差。",
         "冻结嵌入 + 轻量头的首选"),
    ], SAGE)

    models_slide(prs, 17, "03  ·  模型亮点 · 2026", "五个正在改写规则的模型", [
        ("Lingshu-Cell", "阿里达摩院", "约 18,000 基因 · 未公开",
         "把转录组当离散分布去噪：掩码离散扩散，按条件生成。",
         "采样慢；预印本。", "最彻底“换目标函数”"),
        ("AlphaCell", "同济 DELTA", "19,253 基因 · 1.2B 解码器",
         "全基因输入 → 32×128 隐流形 → OT-CFM 建模状态转移。",
         "解码器巨大；可解释性弱。", "连续时间生成路线"),
        ("CellOS", "百曜科技", "3.905 亿细胞 · 12B MoE",
         "JEPA 双视角联合嵌入预测，不复述输入。",
         "厂商口径；未开源。", "值得关注思路，不是数字"),
        ("CAPTAIN", "湖南大学等", "426 万 CITE-seq · 382 蛋白",
         "蛋白 token 作 query、RNA 作 key/value。",
         "面板窄；物种写死为 2。", "CITE-seq 规模化的第一步"),
        ("RegFormer", "华大研究院", "2,500 万细胞 · 45 组织",
         "GRN 引导基因排序 + Mamba。",
         "单物种；复现少。", "先验结构化的最新形态"),
    ], BRICK)

    s = new_slide(prs)
    header(s, "04  ·  交叉矩阵", "哪一类真正回应了哪个问题")
    picture_fit(s, "figs/fig4_coverage.png", ML, 1.56, 8.55, 5.05)
    x = ML + 8.75
    w = W - ML - x
    add_multi(s, x, 1.72, w, 4.8, [
        dict(text="两个立刻可见的结论", size=11, bold=True, color=NAVY, space_after=8),
        dict(text="P3 整行为空：数据泄漏没有架构解，只能靠时间切分与审计。", size=9.6, color=GRAY, space_before=2),
        dict(text="P11 几乎每列都有点：适配是工程问题，所有类都能用冻结、LoRA、小模型缓解。", size=9.6, color=GRAY, space_before=8),
        dict(text="目标层的问题（P8–P10）集中在 D/E 类，因为只有它们换了损失函数。", size=9.6, color=GRAY, space_before=8),
        dict(text="空白不等于无关，而是“没有结构性优势”。", size=9.6, bold=True, color=AMBER, space_before=10),
    ])
    footer(s, 18)

    slide_reality(prs, 19)

    s = new_slide(prs)
    header(s, "04  ·  选型", "从任务出发，而不是从模型出发")
    picture_fit(s, "figs/fig5_decision.png", ML, 1.56, 8.55, 5.05)
    x = ML + 8.75
    w = W - ML - x
    add_multi(s, x, 1.72, w, 4.9, [
        dict(text="三条通用规则", size=11, bold=True, color=NAVY, space_after=8),
        dict(text="① 先跑强基线：HVG / Harmony / scVI / 逻辑回归 / additive。", size=9.6, color=GRAY),
        dict(text="② 零样本与微调分开报告。", size=9.6, color=GRAY, space_before=8),
        dict(text="③ 扰动任务必须报告 DES/PDS，而不是 MSE。", size=9.6, color=GRAY, space_before=8),
        dict(text="用法不是“照着选”，而是“先排除”：先判断任务落在哪一层，再排除结构性代价不可接受的大类。", size=9.6, bold=True, color=AMBER, space_before=12),
    ])
    footer(s, 20)

    slide_theses5(prs, 21)
    slide_advice(prs, 22)
    slide_end(prs)

    out = "单细胞大模型_问题与架构_汇报.pptx"
    prs.save(out)
    return out


if __name__ == "__main__":
    print(build())
