# -*- coding: utf-8 -*-
"""Chapter 5-7, appendices and sources."""


def chapter5(b):
    b.h1("第 5 章", "交叉矩阵：哪类架构回应了哪个问题")
    b.lead("把第二章的十二个问题与第三章的六个大类放进同一张表，会看到一条清晰的边界：越靠近数据层，架构越无能为力；越靠近目标层，换损失比换主干更有效。")

    b.h2("5.1", "覆盖矩阵怎么读")
    b.body("图 5 的每一行是一个问题，每一列是一个架构大类。圆点越大，表示该类的核心设计越直接地针对该问题；空白表示该类在这个问题上没有结构性优势，而不是“完全没提”。判定依据是各模型公开的机制与评测，不是论文里的自述。")
    b.figure("figs/fig4_coverage.png", "问题 × 架构覆盖矩阵（作者依据机制与公开评测判定）",
             note="空白不等于无关：例如 A 类也会报告批次整合指标，但它的结构里没有专门处理批次的机制。矩阵衡量的是“结构性回应”，不是“是否提及”。")
    b.body("两个立刻可见的结论。第一，**P3（数据泄漏）整行为空**——没有任何架构能解决它，只能靠数据审计与时间切分。第二，**P11（适配成本）几乎每列都有点**——因为适配是工程问题，所有类都可以通过冻结、LoRA、小模型来缓解，区别只在程度。")

    b.h2("5.2", "五条规律")
    b.kv([
        ("规律一：越靠近数据层，架构越无能为力。",
         "P1、P2、P3、P4 四个问题里，只有 P2 有真正的架构解（显式协变量、噪声建模、集合损失），其余三个只能靠数据工程与评测制度。把希望寄托在“更大的模型”上，是这类问题最常见的误配。"),
        ("规律二：表示层的问题，被“词表无关 + 软编码”缓解得最好。",
         "P5 与 P6 是过去两年进步最快的两个问题。蛋白语言模型让基因身份不再依赖固定词表；软分箱与分布头让表达值不再被硬边界切断。这两项改进的成本都不高，收益却跨任务可见。"),
        ("规律三：目标层的问题，必须换损失，不能换主干。",
         "P8、P9、P10 三个问题的共同点是“奖励函数错了”。把 Transformer 换成 Mamba、把 12 层加到 40 层，都不会让模型从“重建”转向“预测干预”。State 的集合损失、AlphaCell 的流匹配、Lingshu 的条件扩散，都是从损失入手。"),
        ("规律四：D 类与 E 类在扰动上领先，代价是分辨率与可解释性。",
         "集合/分布级模型天然适合“扰动后这群细胞往哪走”，但不回答“某一个细胞会怎样”；扩散/流匹配模型能给出分布，却很难解释“为什么这个基因变了”。这不是实现缺陷，是建模单元决定的。"),
        ("规律五：F 类在检索、注释、冷启动上最强，在定量任务上最弱。",
         "语言接口把“细胞是什么”变成了可查询的语义，但它读不到“多少”。用 CellWhisperer 做注释、做检索、做解释是合适的；用它做扰动预测或剂量响应，是用错了工具。"),
    ])

    b.h2("5.3", "四种反模式")
    b.body("**反模式一：用 zero-shot 分数选型。** 零样本成绩既受预训练污染影响，也与下游分布强相关；同一模型在不同数据集上的排名可以翻转。正确做法是用自己的 10% 标注做微调，再比。")
    b.body("**反模式二：用 MSE 选扰动模型。** MSE 被近零差异基因稀释，一个“预测无变化”的模型也能拿到不错的分。必须看 DES/PDS 与 DE 基因重叠。")
    b.body("**反模式三：用大模型做小任务。** 注释一个 5 万细胞的数据集，逻辑回归 + 标记基因往往够用；上 8 亿参数模型，收益可能小于调参成本。")
    b.body("**反模式四：忽略许可。** 代码许可、权重许可、论文许可、数据许可四者可能不一致；CC BY-NC-ND 不能商用，无 LICENSE 默认保留所有权利，GPL-3.0 可能传染整个软件栈。这是尽职调查项，不是法务细节。")

    b.h2("5.4", "从任务出发的选型路径")
    b.body("图 6 给出一个从任务出发的路径。它的用法不是“照着选”，而是“先排除”：先判断任务落在哪一层，再排除结构性代价不可接受的大类，最后才在剩下的类里挑模型。")
    b.figure("figs/fig5_decision.png", "任务 → 架构大类 → 代表模型的选型路径")
    b.table(
        "选型矩阵：任务、首选类、代表模型与必跑基线",
        ["任务", "首选类", "代表模型", "必跑基线", "验收指标"],
        [
            ["细胞类型注释", "A / D", "CellFM、Geneformer、CellPLM", "CellTypist、逻辑回归、Seurat", "macro-F1、per-class recall"],
            ["批次整合", "A（辅以显式协变量）", "scGPT、Geneformer", "Harmony、scVI", "iLISI + 生物保守性"],
            ["跨物种 / 跨平台", "A（无词表）", "UCE、TranscriptFormer", "HVG + Harmony", "未见物种/平台的嵌入一致性"],
            ["扰动 / 虚拟细胞", "D / E", "State、Lingshu-Cell、AlphaCell", "additive、无变化、GEARS", "DES、PDS、MAE（分见/未见）"],
            ["药物响应", "C / D", "scFoundation、State", "线性回归、scDrugMap 基线", "跨细胞系 AUROC、校准"],
            ["生成 / 补全", "B / C / E", "scMulan、scFoundation、CAPTAIN", "均值填充、kNN", "分布距离、DE 保真、分位数覆盖"],
            ["空间转录组", "D（空间变体）", "Nicheformer、CellPLM", "Novae、scGPT-spatial", "邻域一致性、空间标签"],
            ["GRN / 可解释", "A（先验或分布头）", "scPRINT、RegFormer、GeneCompass", "GENIE3、SCENIC", "ChIP/Perturb-seq 重叠"],
        ],
        widths=[3.0, 3.2, 4.6, 3.4, 2.0],
        font=7.9,
        note="“必跑基线”不是可选项。多项评测显示，基线跑不过时，换更大的模型通常也不会赢。",
    )


def chapter6(b):
    b.h1("第 6 章", "现实检验：哪些结论站得住")
    b.lead("这一章只做一件事：把“模型方自述”与“独立评测”分开，看哪些结论在多次复现后仍然成立。")

    b.h2("6.1", "独立评测的证据总表")
    b.body("下表只收录有明确实验设计、可查数字的评测。它们的共同点是：都跑了强基线，都报告了失败案例，且多数在多个数据集上重复。")
    b.table(
        "十三项独立评测的核心结论",
        ["研究", "规模", "核心结论"],
        [
            ["scEval（Adv Sci 2026）", "8 类任务 × 10 个 scFM", "scGPT、Geneformer、CellFM 居前，但没有任何模型在所有任务上稳定优于任务专用方法"],
            ["Kedzierska 等（Genome Biol 2025）", "5 数据集零样本", "Geneformer ASW 仅 0.38–0.52，HVG 基线除 PBMC 外全部胜出；scGPT 中位 ASW 0.53 ≈ scVI 0.54；批次整合不合格"],
            ["Boiarsky 等（Nat Mach Intell 2024）", "PBMC 68,450 细胞", "L1 逻辑回归在 accuracy 与 macro-F1 上均胜 scBERT；scBERT 去预训练无显著差异（p=0.34/0.59）"],
            ["Ahlmann-Eltze 等（Nat Methods 2025）", "Norman 双扰动", "所有被测模型误差均高于 additive 基线；交互预测无一优于“无变化”；真实交互仅 4.2%"],
            ["PertEval-scFM（ICML 2025）", "标准化扰动评测", "零样本 scFM 嵌入对简单基线提升有限，分布偏移下尤甚"],
            ["Wu 等（Genome Biol 2025）", "6 个 scFM × 12 指标", "没有单一 scFM 全面领先；资源受限时简单模型更易适配"],
            ["低监督评测（2026）", "7 个 FM × 3 个经典表示", "CellPLM 聚类/注释/批次最好，scMulan 扰动最好，PCA 重建最好；仅 1/7 在聚类上超过最强基线"],
            ["SCMBench（Nat Commun 2026）", "23 种多组学整合方法", "基础模型在多组学整合上不如领域专用模型"],
            ["scDrugMap（Nat Commun 2025）", "8 个 FM + 2 个 LLM", "合并数据 scFoundation 最强，跨数据微调 UCE 最好，零样本 scGPT 最高"],
            ["污染审计（arXiv 2026）", "MinHash 逐细胞比对", "PBMC 3k 80.4%、人胰岛 77.0% 与 Genecorpus-30M 重叠；截止日后数据集 0%"],
            ["稀有类研究（arXiv 2026）", "162 次受控训练", "总体准确率 97.5%，稀有类召回系统性失败，且由数据结构而非预训练决定"],
            ["VCC 2025（Arc）", "300+ 队伍", "扰动模型未在所有指标上稳定超过朴素基线；冠军方案是深度学习 + 统计特征混合"],
            ["饱和立场论文（ICML 2026）", "立场论文", "benchmark 饱和是可识别性失败，不是能力到顶"],
        ],
        widths=[4.4, 3.6, 8.2],
        font=7.7,
    )

    b.h2("6.2", "仍然成立的四条优势")
    b.body("在大量负面证据里，有四条优势被反复确认，值得作为选型的正面依据。")
    b.kv([
        ("① 微调后的分布外泛化。",
         "scGPT 在多发性硬化数据上优于逻辑回归，且训练样本越少优势越大；scFoundation 在多个任务上稳定靠前；Steiner 等在三个任务上发现，用 OOD 数据微调后仍可泛化。"),
        ("② 嵌入作为特征有效。",
         "scGPT/scFoundation 的基因嵌入加线性解码，优于均值基线与随机嵌入；虽然不优于“用训练数据学到的嵌入”，但在标注稀缺时是实用的初始化。"),
        ("③ 预训练确有贡献。",
         "预训练模型普遍优于随机初始化；scGPT 去掉预训练会显著变差。这与“零样本不强”并不矛盾——预训练的价值体现在微调起点，而不是开箱即用。"),
        ("④ 数据域匹配优于规模。",
         "用 Replogle 扰动数据预训练的线性模型，稳定优于通用大模型。这条最反直觉，也最重要：模型的“见过同类数据”比“参数更多”更能决定下游表现。"),
    ])

    b.h2("6.3", "三个还没有被证明的承诺")
    b.body("第一，**零样本通用性**。跨数据集、跨平台、跨物种的零样本嵌入，在受控评测中很少稳定超过强基线。UCE 与 TranscriptFormer 是例外，但它们的优势集中在“把不同来源放进同一坐标系”，而不是“替代专用工具”。")
    b.body("第二，**跨数据集稳健性**。同一模型在不同数据集上的排名会翻转；预处理、tokenization、指标的选择都能改变结论。这意味着“论文里的 SOTA”不能直接迁移到你的数据。")
    b.body("第三，**稀有类可靠性**。总体指标好看与稀有类可用是两件事。稀有类失败主要由数据结构决定，换损失函数、换主干都难以根治。")

    b.h2("6.4", "一张八问验收清单")
    b.table(
        "评估一个 scFM 是否适合你的任务",
        ["问题", "为什么要问", "不合格的信号"],
        [
            ["1. 任务是哪一层？", "注释/整合/扰动/生成的最优类完全不同", "用同一个模型打所有任务"],
            ["2. 强基线跑了吗？", "HVG、Harmony、scVI、逻辑回归、additive", "只与随机初始化比"],
            ["3. 测试集在预训练里吗？", "泄漏会系统性抬高零样本", "无截止日、无语料清单"],
            ["4. 零样本还是微调？", "两者结论经常相反", "把微调成绩说成零样本"],
            ["5. 指标对生物学有意义吗？", "MSE 会被近零差异稀释", "只报 MSE/Pearson"],
            ["6. 稀有类表现如何？", "总体准确率会掩盖长尾失败", "只报 accuracy"],
            ["7. 许可允许商用吗？", "代码/权重/论文/数据许可可能不一致", "CC BY-NC-ND 或无机 LICENSE"],
            ["8. 能复现吗？", "种子、超参、算力、失败案例", "无代码、无种子、无失败分析"],
        ],
        widths=[4.2, 6.6, 5.4],
        font=8.0,
    )


def chapter7(b):
    b.h1("第 7 章", "判断与建议")
    b.lead("下面五条判断不是预测“哪个模型会赢”，而是判断“哪些条件一旦成立，格局会变”。每条都给出可观察的信号。")

    b.h2("7.1", "五条判断（2026–2028）")
    b.kv([
        ("判断一：观测数据接近饱和，扰动数据决定上限。",
         "公开 atlas 已达亿级，继续堆观测数据的边际收益在下降；真正稀缺的是同一细胞类型、同一平台、带对照的扰动数据。可观察信号：扰动数据成本是否降到“每细胞美分”；是否出现跨实验室的扰动数据标准；药企是否愿意用内部 Perturb-seq 换模型。"),
        ("判断二：目标函数从“重建”转向“分布/转移”，集合级损失会成为标配。",
         "State 的 MMD、AlphaCell 的 flow、Lingshu 的条件扩散、CellOS 的 JEPA，都在做同一件事。可观察信号：新论文是否默认报告分布指标；是否出现统一的“状态转移”基准；逐细胞 MSE 是否被审稿人要求替换。"),
        ("判断三：词表无关的基因身份会成为默认。",
         "蛋白语言模型让新基因、新物种、新 panel 不再需要重训词表。可观察信号：新模型是否还依赖固定基因词表；跨物种评测是否成为常规项；ESM-2 类嵌入是否成为标准组件。"),
        ("判断四：通用底座 + 领域适配器，不会有一个主干通吃。",
         "通用表征（UCE、TranscriptFormer、SCimilarity）+ 生成/模拟器（State、Lingshu、AlphaCell）+ 领域适配器（LoRA、蒸馏）+ 文本接口（CellWhisperer），四层分工。可观察信号：是否出现模型卡与适配器市场；是否出现跨模型的统一 tokenization。"),
        ("判断五：评测从排行榜转向“能否替代一次实验”。",
         "VCC 已经把任务定义成“能否替代一次 Perturb-seq”，Cell_Eval 用七项指标覆盖 DES/PDS。可观察信号：VCC 是否成为年度惯例；期刊是否要求提交基准报告；是否出现第三方审计。"),
    ])

    b.h2("7.2", "给研究团队：三条值得走的路")
    b.body("**路线一：做数据，而不是做模型。** 高质量扰动数据的生产成本、元数据标准化、跨实验室去重，是当前最硬的瓶颈，也是最难被追平的壁垒。一个 1,000 万细胞的干净扰动数据集，价值高于一个 10 亿参数的模型。")
    b.body("**路线二：做目标，而不是做主干。** 分布级损失、因果识别、可识别性约束，是 P8–P10 的真正解法。把 Mamba 换成 RetNet 不会让模型更懂干预；把 MSE 换成集合距离或流匹配会。")
    b.body("**路线三：做评测，而不是做榜单。** 时间切分、逐细胞审计、任务化指标、失败案例披露——这些工作不产生引用，但决定了整个领域的判断力。")
    b.body("**不建议**：再训一个同质的大模型。除非你有别人没有的数据，或者别人没有的算力栈，否则在 2026 年做“更大的 scGPT”是边际收益最低的选择。")

    b.h2("7.3", "给选型者：三张表")
    b.body("第一张是第 5 章的选型矩阵：先确定任务落在哪一层，再选类。第二张是代价表（第 3 章的六类天花板）：确认你能接受该类丢掉的东西——分辨率、可解释性、定量精度，还是跨物种能力。第三张是第 6 章的八问清单：八问全部过关，才进入试点。")
    b.body("如果只有一句话：**先用强基线把任务做到 80 分，再问 scFM 能不能把最后 20 分补上**。补不上，不是模型不好，是任务不需要它。")

    b.h2("7.4", "五个开放问题")
    b.bullets([
        "**没有干预数据，能否学因果？** 目前的答案是“只能学到相关的近似”。工具变量、孟德尔随机化、跨物种保守性，都是可能的突破口。",
        "**“细胞状态”的度量是什么？** 现在的嵌入空间由模型定义，换一个模型就换一个坐标系。需要一个与模型无关、可跨数据集比较的状态度量。",
        "**全基因与 HVG 的信息论权衡是什么？** 全基因覆盖稀有标记，但计算与噪声成本高；HVG 高效，但会丢信号。这个权衡目前只有经验，没有理论。",
        "**生成模型的可识别性如何保证？** 扩散/流匹配可以生成“像”的细胞，但无法保证学到的是真实的因果机制。可识别性是生成式虚拟细胞的核心难题。",
        "**跨物种的“同源”到什么粒度？** 基因同源不等于细胞类型同源，更不等于调控网络同源。跨物种迁移的理论边界仍未厘清。",
    ])


def appendix(b):
    b.h1("附 录", "术语、资源与来源")

    b.h2("A", "术语表")
    b.table(
        "本报告使用的核心术语",
        ["术语", "英文 / 缩写", "含义"],
        [
            ["单细胞基础模型", "scFM", "在千万到亿级单细胞数据上自监督预训练、可迁移到多任务的模型"],
            ["标记基因", "marker gene", "在特定细胞类型中高表达、可用于注释的基因"],
            ["高变基因", "HVG", "在细胞间方差大的基因，常用于降维与建模"],
            ["零膨胀", "zero-inflation", "scRNA-seq 中大量零值，既可能是不表达，也可能是未检出"],
            ["双细胞", "doublet", "两个细胞被同一液滴捕获，形成混合表达谱"],
            ["环境 RNA", "ambient RNA", "裂解细胞释放、污染其他液滴的游离 RNA"],
            ["批次效应", "batch effect", "由实验批次、平台、操作者引起的系统性技术差异"],
            ["掩码建模", "masked modeling", "遮住部分输入、让模型预测被遮部分的自监督目标"],
            ["秩编码", "rank value encoding", "按表达量排序、以名次作为 token 的编码方式"],
            ["软分箱", "soft binning", "把连续值映射为多个 bin 的权重，而非硬指派"],
            ["零膨胀负二项", "ZINB", "同时建模过零与计数的概率分布，输出 μ、θ、π"],
            ["零截断泊松", "ZTP", "在正值上归一化的泊松分布，用于计数生成"],
            ["集合距离", "MMD / energy distance", "衡量两个细胞集合分布差异的指标"],
            ["流匹配", "flow matching", "学习从噪声到数据的连续时间速度场"],
            ["联合嵌入预测", "JEPA", "在隐空间预测另一视角的表示，而非重建输入"],
            ["专家混合", "MoE", "多个专家网络 + 门控，稀疏激活以扩大容量"],
            ["差异表达签名", "DES", "扰动后显著变化的基因集合"],
            ["扰动区分度", "PDS", "模型区分不同扰动的能力指标"],
            ["双 dipping", "double dipping", "同一批数据既用于预训练又用于评测"],
            ["可识别性", "identifiability", "模型能否从数据中唯一确定目标机制"],
        ],
        widths=[3.6, 4.0, 8.6],
        font=7.9,
    )

    b.h2("B", "可复现资源")
    b.table(
        "主要模型的代码与权重入口",
        ["模型", "仓库 / 入口", "许可", "备注"],
        [
            ["scBERT", "github.com/TencentAILabHealthcare/scBERT", "GPL-3.0", "2023 年底后基本停更"],
            ["Geneformer", "huggingface.co/ctheodoris/Geneformer", "版本不一", "V1 10M / V2 106M"],
            ["scGPT", "github.com/bowang-lab/scGPT", "MIT", "教程与微调 recipe 完整"],
            ["scFoundation", "github.com/biomap-research/scFoundation", "Apache-2.0", "含 API"],
            ["UCE", "github.com/snap-stanford/UCE", "MIT", "需 ESM-2 嵌入表"],
            ["CellFM", "github.com/biomed-AI/CellFM", "Other", "MindSpore"],
            ["GeneCompass", "github.com/xCompass-AI/GeneCompass", "无 LICENSE", "商用需谨慎"],
            ["CellPLM", "github.com/OmicsML/CellPLM", "BSD-2", "ICLR 2024"],
            ["Nicheformer", "github.com/theislab/nicheformer", "BSD-3", "空间 + 解离"],
            ["State", "github.com/ArcInstitute/state", "CC BY-NC-SA", "非商用"],
            ["TranscriptFormer", "github.com/czi-ai/transcriptformer", "MIT", "12 物种"],
            ["scPRINT", "github.com/cantinilab/scPRINT", "GPL-3.0", "含 GRN 基准"],
        ],
        widths=[2.8, 7.6, 2.6, 3.2],
        font=7.8,
    )

    b.h2("C", "主要来源")
    b.body("以下按主题分组。模型类条目给出论文或预印本标识；评测类条目给出期刊与 DOI；厂商口径的条目单独标注。信息截至 2026 年 10 月。")
    b.callout("引用说明", "标注“Anonymous”的条目为预印本阶段、作者名单尚未最终确认的工作，引用时请以正式发表版本为准；标注“厂商口径”的数字未经独立复现，不应作为选型依据。")
    b.h3("", "模型原文")
    refs_models = [
        "Yang F, et al. scBERT as a large-scale pretrained deep language model for cell type annotation of single-cell RNA-seq data. Nature Machine Intelligence, 2022. doi:10.1038/s42256-022-00534-z",
        "Theodoris CV, et al. Transfer learning enables predictions in network biology. Nature, 2023. doi:10.1038/s41586-023-06139-9",
        "Cui H, et al. scGPT: toward building a foundation model for single-cell multi-omics using generative AI. Nature Methods, 2024. doi:10.1038/s41592-024-02201-0",
        "Hao M, et al. Large-scale foundation model on single-cell transcriptomics. Nature Methods, 2024. doi:10.1038/s41592-024-02305-7",
        "Rosen Y, et al. Universal Cell Embeddings: a foundation model for cell biology. bioRxiv, 2023. doi:10.1101/2023.11.28.568809；期刊版 Nature, 2026.",
        "Yang X, et al. GeneCompass: deciphering universal gene regulatory mechanisms with a knowledge-informed cross-species foundation model. Cell Research, 2024. doi:10.1038/s41422-024-01034-y",
        "Schäfer P, et al. Nicheformer: a foundation model for single-cell and spatial omics. Nature Methods, 2025. doi:10.1038/s41592-025-02814-z",
        "Kalfon J, et al. scPRINT: pretraining on 50 million cells allows robust gene network predictions. Nature Communications, 2025. doi:10.1038/s41467-025-58699-1",
        "Kalfon J, et al. scPRINT-2: a 350-million-cell foundation model across 16 species. bioRxiv, 2025. doi:10.64898/2025.12.11.693702",
        "Wu H, et al. CellFM: a large-scale foundation model pre-trained on 100 million human single-cell transcriptomes. Nature Communications, 2025. doi:10.1038/s41467-025-59926-5",
        "Chen J, et al. TranscriptFormer: a generative foundation model for cross-species transcriptomics. Science, 2026；预印本 CZI, 2025.",
        "Arc Institute. State: a model of cellular state transition. Cell, 2026；预印本 2025.",
        "Wen H, et al. CellPLM: pre-training of cell language model beyond single cells. ICLR, 2024. doi:10.1101/2023.10.03.560734",
        "Bian H, et al. scMulan: a multitask generative pre-trained language model for single-cell biology. bioRxiv, 2024. doi:10.1101/2024.01.25.577152",
        "Anonymous. CAPTAIN: a multimodal foundation model for RNA and surface proteins. Nature Communications, 2026. doi:10.1038/s41467-026-72882-y",
        "Fang S, et al. RegFormer: a single-cell foundation model powered by gene regulatory hierarchies. Nature Communications, 2026. doi:10.1038/s41467-026-72198-x",
        "Anonymous. CellVQ: vector-quantized cell language model. Nature Communications, 2026. doi:10.1038/s41467-026-70071-5",
        "Anonymous. CellWhisperer: a multimodal foundation model for cell biology. Nature Biotechnology, 2025. doi:10.1038/s41587-025-02857-9",
        "Levine L, et al. Cell2Sentence: teaching large language models the language of biology. bioRxiv, 2023. doi:10.1101/2023.09.11.557287",
        "Chen Y, Zou J. GenePT: a simple but hard-to-beat foundation model for gene-level tasks. NeurIPS, 2023. PMC10614824.",
        "Anonymous. LangCell: language-cell pre-training for cell identity. arXiv:2405.06708, 2024.",
        "Heinlein L, et al. Universal cell embeddings enable cross-study cell retrieval. Nature, 2024.",
        "Shen H, et al. tGPT: generative pretrained transformer for single-cell transcriptomics. iScience, 2023.",
        "Anonymous. xTrimoGene: an efficient and scalable representation learner for single-cell RNA-seq. NeurIPS, 2023. arXiv:2311.15156.",
        "Anonymous. scDifformer: diffusion post-training for single-cell foundation models. Nucleic Acids Research, 2026. doi:10.1093/nar/gkag706",
        "阿里达摩院. Lingshu-Cell: masked discrete diffusion for transcriptome generation. 技术报告, 2026-08.",
        "同济大学 DELTA Lab. AlphaCell: a world model for cellular state transition. 预印本, 2026-03.",
        "百曜科技. CellOS: a 12B MoE foundation model for virtual cell. 技术报告, 2026-07（厂商口径）.",
    ]
    for i, r in enumerate(refs_models, 1):
        b.ref(i, r)

    b.h3("", "评测、批评与方法")
    refs_eval = [
        "Liu T, et al. Evaluating the utilities of foundation models in single-cell data analysis. Advanced Science, 2026. doi:10.1002/advs.202514490",
        "Kedzierska KZ, et al. Zero-shot evaluation reveals limitations of single-cell foundation models. Genome Biology, 2025. doi:10.1186/s13059-025-03574-x",
        "Boiarsky R, et al. Deeper evaluation of a single-cell foundation model. Nature Machine Intelligence, 2024. doi:10.1038/s42256-024-00949-w",
        "Ahlmann-Eltze C, Huber W, Anders S. Deep-learning-based gene perturbation effect prediction does not yet outperform simple linear baselines. Nature Methods, 2025. doi:10.1038/s41592-025-02772-6",
        "Wenteler A, et al. PertEval-scFM: benchmarking single-cell foundation models for perturbation effect prediction. ICML, 2025. PMLR 267:66633–66677.",
        "Wu J, et al. Biology-driven insights into the power of single-cell foundation models. Genome Biology, 2025. doi:10.1186/s13059-025-03781-6",
        "Ali S. Auditing pretraining contamination in single-cell foundation model benchmarks. arXiv:2607.20572, 2026.",
        "Dong Z, Zhong J. Rethinking class imbalance for single-cell foundation models. arXiv:2609.23325, 2026.",
        "Steiner N, et al. A systematic evaluation of single-cell foundation models on cell-type classification. WSDM, 2025. doi:10.1145/3701551.3708811",
        "Anonymous. SCMBench: a comprehensive benchmark for single-cell multi-omics integration. Nature Communications, 2026. doi:10.1038/s41467-026-72570-x",
        "Anonymous. scDrugMap: benchmarking foundation models for drug response prediction. Nature Communications, 2025. doi:10.1038/s41467-025-67481-2",
        "Arc Institute. Virtual Cell Challenge 2025: results and lessons. 2025. arcinstitute.org/news/virtual-cell-challenge-2025-wrap-up",
        "Anonymous. Position: saturation in single-cell foundation model benchmarks signals identifiability failure, not solved capability. ICML, 2026.",
        "Bunne C, et al. How to build the virtual cell with artificial intelligence. Cell, 2024. doi:10.1016/j.cell.2024.11.015",
        "Lopez R, et al. Deep generative modeling for single-cell transcriptomics. Nature Methods, 2018. doi:10.1038/s41592-018-0229-2",
        "Choromanski K, et al. Rethinking attention with Performers. ICLR, 2021. arXiv:2009.14794.",
        "Anonymous. HEIMDALL: modular decomposition of single-cell tokenizers. 2026.",
        "Anonymous. A large-scale controlled study of expression value encoding in single-cell foundation models. 2026.",
    ]
    for i, r in enumerate(refs_eval, len(refs_models) + 1):
        b.ref(i, r)
