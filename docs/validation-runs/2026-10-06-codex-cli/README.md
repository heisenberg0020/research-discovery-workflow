# Codex CLI 实测与可复核行为试走

[English summary](#english-summary) · [固定方案](PROTOCOL.md) · [语义复核](ASSESSMENT.md) · [输入摘要锁](INPUT_LOCK.json) · [重现说明](REPRODUCE.md)

2026-10-06，在 macOS 上使用 Codex CLI **0.160.0** 和已有 ChatGPT 登录，对仓库 v1.2.0 分发的 **Workflow v1.0.0** 完成一次小范围客户端与行为检查。六次主调用各执行一次，全部正常退出，未重抽、重试或改动冻结 Workflow。

这次新增的是**实际运行证据**，不再仅是作者编写的教学轨迹。但输入仍是专门构造的虚构有限问题，不是现实论文、真实数据或随机研究任务；没有检验科研选题质量。

## 结果先说清

| 检查 | 实际观察 | 证据与边界 |
| --- | --- | --- |
| L0：读取入口 | 只给 Skill 名称后，执行器定位并从本地读取入口、八份引用与准备器源码，没有启动研究 | [最终回复](evidence/L0/final.md)；证明名称调用下的实际读取路径，不能仅靠磁盘读取认证内部注册机制 |
| B1：首次无旧成果 | 两状态报告都完整识别状态，保留具体解码与 `min{4,c_q,c_b}`；保存原 Q5，做分开的实际澄清；Q6 不适用后完成比较与对话说明 | [最终回复](evidence/B1/final.md)；[比较计划](evidence/B1/output/first-pass/Q7-A-plan.md)；没有强迫发明新方法 |
| B2-pre：旧包未交付 | 发现 `5q` 漏中心，修订为 `20+5q`；原损失 400 / 含费 401，修订含费 1；原稿未变，停在 `pending_handoff` | [最终回复](evidence/B2-pre/final.md)；[真实修订](evidence/B2-pre/output/q5-repaired/REPORT.md)；[交接回执](HANDOFF_RECEIPT.json) |
| B2-post：延迟交接 | 只收到指定旧包后补入同费用直接报告对照，承认旧包已有正确机制；不将重合当独立确认或制造新算法 | [最终回复](evidence/B2-post/final.md)；[合流分析](evidence/B2-post/output/continuation-v2/RECONCILIATION.md)；前阶段五份文件保持原字节 |
| B3：主问题资源缺口 | 区分数学表示等价与真实操作员收益；给出 q/r/x 三组和标签要求，但不把未识别人群、设备与测量条件说成已就绪 | [最终回复](evidence/B3/final.md)；[部分计划](evidence/B3/output/PLAN.md)；Q7-A 与完整 Q7-B 未完成，是正确的部分交付而非加载失败 |
| B4：最终洞察说明 | 对话本身解释机制、强替代、成本边界和结果决策；粗报告使用合法整数动作 1，不误用条件均值 4/3；155 策略 / 465 项只是未执行工作量 | [最终回复](evidence/B4/final.md)；[比较核对](evidence/B4/output/comparison-audit.md)；没有伪造历史探索或经验效果 |

逐观察采用 demonstrated / inconsistent / unobserved / not applicable，而不是用标题匹配打一个总分。实际产物和事件顺序支持以上科学内容与状态处理；**独立子代理创建及强隔离仍未得到充分可观察证据**。执行器正文声称使用 `fork_turns=none`，日志有部分等待事件，却没有明确的创建调用。不能把自述升级为已认证的独立性。

## 这轮说明了什么

第一，科研机制能进入最终交付，而不只存在于提纲：B1 保留两个动作函数及成本选择；B2 真正改了消费操作，不是只补一句风险说明；B4 将局部成本差补成三方选择边界。

第二，流程能接受“简单已有答案已足够”。两个形式题都没有新算法需求。最终解释仍然有内容：哪些收益属于信息、哪些属于表示、什么条件会改变决策。不能把没有新算法误记为探索失败，也不能把这样的教学推导当现实新颖成果。

第三，本次未经现场指导的 B3 没有重复首版开发记录中“局部形式证明替代整体经验就绪”的错误。它还补出了读数规则错误与真实设备状态错误的区别。这个观察支持该小场景的状态边界，**不证明此类错误已普遍消失**。

第四，输入隔离与宿主独立性是不同证据。旧包确实未复制入 B2-pre 工作根，并在检查其修订后才交付；这证明本次包的交接顺序，不证明旧目录不可读、系统记忆关闭或所有子代理未接触其他上下文。

## 留下的失败与未覆盖项

- L0 的读取输出有 `xcrun` 临时缓存创建被只读沙箱拒绝的警告；后续直接读取完成，调用最终退出 0。保留原警告，不把它删除成全程无误。
- B2-pre、B3、B4 初始清单命令曾因 `output/` 尚不存在返回 2，之后正常建档并完成。它们是局部命令错误，不是科学阴性或整次调用失败。
- 所有主调用 stderr 均有客户端状态数据库的查找回退警告。原日志保留本地；公开记录不导出诊断性私人路径。警告不能证明读取了私人科研内容，也不能被忽略成“清空全部历史已验证”。
- 未测 Codex 桌面 GUI、Claude Code、Cursor、Windows 客户端、真实检索、全文获取、真实资源资格、新颖性和两轮优越性。
- B2 是一个晚阶段旧包续接，不是两次从 Q0 开始的完整独立研究；B4 的路线历史是输入中的作者重构，本次没有补造过去的独立执行证据。
- 使用客户端默认模型，没有模型覆盖；该日志未给出足以确认的实际模型名称，身份记为未知。

## 时间与客户端所报用量

| 主调用 | 秒 | input | 其中 cached input | output |
| --- | ---: | ---: | ---: | ---: |
| L0 | 52.704 | 143,911 | 115,840 | 1,429 |
| B1 | 382.631 | 1,177,392 | 1,122,944 | 10,916 |
| B2-pre | 129.894 | 222,681 | 195,456 | 4,182 |
| B2-post | 149.182 | 222,675 | 186,496 | 4,848 |
| B3 | 115.912 | 115,094 | 91,776 | 3,900 |
| B4 | 142.138 | 123,936 | 87,680 | 4,828 |
| 所报字段合计 | 不相加为墙钟时间 | 2,005,689 | 1,800,192 | 30,103 |

输入包含缓存部分，**不能再把 cached input 加一遍**。六份主会话字段的 input+output 算术合计是 2,035,792；原生子代理独立用量未闭合捕获，是否已经计入未知，因此这不是全部实际成本或账单。reasoning-output 字段原样留在各 `usage.json`，不再次加进总数、不发布推理文本。并行调用的耗时不能直接相加作为用户等待时间。

用量不小，尤其 B1；这套 opt-in 试走会消耗真实客户端额度，不应误当无模型调用的单元测试。没有配置额外 API key 或付费 API；沿用已有 ChatGPT 登录。

## 如何核查证据

每个 `evidence/<case>/` 保存执行提示词、调用参数、退出状态、客户端所报用量、脱敏最终回复、相关 completed 事件及产物。`export.json` 记载原件摘要、替换与遗漏计数。原始 stdout/stderr 保留在本地忽略目录，不放入发行包。

公开文本是**机械脱敏副本**，不是字节相同的原日志：个人路径和动态标识替换为稳定标签；本地 Markdown 链接转成文字路径；隐藏 reasoning、开始/中间状态与无关诊断不导出。保留科学数值、输出、局部错误与阶段顺序。脱敏工具没有资格证明任意原日志都不存在敏感信息，发布前仍做本范围人工检查。

方案先确定六类调用。L0 先执行，随后在 B1 等行为调用启动前补齐公开父 `AGENTS.md` 的披露和结构化观察说明；这个时序见 `INPUT_LOCK.json`，不冒充所有文字都在 L0 前锁定。测试工作根位于本公开仓库的忽略 `runs/` 子树，可能继承公开父指令；执行器未收到此协议、判定标准、兄弟案例或未交付旧包。

B4 的末尾 `git status` 还看到了父公开仓库的 `docs/validation-runs/` 改动目录名，没有读取协议或判定内容。这也是公开仓库元数据仍可见的具体边界，不能称为完全空白的文件环境。

## English summary

Six one-attempt Codex CLI 0.160.0 invocations on macOS finished with exit 0 using an existing ChatGPT login. The frozen Workflow was not changed. The fictional cases demonstrated local entry/reference reading, first-use handling, actual paper repair before a delayed handoff, honest main-resource incompleteness, and substantive final in-chat reporting.

Disk access does not certify internal auto-registration. Child creation/isolation was not sufficiently visible in the captured trace; claims in executor prose are not independent verification. No GUI/other-host certification, real research efficacy, novelty, retrieval quality, or two-pass superiority follows. Reported primary-turn usage is retained without double-counting cached input and without claiming closed child costs or billing totals. Public evidence is sanitized, with transformations and omissions declared.
