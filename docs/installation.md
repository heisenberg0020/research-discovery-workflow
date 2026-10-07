# 安装、启动与更新

[English](installation.en.md) · [兼容范围](compatibility.md)

需要能读取本地 Skill 文件的 Agent 客户端。仓库辅助工具使用 **Python 3.10+ 标准库**，不需要 pip 依赖或另配 API Key；实际检索与模型能力由宿主提供。本页是可选使用辅助，不增加科研阶段；执行要求以[冻结 Skill](../skills/research-discovery-workflow/SKILL.md)为准。

## 1. 获取文件

### 克隆仓库

```sh
git clone https://github.com/heisenberg0020/research-discovery-workflow.git
cd research-discovery-workflow
```

这会获取默认分支。固定 v1.4.0 可使用 `git clone --branch v1.4.0 --depth 1 https://github.com/heisenberg0020/research-discovery-workflow.git`。若选择其他已发布版本，把标签换成该版本。

### 下载发行包：先核验，再解压

从 [Releases](https://github.com/heisenberg0020/research-discovery-workflow/releases) 的同一个版本下载自定义发行资产 `research-discovery-workflow-1.4.0.zip`、`manifest.json`、`SHA256SUMS`，放在同一目录。选择其他版本时，将以下 ZIP 名称与目录名中的 `1.4.0` 换成下载的实际版本。GitHub 自动生成的 “Source code (zip)” 不是这套资产，文件布局和核验方式不同。

在下载目录运行以下两种方式之一，**两项均显示成功后再解压**：

```sh
# macOS：已提供 shasum 时
shasum -a 256 -c SHA256SUMS
```

```sh
# Linux 或其他已提供 sha256sum 的环境
sha256sum -c SHA256SUMS
```

两种命令都会核对 ZIP 与 `manifest.json` 的字节摘要。若命令不存在、文件缺失或核验失败，先解决问题，不继续使用这一份下载。SHA-256 检查只能说明文件与这份校验清单一致；下载的 `SHA256SUMS` **不是真实性签名**，不能单独证明来源可信或排除资产一起被替换。

核验后用解压工具打开 ZIP，或运行：

```sh
unzip research-discovery-workflow-1.4.0.zip
cd research-discovery-workflow-1.4.0
```

ZIP 内的顶层目录是 `research-discovery-workflow-1.4.0/`，入口是其下的 `skills/research-discovery-workflow/SKILL.md`。保留外部的三份发行资产。下载和摘要核验不需要源码 Git 仓库；Windows 可用现有校验工具核对两项 SHA-256，但本页的 shell 命令及客户端加载没有 Windows 兼容认证。

## 2. 选择并核对 Python

不同环境可能使用 `python3`、`python` 或完整可执行文件路径；不要仅凭命令名称判断版本。在 macOS/Linux shell 中选择本机实际可用的命令，运行检查，然后沿用这个变量：

```sh
RDW_PYTHON=python3  # 按实际环境改为 python 或可执行文件的完整路径
"$RDW_PYTHON" -c 'import sys; print(sys.executable); print(sys.version); raise SystemExit(0 if sys.version_info >= (3, 10) else "Python 3.10+ is required")'
```

检查必须成功且版本至少为 3.10，才能运行后面的 Python 辅助工具。Windows 的启动方式取决于本机安装，例如 `py -3`；须同样核对实际版本，不能把 shell 变量示例直接当作 PowerShell 命令。仅让宿主显式读取完整 Skill 包，不需要 Python，见[显式读取备用入口](compatibility.md#显式读取备用入口)。

## 3. 先预览，再安装

从克隆或解压后的包根目录运行；后续命令沿用同一终端中已核对的 `RDW_PYTHON`：

```sh
"$RDW_PYTHON" scripts/install.py --dry-run
"$RDW_PYTHON" scripts/install.py
```

默认目标是当前用户主目录下的 `.agents/skills/`（POSIX 写作 `$HOME/.agents/skills/`），对应[官方 Skill 加载表](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills)的 USER 路径。`CODEX_HOME` 不改变本安装器默认值。工具不修改环境变量或客户端全局配置；只有安装命令写入目标，预览不创建目录。

若 `research-discovery-workflow` 同名目标已存在，包括符号链接，安装器停止，不覆盖或自动升级。它复制冻结 Skill 的入口、引用、元数据、准备器，并附带根目录 MIT 许可证；示例、测试和研究结果不属于安装载荷。

需要项目级、自定义或旧路径时用 `--dest` 显式指定；它仍可指向 `.codex/skills` 或 `CODEX_HOME/skills` 等实际目录，本次不宣称这些旧路径加载失效：

```sh
"$RDW_PYTHON" scripts/install.py --dest ./local-skills --dry-run
"$RDW_PYTHON" scripts/install.py --dest ./local-skills
```

安装后的入口为 `./local-skills/research-discovery-workflow/SKILL.md`。自定义位置是否被客户端发现，由客户端实际能力决定。在宿主中重新加载或重启 Skill 列表后，可做下面的可选读取检查；文件安装成功不等于宿主已加载。现有实际回执针对项目级 `.agents/skills`；本次没有向个人默认用户目录新安装，也未验证这条用户级宿主加载路径。

本次默认路径决定、版本匹配的无模型 schema 检查及未执行边界见[安装校准回执](validation-runs/2026-10-06-installation/README.md)。

## 4. 可选：只检查读取，不启动调研

把下面这段发给宿主。它只是使用诊断，不是新增科研阶段，也不要求完成它才能使用 Workflow。

```text
本条请求仅检查 research-discovery-workflow 是否可读取，不启动科研。
定位你实际可用的 SKILL.md，报告其真实路径；不要仅凭 Skill 名称宣称已加载。
读取该入口，并按其本地引用定位文件，报告已读取和缺失或不可读取的引用。
说明宿主实际提供的检索、文件访问、新上下文和记忆控制能力及限制；无法确认的项写明无法确认。
不要创建研究工作根、运行准备器、检索论文、生成研究候选或执行 Q0–Q7。
如果无法自动发现 Skill，报告问题并等待显式文件路径。
```

自动发现不可用时，使用[显式读取备用入口](compatibility.md#显式读取备用入口)，并保留整个 Skill 目录及其引用。

## 5. 在新上下文里开始

复制[中性兴趣文档示例](../examples/neutral-brief.md)到自己的文件并填写，记下该文件的实际路径和本轮工作根。

若选择准备器，在发启动请求**之前**运行一次；它不是必需步骤。父目录须已存在，目标须不存在：

```sh
mkdir -p ./runs
"$RDW_PYTHON" skills/research-discovery-workflow/scripts/prepare_run.py \
  --root ./runs/pass-1 --brief ./my-neutral-brief.md --pass-number 1
```

将 `my-neutral-brief.md` 替换为实际填写的文件。此路径从包根调用；从已安装 Skill 调用时换成实际安装路径。命令完成只表示目录已准备，**调研尚未启动**。

在新的非 fork 对话中，将实际 brief 路径与本轮工作根填入[首页启动请求](../README.md#quick-start)，或提供给[冻结第一轮启动提示词](STARTER_PROMPTS.zh-CN.md#第一轮新对话只附兴趣文档)。用了准备器就填写它打印的 `Prepared` 根；不用准备器则指定自己的新工作根。不要对已有本轮目录再次运行准备器。安装和读取检查均不会启动调研；宿主隔离限制如实记录。

[第二轮开始](../README.md#second-pass)与[`pending_handoff` 后的指定交接](../README.md#pending-handoff)直接连接现有冻结用法；中断的已有工作用[继续同一轮入口](compatibility.md#resume-run)。

## 更新与保留旧版本

仓库分发版本不改变字节冻结的 Workflow v1.0.0，无需为获得新科研能力替换个人 Skill。版本变化见[版本记录](../CHANGELOG.md)。

默认路径调整不自动迁移、删除或覆盖旧安装；冻结英文指南保留其发布时的旧路径说明，当前辅助安装命令以本页为准。若确需更换安装，先检查现有 Skill 是否有个人改动并另存备份，再自行决定新目录和切换方式。安装器没有 `--force`，不会删除旧目录；可以先在新的自定义目标试装。改变目录不保证客户端会发现它。

## 可选：核验包内清单与维护者打包

完成下载摘要核验、解压并检查本地脚本后，可以用包内工具核对完整归档清单。若三份下载资产位于解压目录的上一级：

```sh
"$RDW_PYTHON" scripts/build_release.py --verify ../research-discovery-workflow-1.4.0.zip
```

`--verify` 不需要 Git 仓库，不解压或安装，也不启动研究。它检查归档内容与外部清单一致；仍不是真实性签名或科研质量证明。

只有维护者**构建**发行包需要 Git、干净的已提交源码、已存在的父目录以及未存在的输出目录：

```sh
"$RDW_PYTHON" scripts/check_repo.py
"$RDW_PYTHON" -m unittest discover -s tests -v
mkdir -p ./dist
"$RDW_PYTHON" scripts/build_release.py --output ./dist/v1.4.0
"$RDW_PYTHON" scripts/build_release.py --verify ./dist/v1.4.0/research-discovery-workflow-1.4.0.zip
```

构建版本取自 `VERSION`，请让示例目录与实际版本一致。构建只读取已提交、允许公开的文件，不包含本地运行目录或缓存。
