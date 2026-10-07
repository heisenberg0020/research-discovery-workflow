# 原生公开专题产物与失败记录

对应[公开专题案例](../../use-cases/forecast-uncertainty-2026-10-06/README.md)。这是实际 worker 保存产物的机械导出，不是 Codex CLI 事件捕获，也不编造宿主调用日志或闭合成本。

## 保存的范围

| 包 | 内容与状态 | 入口 |
| --- | --- | --- |
| PASS1 | 最初导出的接续快照，保留为历史，不代替最终 closing | [索引](evidence/PASS1/RUN.md) · [副本/原件摘要](evidence/PASS1/export.json) |
| PASS1-CLOSING | 执行器 final 后的最新第一轮；主计划 incomplete，原 Q5/评审/修订保留 | [索引](evidence/PASS1-CLOSING/RUN.md) · [副本/原件摘要](evidence/PASS1-CLOSING/export.json) |
| PASS2-SETUP-FAILED | 同一输入及检索前的上下文暴露失败；没有科学提案或交接 | [索引](evidence/PASS2-SETUP-FAILED/RUN.md) · [副本/原件摘要](evidence/PASS2-SETUP-FAILED/export.json) |

原第一轮模型兼容错误、接续及第二轮状态工具暴露分别见[接续记录](../../use-cases/forecast-uncertainty-2026-10-06/RESUME_NOTE.md)。不能将第一轮旧 RUN 标题或 Q7-A 文件名当成完成声明；新增 closing 与实际正文解释最终 partial 状态。

第一轮接续前已有的 12 份科学 Markdown 原件字节一致；接续另加四份 closing 文件。导出的 PASS1 含这 16 份产物以及 BRIEF/RUN。第二轮失败包含 BRIEF/RUN/失败说明三份。原始副本在本地限定备份中保留，不随包公开。

最终打包核对发现最初 PASS1 导出早于执行器 final 的两项补充：Q7-A 增加 PID burn/dev 拟合时序及资源行，CHAT_REPORT 补入相同解释。没有改动原 12 份科学产物，也没有重新生成候选。原快照保留，另导出 PASS1-CLOSING 供最新阅读；它的 18 份原件摘要均与停止后的工作根一致。不能把中间副本与最终原件的差异说成原稿被覆盖或新一轮证据。

## 导出与可核对内容

导出仅读取指定工作根的 output 与 BRIEF/RUN。已知工作根和个人绝对路径被替换，本地 Markdown 文件链接改为标签与代码路径；原始公开来源 URL 保留。每包 export.json 列出原件及公开副本 SHA256、字节或替换计数，公开 checker 核对 public_files。

这不是通用秘密检测器。只公开经范围检查的文本，没有论文/PDF 全文、缓存、私人历史、配置或凭据。不会反向改写科学原件，导出缺少完整原生事件流，input_tokens、output_tokens、closed_total_tokens 都为 null。不能从文件数或主 worker 自述恢复完整执行追踪。

三个公开副本仅去掉多余的 EOF 空白行，确切文件列于各 export.json 的 public_normalizations；raw_sources 摘要仍对应保留的原始字节，public_files 摘要对应调整后的公开副本。原件未改，旧 CLI 证据也未重新导出。

主 worker 的新建由协调者实际操作；T/U 和评审等子输入边界以可见操作与执行器声明分别说明，不转换成宿主强隔离认证。真实科研含义与阅读覆盖限制见[实质复盘](../../use-cases/forecast-uncertainty-2026-10-06/ASSESSMENT.md)。

## English scope

These are sanitized copies of actual native-worker saved artifacts, not invented CLI events. Pass 1 is a partial planning closure after a disclosed executor interruption/resume. Pass 2 stopped at Setup after a status tool exposed prior results, before research generation. Original artifacts and the failure are retained. Declared public-file hashes are checked; complete event capture, closed costs, host-wide isolation, research quality and a completed two-pass reconciliation are not established.
