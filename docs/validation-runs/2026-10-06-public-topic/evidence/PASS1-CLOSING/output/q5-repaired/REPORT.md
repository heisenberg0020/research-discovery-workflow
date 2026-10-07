# Q5-R修订提案：几何已知之后，过去动态还解释多少实现损失？

2026-10-06。原稿 `../q5-original/REPORT.md` 保持不变；fresh评审见 `../q5-review/REVIEW.md`。本稿是本轮独立范围内的纸面修订，没有旧材料、数据实验或数值复现。

## 研究核心与实际成熟度

现有盒式predict-then-optimize答案已经能精确判断一个给定半径会不会改变动作：比较q与几何开关κ即可。稳态m把一段半径波动压成摘要；它不是已建立的实际成本预测器。我们保留的主问题是：**在自然时间流的全信息成本决策中，当前已知动作/几何之外，过去半径响应和方向残差是否还能提供可重复的未来损失信息；有限输出控制政策的差异是否有实际价值？** 不是首次决策校准、不是新κ，也不是以动作改变证明代价。[Dronavajjala2026 §3–4](https://proceedings.mlr.press/v329/dronavajjala26a.html)。

研究将严格分成几何身份核对、未来损失信息比较和外生成本流政策比较。前者属于既有结论；后两者若有合适数据与稳定heldout效应，才可能产生新的条件解释。主实证资源仍未资格完成：PeMS说明支持传感器档案/速度/metadata，但完整路径成本、真实发布vintage与合格替代路径未落实。定稿档案的假定时钟回放只能回答更窄的代理问题，不完成实际在线自然流主对象。整体是**明确提案、资源与验证partial**；不因纸面接口修好就称经验成熟。

## 1. 决策映射、损失与既有几何

令V={v_1,…,v_K}⊂{0,1}^E为开发期冻结的候选路径；P=conv(V)，非负有限路径。发行前已知ĉ_t、σ_t>0与有限q_t≥0。U_t={c:|c−ĉ_t|≤q_tσ_t}，x^0_t=argmin_V ĉ_tᵀv，x^q_t=argmin_V(ĉ_t+q_tσ_t)ᵀv；固定字典序tie。对唯一名义点，Δ_{tk}=ĉ_tᵀ(v_k−x^0_t)、δ_{tk}=σ_tᵀ(x^0_t−v_k)，κ_t=min_{δ>0}Δ/δ，min∅=∞。q=κ、零Δ另记tie，不把严格不等式用在边界；有限V的κ不认证全图。

当q≠κ，J_t=1{x^q≠x^0}=1{q>κ}，是已有身份。令d_t=x^q−x^0，观测c之后ε_t=c_t−ĉ_t；R_t=c_tᵀd_t=A_t+D_t，A_t=ĉ_tᵀd_t在发行前已知，D_t=ε_tᵀd_t事后才可见。R负值代表相对名义动作改善，G_t=c_tᵀx^q−min_V c_tᵀv≥0是另一个hindsight对象。若d=0，则R=D=0，不能作为模型学出的收益。robust目标值、J、R/G、issued coverage分开；覆盖只给|D_t|≤q_tσ_tᵀ|d_t|。

纸面构造保留：ĉ=(M,M+Δ)、σ=(a,b)，a>b>0、q>Δ/(a−b)、M>qa。robust选动作2；同盒内c^-=(M+qa,M+Δ−qb)给R^-=Δ−q(a+b)<0，而c^+=(M−qa,M+Δ+qb)给R^+=Δ+q(a+b)>0。没有执行模拟；这是语义代数，不是novelty或efficacy证据。q=(1,3)与κ=(2,4)/(4,2)的两轮边际相同例只说明一般预visible半径下joint关系不可由marginals确定，不宣称同一ACI能生成它们。

### 静态m的合法分支

不得对含κ=∞的混合直接算Eκ再将m=∞叫“从不切换”。报告p∞与有限κ分布；∞状态下有限q不改变名义动作。m=(Eκ−q*)/sd(q)只在有限矩、sd(q)>0且κ变动相对小的近稳态子流中使用。Gaussian与独立近似若满足，可用(1−p∞)E[Φ((q*−κ)/sd(q))|κ有限]；它仍是近似，不升级为漂移保证。sd(q)=0时直接比较固定q与κ，不除零。所有估计只用已可见past窗口；官方全pilot预测均值/最终σ属于事后诊断，不能在test未来窗口预测中使用。

## 2. 有限输出政策接口（修F1）

科学比较针对**有限盒操作变体**。原ACI/PID允许全/空集合或无穷阈值，不能把q=0冒称空集，也不能把∞盒一般robust目标当有限唯一动作。本方案开发期固定共同q_max、σ floor以及empirical quantile规则；所有实际输出q=clip(q_raw,0,q_max)，所有反馈用实际issued q/σ。因裁剪与后述到达更新，原任意序列精确coverage保证不自动继承；报告α边界命中、半径clip率与实际覆盖。原无限输出版本可作独立coverage参考，不能混入有限成本frontier。

每个σ分支分别维护同单位scores：固定σ_dev取train/burn-in residual尺度；动态σ_t为相同ĉ误差的EMA+固定floor，独立于每控制器q，故同分支控制器共享σ。发行时保存forecast、σ、q、专家集合、generator centers。观察s=max_E|c−ĉ|/σ_pre后，先判断所有实际issued事件，再更新σ并append s；历史score不重新用新σ或重训forecast改写。

| 有限操作变体 | 状态、raw输出与观察后的操作 |
|---|---|
| Rolling | past W个完整issued scores，q_raw=Q_{1−α}(past)，输出clip；append后才可影响下一轮。Q用事先冻结的经验分位数inverse-CDF规则，ties包含≤，不混linear插值。 |
| QT | q_raw状态u，输出clip(u)；完整反馈后u←u+η(e_issued−α)。clip不回写u，另记saturation；u可有限时间漂移，不给覆盖证明。 |
| ACI-style | 状态a∈[a_min,1−a_min]；q_raw=Q_{1−a}(past)，输出clip；a←clip(a+γ(α−e_issued),a_min,1−a_min)。a_min开发冻结；此投影版不冒称原ACI定理。 |
| DtACI-style | γ_i专家各有a_i，上述同一有限family产生各issued q_i，确定性输出ā=Σp_i a_i对应有限q（不是平均半径）；完整反馈算各自e_i并更新a_i。权重按exp[−η_w ℓ(β,a_i)]再fixed-share ξ/L混合，ℓ(β,a)=α(β−a)−min(0,β−a)。β以保存的发行前empirical family反演，未覆盖任何允许level置0、覆盖所有置1、ties固定。clip使pinball/真实miss关系可能不再等价，故明确是有限操作适配，不移交DtACI原regret/coverage定理。使用log weights避免算术下溢。 |
| PID-style | 过去可见s的分位scorecaster qhat（仅lags、日历、σ/forecast摘要）；n个已完成反馈E_n=Σ(e−α)，q_raw=qhat+K_I tan(E_n log(n+1)/(C_sat(n+1)))，argument越界取signed∞再clip。qhat至少与rolling、same-information条件分位简单替代比较；参数/刷新预算开发冻结，不称首次scorecaster+feedback。 |

候选grid和初始化在Q7-A固定，不以未来cost决定q_max；固定/动态σ支不可交换旧q或按数值q直接比较physical width。引用依据为[ACI §2/4.1](https://papers.nips.cc/paper/2021/file/0d441de75945e5acbc865406fc9a2559-Paper.pdf)、[DtACI Alg1/2](https://jmlr.org/papers/volume25/22-1218/22-1218.pdf)、[PID Eq5/Thm1](https://proceedings.neurips.cc/paper_files/paper/2023/file/47f2fad8c1111d07f83c91be7870f8db-Paper-Conference.pdf)。借用这些机制，不包装新算法。

## 3. 两个竞争解释，三类不同证据（修F3）

H_sufficient：当前forecast、实际选定d、A、路径gap/半径及预声明context已充分，过去动态没有有意义的额外损失信息；盒几何或预测器可能才是大头。H_history：在这些事前状态之外，过去已到达的方向残差及q/κ变化仍预测D的条件位置或尾部，且一些有限政策差异有稳定成本后果。它们可以在不同条件共存。本轮没有已测effect。

1. **几何核对**：计算每轮κ/J，仅检查issued身份；m和past neutrality预测未来12个5min起点的切换频率，是既有摘要的适用性研究，非创新的J模型。test整段均值不作输入。
2. **未来损失信息**：主要target为下一发行动作实现的D_t，以及R_t=A_t+D_t，先按OD等权聚合再对day分块。不只让m预测cost。B0拥有当前ĉ/σ/q/d、A、gap/physical path radius、日历及共同可见历史的简单last-window directional residual mean/tail；B1额外刻画past q/κ变化、有限κ分位与directional residual趋势/交互。same-model容量、输入维度及调参预算匹配，对新增feature另以过去已可见、不涉及future的时间-shift placebo作敏感性。比较development冻结的heldout squared/pinball loss(0.9tail)和预测tail校准；当期ε只作事后分解，不能feature。胜出只支持额外信息，不单独证成某一种漂移因果链。
3. **政策价值**：同一个外生完整cost流，frozen配置比较nominal及所有有限政策的cᵀx、R/G、coverage和path radius。dev选取coverage目标0.90、容忍±0.01下集合代价最低配置（每方法共同grid预算）；test不再次选最有利frontier点。全test frontier只描述。无coverage重叠或clip主导则不作equal-coverage价值主张。固定σ是不同score单位/政策的对照，不能独自当“尺度运动因果效应”。各OD共用cost流，不能当12份独立复现；日历周block不确定性与分OD可迁移性分开。

有辨别力的结果：B1增量信息与policy成本差都成立，才继续联合动态解释；只有policy差而B1无增量则只知方案不同，不知机制；B0/rolling足够则采用现成简单解释/控制；只换geometry有效则转向形状价值而不否定动态在别处有用；无漂移/缺标签/低power保持未知。阴性结果不会被重抽成正向。

## 4. 非盒强替代的确切有限V适配（修F5）

CPO已经用条件生成器与非凸集合，不是uniform-box。有限路径适配只借其score/支持函数，非原continuous allocation复现。[CPO §3–4与App A/B](https://www.ambujtewari.com/research/patel24conformal.pdf)。发行前冻结生成器给b_{t1:S}；选择预visible可逆A_t（第一版A=I或train对角尺度），score=min_l||A_t(c−b_{tl})||_2，past issued scores得到r_t。U=∪_l{c:||A_t(c−b_{tl})||_2≤r_t}。

对每个v∈V，未截断集合的support B_t(v)=max_l b_{tl}ᵀv+r_t||A_t^{−T}v||_2，取argmin_V B；固定tie。例：A=I、v=e_1时B=max_l b_{l1}+r，两个路径直接算两种support后选，中心/半径只在反馈后更新。正成本实际数据可以在数学uncertainty集合中允许负lower corner；如另截c≥0，则必须重算support，不能沿用公式。

**geometry层**让同生成器、同S、同信息/刷新给盒envelope u_j=max_l b_{lj}+r||(A^{−1})_{j,:}||_2，其nonnegative v支持uᵀv；这是union的bounding box、coverage可更多，先报告containment差，再用各自past score校准matched-coverage frontier。另报original point-box vs full generator方案时，只归因总方案而非shape。生成器是否准确/预算多少未知；第一阶段可用past同日历状态残差条件resampling作为廉价CPO-style实例，不能用它的失败否定原论文更强flow/diffusion生成器。原静态exchangeability保证不移交自然漂移；本研究测实际issued事件。

## 5. 资源时钟、资格与保留的主要缺口（修F4）

保持主要对象为自然时间流的全信息决策；不把静态网络/随机生成轨迹补成它。PeMS可提供真实传感器archive，但其completed/imputed proxy不等于实际行车counterfactual。拟选District7一段固定版本210天、5min速度与station/direction/metadata；E/12OD/V只用train/dev地图与规则冻结，必须至少两条合格替代路径。length与station覆盖段对应、direction/connector、sample/observed/imputed/health及处理版本是具体资格门。GIS入口本轮返回空文本；不声明已经得到可用mapping。

时钟必须记录 origin o=end(interval t−1)，target interval t（h=1个5min），measurement time r、实际available_at a_{jr}，完整向量最早反馈F_r=max_j a_{jr}。所有issued预测/集合和专家事件存pending，只有全向量到达才更新。variable delay时采用显式arrival-ledger有限变体：按已到达origin顺序算保存的issued events，更新当前state；不是发行参数相位重置的τ-DACI，不借其证明。missing全向量暂pending，不偷填即时标签。若最终某target未补全，覆盖/损失不可评估并报告所影响比例/选择，不重新选test E来优化。

若无真实发布vintage，允许的fallback仅是单版本completed archived proxy按预声明δ=0/1/12/288个interval揭示；其cost=c_j=length_j/max(speed_j,v_min)，v_min开发前选定物理floor（第一版1km/h），补齐字段必须已有explicit flag，不以未来test结果重补。此时研究的是**该揭示假设与capped proxy下的序贯回放**。它保留方向/半径关系，但不完成主要实际在线时钟主张。health按全天判定，不是事前feature；observed-only敏感性属于不同target/选择，不能混为真实ground truth。

90train+30burn-in+30dev+60test=210天。forecast train拟合后冻结；每candidate配置用同burn-in独立启动，dev后不reset而连续进入test，只有允许的在线反馈更新；dev之外参数不调。完整cost matrix E200–1000、60480行float64≈96.8–483.8MB，多个sigma/policy日志/centers另计。CPU/内存、generator工作量、uncertainty与compute资格详见Q7-A；这些是推算计划不是实测。

## 6. 储备、修订史与验证

储备B（成本分位数×同信息tail归因）依然partial，缺合格联合资源与相关决定性深读，不因A修好而成熟。延迟/事件没有被硬做成第二个候选：2026-09 τ-DACI已有相位界，其方法与global-arrival递推不同；不宣称首次延迟处理。

原稿→评审→实际改变：有限q与列举控制器输出不兼容→增加finite variants、clip反馈与撤回继承保证；m混∞/零方差未定义→分支而非错误标签；弱m cost对照/政策差直接解释机制→三证据层和strong cost predictor、dev冻结、dependent OD账本；PeMS未明时钟/210day歧义→available_at/pending规则、主资源partial、fallback界限与210day明确split；CPO操作/模型预算不清→精确support+same generator geometry对照。

纸面核验：主worker读完fresh REVIEW，再复读本修订科学内容；检查两行动R符号、覆盖D上界、finiteq下κ∞不切换、zero sd分支、miss使ACI水平下降/QT阈值上升/PID积分上升，DtACI专家feedback各用自己的issued集合，union support和envelope维度一致。还重新读取JMLR原Algorithm1/β/ℓ及PID Eq5/Thm1，未执行代码。修复了操作/语义与比较，不证明经验效果、因果识别或新颖性。主数据资格与实际clock、nonbox强模型执行预算未完成；Q5-R完成的是reviewed partial提案。
