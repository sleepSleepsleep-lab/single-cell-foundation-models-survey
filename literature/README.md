# AI + 生物重要论文：32 篇清单

这是另一条线的调研，时间在 2026-10 中旬，比单细胞那份早几天。当时的动机很简单：单细胞基础模型的很多设计其实是照着蛋白质和基因组那边的做法搬过来的（掩码建模、词表、位置编码），不先把上游读一遍，评价容易被论文自己的叙事带走。

## 里面有什么

| 文件 | 说明 |
|---|---|
| `papers.csv` | 32 篇的元数据：主题、年份、一作、题名、发表处、DOI、引用量、OA 状态、页数 |
| `AI+生物_重要论文调研报告.html` | 主报告：筛选标准、领域地图、32 张卡片、版本说明、精读路线 |
| `AI+生物_重要论文调研报告.pdf` | 同上的打印版 |

## 七个主题

| 主题 | 篇数 | 代表工作 |
|---|---|---|
| 蛋白质结构与生成 | 6 | AlphaFold3、RFdiffusion、Chroma、RoseTTAFold All-Atom、ESM3、Boltz-2 |
| 基因组与调控 | 5 | Enformer、Borzoi、AlphaGenome、Evo、Nucleotide Transformer |
| 单细胞与转录组 | 6 | Geneformer、scGPT、scFoundation、UCE、State、CellFM |
| 空间与病理影像 | 4 | UNI、CONCH、Prov-GigaPath、RETFound |
| 药物发现与分子生成 | 3 | Antibiotic discovery、TamGen、DiffDock |
| 生物医学大模型与 Agent | 4 | BioGPT、Med-PaLM 2、Biomni、CellWhisperer |
| 虚拟细胞与总览 | 4 | AIVC、Tahoe-100M、TranscriptFormer、SciPhi |

## 筛选标准

时间上以 2023-01 到 2026-10 为主，破例留了三篇奠基性工作（Enformer 2021、BioGPT 2022、DiffDock 2022/ICLR 2023）。来源以 Nature / Science / Cell 及子刊、ICLR / NeurIPS / ICML 和高影响力预印本为主，影响力看 OpenAlex 引用量加引用速度。每个子领域留 3–6 篇，同一模型家族只保留最有代表性的一篇。

## 为什么没有 PDF

32 篇全文（395 MB）在本地存着，没有放进仓库。其中 16 篇是出版社或机构库的原版，另外 16 篇是 bioRxiv 预印本、PMC 渲染版、arXiv 或页面打印版——多数不是可以再分发的版本。按 `papers.csv` 里的 DOI 自己取即可，标了 `oa_status` 的可以先从金色 OA 的试。

## 和单细胞报告的关系

单细胞那份报告（仓库根目录的 README）是这份的下游。两份的侧重不同：这份讲「这个方向上有什么重要工作」，那份讲「同一个问题，不同模型怎么解、代价是什么」。后者里 12 个问题的一半，答案要先看懂这份里的编码器和训练目标。
