# Q1-T 来源与实际阅读记录

实际检索/阅读日期：2026-10-06。以下均是本轮新获取的公开原始论文；导航中的综述/二手解释没有当作科学证据。HTML/PDF 公开原件通过 web 或静态 stdin 文本转换阅读；未下载数据、运行作者代码或执行论文实验。原件链接不是本轮复现。source overlap 在接收另一条路线前未知，不声称独立证据。

## S1 Gibbs & Candès：Adaptive Conformal Inference Under Distribution Shift

- 版本：NeurIPS 2021 [正式 PDF](https://papers.nips.cc/paper/2021/file/0d441de75945e5acbc865406fc9a2559-Paper.pdf)，[arXiv](https://arxiv.org/abs/2106.00170)。
- 实际阅读：§1–2 得分/量化阈值/递推、§2.1 step-size tradeoff、§2.2 历史金融例、§4.1 Lemma/Proposition 4.1 及望远镜证明；读到 §4.2 HMM setup，没有复核其全部推导/附录。
- 关键条件与作用：`α_{t+1}=α_t+γ(α-err_t)`；长期经验覆盖与逐点概率覆盖有区别，基本界依赖参数的有界区间及极端阈值扩展。图示金融股票子集按明显非自适应失败挑选，不能估发生率；实证没有下游交易损失。它建立当前基本答案，限制“漂移使 CP 完全失效”的说法。

## S2 Angelopoulos, Candès & Tibshirani：Conformal PID Control for Time Series Prediction

- 版本：NeurIPS 2023 [正式 PDF](https://proceedings.neurips.cc/paper_files/paper/2023/file/47f2fad8c1111d07f83c91be7870f8db-Paper-Conference.pdf)，[arXiv](https://arxiv.org/abs/2307.16895)。
- 实际阅读：PDF pp.1–7，全读 §1、Theorem 1、§2.1–2.4、§3 设置，查看 Fig.2/3 caption；未完整审附录 A、F、后续全部表。
- 条件/作用：P 为量化损失反馈，I 为满足 saturation 的累积错误映射，scorecaster 为过去可见信息预测阈值；长期保证与 scorecaster 的有效信息是不同事。§2.3 明确无信号的过强 scorecaster 会伤害稳定性。COVID/电力是历史预报评估，不能把后处理称官方部署；数据 revision/vintage、4 周 ahead 中的完全信息时序未核完。

## S3 Bhatnagar 等：Improved Online Conformal Prediction via Strongly Adaptive Online Learning

- 版本：ICML 2023/PMLR202 [正式 PDF](https://proceedings.mlr.press/v202/bhatnagar23a/bhatnagar23a.pdf)。
- 实际阅读：§2 设置、Alg.1/2、§3、§4.1–4.2、§5.1 设置与表1/2；附录 C 的 Assumption C.1/C.2、Theorem C.3 与证明结构原文（density→quantile distance→CDF Lipschitz），没有逐行审全部技术 lemma。
- 条件/作用：任意序列的强自适应 quantile regret 不自动推出同样一般的局部覆盖；局部概率结论需要密度上/局部下界与变化项。随机 expert variant 的总体覆盖另有权重平滑项。多 horizon 实证每次预测 H 点、见到所有结果后移动 H；真实重叠 origin 的延迟不能无说明地视为相同。它是当前强替代，而非只有长期保证的弱基线。

## S4 Hallberg Szabadváry：Adaptive Conformal Inference for Multi-Step Ahead Time-Series Forecasting Online

- 版本：COPA2024/PMLR230 论文；实际原文为 [arXiv:2409.14792v1](https://arxiv.org/html/2409.14792v1)，2024-09-23；[正式记录](https://proceedings.mlr.press/v230/hallberg-szabadvary24a.html)。
- 实际阅读：§1–3、MIMO-CRR Alg.1、误差矩阵/diagonal 时序、Eq.(8)–(10)及继承理由；§4 的设置与三个示例解释/表述，§5 大意。不是实际运行。
- 条件/作用：每个 horizon 控制输入利用现在揭晓的、先前 origin 所做预测之误差。作者称继承 ACI finite-sample bounds，但未给专门 delayed-feedback 证明；强制最小 significance 以排除无限集合时原文也承认可破坏这些界。电力例子明确是 illustration，不能当竞争性能验证。
- **纸面待核点，不宣称正式反驳：**单步 ACI 的参数 `[-γ,1+γ]` 范围不能直接照搬到延迟状态；队列中的旧漏覆盖在参数已经变为负后仍可继续向下推动。解释用符号案例：h=2、初值 .1、γ=.1，连续三条已在先前起点发布的漏覆盖到达，可使参数依次为 .01、-.08、-.17；最后超出单步 -γ。没有模拟，只有递推代数。这使 Eq.(9)/(10) 的有限界常数和原文“直接继承”需要复核；不据此否定渐近目标或延迟方法整体。综合不能把论文声称的界当本轮已证明定理。

## S5 Renkema, Brinkel & Alskaif：Conformal Prediction for Stochastic Decision-Making of PV Power in Electricity Markets

- 版本：Electric Power Systems Research234 (2024),110750；[公开作者/机构 PDF](https://research-portal.uu.nl/ws/portalfiles/portal/230093022/1-s2.0-S0378779624006369-main.pdf)；实际深入阅读 [arXiv:2403.20149v1 HTML](https://arxiv.org/html/2403.20149v1)，2024-03-29。
- 实际阅读：§I–VI，包括 CP/CPS、KNN/分箱、动作规则、chronological splits、场景生成、表III–V与讨论；读 Appendix A 的 EUM/CVaR formulation，未独立审求解器实现与全部公式正确性。
- 作用：同一 RFR 的 CP/CPS 排序可在 WIS 与动作收益间不同；“最保守”动作也未必最少偏差。证据性质为历史数据+离线决策计算，非部署。已知日前价格、历史价格 cluster、聚合175套PV、小时平均结算、待补 price-bid 组件，限制结论；收益提升不是本轮验证的因果效果。
- 阅读疑点：§II-C3 的文字方向与 Eq.(1) 的成本分位数关系需区分；后续应直接核对损失定义与公式，不照搬含糊文字。

## S6 Marx, Kuleshov & Ermon：Calibrated Probabilistic Forecasts for Arbitrary Sequences

- 版本：TMLR03/2025；实际深读 [arXiv:2409.19157v2 HTML](https://arxiv.org/html/2409.19157v2)，2025-02-28；[正式 OpenReview PDF](https://openreview.net/pdf?id=nuIUTHGlM5)。v1先导航，决定性判断使用v2。
- 实际阅读：§1–5（payoff/decision calibration、Conditions1–3、Propositions4.1/4.2、Theorem4.3、no-regret与多个payoff、ORCA及近似影响）、§6设置/§6.3风电任务、§8 limitations。未全审附录C专用oracle和全部证明。
- 作用：决策校准和在线一般框架已经存在。存在性oracle保证不能不加条件移交到近似ORCA；outcome compact、payoff bounded/consistent/continuous，实用算法需可微近似/可表达参数化。风电实验损失为给定不对称成本，是作者设计任务而非实际部署；长期集合性质不认证单个决策。它构成画像A的强挑战与正面设计原则。

## S7 Bastani 等：Practical Adversarial Multivalid Conformal Prediction

- 版本：NeurIPS2022 [正式 PDF](https://papers.nips.cc/paper/2022/file/bcdaaa1aec3ae2aa39542acefdec4e4b-Paper-Conference.pdf)。
- 实际阅读：摘要与intro，PDF pp.3–7的§2 Definition2.1、§3 smoothness Definition3.1、Alg.1、Theorem3.1与proof sketch，未深读全部实证/附录证明。
- 作用：交叉组和阈值桶条件的在线经验覆盖已有处理；累积组/桶误差按访问次数归一化，邻桶阈值随机化。保证是指定组集合、score bounded/smooth、随机/期望形式；罕见条件的少访问、小窗口与逐人逐点保证不能互换。撤回“没有在线分组可靠性方法”的泛化。

## S8 2026年的当前性导航与有限阅读

- Rahul Vaze，[Simultaneous Coverage and Efficiency Guarantee in Online Conformal Prediction，arXiv:2607.26577v1](https://arxiv.org/html/2607.26577v1)，2026-07-29。读摘要、§1.1–1.7中定义、model/guarantee概述；未审后续定理证明或复现。ModelI 的误差是 score欠幅，benchmark是`r_t`，界含score path length；ModelII 则是trueCDF/quantile drift，不能混为同一保证。它撤回广义“非抵消覆盖与动态效率没人处理”的首创幻想；尚不能认定资源/条件下充分解决。
- [Online Localized Conformal Prediction，arXiv:2605.05497](https://arxiv.org/abs/2605.05497)：仅检索摘要级导航，未核全文。不得用来声称最佳性能或所有异质性已解决。
- [Online Conformal Prediction for Non-Exchangeable Panel Data，arXiv:2605.17705](https://arxiv.org/abs/2605.17705)：仅摘要级导航，未核全文；延迟目标反馈/同刻其他单位这类信息结构后续可能改变画像B，现阶段保持未知。
- 检索出现2026 partial-feedback与 retrospective adjustment 工作，未深入；不能因此判断无人处理或已经充分解决。

## 获取失败/不完整的保留

- 机构PV PDF首次可定位为8页原件，随后web按line读取多次Internal Error；换作者公开arXiv HTML路径成功，深入判断基于明确v1，没有重抽结果。
- ORCA作者PDF首次可定位为27页，web后续line读取Internal Error；PMC随后出现reCAPTCHA。换公开arXiv v2全文路径，使用现有Python标准HTML解析器静态读取成功。
- PMLR多步论文PDF路径与其原始GitHub assets路径在web均Internal Error；换同一作者arXiv v1成功。没有声称已读取失败的PDF全文。
- 所需系统`pdftotext`不可用；没有安装。现有`pypdf`只用于公开PDF静态文字阅读，其包可用性不是研究结果。
- 本轮检索关键词覆盖online/time-series/nonstationary、decision calibration、electricity/PV profit、local/multivalid、multi-step/delayed以及直接后续；检索失败和未读来源没有当作不存在或新颖性证据。

## 本轮理解边界

关键已有答案与接口已可解释；尚缺新科学证据的是实际短窗决策成本、未知价格与联合尾部、可见先行信号、部署反馈/修订时间、对新的具体操作是否有价值。尚缺阅读的是S2数据vintage、S4延迟界审计、S6专用decision-oracle、S8最新完整技术对比。没有任何训练/实证验证完成。
