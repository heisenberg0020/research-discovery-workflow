# 两轮如何交接：脚本化演示

这里展示的是**两个有意编排的替代思路**，不是两个独立运行的证据。作者同时拥有全部文件，没有实施读访问拒绝、记忆清空或新会话隔离；下列“扣留”规则是对真实运行的示意，未在本包强制执行。第二轮无需更不同、更优或获胜。

## 共同输入与第一轮

两轮应使用同一个[中性简报](neutral-brief.md)（[English](neutral-brief.en.md)）及冻结工作流，不向第二轮提前传递第一轮的候选名称、原稿错误、排序或修订答案。第一轮通过 Q5-R、Q6 `not_applicable`、Q6-P `skipped`、Q7-A 后形成[最终解释](pass-1/final.md)。

第一轮的教学链为边际折扣 → 明确联合观测 → 修正未到达与及时后验 → 状态/内容分解；第二轮从条件内容价值出发。这样的差异是编排选择，不是独立发现、重复验证或工作流效果。

## 第二轮 Q0–Q4 的替代路径

Q0 不改变理论目标、收益、成本或数据范围。Q1-T 先问“购买决策到底比较什么价值”；Q1-U 先从及时子群的条件 VOI 开始。二者在真实运行中应先保存各自判断再交换，这里仅示意该逻辑。

Q1-S 连接条件化与获取价值：及时内容可能与普通信号不同，但购买的参照是原先无观测，不是已经知道 `R=1`。Q2 形成“条件内容账户”与“嵌套信息价值分解”两个对象。Q3 写出 `D_timely` 并追踪信息时序。Q4 保留完整贝叶斯为强比较器，初步识别需要状态控制，但将原始遗漏留到 Q5-R 以展示修复，而非假称已经正确。

## 第二轮 Q5 → Q5-R

[Q5 原始快照](pass-2/q5-original.md)把 `p·D_timely` 当总毛价值。它比第一轮原稿更重视及时条件分布，却遗漏状态价值；这种局部改善不能证明第二轮更好。

[Q5-R 回顾与修订](pass-2/q5-repaired.md)发现购买目标与行动目标不一致，修订成 `(VR−V0)+p·D_timely`，并用 `R=1[Y=1]` 的解析模型检验。原稿与修订分别保存。此节点之前，真实第二轮应没有收到任何第一轮研究输出；此包由于是编排材料不能主张实现了这一历史事实。

## 只在 Q5-R 之后交接的显式包

示意允许复制到第二轮 handoff 区的文件**恰为**：

1. `pass-1/q5-repaired.md`：完整机制、充分条件、反例与所有解析对照。
2. `pass-1/final.md`：比较设计、资源资格、推导工作量与结论边界。
3. `sources.md`：当前包使用的公开原文、位置与阅读深度。

不复制整个第一轮目录、私人历史项目、模型配置或未列结果。第一轮没有真实实验，因此不存在可以虚构交接的实验日志。原始快照仍供读者审阅，但不在本示意的先前成果交接名单中。实际实现时文件复制不是自动授权读其他材料，目录也不是安全边界。

```text
真实运行应有的输入边界（本材料未强制）
pass-2/independent/  ← 共同中性简报、冻结工作流、当轮公开资料
Q5-R 完成
pass-2/handoff/      ← 上述三个显式文件
Q6 与以后            ← 已暴露的、知情合并上下文
```

## Q6：逐声明协调，不投票

| 声明 | 包内比较 | 交接后的变化 |
|---|---|---|
| 普通 VOI 的边际折扣 | 第一轮修订有共同独立擦除的充分条件 | 第二轮采用该推导；不将条件升级成必要条件 |
| 及时子群内容的条件化 | 第二轮明确写 `D_timely`；第一轮完整公式已包含它 | 两种表达代数相同，撤回独立新方法身份 |
| 状态价值 | 两轮修订均用 `VR−V0` | 保留同模型状态控制，无新增经验支持 |
| 比较方案 | 第一轮已经提供八单元与 81 核的具体工作量 | 保留更完整的第一轮方案，不因为它较早而淘汰 |

无真实观察可作为增量证据；两轮重用同一公开文献与人为模型不能算独立确认。合并结果保留第一轮完整联合质量表达，以第二轮的“内容相对于已知状态”表达帮助教学。合并是表达与解释的协调，不是把两个模块拼成新算法。

## Q6-P / Q7-A / Q7-B

Q6-P 继续 `skipped`：解析推导已经辨别这两个错误普遍声明，没有启动试验的理由或授权。Q7-A 保留[第一轮四问计划](pass-1/final.md)：完整贝叶斯为强比较器，八单元对象与策略集合是合格形式资源，81 核枚举仅作未执行的核对计划，9,396 是推导贡献次数而非测量运行时间。主理论目标没有改变，真实应用资源仍不合格。

Q7-B 的实际可用综合是：用 `Z` 的最大期望收益给购买定价；在共同独立擦除下使用简化；通过 `V0→VR→VZ` 解释收益来源。任何方案在相同真实模型与可见信息下都不能超过 `max_δ E[u(δ(Z),θ)]`。剩余有意义的形式工作是整理更弱的相等条件，并核对有限策略实现；现实应用需另行模型辨识。最终结果不要求选择第二轮候选。

该材料完成了脚本化交接解释。没有完成两个独立运行、工作流有效性验证、经验复现或现实收益测试。

## English handoff notes

This is a scripted teaching demonstration, not two independent runs. In real use, pass 2 receives the same [neutral brief](neutral-brief.en.md) and frozen workflow, but no pass-1 outputs before its own Q5-R ends. The directory does not enforce withholding or clear memory.

Only after that point, the illustrated authorized packet contains exactly [pass-1/q5-repaired.md](pass-1/q5-repaired.md), [pass-1/final.md](pass-1/final.md), and [sources.md](sources.md). It does not contain the whole prior workspace. Before handoff, pass 2 repairs its own omitted status value; afterward, Q6 compares claims and retains the stronger complete pass-1 design. Pass 2 need not win, and shared sources do not count as independent confirmation.

Q6-P remains skipped. Q7-A retains the finite formal plan; the 81-kernel grid is not executed. Q7-B explains the actual observation, applicable shortcut conditions and status/content decomposition without claiming empirical benefit, novelty or workflow effectiveness. The [English walkthrough](README_EN.md) gives the full mathematical route.
