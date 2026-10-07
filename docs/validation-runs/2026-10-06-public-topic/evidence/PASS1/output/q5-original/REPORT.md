# Q5独立原稿：共同漂移下，覆盖盒改变动作是否真的昂贵？

2026-10-06；原稿保存后不再改写。无旧材料，尚未Q5-R。完成的是公开文献/纸面机制与规划，不是科学效果实验。

## 研究核心

现有答案不是“校准只能保证覆盖”。ACI/DtACI/PID已分别反馈总体误差、组合步长或预测残差；CDT/Rolling RC已有直接有界风险反馈。针对predict-then-optimize，Dronavajjala2026给出盒式robust决策的精确单轮开关κ以及稳态摘要m。我们拟研究的是：在自然时间流中，校准半径与决策几何一起漂移时，静态“free/critical/costly”标签在什么条件下足以解释**实际相对成本**，什么时候还必须看残差的方向与漂移响应。目标是条件解释/价值研究，而非再发明κ或新的反馈组合。[开关原件](https://proceedings.mlr.press/v329/dronavajjala26a.html)；[DtACI](https://www.jmlr.org/papers/v25/22-1218.html)；[CDT](https://arxiv.org/html/2310.05921v3)。

这个区别可能影响预测服务是否需要更复杂的动态校准、还是更好的集合几何/预测器。但实际高损失是否足够多、能否被简单方法解释，本轮没有效应数据。已有CPO用条件生成样本构造union-of-balls并robust优化，其静态交换性条件和continuous可分流行动与我们有限单路径动作不同；不能当作弱盒对照。[CPO §3–4/Appendix A/B](https://proceedings.mlr.press/v238/patel24a.html)。

## 操作、对象与时序

动作t前看到历史H_{t−1}、当前context，生成ĉ_t、σ_t>0、q_t≥0，issued盒U_t={c:|c−ĉ_t|≤q_tσ_t}。在事前固定有限路径V={v_1,…,v_K}内，x^0=argmin ĉᵀv，x^q=argmin(ĉ+qσ)ᵀv。nominal唯一且无threshold tie时，已有κ=min_{δ>0}Δ/δ，Δ=ĉᵀ(v−x^0)，δ=σᵀ(x^0−v)，J=1{q>κ}；固定tie规则，零Δ另记。全图证书不由有限V给出。

观察全向量c后算score=max_j|c_j−ĉ_j|/σ_j与issued误差，再更新尺度/quantile。定义d=x^q−x^0、ε=c−ĉ，实际premium R=cᵀd=ĉᵀd+εᵀd。R可负，hindsight regret G=cᵀx^q−min_V cᵀv≥0。robust目标值、J与R/G分别报告，不把改动作叫成本。覆盖事件只给|εᵀd|≤qσᵀ|d|。

纸面构造（未运行）：ĉ=(M,M+Δ)，σ=(a,b)，a>b>0、q>Δ/(a−b)、M>qa，则robust从动作1变2。c^-=(M+qa,M+Δ−qb)和c^+=(M−qa,M+Δ+qb)均被issued盒覆盖，却R^-=Δ−q(a+b)<0、R^+=Δ+q(a+b)>0。同一几何和覆盖可对应相反损益，这是对象区别，不是新定理或反驳worst-case目标。另一个两轮q=(1,3)、κ=(2,4)/(4,2)说明边际摘要不能固定联合crossing；不声称这些是同一ACI可达轨迹。

## 两个解释与对照

H_geom：稳定几何近临界与盒方向已足够，静态m/官方直接neutrality能描述成本；更强非盒几何会使控制动态研究应用价值变小。H_joint：q与κ共同运动、阈值跟随滞后及ε方向聚集会形成静态摘要遗漏的局部损失，在相同预测、路径、信息下改变控制动态仍会改变成本frontier。

固定forecast和V，不重训来给某控制器额外信息。rolling quantile/ACI/DtACI/PID都用相同已到达历史；开发期调α/γ/window/expert/predictor，test不调。每个方案另有固定σ_dev与动态共享σ分支。只比较coverage、集合代价frontier重叠档的R/G，不把一个差步长当全部ACI。漂移分层用预visible日历、开发定义的state rule或未看test cost的外部事件；如果test没有预声明条件，仅报无识别证据。每轮exact κ是几何核对oracle，不能作为预测J的“新模型”。静态m与joint描述预测未来R风险时信息与刷新频率一致，容量匹配。移位打乱q/κ只作关联敏感性，不作自然反事实。

作者官方main代码的静态检查发现：动作采用pre-update radii，coverage却可在score插入buffer后计算。原件core文件可用past=[0,0,0,0,1],α=.1,s=.7纸面追踪：linear q_pre=.6 miss，q_post=.85 covered。未来必须freeze issued q/σ；这只定位本次读取实现的接口，不否定论文全部实验或推断所有脚本相同。原文件保留作基线描述，不在本轮执行或修改。

## 资源与分阶段计划

拟用Caltrans PeMS一段单版本180天、5min站点speed/quality/missingness/metadata，选200–1000个可对齐freeway links及12组OD；成本定义为link长度除以同刻sensor speed的**代理**，不是实际行车干预结果。需至少两条可行替代路径、站点地图一致、quality/观测字段、稳定发布版本。PeMS官方提供免费申请与archive，但本轮未申请/下载；获取与合格字段是conditional，不用TLC起终点数据冒充全路网成本。[PeMS 官方](https://dot.ca.gov/programs/traffic-operations/mpr/pems-source)；[处理文档](https://cagov.github.io/caldata-mdsa-caltrans-pems/data/data-transform/)。TNTP只能回答静态网络/建模问题，不替代自然漂移流。

90天train、30天dev、60天heldout test，另切30天burn-in只用于启动；路径V在dev固定。E=200–1000、T=180×288=51840，cost matrix float64约83–415MB（推算非实测），含metadata/controllerlogs约1–3GB预留（假设）。K=5–20条/OD，候选内vector dot，不需要全图vertex enumeration；工作量至少12×17280×(1+4×2)≈187万组路径评估，乘K/E稀疏support与开发网格；未测CPU时间，不承诺小时数。CPO强几何对照可先在同有限V用生成样本求max+balls robust成本；训练/生成预算需另外确认，不能声称已具实现复现。

第一步未来授权后资格检查字段与路网（本轮不执行）；第二步完整issued事件接口核对；第三步冻结比较与temporal splits；第四步执行未来实验并比较matched frontiers和分层R/G。若强简单rolling/PID与静态标签足够，采用现成方案、只保留解释边界；若联合动态改善heldout损失并超过same-information静态对照，继续机制研究；若只有coverage不同，撤回动态归因；若没有有效漂移/样本，维持未知而非宣布假设死。

## 其他候选、状态与未完成

T-A/U-A产生另一归因草图：不对称成本的动作分位数τ=c_s/(c_s+c_d)与残差尾预测；让校准器独占z信息会不公平。可比较同信息conditional基分布、tail+反馈、COP及直接决策校准，但缺合格的事前成本/输入vintage/结算联合资源，故储备partial，不伪装成熟方案。

T-B延迟有限界后来遇到2026-09 arXiv2609.07251v1相位递推与显式界，已有更强答案；相位重置与全局累加旧error不是同一控制器，原多步界疑点待核，不开发成“首次延迟”提案。事件无偏和action-conditional邻居仍有闭环/选择反馈理解缺口。

工作状态：Q0–Q4公开探索/展开已做；Q5原稿形成。主候选机制明确，实际效应与新颖性未验证；资源与CPO实现预算conditional、部分实证细节待审。Q5-R尚未做；无旧材料，Q6将not_applicable；无实验或效果数字。本轮没有科研成功承诺。
