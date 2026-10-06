# 可选实测重现说明

[实际结果](README.md) · [固定方案](PROTOCOL.md)

这不是安装、科研或 CI 的必做步骤。**下列 capture 命令会启动真实 Codex 模型调用，消耗已有账户额度。** 只在主动选择此检查时运行；单元测试和普通打包不会调用它。不承诺复现相同答案或耗时。

先阅读协议、选定虚构输入与提示词，检查当前 `codex exec --help` 是否支持记录中的选项、`codex --version` 和 `codex login status`。本次测的是 0.160.0；新版选项或事件格式需要重新核对，旧回执不是对新版的保证。登录应是已存在的 ChatGPT 登录，工具不读凭据、不配置 API key，不支持 API-key 回退。

在仓库根目录选择 Python 3.10+，使用**新的命名输出路径**。以只读 L0 为例：

```sh
RDW_PYTHON=python3
"$RDW_PYTHON" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else "Python 3.10+ required")'
mkdir -p runs/my-client-check/workspace runs/my-client-check/records
"$RDW_PYTHON" scripts/install.py --dest runs/my-client-check/workspace/.agents/skills
"$RDW_PYTHON" docs/validation-runs/2026-10-06-codex-cli/tools/run_one.py \
  --workspace runs/my-client-check/workspace \
  --prompt docs/validation-runs/2026-10-06-codex-cli/prompts/L0.md \
  --record runs/my-client-check/records/L0 \
  --sandbox read-only
```

`run_one.py` 是这个小检查的 opt-in 记录器，不是科研控制器。每次只运行一个明确请求；拒绝已有记录目录；捕获原提示、JSONL、最终回复、状态和墙钟耗时。单调用 900 秒超时则停止并保存记录，不自动重试、切换模型或重新抽取结果。默认模型沿用客户端，无保证的身份不补填。

行为调用应各建新工作根，只复制对应 `fixtures/<case>/` 的当前材料到 `input/`，安装不变 Skill，使用对应 prompt 与 `workspace-write`。不要把协议、判定标准、其他案例或整个仓库资料复制进去。源码脚本只移除本次调用的 API-key 环境变量，不改全局配置。新目录和这些 flags 也不提供任意读取隔离或全局记忆清除。

B2-pre **不复制** `old-handoff.md`。先读取实际 review、repaired proposal 和状态，确认可交接；原稿做摘要对比，先保存 pre 产物快照，才把唯一获准旧包复制进 `handoff/` 并执行 B2-post。后者是新的临时上下文承接已保存文件，不是假装前一个会话始终未中断。不能为得到更好结果跳过失败或覆盖原件。

记录完毕后可以选择导出脱敏证据：

```sh
"$RDW_PYTHON" docs/validation-runs/2026-10-06-codex-cli/tools/export_evidence.py \
  --record runs/my-client-check/records/L0 \
  --workspace runs/my-client-check/workspace \
  --output runs/my-client-check/public-copy/L0
```

导出本身不运行模型，默认复制当前工作根的 `output/`；如需 pre 快照，可用 `--artifacts` 指定保存的 output 根。发布前人工核对脱敏、副本范围和遗漏记录；不要把原日志、凭据或私人研究资料直接提交。脚本测试只检查合成事件的结构与转换，不能代替人工行为理解或隐私检查。

这里只测一个实际客户端路径。[官方 Skill 说明](https://learn.chatgpt.com/docs/build-skills)说明仓库 `.agents/skills` 入口，[非交互调用说明](https://learn.chatgpt.com/docs/non-interactive-mode)介绍 JSONL 与临时运行选项；实际能力仍以你的客户端、调用回执与声明边界为准。
