# 单细胞基础模型（scFM）的基准评测与批评性研究：痛点与争议

## 一、系统性评测

**1. scEval（Liu T 等，耶鲁大学；*Advanced Science* 13(27):e14490, 2026；DOI 10.1002/advs.202514490，预印本 2023）**：8 类任务、10 个 scFM；scGPT、Geneformer、CellFM 居前，但「在任何任务上都不稳定优于任务专用方法」，并称这「动摇了开发 scFM 的必要性」；同时量化超参数、初始设置与训练稳定性，给出预训练/微调指南。

**2. Kedzierska 等（Microsoft Research；*Genome Biology* 26:101, 2025；DOI 10.1186/s13059-025-03574-x）**：5 数据集 zero-shot 评测，Geneformer 的 ASW 仅 0.38（胰腺）–0.52（PBMC 95k），HVG 基线在除 PBMC 外全部数据集上胜过它；scGPT 中位 ASW 0.53 ≈ scVI 0.54，但胰腺 AvgBIO 相对 HVG 由 0.60 降至 0.52；批次整合不合格；预训练数据超过阈值后不再带来增益。

**3. PertEval-scFM（Wenteler 等，伦敦玛丽女王大学；ICML 2025, PMLR 267:66633–66677）**：标准化扰动预测评测，zero-shot scFM 嵌入对简单基线「提升有限」，分布偏移下尤甚。

**4. Ahlmann-Eltze、Huber、Anders（EMBL；*Nature Methods*, 2025；DOI 10.1038/s41592-025-02772-6）**：5 个 FM + 2 个深度学习模型对撞线性基线；Norman 双扰动留出 62 个，所有模型误差均高于 additive 基线，交互预测无一优于「no change」；FDR 5% 下仅 5,035/124,000（4.2%）为真实交互。

**5. Boiarsky 等（MIT/Broad；*Nature Machine Intelligence*, 2024；DOI 10.1038/s42256-024-00949-w）**：PBMC（68,450 细胞）上 L1 逻辑回归在 accuracy 与 macro-F1 上均胜 scBERT；scBERT 去预训练无显著差异（p=0.34/0.59），其预训练 78% 准确率未对应有意义的基因表征；scGPT 仅在多发性硬化（分布外）数据上胜出。

**6. Wu 等（浙江大学；*Genome Biology*, 2025；DOI 10.1186/s13059-025-03781-6）**：6 个 scFM、12 项指标，「没有单一 scFM 全面领先」，简单模型在资源受限时反而更易适配。

## 二、批评与复现问题

**数据泄漏。** Ali（哥伦比亚大学，arXiv:2607.20572）以 MinHash 逐细胞审计：PBMC 3k 有 80.4%、人胰岛图谱有 77.0% 的细胞与 Genecorpus-30M 显著重叠（p<0.05），截止日后的 AIDA v2 与 Tahoe-100M 为 0%；污染细胞在同供体、同细胞类型内嵌入更「紧」（置换 p=0.030/0.014/<0.002）。Kedzierska 亦承认胰腺数据与 Geneformer 预训练部分重叠（非重叠子集结论一致），且当时无法获知 scGPT 预训练数据。这类重叠实为「双重 dipping」：同一批细胞既塑造预训练表征，又充当 zero-shot 评测集；因模型方不公开逐细胞训练清单，只能靠指纹与成员推断间接审计。

**超参与初始化。** Boiarsky 显示 scBERT 微调对超参数与随机种子高度敏感；scEval 把「超参数、初始设置、稳定性」列为核心评测维度，说明默认配置下可比性不足。

**观点交锋。** *Nature Machine Intelligence* 2024 刊出「Deeper evaluation of a single-cell foundation model」与 scGPT 作者的「Reply to: ...」（DOI 10.1038/s42256-024-00948-x）；*Nature Methods* 2025 亦以「Single-cell foundation models evaluated」作专门评述（DOI 10.1038/s41592-025-02735-x）。

## 三、指标与方法学问题

**MSE/Pearson 与生物学脱节。** L2 与 Pearson delta 被大量近零差异基因稀释：误差高于 additive 基线的模型仍可被描述为「接近」，而真正有信息的交互仅占 4.2%，指标对稀疏生物信号不敏感。

**批次与标注混淆。** scContam 证明数据集级 ASW 比较会被标注协议系统性混淆；Kedzierska 则出现「zero-shot 批次整合失败、ASW 仍好看」的背离，指标优劣与生物信号保留并不同向。

**稀有细胞类型。** Dong 与 Zhong（arXiv:2609.23325）完成 162 次受控训练（3 骨架 × 3 数据集 × 6 种长尾损失 × 3 种子）：总体准确率可达 97.5%，但 rare-class recall 系统性失败，且失败由数据集结构而非预训练决定。

**指标选择。** 只有改用 macro-F1，scBERT 在难分 CD8 亚群上的劣势才暴露出来。

## 四、仍然成立的优势

1. **微调 + 分布外泛化**：scGPT 在多发性硬化数据上优于逻辑回归，且训练样本越少优势越大；Steiner 等（L3S Hannover；WSDM 2025；DOI 10.1145/3701551.3708811）在 myeloid/胰腺/MS 三任务上发现 scFoundation 稳定最佳、Geneformer 甚至劣于基线，但用 OOD 数据微调后仍可泛化。
2. **嵌入作特征有效**：scGPT/scFoundation 基因嵌入加线性解码优于均值基线与随机嵌入，但不优于用训练数据学到的嵌入。
3. **预训练确有贡献**：预训练模型普遍优于随机初始化，scGPT 去预训练则显著变差。
4. **数据域匹配优于规模**：用 Replogle 扰动数据预训练的线性模型稳定优于所有模型。

**小结**：可复现优势集中在「微调/特征提取 + 域内或近域任务」；zero-shot 通用性、跨数据集稳健性与稀有类可靠性仍未成立。

## 五、来源列表

1. Liu T, Li K, Wang Y, Li H, Zhao H. *Evaluating the Utilities of Foundation Models in Single-Cell Data Analysis.* Advanced Science 13(27):e14490, 2026. https://doi.org/10.1002/advs.202514490 ；预印本全文 https://www.biorxiv.org/content/10.1101/2023.09.08.555192v6.full
2. Kedzierska KZ, Crawford L, Amini AP, Lu AX. *Zero-shot evaluation reveals limitations of single-cell foundation models.* Genome Biology 26:101, 2025. https://doi.org/10.1186/s13059-025-03574-x ；本文数字引自预印本 https://www.biorxiv.org/content/10.1101/2023.10.16.561085v2.full
3. Wenteler A, Occhetta M, Branson N, et al. *PertEval-scFM: Benchmarking Single-Cell Foundation Models for Perturbation Effect Prediction.* ICML 2025, PMLR 267:66633–66677. https://proceedings.mlr.press/v267/wenteler25a.html
4. Ahlmann-Eltze C, Huber W, Anders S. *Deep-learning-based gene perturbation effect prediction does not yet outperform simple linear baselines.* Nature Methods, 2025. https://doi.org/10.1038/s41592-025-02772-6 ；全文 https://www.biorxiv.org/content/10.1101/2024.09.16.613342v5.full
5. Boiarsky R, Singh N, Buendia A, Getz G, Sontag D. *Deeper evaluation of a single-cell foundation model.* Nature Machine Intelligence, 2024. https://doi.org/10.1038/s42256-024-00949-w ；预印本 https://www.biorxiv.org/content/10.1101/2023.10.19.563100v1.full
6. Wu J, Ye Q, Wang Y, et al. *Biology-driven insights into the power of single-cell foundation models.* Genome Biology, 2025. https://doi.org/10.1186/s13059-025-03781-6
7. Ali S. *Auditing pretraining contamination in single-cell foundation model benchmarks.* arXiv:2607.20572, 2026. https://arxiv.org/html/2607.20572v1
8. Dong Z, Zhong J. *Rethinking Class Imbalance for Single-Cell Foundation Models.* arXiv:2609.23325, 2026. https://arxiv.org/abs/2609.23325
9. Steiner N, Li Z, Vosoughi O, Schrader J, Roy S, Nejdl W, Tang M. *A Systematic Evaluation of Single-Cell Foundation Models on Cell-Type Classification Task.* WSDM 2025:1112–1113. https://doi.org/10.1145/3701551.3708811
10. *Reply to: Deeper evaluation of a single-cell foundation model.* Nature Machine Intelligence, 2024. https://doi.org/10.1038/s42256-024-00948-x
11. *Single-cell foundation models evaluated.* Nature Methods, 2025. https://doi.org/10.1038/s41592-025-02735-x
12. *Position: Saturation in Single-Cell Foundation Model Benchmarks Signals Identifiability Failure, Not Solved Capability.* ICML 2026（仅核对标题页，未用于正文论断）. https://icml.cc/virtual/2026/72083
