# 第一轮同轮接续：科学洞察与 partial 状态

2026-10-07。这一轮保留下来的问题是：**几何已经告诉我们不确定性盒会不会改变动作之后，过去的校准动态还提供多少未来损失信息，值得付出多少控制复杂度？** 已形成具体提案和可核查的比较操作，但主自然时间流资源尚未合格，整体 Q7-A 为 incomplete；本报告是局部科学汇报，不能标记完整 Q7-B 或经验验证完成。

前执行器已实际保存 T/U、Q1-S、Q2–Q4、Q5原稿、fresh评审、Q5-R修订和Q6 not_applicable，RUN旧头部滞后。本次是已知情的同轮接续，从Q7-A继续，没有新的独立探索，没有重抽输出或寻找旧成果。原稿、评审、修订与全部旧科学产物字节保留；没有训练、评测、模拟、数据实验、安装、账号申请或付费/远程计算。

这一轮首先澄清了三种不同答案。ACI控制长期漏覆盖频率；DtACI组合不同步长，局部coverage结论还需要相应分布条件；PID用残差score预测加误差积分，已经把可预测成分与反馈纠偏接起来。直接有界风险反馈和决策校准也已有方法。因此，“预测残差＋反馈”“从coverage改叫decision loss”本身不构成新贡献。长期频率、短窗表现和一次行动安全仍是不同目标，不能互相代替。[ACI §2/4.1](https://papers.nips.cc/paper/2021/file/0d441de75945e5acbc865406fc9a2559-Paper.pdf)、[DtACI Alg1/2与局部条件](https://jmlr.org/papers/volume25/22-1218/22-1218.pdf)、[PID Eq5/Thm1](https://proceedings.neurips.cc/paper_files/paper/2023/file/47f2fad8c1111d07f83c91be7870f8db-Paper-Conference.pdf)、[Conformal Decision Theory](https://arxiv.org/html/2310.05921v3)

T从预测消费者的成本、动作截止与反馈时钟向下，U从残差信息、反馈和决策事件向上。T的电力例说明动作使用的是成本决定的特定分位数：若 L(a,y)=c_d(a−y)_++c_s(y−a)_+，正事前成本给 τ=c_s/(c_s+c_d)，动作是 F^{-1}(τ)。作者的PV历史计算中预测评分和收益排序可能不同，但这是离线决策证据，不能单独归因校准或称部署成功。U进一步指出：若校准器比基分布预测器多拿及时信息/刷新预算，所谓tail收益也可能只是信息优势。两者形成“同信息尾结构归因”储备，但尚缺同流成本、forecast vintage和结算资源，保持partial。[PV原研究](https://arxiv.org/html/2403.20149v1)

主方向来自主worker另一条公开原件阅读，而不是伪称T/U共同发现。盒式预测后优化已有精确开关：开发期冻结有限非负路径V，名义动作 x⁰=argmin_V ĉᵀv，robust动作 x^q=argmin_V(ĉ+qσ)ᵀv。对每条竞争路径定义 Δ=ĉᵀ(v−x⁰)、δ=σᵀ(x⁰−v)，κ=min_{δ>0}Δ/δ；空集合时κ=∞。唯一名义动作且非边界时，动作变化恰是q>κ。q=κ与ties单列，有限候选κ不认证全图。Dronavajjala的稳态m进一步近似切换频率，但需要Gaussian/近独立及κ相对稳定等条件；它没有建立实际成本预测器。[COPA2026 §4、Thm3–6](https://proceedings.mlr.press/v329/dronavajjala26a.html)

真正保留的区别在实现损失。令 d=x^q−x⁰、ε=c−ĉ，则相对成本 R=cᵀd=ĉᵀd+εᵀd=A+D。A发行前已知，D直到真实成本到达才可见。R<0才表示相对名义改善；非负 hindsight regret G=cᵀx^q−min_V cᵀv是另一对象。覆盖只限制 |D|≤qσᵀ|d|，不能确定R符号。一个解释用两行动构造可以在同一盒覆盖、同一切换下分别得到正负R；这是代数语义，没有产生实验成绩，也没有反驳worst-case优化目标。κ∞与有限κ混合不能直接求Eκ来计算m，零方差也不能除；修订已保留这些分支。

这使问题从“改一个开关诊断”变成可区分的条件解释。强替代是：当前预测、路径几何、实际选定d与简单方向历史已经足够，更复杂动态没有有用增量。研究假设是：在这些事前输入之外，q/κ响应和方向残差趋势仍帮助预测D的条件位置或尾部，并且某些有限政策差有实际成本后果。如果强简单方案足够，采用它就是有意义的研究决定；不需要为保住新算法而弱化对照。

Q5-R把这个解释接上了真正的输出接口。所有控制器实际发行q=clip(q_raw,0,q_max)，只用保存的issued q/pre-σ算本次误差，再更新状态。rolling用过去score分位；QT在miss后提高raw阈值；ACI在miss后降低level；DtACI各专家按自己的issued集合更新并用fixed-share权重；PID用合法过去scorecaster和累计误差的饱和积分，其burn阶段先用rolling qhat，dev起点才用已到达burn标签拟合并冻结条件预测器，不能把未来拟合回写burn。finite clipping、level投影和到达更新改变了原算法，不能自动继承无限/空集合版本的保证。固定与动态σ各自维护同单位score，不交换旧q。原实现的静态时序检查只定位某些coverage统计可用post-update q的问题，没有运行复现，也不推翻原论文全部数值。

Q7-A已把验证拆成三个具体比较。

第一，exact κ/J只是既有身份核对；合法过去m或neutrality预测未来窗口切换，不能把恒等式回归当新发现。第二，固定finite rolling W=288、α=.10、动态σ的reference action，对B0+与B1使用同一当期d。共同base保留完整当前几何/context、A与过去方向mean/tail；方向历史用当前d重投影已到达完整残差ε_rᵀd，避免旧行动D_r的变化制造增量。两者各加8个同维history slots：B0+给额外简单多窗口摘要，B1给q/κ变化、p∞、crossing和方向交互；同线性learner、标准化、调参及拟合预算。forecast先train冻结，burn产生诚实issued训练行，dev选参数，test前只用已到达标签同规则refit一次后冻结。heldout squared/pinball改善只支持这组特征/learner下的信息增量，不证明漂移因果链或普遍充分性；R=A+D意味着D/R的预测loss相同，不重复计证据。d=0直接输出0，并另报active子流。

第三，同一外生成本流比较五个finite家族×二σ分支与nominal。每家族/分支16个开发配置，dev先要求issued覆盖 .90±.01，再以OD等权physical upper path radius锁定配置；test不重选最有利frontier点。报告真实cᵀx、R/G、覆盖、clip与半径；没有合格配置、test实际覆盖不重叠或clip主导时，不作等覆盖价值结论。12OD共用成本流，coverage分母仍是完整向量origins；成本先OD等权再按day聚合。60testday只有约8.6周，大量五分钟行不能制造独立复现或power保证。

强几何挑战也保留下来。CPO已经用conditional样本形成union-of-balls，并优化robust成本；原交通例是天气派生成本和连续分流，不能用它直接验证自然单路径流。本有限V适配发行前保存中心b_l与尺度A，score=min_l||A(c−b_l)||₂，past score给r；路径support为 max_l b_lᵀv+r||A^{-T}v||₂。shape对照用同生成器、同中心、同信息及预算，把union同它的bounding box比较；各自score校准、dev锁定，box的零半径core若覆盖过高就诚实报告无匹配。原实验用squared-L2，本适配用L2，半径单位不能混。[CPO §3–4/App A/B](https://www.ambujtewari.com/research/patel24conformal.pdf)

一个新的归因澄清是：线性成本下support(U)=support(conv U)。所以union比box的收益反映共同几何约束——不同坐标的极值不一定能够同时发生——不能单独说“非凸性带来收益”。同generator形状比较能回答这个差别；point-box与完整generator的总方案差不能只归因shape。廉价joint残差resampling只是可定义实例，其失败不能否定更强flow/diffusion CPO。公开固定版软件有GPCP/union接口，但batch校准不等于本方案issued/pending ledger，也不是强模型预算已合格。[静态软件入口](https://github.com/yashpatel5400/robbuffet/tree/01275c768dacd0be16cf28c391da99813ca14ff7)

决定当前成熟度的是主资源。PeMS官方确有长期archive、五分钟speed、质量/补齐和站点信息；本次补读还找到segment_start/end、length、direction与SCD2历史配置入口，比“有metadata”更具体。但current站点表去掉有效起止，历史log又与current配置关联，不能直接把它认证为候选210天历史mapping。五分钟补齐mart只保留ML/HV过去4天，sample_timestamp为区间起点，日health/补齐不能当同日事前信息；逐record公共available_at未落实。道路方向linework与公开GIS提供候选几何，却尚未构造至少两条每边都有成本的合格替代路径。免费账号也尚未申请，历史重处理必须锁版本。[PeMS资源/版本](https://dot.ca.gov/programs/traffic-operations/mpr/pems-source)、[历史配置](https://cagov.github.io/caldata-mdsa-caltrans-pems/dbt_docs/#!/model/model.caldata_mdsa_caltrans_pems.int_vds__station_config)、[五分钟mart](https://cagov.github.io/caldata-mdsa-caltrans-pems/dbt_docs/#!/model/model.caldata_mdsa_caltrans_pems.imputation__detector_imputed_agg_five_minutes)

因此尚缺四项资格证据：固定210天单版本成本/质量档案标识；该期覆盖段单位、方向和connector mapping；每OD至少两条逐边成本可评估的路径；合法feed或保存发布vintage，能确定available_at与完整向量反馈F=max_j a_j。单版定稿archive加人工δ=0/1/12/288 intervals，只能回答capped speed/length代理和这些揭示假设下的回放，不能完成真实在线时钟主对象。TNTP静态网、TLC端点或符号接口核对也不能替代它。[处理链](https://cagov.github.io/caldata-mdsa-caltrans-pems/data/data-transform/)、[健康诊断](https://cagov.github.io/caldata-mdsa-caltrans-pems/data/detector-health/)

计算账本已有明确量级而没有伪造小时数。210天×288=60480origins；90train/30burn/30dev/60test对应25920/8640/8640/17280。E200–1000的float64成本矩阵96.8–483.8MB，cost/forecast/两σ约0.39–1.94GB。12OD×11锁定政策的test动作约228万；若每finite分支开发16配置，burn+dev全grid加锁定test共3567万动作。共享路径projection避免每政策重复沿边求和；learner拟合与DtACI专家另计。CPO式S10–50每seed需35–173万个完整vector，全存中心约0.55–13.82GB，五种子还要乘5；强生成模型训练/采样预算仍未知。8–16GB内存、10–100GB稳定产物只是工程预留，不是已检查设备或已获预算。未测吞吐，CPU时长只能由工作量和未来测得吞吐估算。

这些比较会真正改变研究：B1增量和合格政策成本差同时成立，才继续联合信息/价值解释；只有policy差则机制未辨；B0+/rolling足够则采用简单方案；只有joint geometry有效则研究形状价值；无覆盖重叠、有效变化、足够active样本或合法资源时保持未决。正向结果不证明所有机制，弱null与执行失败也不杀死方向。最有信息的后续工作是资格检查真实时钟与路径，而不是先跑方便小实验。

本轮授权的公开阅读、纸面修复和可交付报告已收尾；提案形成，局部操作与来源界限已有依据，主比较计划及资源仍partial，经验/新理论验证为零。Q6=not_applicable，Q6-P=skipped；储备尾结构与延迟/事件未被冒称第二成熟方向。本轮停止，不自动启动另一轮或实验。

## 第二轮 Q6 的最小材料清单

第二轮须从同一BRIEF和冻结Skill独立开展，直到自己的Q5-R后才交接以下四份，不提前提供候选名字或路线判断。材料是同一第一轮的不同阶段，不构成四份独立证据。

1. output/q5-repaired/REPORT.md：修订机制、finite控制器完整操作、纸面例、已撤回与保留的科学主张。
2. output/final/Q7-A.md：确切对照/选择/时钟/资源资格、推算账本、结果决定分支与incomplete状态。
3. output/final/CHAT_REPORT.md：本自包含科学解释和成熟度，避免只继承文件标签。
4. output/final/SOURCE_SUPPLEMENT.md：决定性原件、具体版本/位置、本人或worker实际阅读深度与未读/失败界限。

Q5原稿与fresh评审保持可追溯；只有比较修复前后具体争点需要时再补给，不必把整个root或tmp/原PDF挂给第二轮。第一轮没有实验/raw结果可交接，也没有旧成果要寻找。重复原文不算独立确认，第二轮可以保留更强第一轮主张或判定同样partial，不预设必须更好。
