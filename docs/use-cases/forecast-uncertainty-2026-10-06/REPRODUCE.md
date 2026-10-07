# 如何再使用这个公开专题

本次输入是 [BRIEF.md](BRIEF.md)，摘要与冻结版本见 [INPUT_LOCK.json](INPUT_LOCK.json)。它不包含先前候选、指定论文、预期答案或具体方法名。执行范围仅为公开材料调研、纸面构思和 planning；不是获准运行实验的入口。

以下是未来重新使用时的预定方法，不是本次全部成功的声明。本次实际为第一轮主资源不足的 partial 收尾、第二轮 Setup 暴露停止；用户选择不重做，也未执行双轮合流。参见[案例状态](README.md)与[中断记录](RESUME_NOTE.md)。

1. 使用字节冻结的 Workflow v1.0.0，在新的、非 fork 上下文和新工作根仅提供该 brief。按[第一轮启动入口](../../STARTER_PROMPTS.zh-CN.md#第一轮新对话只附兴趣文档)完成探索；没有旧材料则 Q6 不适用。保存原 Q5、独立复盘/修訂和最后说明。
2. 第一轮完成后，第二轮另建上下文与工作根，仍只给同一 brief。第一轮成果由使用者保管在第二轮输入之外，按[第二轮入口](../../STARTER_PROMPTS.zh-CN.md#第二轮另开新对话仍只附同一份兴趣文档)到 Q5-R 后停在 `pending_handoff`。
3. 先读取、保存第二轮原稿及修订摘要，再按[指定交接入口](../../STARTER_PROMPTS.zh-CN.md#第二轮完成-q5-r-后的指定交接)给出第一轮允许读取的提案、比较方案和来源文件，而不是整个目录。承接第二轮 Q6–Q7，不把接触旧成果后的版本说成独立发现。

每一步实际做到哪里，以产物内容与真实状态为准。关键来源如果取不到全文，只标注摘要/局部阅读并保留证据缺口。两条路线使用真正可用的新上下文；没有此能力则记录知情自审限制。新目录不保证拒绝读取其他文件，工具、全局技能目录、记忆与账户设置也不会被本仓库自动封闭。

本次案例使用宿主原生 worker 和公开 web 工具，而非另配置付费模型 API。提供给 worker 的冻结 Skill 由既有准备器复制；不是重新设计科研流程。对话工具产生的完整事件流和闭合 token 账单未被本案例捕获，不把阶段文件或 worker 自述当成完整执行追踪。

再次检索会受到日期、来源更新、搜索工具与模型差异影响。相同输入不要求得到相同候选，也不说明第二轮一定更好；重复引用同一原件不形成两份独立科学证据。再使用时应在新范围下判断真实资源与执行授权，不自动继承这个案例尚未拥有的实验条件。

## English summary

Use the same neutral brief in two fresh contexts, keeping pass-1 outputs out of pass 2 through Q5-R. Snapshot pass 2 before a scoped Q6 handoff. Retain original proposals, actual repairs, source-read depth, unresolved conditions and the final explanation. This case is public-source discovery and planning, not an experiment or a success-rate test. Host context separation is not a filesystem sandbox; complete event and token-cost capture is not established.
