# 主worker本轮公开原件阅读记录

## 检索/隔离

2026-10-06 首次中性检索为 online prediction uncertainty changing environments conformal prediction decisions sequential primary papers。后续查 decision calibration、switching costs、online omniprediction 和近邻。搜索结果中的综述、二手评述或镜像只做导航；决定性内容使用论文原件/作者官方代码。没有将这些候选或结论发给 T/U。

## S-C1：When Is Conformal Coverage Free?（COPA 2026）

- 原始页：https://proceedings.mlr.press/v329/dronavajjala26a.html 。原 PDF：https://raw.githubusercontent.com/mlresearch/v329/main/assets/dronavajjala26a/dronavajjala26a.pdf 。官方实现：https://github.com/chandrad/conformal-ops 。本轮读取日期 2026-10-06，下载的 proceedings PDF 共28页。web raw-PDF 先失败（application/octet-stream）；curl→已有pypdf的不同合法路径成功。未执行其代码。
- 实际深度：主worker已逐页读完 PDF pp.1–28，特别是 §3 scoring/timing、Thm2–3/Prop4 的原始证明、Thm5–6 条件/证明、Prop7 sketch、§5 全部实验条件、§6 限制、Appendix A算法；参考文献逐项作为导航而非自动已读。城市网络是基于TNTP+BPR+Frank–Wolfe的建模计算研究，不是公共部署的观测。
- 可改变判断：已存在一个精确的单轮决策开关几何对象。对非负有界 polytope P 与盒半径 r=qσ，robust LP 的 cost 是 ĉ+qσ。名义唯一顶点 v* 与竞争顶点 v_k 的 gap Δ_k=ĉᵀ(v_k−v*)，δ_k=σᵀ(v*−v_k)。首个反超量 κ*=min_{δ_k>0} Δ_k/δ_k；q<κ* 则名义点仍唯一最优。证明本身不需要 TU，作者 Prop4 也明确承认这一点。不能把建立此对象当作新贡献。
- 条件/挑战：m=(Eκ*−q*)/σ_q 的开关概率近似需要 q 的 Gaussian steady-state，以及 q 与 κ* 的独立近似；二者共享 EMA σ。Thm5 还承认 buffer 与控制变量共用同一 score stream，遗漏的协方差不是实用参数下的更低阶项。Prop7 是依赖 near-independent detour gaps 的 proof sketch，非一般拓扑定律。作者代码允许 competitors oracle 近似而非全顶点证明。
- 内部需注意：§3.1 文字描述 α update 方向与公式相反；公式 α_next=α+η(α−err) 在 miss 时降低 α（更宽）。有 clip 的版本不能直接继承未裁剪控制器的望远镜恒等式覆盖界。§5.4 的“即使完美predictor仍拓扑约束”强推断与 Thm3(ii) 的 vanishing σ、positive gap、bounded q 充分条件需要区分，前者不能由两个预测器消融直接推出。能源表格的 committed set 与完整 vector neutrality 不同，原文和 README 均承认。当前不将这些当作本轮实验反驳，只是原件界限。

## S-C2：Conformal Decision Theory（arXiv:2310.05921v3, 2024-05-02）

- 原件：https://arxiv.org/html/2310.05921v3 ，论文官方项目：https://conformal-decision.github.io/ 。读取 HTML §I–IV（定义、Thm1和lemma证明）及 §V-A decision parameterization/Table1、batch §IV；其他案例仅到导航，不宣称全篇读。
- inputs/operations：每轮先给出决策族 D_t^λ，采取 D_t^{λ_t}(x_t)，观测 bounded actual loss ℓ_t∈[0,1]，再 λ_next=λ+η(ε−ℓ)。若 eventual safety（持续在 λ_safe 以下 K 步使平均loss≤ε_safe≤ε）存在，得 prefix empirical-risk bound ε+((λ1−λsafe)/η+K)/t。
- 关键理解：恒等式风险界来自 λ 的望远镜和下界；这不是单次行动安全、不能无条件当作任意窗口风险界。安全备份需领域保证；预测集合可退到全空间，真实机器人决策未必有这样安全行动。paper 的 simulations 不是部署证据。批处理还需 counterfactual losses，且是不同交换性设置。
- 可改变判断：直接决策损失控制已有强框架；任何“从 coverage 换成 decision loss”的提案须与该操作逐项比而不能声称首次。

## S-C3/S-C4：仅导航或部分理解，尚不支持完整新颖性/强度判断

- Gibbs & Candès, JMLR 2024：https://www.jmlr.org/papers/v25/22-1218.html 与 https://jmlr.org/papers/volume25/22-1218/22-1218.pdf 。web find失败后主worker curl取得36页原PDF，读 pp.1–14 和 pp.23–28：§2.3 Algorithm1/§3.4 Algorithm2、§3.1 regret、§3.2 local coverage、§3.3 long term条件、Appendix C.1–C.6证明。保留其他数据案例未读。DtACI 的 fixed-share exponential expert weighting 提高近期loss权重，比较多个ACI step sizes；它已有局部 pinball regret保证。把 regret换为参数误差与coverage gap需要conditional beta density lower bound和 Lipschitz coverage。用于实际的constant η/σ一般不精确长期校准；decay到0对应Thm6。不能泛称“局部coverage未有人处理”，也不能用纯regret代替无条件局部风险。
- Dynamic Regret Bounds for Online Omniprediction with Long Term Constraints：https://arxiv.org/html/2510.07266v1 。读取 §1–2 的 setting、linear/Lipschitz utility/constraints、full outcome timing、动态可行比较类及 subsequences；实际 HTML 顶部 arXiv version-date 与文内 August 2026 日期不同，未进一步核对。方法/proof尚未读，不能给它强度排名。它是未来 direct-decision 比较的有力范围提醒。
- Optimal training-conditional regret for online conformal prediction：https://arxiv.org/html/2602.16537v1 。仅摘要/目录， independently generated shifts及training stability等条件暂未精读。

本记录保持 acquired、partially read、understood、validation 分离；全轮尚无实验或新定理验证。

## 后续决定性复读（主worker本人，2026-10-06）

- **CPO阅读升级**：上文“仅摘要”是当时状态，现在curl保存作者PDF于tmp/coordinator/cpo.pdf，已有pypdf抽取。共19页；完整读pp1–8主文、p13 Appendix A/B，包括coverage upper bound的diameter证明与minmax优化核心；余下训练实验附录未系统读。conditional生成K样本、min-distance score形成union of balls，逐ball support最大化、外层convex projected subgradient，K内层cost线性增长。K选择的volume估计须不同DC1/DC2，不用calibration labels调K。静态exchangeability保证不能用于本轮自然流。正式routing是continuous traffic flow，多数非盒几何可能分流，TU不使一般非线性robust目标最优点必为path。它限制本轮不得将CPO宣传成弱box或将单path限制胜利叫普遍优越。本文p13 Lipschitz符号在uncertain-cost与w处复用有检查余地；本轮不从其打印步数公式估算训练时间。
- **显式延迟近邻**：El Halabi/Brandt, Adaptive Conformal Inference Under Delayed Feedback: Coverage Guarantees and a Delay-to-Memory Diagnostic, arXiv2609.07251v1(2026-09-07)，https://arxiv.org/html/2609.07251v1 。主worker完整读§1–4.3、Appendix A.1/A.2，§4.4只读设定，不记proof已读；§8作作者解释导航，模拟不验证。递推α_{t+τ}=α_t+γ(α−err_t)，算法从queue取issued parameter后重置，τ条相位ACI即已有finite bound O(τ/(γT)+τ/T)。这与当前全局参数累加旧error不同，不能称其推翻所有延迟ACI。它撤回本轮潜在“首次显式delay bound”贡献，未完全解决action-window实际损失。
- **官方CPO实现资源升级**：论文csi repo README https://github.com/yashpatel5400/csi 已声明后续工作移到 https://github.com/yashpatel5400/robbuffet 。完整读新repo README(2026-10-06 main)：MIT，PyTorch+CVXPY，L1/L2/Linf/Mahalanobis几何与affine support，GPCP union/Danskin；METR-LA例依DCRNN submodule/pretrained预测生成。未安装/运行，未读完其实际模块/核对paper复现，因此只记可用接口描述，不认为已经可复现全实验或实现认证。未来采用必须pin commit、审计issued时序与shape。
  公开commits API本轮解析main为 `01275c768dacd0be16cf28c391da99813ca14ff7`（author commit-date2025-12-24），可作为未来静态核对入口；未检查其全部模块。这里的日期是公开git元数据，不是本轮执行时间。论文原csi的重定向与robbuffet接口变化不能默认为同版论文实验已可复现。
- **PeMS进一步质量复读**：https://cagov.github.io/caldata-mdsa-caltrans-pems/data/detector-health/ 完整相关正文/表读。quality是按detector按天判断，5am–10pm一天统计可造成post-event健康标签；明确“不做real-time checks”，missing/bad值补齐同天数据，ramp不impute。故health不能作为当时可见feature或动作纳入/剔除规则。https://cagov.github.io/caldata-mdsa-caltrans-pems/data/data-transform/ 官方指Caltrans linear referencing GIS portal，点击GIS页返回0文本，本轮不能据此确认connector拓扑/具体station mapping。这是真正资源条件，不能把“有metadata”冒称所有route links已合格。Archive定稿proxy replay≠actual实时forecast部署；live vintage/latency尚未证实。

## 进一步导航/近邻边界（未据此声称全篇理解）

- Conformal Contextual Robust Optimization (Patel/Rayan/Tewari, AISTATS2024)，原始页 https://proceedings.mlr.press/v238/patel24a.html 和作者 https://www.ambujtewari.com/research/patel24conformal.pdf ，仅摘要及导言/导航，conditional generative nonconvex region与静态交换性batch设定的强几何替代应保留，不能把它简化成所有维度统一radius的弱对照。
- Decision Theoretic Foundations for Conformal Prediction: Optimal Uncertainty Quantification for Risk-Averse Agents (Kiyani et al., ICML2025)，https://proceedings.mlr.press/v267/kiyani25a.html ，摘要及公开原PDF §2 对RA-DPO的摘取导航已读。VaR-utility、max-min policy以及expectation-vs-quantile distinction为强答案范围；未读完proof，最终若用于决定性新颖性判定需补读。
- Online Conformal Prediction with Adversarial Semi-Bandit Feedback via Regret Minimization (Yang/Kim/Park, ICLR2026/arXiv2604.17984v1)，https://arxiv.org/html/2604.17984v1 ，读取§1–4.3及4.4开头的原设置/损失/lemma。它的partial指label可能不见，但**每轮chosen set的miscoverage indicator始终可见**；label只在覆盖时额外给出。因此不能将它直接当 arbitrary missing binary feedback 的解决方案。方法离散threshold arms、EXP3.P和monotonic inferred feedback；尚未复核完整proof，coverage bound里C_MC/C_gap依赖的条件也未完全重建，不能给强度排序。它至少否定“partial feedback完全无人处理”的说法。该分支是否值得开发须由route/synthesis判断，当前不自动选。

## S-C5：作者官方实现的静态时序检查

实际完整阅读 `conformal_ops/diagnostics/free_coverage.py`（Git blob SHA c902730dfd5fd191b6468c22800d3fd7bf04b27c）和 `conformal_ops/core/online_conformal.py`（SHA 02d51a9e308f04175c759d2354a2c568ce50d158），2026-10-06 main，未执行。原始链接分别为 https://raw.githubusercontent.com/chandrad/conformal-ops/main/conformal_ops/diagnostics/free_coverage.py 与 https://raw.githubusercontent.com/chandrad/conformal-ops/main/conformal_ops/core/online_conformal.py 。GitHub网页树访问失败后，公开GitHub contents API只读导航到这些确实存在的文件。

`diagnostics.run` 在动作之前获取 issued radii，但 `OnlineConformal.update` 先把新 score 插入 buffer，再 `_get_q()`，再计算 `covered`。因此其统计 `coverage` 及反馈 `err` 的比较阈值可以与已发出 prediction set 的 q 不同。这是静态、可纸面复核的接口缺陷，不是已运行复现实验。**构造例（只解释语义）**：past scores=[0,0,0,0,1]、alpha=.1 时 linear quantile q_pre=.6；本轮 score=.7，在已发集合中 miss。append后六项的 .9 quantile q_post=.85，代码会把当前 score记 covered。故纸面上不能直接把该实现的 `coverage` 列等同issued coverage；需要按 paper 程序冻结 pre-q、pre-σ 后再观测更新。原论文其余实验可能有不同实现，未获对应 exact scripts/config，因此本检查不推翻所有数字，数值证据保留 reproduction gap。

诊断的解析κ使用全pilot预测均值 `c_rep=C_pred.mean(axis=0)` 和最终 `oc._sigma`，并非每轮 `(ĉ_t,σ_t)`。未来比较必须公平保留这一具体官方基线，另给每轮 exact geometry oracle；不能把官方已包含的直接测得neutral fractions包装为新诊断，也不能把后验全pilot均值当预部署每轮可用信息。

## S-C6：资源资格说明

- NYC TLC官方页 https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page ，2026-10-06读取 relevant introduction/download availability。数据字典2025-03-18 https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf 完整读。仅pickup/dropoff times+taxi-zone IDs、距离、费用等，不含逐路段轨迹或每时每路段counterfactual travel times；不能直接当完整路网成本向量。官方说明数据由providers提供，accuracy不保证；当前页说通常两个月发布延迟。2019 guide的CSV/半年发布描述过时，以当前页PARQUET/月度为准。没有下载或分析行程数据。
- TNTP官方库 https://github.com/bstabler/TransportationNetworks ，读取README的License、TNTP格式及网络规模。academic research only、需出处归因；静态network/link capacities/BPR params/OD demands+reference flows资源，SiouxFalls76links，Anaheim914，Philadelphia40003。其真实网络几何不等于自然漂移的在线实测全成本。没有下载数据、求解流或模拟。
- Caltrans官方 PeMS数据资格：https://dot.ca.gov/programs/traffic-operations/mpr/pems-source （relevant introduction、account access、PeMS14-vs12全段）与 https://cagov.github.io/caldata-mdsa-caltrans-pems/data/data-transform/ （全页）。提供大量freeway detectors和十年以上archive；免费申请账号，官方说通常1–2工作日批准，本轮未申请或验证账号。现代化流程原始30秒VDS→5分钟per-lane→station speed/flow/occupancy；缺测/坏detector有imputation，历史数据可能重处理。速度是估算/融合/补齐观测，不等于每个route干预下旅行时间。字段资格、观测/imputation标记、station metadata/GIS对齐和历史版本必须在未来获取后检查；不可混用PeMS12/14造“自然漂移”。
