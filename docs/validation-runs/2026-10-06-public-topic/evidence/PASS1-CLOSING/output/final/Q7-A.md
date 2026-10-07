# Q7-A 定向比较与资源账本：主对象仍 incomplete

2026-10-07，接续同一 pass-1。以已保存的 Q5-R 为起点；未重新探索或重抽候选，未读取旧材料。原 Q5、fresh 评审、Q5-R 和路线产物保留。此处新增的是比较的具体化与公开资源资格核查，不是实验结果。

## 1. 保留对象、现有答案与解释边界

主问题保持为：自然时间流、合法发行前信息、外生成本全反馈、开发期冻结有限路径集下，当前动作几何之外，过去动态是否仍提供未来实现损失信息；有限输出政策是否有决策价值。速度/长度是明确的外生成本代理，不能据此声称真实行程反事实或路由干预效果。合法时钟、完整成本和路径资格缺一，不将档案假定延迟回放升级为主对象。

最接近的答案是 Dronavajjala 的 COPA2026 §4：非负有限路径 V 上，盒 U_t={c:|c−ĉ_t|≤q_tσ_t} 的 robust 动作为 argmin_V(ĉ_t+q_tσ_t)ᵀv。名义 x⁰ 唯一且非 tie 时，Δ_k=ĉᵀ(v_k−x⁰)、δ_k=σᵀ(x⁰−v_k)、κ=min_{δ_k>0}Δ_k/δ_k，min∅=∞；J=1{x^q≠x⁰}=1{q>κ}。这是既有精确身份，不需要 TU 作为产生开关的条件，也不是本轮贡献。q=κ、名义 ties 单独记录；有限 V 不认证全图。

该文稳态 m=(Eκ−q*)/sd(q) 描述切换频率，依赖 stationary-score Gaussian 近似、q 与 κ 近独立，以及 κ 方差相对较小；不能把它作为已有实际损失预测器。κ=∞ 的质量 p∞ 单独报告；m 只在有限矩、正方差的合格子流使用，sd(q)=0 直接比较。其 §5 使用固定 α=.1、η=.05、W=200 与3–5个种子，主要验证中性比例/维度；城市网络部分还包含 TNTP+BPR/均衡计算。作者报告不能补齐本轮合法历史时钟或动态损失信息比较。本人接续重读原 PDF pp.3–5、9–18，尤其 Thm3、Prop4、Thm5–6；本轮原执行器此前已读全28页。[原论文](https://proceedings.mlr.press/v329/dronavajjala26a.html)

实现差距也明确：本轮原静态检查的官方 core 可在 append 当前 score 后求 q 再记 coverage。未来比较采用冻结 issued q/σ 的独立账本，不把该列直接当 issued 事件；没有执行复现，不能据此推翻论文全部实验。官方诊断的全 pilot 代表预测和最终 σ 只作事后描述；合法预测基线使用相同过去窗口。

损失对象：d_t=x^q_t−x⁰_t，ε_t=c_t−ĉ_t，A_t=ĉ_tᵀd_t 事前已知，D_t=ε_tᵀd_t 事后可见，R_t=c_tᵀd_t=A_t+D_t。R<0 表示相对名义改善；G_t=c_tᵀx^q_t−min_V c_tᵀv≥0 属于 hindsight。盒覆盖只给 |D_t|≤q_tσ_tᵀ|d_t|。所以同一覆盖和切换可以有相反 R；Q5-R 的两行动纸面构造是语义核对，没有生成经验成绩。

两个待区分的解释保持为 H_sufficient：强的当前几何/context 加简单可见方向历史已足够，额外 q/κ 动态没有有用增量；H_history：在这些输入之外，已到达的 q/κ 变化和方向残差趋势/交互仍提供可重复的未来 D/R 信息，并且部分政策差有成本意义。二者可以分条件共存。下面分别检验几何身份、预测信息、政策价值；不拿一个层的成功替另一个层作证明。

## 2. 统一发行接口与预声明比较

origin o 为上一五分钟区间结束，target 为紧接的五分钟区间，h=1。sample_timestamp 若是区间起点，须先转换为 target 区间，不能当已收齐时刻。记每边实际 available_at=a_jr，完整反馈 F_r=max_j a_jr。每次发行保存 ĉ、pre-σ、实际 q、路径 d、各专家 issued 集合及生成中心；到达后先用保存状态算事件，才更新当前控制器/尺度、append score。可变延迟采用 Q5-R 的 arrival-ledger 有限变体：把此刻已完成且未处理的 origins 按 origin 排序处理，未齐者留 pending，不暗等未齐旧 origin、也不补即时标签。它不是 τ-DACI 的按发行参数相位重置法，不移交其证明。

共用冻结预测器：计划首90天仅训练，每边用固定20维以内的日历与合法可见 lag 特征作 ridge 点预测，正成本输出 floor；拟合后不重训。train 尾部未到达的标签不用。σ_fixed 由 train 可见残差确定，不能用完整 burn-in 回头改其前段 issued 轨迹。动态 σ 为 |ε| 的 EMA，半衰期288次完整反馈，初始化同 train 尺度，floor=max(0.01分钟, train 尺度的1%)。固定/动态分支维护自己的 score=max_E|ε|/σ_pre 与历史，单位不能互换。共享有限 q_max=25、a_min=.001；它们是前瞻工程约定，报告 clip/saturation，未证明足够大。Q5-R 的有限 rolling、QT、ACI-style、DtACI-style、PID-style 操作与更新方向不变；裁剪、投影、到达更新不继承原无限输出算法的覆盖/遗憾保证。[ACI §2/4.1](https://papers.nips.cc/paper/2021/file/0d441de75945e5acbc865406fc9a2559-Paper.pdf)、[DtACI Alg1/2](https://jmlr.org/papers/volume25/22-1218/22-1218.pdf)、[PID Eq5/Thm1](https://proceedings.neurips.cc/paper_files/paper/2023/file/47f2fad8c1111d07f83c91be7870f8db-Paper-Conference.pdf)

每家族每 σ 分支16个开发配置，nominal 不需 coverage 配置。α_target∈{.05,.10,.15,.20}，与下列四选一交叉：rolling W∈{72,288,2016,8064}；QT η∈{.001,.01,.1,1}；ACI γ∈{.001,.005,.01,.05}，W=2016；DtACI η_w∈{.01,.05,.1,.5}，四个 γ 专家取 ACI 网格，fixed-share ξ=.01、W=2016；PID K_I∈{.1,.5,1,2}，C_sat=4，scorecaster 用日历及已可见 s 的 lags 1/12/288、rolling 分位等同信息输入作线性条件分位预测，仅 burn 样本拟合。经验分位数固定 inverse-CDF（≤记覆盖）。状态初值 a=α_target、专家均权、QT/PID 基阈值取 train 分数经验分位；空历史阶段只用这些预定初值，不从未来初始化。

PID的burn发行不能偷用burn结束才拟合出的scorecaster。具体规则：burn期间qhat为同可见score的rolling W=2016分位；dev起点只用此刻已到达的burn score行拟合条件分位qhat，随后冻结到test（四α×两σ共8个scorecaster，全部K_I共享对应模型）。该预声明一次转换不改写burn issued事件，也不重置积分状态。拟合失败时保留原rolling qhat并标记条件预测器未合格，不能声称完整PID实例完成。

以上 grid 是比较 envelope，不宣称覆盖所有最优实现；若严重 clip、优化未收敛或 scorecaster 训练样本不足，记操作/测量问题，不挑一个差参数宣布原方法失败。参数值不以 test 调整。

### 2a. 几何身份核对

对两个 σ 分支共享每轮 κ、p∞、ties、J。exact κ/J 检查 issued 动作身份；过去7天 neutrality、合格 m 和独立近似仅预测未来12个起点的切换频率。主结果是身份是否一致及摘要在其合法条件下的误差，不以回归 q−κ 重新发现恒等式。q/κ共同边际的纸面例只说明一般边际摘要不充分，不是同一 ACI 可达轨迹或真实漂移证据。

### 2b. 未来 D/R 信息：固定动作，强基线，合法历史

主要 reference 固定为 finite rolling W=288、α_target=.10、dynamic σ，完全独立于最终 test 输赢；每轮的同一 d_t 对所有损失预测器固定。d=0 时 D=R=0，直接输出0，并同时报告全部 origin 和事前可知 d≠0 子集有效数。禁止把其他控制器生成的不同 d 或事后 ε 当 feature。

共同 base 包含完整当前 ĉ、σ、d、q、A，候选路径 gap/physical radius、路径标识及日历/可见缺测 context；并保留过去已到达完整残差在当前 d 上的投影 z_{r,t}=ε_rᵀd_t，于过去12/288/2016个 origins 的均值、0.9分位及样本量。使用当前 d 重投影合法历史，避免旧行动 D_r 自身的变动制造增量。缺标签不填未来，统计只对已可见完整向量，缺失与 stale-age 为共同输入。

在这个强 base 之外，两模型各有8个 history slots。B0+ 给过去72/8064 origins 的 z 均值与0.9分位（4项）、同样两窗口可见 complete-score 的均值与0.9分位（4项）；B1 给 q 的12/288均值变化、有限 κ 的12/288中位数变化、过去288的 p∞、q−κ>0 频率、z 短长均值差与当前有限 q−κ 的交互、z 的短长 tail 差（8项）。κ∞交互设0且另含 p∞，历史不足的 mask 对两模型等维保留。不同窗口按 origin 长度界定，不能把已到达的未来 origin 排进过去。

B0+、B1 同参数维度、同线性 squared-loss+L2 和0.9 pinball+L2 learner、同标准化/拟合求解器、λ∈{1e−4,1e−2,1}、相同收敛容忍1e−6/最多1000次全数据等价 pass。learner 使用 forecast 已冻结后的 burn30天 honest issued 行，只有拟合截止前已到达标签；dev30天挑 λ/检查收敛，test 前仅用 burn+dev 中已到达行同规则重拟合一次，此后冻结。B0-base vs B1 的 nested 比较另报，但标出多8维容量差；B0+ vs B1 是同容量表征比较，不能声称控制了所有有效自由度。B0+ 不被删去原有方向 mean/tail。

主要估计是 day 内 OD 等权的 heldout MSE 与 pinball 差，再按 day 聚合；R 由已知 A+预测 D 得到。于是 D/R 的 squared 与 pinball loss完全相同，不重复计为两份证据。报告连续效应、tail校准、active频率，不能以事后窗口挑赢。若 B1 只胜弱 m、不胜 B0+，不支持额外动态信息。胜出只支持这个 feature/learner family 下的信息增量，仍可能代理遗漏 context；不是因果漂移链证明。过去7天 shift-placebo只移已可见新增 history slots，mask和base不动，作为关联敏感性。

### 2c. 政策价值：开发锁定，再同流配对

五有限家族×二σ分支，每个配置在同 burn 独立启动、dev后连续进入test，只允许指定反馈状态更新。dev先要求完整E-vector issued覆盖 .90±.01；合格配置中最小化 OD等权、V内均值的 physical upper radius qσᵀv，tie按固定grid序。每分支锁一个配置，test共有10个finite加nominal。dev合格为空则该分支没有确认性matched-coverage结果，仍可描述全grid。test不再选点；实际 test覆盖即使不同于名义目标也必须显示，偏离或clip主导时不作等覆盖成本主张。

逐 origin 同外生成本比较 cᵀx、R/G、J、issued coverage与路径半径；coverage分母是完整E-vector origins，不能乘12OD。成本先OD等权再day平均，配对差与相同流共因子的处理相连。约60testday=8.6calendar weeks，不是17280个独立样本；预声明7day block、2000个paired block resamples只作为弱依赖假设下不确定性计划，另报周序列/OD差异。若目标实际有效天数太少、仅1次变化或 missing选择严重，保留低信息结论。

成本实用阈值预声明为 dev 名义平均路径分钟的1%（代理研究约定，未获部署方意义确认）；不给未经数据支持的power保证。统计改善小于该阈值时允许采纳简单方案。固定 σ 另改 score单位与政策，不单独识别尺度运动的因果效应。

## 3. 强几何替代：精确有限V操作与归因

CPO 已有 conditional sampler、min-distance score、union-of-balls、逐球内最大化与外层投影；原 §4.2 使用雨量生成器→速度成本和可分流 continuous allocation，不是自然路段实测单路径流。本人接续重读 pp.2–8、13，原 worker此前读主文/核心附录。其 i.i.d./exchangeability 校准保证不能原样搬到自然漂移。[CPO §3–4/App A/B](https://www.ambujtewari.com/research/patel24conformal.pdf)

有限V适配保留 Q5-R：发行前存 b_{t1:S}、预可见可逆 A（第一版train对角尺度固定）。s_union=min_l||A(c−b_l)||₂，past issued scores 给 finite r。对非截断集合 B_union(v)=max_l b_lᵀv+r||A^{-T}v||₂，选 argmin_V B。若另限制 c≥0，需重算 support。现阶段不复现原连续分流，更不把其流/扩散生成器替换成廉价 resampling 后以失败否定论文。

同一生成器/中心/信息/种子/刷新给 box：m_j=(max_l b_lj+min_l b_lj)/2，a_j=(max_l b_lj−min_l b_lj)/2，h_j=||(A^{-1})_{j,:}||₂>0。s_box=max_j[(|c_j−m_j|−a_j)_+/h_j]，U_box(r)={c:|c_j−m_j|≤a_j+r h_j}，B_box(v)=(max_l b_l+r h)ᵀv（v≥0）。先用共同r核对 union⊂box；再各自用past score和相同finite rolling（W四值×α四值）开发锁定覆盖方案。形状两边dev合格中最小化OD/路径等权mean[B_shape(v)−b̄ᵀv]，其中b̄为共同中心均值、属于conv{b_l}，这个support premium非负；不能用可能不在conv中的coordinate中点m作为union的共同基准。r_max在train冻结为25×Q_.99(train min-distance score)，零尺度时floor=0.01变换单位，两边共同使用。box r=0已有中心envelope core，若它覆盖已>.91，r≥0无法达到 .90±.01：报告无overlap，不靠test重调shape。双方都用发行时保存中心作本次反馈。原CPO实验Eq12用squared-L2，本适配用L2范数；若借前者quantile必须sqrt再作几何radius，不能混单位。

新的归因澄清是纸面身份：线性目标下 support(U)=support(conv U)。因此 union-vs-bounding-box 的作用来自共同几何约束/不同坐标极值不能同时发生，不能单独归因“非凸性”。同生成器形状比较有意义；原point-box vs完整generator的差只属于总方案。

可定义的低预算 sampler 实例是以合法已到达的完整残差向量作为 joint bank，按 train冻结的日历距离选择过去邻居、事前种子 resample，b=ĉ+ε_neighbor；S=10/50、5个事前种子，不能每边独立采样破坏joint结构。这个实例只能回答该bank下的几何价值。代表原CPO强模型的 conditional flow/diffusion 是否对目标E/clock可用、训练/采样预算多少，本轮仍未资格；静态软件入口不是已验证模型。

公开 robbuffet commit 01275c768dacd0be16cf28c391da99813ca14ff7 的 README/License/scores.py/calibration.py 本人已完整静态读：MIT、GPCP min-L2及UnionRegion接口存在；校准是batch且默认NumPy quantile，没有本方案pending ledger。需自定义issued封装/经验分位规则和对角变换，未安装/运行，未审全部region/optimizer。[固定版接口](https://github.com/yashpatel5400/robbuffet/tree/01275c768dacd0be16cf28c391da99813ca14ff7)

## 4. 真实资源资格：有实名路线，未获得主资源

拟定目标为 District7、PeMS单一处理版、2024-01-01至2024-07-28的210天（在未读数据前指定的候选期，不是已证实有合格样本的事实）。90train/30burn/30dev/60test按连续日期划分，E计划200–1000、12OD、K计划5–20；至少2条合格路径才入资格。train/dev地图和规则冻结V，不按test成本挑OD/E；缺connector或完整成本不能由静态TNTP、TLC端点或仅ML邻站图补成同一对象。

公开证据确实推进了字段理解。官方 dbt current stations 有 station_id、segment_start/end、length、freeway/direction、postmile与点geometry；SCD2 station_config有有效起止，给出历史配置入口。本人读其Description/全部Columns/Code：current表明确去掉有效起止且只留_valid_to is null；SCD2显示config log与current config按station_id合并，不能直接保证所有位置/方向字段都是当时vintage。有效时间也不等于可用时间。[current站点](https://cagov.github.io/caldata-mdsa-caltrans-pems/dbt_docs/#!/model/model.caldata_mdsa_caltrans_pems.geo__current_stations)、[历史配置入口](https://cagov.github.io/caldata-mdsa-caltrans-pems/dbt_docs/#!/model/model.caldata_mdsa_caltrans_pems.int_vds__station_config)

五分钟imputation mart给sample count、speed、health/imputation标记；sample_timestamp是区间起点，且该公开schema只保留ML/HV过去4天。它不是合格210天完整路网档案。官方处理说明日计算mart、坏/缺测补齐；health按全天判断、ramp不补齐。因此未知的available_at不能设成sample_timestamp，同日health不能直接作为事前feature。已读schema没有逐record available_at；不是证明全部内部系统都没有。[五分钟mart](https://cagov.github.io/caldata-mdsa-caltrans-pems/dbt_docs/#!/model/model.caldata_mdsa_caltrans_pems.imputation__detector_imputed_agg_five_minutes)、[处理链](https://cagov.github.io/caldata-mdsa-caltrans-pems/data/data-transform/)、[健康诊断](https://cagov.github.io/caldata-mdsa-caltrans-pems/data/detector-health/)

定向资源worker还完整读官方 SHN 2022-10-10抽取的方向linework schema：Direction、AlignCode、geometry与实际odometer起止，postmile不等于真实长度；nearby_stations只为同freeway/direction的imputation邻站。All Roads公开schema/CC BY4.0给方向道路几何候选，但不支持historic-moment且不保证完整/及时。这些是历史mapping路线，尚未构造任何两条逐边有成本的路径。[SHN字段](https://cagov.github.io/caldata-mdsa-caltrans-pems/dbt_docs/#!/source/source.caldata_mdsa_caltrans_pems.geo_reference.shn_lines)、[All Roads许可](https://caltrans-gis.dot.ca.gov/arcgis/rest/services/chhighway/All_Roads/FeatureServer/0/iteminfo)

PeMS官方支持十年以上archive与免费申请，通常1–2工作日审批，账号未申请；PeMS14曾重处理历史速度。资源worker读申请页：实时feed另有批准条件，免费web账号不证明获得实时feed。公开目录/表LAST MODIFIED也不是初次到达日志。[PeMS资源/版本](https://dot.ca.gov/programs/traffic-operations/mpr/pems-source)

完成主资源资格所缺的是四个可指定证据：本候选210天、单版本成本/质量文件的确切档案标识；与该期一致的覆盖段单位/方向/connector mapping；每OD至少2条逐edge成本可评估的具体路径；合法feed或保存发布vintage/到达账本，使a_jr/F_r可核对。存在官方schema及账号路线只能支持下一步资格检查，不能把这些未证实条件叫已qualified资源。

若没有真实vintage，Q5-R允许fallback为单版 completed archive、预声明δ=0/1/12/288 intervals揭示、c_j=length_j/max(speed_j,1km/h)；单位先统一为分钟。它只回答capped proxy与人工时钟假设下的回放，未完成主对象。observed-only是另一选择性target，不能把imputed成本叫真实行程ground truth。当前连完整历史mapping/210day已获档案也未落实，所以fallback也只是设计，不声称已可执行。

## 5. 执行 envelope：推算，不是实测或已获预算

所有数量按完整五分钟向量、12OD、K5–20、每路径h10–100个边的假设推算；真实缺测会降低有效数。CPU/GPU/elapsed与机器性能均未测，不读用户配置。政策是确定性序贯回放，复制种子不产生独立自然流。

| 项目 | 可审计工作量/存储 | 资格或遗漏 |
|---|---|---|
| 时间与样本 | 210×288=60480 origins；train25920、burn/dev各8640、test17280；post-fit34560 | 60day仅约8.6week；missing/arrival tail另减 |
| test锁定政策 | 17280×12×11=2,280,960个动作；K倍=11.405–45.619M候选访问 | 不是独立样本数 |
| 完整开发grid+锁定test | g=16时，207360×(12+10g)=35,665,920动作；K倍178.330–713.318M候选访问 | 包含burn+dev全grid；不额外test重新选frontier |
| 共享路径预计算 | post-fit的ĉ、c、2σ四张：4×34560×12×K×h=0.083–3.318B边加和；随后q组合为O(T×12×K×configs) | fixedσ实际可只算一次；score O(2TE)、DtACI4专家状态另计 |
| 原始矩阵 | 一张60480×E float64=96.768–483.840MB；cost+forecast+2σ=0.387–1.935GB | derived decimal单位，未含缺测/版本/clock/原始文件 |
| policy日志 | 最终11政策post-fit每scalar36.496MB；8scalar≈291.963MB | fullgrid若全存：每scalar285.327MB；专家ledger另计 |
| 同信息D/R learner | burn最多N_b=103680行，burn+dev最多N_bd=207360行；p约3E+K+context+共同history+8；开发12拟合，dev锁λ后4次refit，F≤1000pass为O(Fp(12N_b+4N_bd))，test O(4N_test p) | 收敛/有效标签未知；p~650–3100时全dense单设计约1.1–5.1GB，宜stream，tail/df不能假装等同 |
| frozen点预测 | 每link p_f≤20，train ridge累积O(E N_train p_f²)、solve O(E p_f³)，inference O(TEp_f) | train内模型差/合法lag仍需资源资格；不计为本轮训练 |
| PID scorecaster | 8个条件分位模型，burn每分支最多8640完整score行、p_s≤20；拟合O(8F N_burn p_s)，同α/σ的4个K_I共享 | 仅dev起点可见标签；burn用rolling qhat；优化资格/epoch未知，不能复制未来拟合回burn |
| CPO-style sampler | 每seed post-fit生成T×S=345600–1,728,000个完整vector；TE S=69.120M–1.728B元素；score同阶，路径support O(T S×12Kh)=0.207–41.472B边项 | S10/50、5seed则相应乘5；共享中心与path projection，box/union不各重生成；A仅I/diagonal有此score阶，dense A为O(TSE²) |
| CPO中心保存 | 每seed全存0.553–13.824GB；δ=288时pending float64上界约4.608–115.200MB | 保存vector IDs/种子/发行版本可减，但真实variable-delay无该上界 |

规划内存为8–16GB、稳定产物10–100GB（排除未获取原始档案、含5seed中心高端约69GB），这是工程预留条件，未查本机、未获预算。可stream序贯score与fit，避免全grid×E复制。CPU用以上工作量除未来实测吞吐估算；没有可移植的当前小时数。CPO原文的另一个任务/原论文CPU时间不能用于本E/S/grid。真实strong conditional flow/diffusion训练、采样调用、显存和模型资格仍未估得，不能用resampling的低预算认证strong替代已经包括。

若以后授权，第一段仅资格核查和静态适配预计1–3人日、ledger/对照实现与复核约2–5人日，是工作分解假设，排除账号/合作/vintage等待和实验执行时长。未知的vintage获得时间没有可诚实给出的上界。此轮没有运行任何benchmark、模拟、训练、评测、安装或付费服务。

## 6. 结果怎样改变研究，以及实际止点

| 将来的可区分结果 | 对应研究行动 |
|---|---|
| B1超过B0+且锁定policy在合格相近覆盖下有实际成本差 | 继续该条件下联合动态的信息/价值解释；进一步区分context代理与漂移机制，不称因果已识别 |
| 有policy差但B1无增量 | 保留政策比较，撤回凭policy差解释q/κ历史机制 |
| B0+/rolling/条件分位scorecaster足够或差小于实用阈值 | 采用简单现成方案，把贡献缩到必要动态的适用边界 |
| 同generator joint geometry比box有效而半径控制差小 | 转向几何价值解释；证据针对joint约束，不能说非凸性本身或所有dynamic无用 |
| 无coverage重叠、clip主导、无有效变化、极少active/有效天数 | 无识别或低power，改测量/资源；不把null或执行失败当机制反证 |
| 合法时钟/历史mapping无法取得 | 主自然流计划保持incomplete；archive假定delay仅为更窄代理问题，不替代主对象 |

Q7-A在比较操作、强对照、结果分支和工作量上有实质进展；**整体仍 incomplete**，原因是保留主对象没有已qualified的完整资源底座，strong生成模型预算也未资格。储备B的事前成本×尾结构归因继续partial，延迟/事件不升级第二成熟提案。Q6=not_applicable、Q6-P=skipped不变。下一步不是执行方便实验，而是在未来相应授权下按四项证据取得具体主资源资格；本轮到自包含partial报告后停止，不标记综合Q7-B完成。
