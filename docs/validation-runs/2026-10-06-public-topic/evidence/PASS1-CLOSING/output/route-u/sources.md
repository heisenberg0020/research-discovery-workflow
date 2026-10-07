# Q1-U 原始来源与阅读记录

实际检索日：2026-10-06。仅当前轮新获取的公开来源。网页检索用于定位，科学判断依据下列原始论文。没有运行作者代码或实验。本文件与 first-pass.md 一起先于 T/U 交换保存。

## 决定性来源

| ID / 精确来源版本 | 本轮实际阅读深度 | 能改变的判断 / 条件 / 作用 |
|---|---|---|
| S1 Gibbs & Candès, **Adaptive Conformal Inference Under Distribution Shift**, NeurIPS 2021 [正式 PDF](https://papers.nips.cc/paper/2021/file/0d441de75945e5acbc865406fc9a2559-Paper.pdf) | 原文 score/校准构造；更新式；§4.1 Lemma 4.1 与 Proposition 4.1 证明。未系统阅读 HMM 理论及全部实验。 | 决定反馈保证靠参数有界与求和而非准确学习每次分布。极端全/空输出参与保证；撤回“长期覆盖即可可靠决策”的推断。 |
| S2 Angelopoulos, Candès & Tibshirani, **Conformal PID Control for Time Series Prediction**, NeurIPS 2023 [正式 PDF](https://proceedings.neurips.cc/paper_files/paper/2023/file/47f2fad8c1111d07f83c91be7870f8db-Paper-Conference.pdf) | 主文 pp.1–2，式(5)、Theorem 1；Appendix A 的 Proposition 1/2、Theorem 1 证明段；浏览实验情境与部分表，未复核完整实验。 | 把预测残差与反馈纠偏组合已经存在；饱和条件允许任意 scorecaster 的长期保证。决定 U-A 研究归因而非首次组合。 |
| S3 Areces, Mohri, Hashimoto & Duchi, **Online Conformal Prediction via Online Optimization**, ICML 2025 / PMLR 267 [正式 PDF](https://raw.githubusercontent.com/mlresearch/v267/main/assets/areces25a/areces25a.pdf) | 正式版 pp.1–5（Algorithm 1、Examples 3.1–3.3、Theorems 4.1/5.1）；pp.18–21 C.1 全部核心推导及 C.2 条件一致性的密度转换/Robbins–Siegmund 论证入口。C.2 后续收敛闭合步骤未读完；有限样本与实验未完整审计。 | 线性条件分位建模已能同时承接两种不同保证；学习率、固定参数表示、密度等有实质作用。未把特定 stochastic 条件升级成任意漂移保证。 |
| S4 Feldman, Ringel, Bates & Romano, **Achieving Risk Control in Online Learning Settings**, [arXiv:2205.09095v7](https://arxiv.org/pdf/2205.09095v7), 2023-01-27 | pp.4–7 的 Rolling RC、Theorems 1–3、多个风险；p.14 Appendix A.1 的参数有界与望远镜和证明；p.16 多风险证明及 MC 命题。 | 直接有界损失反馈已有强答案，但极端输出须把损失放在目标两侧。主文 p.5 的 C 简写与附录不一致；本文采用附录明确的 1/γ 因子。多风险精确控制条件更强。 |
| S5 Noarov, Ramalingam, Roth & Xie, **High-Dimensional Prediction for Sequential Decision Making**, ICML 2025 / PMLR 267 [正式 PDF](https://raw.githubusercontent.com/mlresearch/v267/main/assets/noarov25b/noarov25b.pdf) | pp.3–8：protocol、Definitions 2.1/2.2、Algorithm 1、Theorem 2.4 证明、效用/行动定义、Theorem 3.7 推导、组合优化入口。未读组合优化全部证明。另读 [2023 arXiv v2](https://arxiv.org/pdf/2310.17651v2) 的引言/预测集应用导航，未审计其预测集证明。 | 只针对有限决策事件的无偏已能转成下游 regret。正式版原保证对算法随机化取期望；对手知道分布但不能依本次随机实现决定状态。通用内层 t² 次操作使成本成为真实条件。 |
| S6 Hu, Wu, Xia & Zou, **Distribution-informed Online Conformal Prediction**, ICLR 2026 / [arXiv:2512.07770v2](https://arxiv.org/pdf/2512.07770v2), 2026-02-24 | pp.3–7：§3.1–3.3，CDF 提示双更新、Proposition 1/2、Theorems 1–3 条件；通过网页读 Appendix B.2 的 Bregman 证明部分，未完整核验 B.1/B.3。 | CDF 提示是 U-A 强替代。局部损失改善需方向与正则条件；长期覆盖与任意步长有限界不同。PDF 动态步长公式的解析/排版有异常，未用该式推出新结果。 |
| S7 Ramalingam, Kiyani & Roth, **The Relationship between No-Regret Learning and Online Conformal Prediction**, [arXiv:2502.10947v1](https://arxiv.org/pdf/2502.10947v1), 2025-02-16 | 原文 pp.8–10 的 Examples 3.1/3.2、Theorems 3.1–3.5 与证明提纲；Lemma 3.1 下界及相关附录部分。未完整读全部 swap/group 证明。 | 外部 regret 与覆盖不等价；阈值/群组 swap 关系依赖 smoothness、离散与事件出现数。作为信号选择的阴性证据，不给新算法背书。 |

## 已读但未足以支撑成熟判断的来源

- S8 Liang, Ren & Chen, **Optimal training-conditional regret for online conformal prediction**, [arXiv:2602.16537v2](https://arxiv.org/pdf/2602.16537v2), 2026-03-05。完整读 pp.3–6 问题、时序、独立性与漂移对象；读到漂移检测/阶段与 doubling 机制的部分文字。未完整读取稳定性、minimax 条件与证明，因长提取输出截断也不把后续页算已读。它支持把训练条件偏差绝对值累计看作不同目标；作者最优性论断未在本轮完成复核。
- S9 Gibbs & Candès, **Conformal Inference for Online Prediction with Arbitrary Distribution Shifts**, JMLR 25(162), 2024 [正式 PDF](https://jmlr.org/papers/volume25/22-1218/22-1218.pdf)。读 pp.3–4 的原 ACI 设定与振荡批评，及部分 Appendix C regret 证明/步长条件；没有完整读 DtACI 算法与全部理论。保留为后续多步长强替代，未在本首轮宣称完整重构。
- S10 Bastani et al., **Practical Adversarial Multivalid Conformal Prediction**, NeurIPS 2022 [正式 PDF](https://papers.nips.cc/paper/2022/file/bcdaaa1aec3ae2aa39542acefdec4e4b-Paper-Conference.pdf)。读 Algorithm 1 及 Theorem 3.1、Lemma 3.2 相关段。知道其多群组/阈值目标、随机化与 smooth-adversary 限制，但未逐步读完算法全部细节与证明，不作为已验证的新机制。
- S11 Garg, Jung, Reingold & Roth, **Oracle Efficient Online Multicalibration and Omniprediction**, SODA 2024 [原会议记录](https://epubs.siam.org/doi/10.1137/1.9781611977912.98)、[作者 preprint](https://arxiv.org/pdf/2307.08999)。取得 PDF，但本轮仅导航/摘要；未拿其 oracle 性能或下界作为决定性结论。
- S12 Zhu et al., **Conformal Risk-Averse Decision Making with Action Conditional Guarantee**, [arXiv:2606.05551](https://arxiv.org/abs/2606.05551)。仅检索摘要；具体行动条件机制/证明未读。它足以阻止 U-B 宣称“首次行动条件保证”，不足以判断其与本轮在线事件目标是否等价。

## 获取失败、替代路径与阅读限制

1. `https://arxiv.org/html/2602.16537v1` 网页读取返回 Internal Error。改用合法 arXiv PDF；网页之后仍有 section/open/find 错误，使用系统已有 pypdf 从公开 PDF 在内存抽取文本，确认本次实际版本 v2。没有重启研究来挑较好结果。
2. ICML 2025 optimization 官方 raw PDF 的网页读取返回 Internal Error；其 OpenReview PDF 跳转浏览器验证页。改为从会议官方 raw PDF 在内存解析，成功读指定原文页。没把验证页当论文。
3. COP OpenReview PDF 同样跳转验证页；改用 arXiv PDF v2，取得原文。动态学习率式存在明显重复索引/符号解析问题；保留而不自行补出有利公式。
4. Rolling RC 和 DriftOCP 的网页首次取得 PDF 后，多次指定行/find 失败；内存文本解析成功。系统 `pdftotext` 不可用，检查并使用了已有 pypdf；无安装、无全局配置修改。
5. 一次合并长 PDF 提取输出被工具截断。后续对决定性页做更小范围原文读取；没有把被截断的章节记为已理解。

## 检索覆盖与限度

检索从 adaptive conformal、online quantile tracking、sequential risk control 扩展到 multivalid、swap regret、omniprediction、decision-event prediction，并查到了 2026 年公开原件。搜索也返回二手站点与论坛；它们只用于导航，未用作科学证据。主要原件来自会议/PMLR/JMLR/arXiv；没有商业部署或真实决策价值的独立证据。未穷尽所有预测不确定性路线，未做新颖性认证。第一轮 stop point 下，S8–S12 的理解缺口保留给后续有针对性的阅读，不能以文件已保存代替它们。
