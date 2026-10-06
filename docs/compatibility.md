# 能力、兼容与验证边界

[English](compatibility.en.md) · [安装说明](installation.md)

这是指导 Agent 的 Skill；科研执行要求以[冻结入口](../skills/research-discovery-workflow/SKILL.md)和其引用为准。仓库辅助工具与本页是可选使用支持，不增加科研阶段，也不提供模型或检索服务。仓库分发版本保持 Workflow v1.0.0 字节冻结。

| 项目 | 实际范围 | 尚不能据此认定 |
| --- | --- | --- |
| Skill 文本 | `SKILL.md` 与本地引用自包含；可显式读取完整包 | 所有客户端会自动发现或遵从 |
| Codex 元数据 | 提供 `agents/openai.yaml` | 安装工具会重启客户端或修改注册配置 |
| Python 工具 | Python 3.10+ 标准库；安装、检查、目录准备和打包 | 提供模型、搜索服务或实验执行器 |
| 隔离 | 新上下文、干净目录、限定输入按宿主能力落实 | 准备目录会清除记忆或限制任意旧文件读取 |
| 检索能力 | 使用宿主实际提供的工具；七项上游能力可选接入 | 捆绑了第三方检索脚本、账号或付费服务 |
| 先导实验 | 冻结流程中的可选步骤，执行按实际授权 | 安装或 planning 请求授权训练与评测 |

<a id="loading-check"></a>

## 宿主需要落实什么

客户端必须能读取入口及其相对引用。自动发现、`$research-discovery-workflow` 调用方式、自定义安装目录和列表刷新取决于宿主实际支持。文件复制成功只说明安装器工作完成，不能替代实际加载证据。

新对话、记忆控制、文件读取边界和检索工具同样由宿主提供。不支持的能力应明确记录，不能把新目录描述为沙箱或把已有上下文说成完全空白。可以使用[安装说明中的可选读取检查](installation.md#4-可选只检查读取不启动调研)，仅确认实际路径、引用与宿主限制；该检查不启动调研，也不是新增阶段。

## 显式读取备用入口

如果宿主不能自动发现 Skill，但能读取本地文件，可保留整个 `skills/research-discovery-workflow/` 目录，显式指定入口。不要只复制 `SKILL.md`；它依赖同目录下的 `references/`、`scripts/` 和 `agents/`。仓库示例和本页不替代这些引用。

用真实绝对路径替换下面的路径，即可做只读加载检查：

```text
请直接读取 /absolute/path/to/research-discovery-workflow/SKILL.md。
将它作为权威科研 Workflow，按该入口要求，从同一 Skill 目录解析和读取本地引用；保留完整包，不用本页摘要替代引用。
本条只检查读取：报告实际入口路径、已读取和缺失的引用，以及宿主检索、文件访问、新上下文和记忆控制的真实能力与限制。
不要开始科研、创建工作根、运行准备器、检索论文、生成候选或执行 Q0–Q7；等我另发启动请求。
```

真正启动时，在新的非 fork 对话使用[冻结启动提示词](STARTER_PROMPTS.zh-CN.md)，把 Skill 调用行换成以下两行，并附上实际中性 brief 和指定工作根：

```text
请直接读取 /absolute/path/to/research-discovery-workflow/SKILL.md，并以它作为本次研究与 planning 的权威 Workflow。
按入口要求，从同一完整 Skill 目录解析和读取本地引用，再执行我提供的启动请求。
```

默认安装入口是 `$CODEX_HOME/skills/research-discovery-workflow/SKILL.md` 或 `$HOME/.codex/skills/research-discovery-workflow/SKILL.md`；自定义安装、仓库和解压包使用各自实际路径。让宿主解析实际路径，不要假定提示词会展开 shell 变量。显式读取同样不保证指令遵从或隔离能力。

## 什么得到过检查

v1.0.0 完成过标准库文件测试、元数据检查和少量虚构材料的 Agent 行为试走，失败修正与限制保留在[原始验证记录](VALIDATION.md)。这些记录不能证明选题质量、科研成功率或两轮优越性。

仓库新增检查关注冻结文件未变、文档与资产链接、临时目录安装、拒绝覆盖和发行包摘要。已记录的 v1.1.0 结果见[发行说明](releases/v1.1.0.md)，后续版本见[版本记录](../CHANGELOG.md)；远程 CI 以实际 [Actions](https://github.com/heisenberg0020/research-discovery-workflow/actions) 回执为准。

CI 只在其配置的 Python/操作系统组合上检查仓库代码。它没有验证各客户端的 Skill 加载、完整研究或隔离效果。可选读取提示词只是供使用者检查的请求，本页不声称已真实测试任何宿主加载。Windows 本地符号链接测试可能需要相应权限；未执行的检查不能记作通过。

## 其他客户端

可按客户端支持的 Skill 导入方式使用，或用上面的显式读取入口。目前没有对 Claude Code、Cursor 等宿主做完整兼容认证。Codex 元数据不能据此推断其他宿主的工具权限、记忆行为或自动加载路径。

## 常见问题

**安装了就开始调研了吗？** 没有。安装只复制文件，准备器只准备空目录，读取检查只检查文件与宿主能力。启动仍需在合适的新对话中给 brief 和明确请求。

**是否依赖另外七个 Skill？** 不依赖。它们是[可选能力映射](../skills/research-discovery-workflow/references/upstream-capabilities.md)，没有它们可使用宿主已有工具。

**第一次使用没有旧成果怎么办？** 冻结流程允许 Q6 `not_applicable` 后继续，不需要虚构旧结果。

**Q7-A 还缺资源，可以汇报吗？** 可以汇报实际局部进展与缺口，不能宣称完整 Q7-B 已完成；具体标准以冻结指令为准。

**第二轮一定更好吗？** 不是。合流可以保留第一轮更好的构思；重复来源不等于独立复现。
