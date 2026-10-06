# 安装、启动与更新

需要能读取本地 Skill 的 Agent 客户端。仓库辅助工具只使用 **Python 3.10+ 标准库**；不需要 pip 安装依赖或另配 API Key。实际检索和模型能力由宿主提供，见[兼容范围](compatibility.md)。

## 1. 获取仓库

```sh
git clone https://github.com/heisenberg0020/research-discovery-workflow.git
cd research-discovery-workflow
```

要固定本版，克隆时加 `--branch v1.1.0 --depth 1`。也可以在 [Releases](https://github.com/heisenberg0020/research-discovery-workflow/releases) 下载 ZIP、`manifest.json` 和 `SHA256SUMS`，保留三者在同一目录。核验后解压，进入包根目录。

## 2. 先预览，再安装

```sh
python scripts/install.py --dry-run
python scripts/install.py
```

默认目标：设置了 `CODEX_HOME` 时使用其 `skills/`，否则使用 `$HOME/.codex/skills/`。不会修改 `CODEX_HOME` 或全局配置。只有安装命令会写入目标；预览不创建目录。

若 `research-discovery-workflow` 同名目标已存在，包括符号链接，安装器停止，不覆盖、删除或自动升级。安装器复制冻结 Skill 的入口、引用、元数据、准备器，并附带根目录 MIT 许可证；不复制研究结果、示例、测试或缓存。

需要其他目标时显式指定：

```sh
python scripts/install.py --dest ./local-skills --dry-run
python scripts/install.py --dest ./local-skills
```

自定义位置是否被客户端发现，须按客户端实际能力配置；这个命令不修改客户端配置。安装后在宿主中重新加载或重启 Skill 列表，确认能调用 `$research-discovery-workflow`。本次未覆盖你的个人安装。

## 3. 在新上下文里开始

复制[中性兴趣文档示例](../examples/neutral-brief.md)到自己的文件并填写。不要把旧候选或旧架构作为默认答案，除非你明确要做有种子探索。

在新的非 fork 对话中提供实际 brief，指定干净工作根，使用[第一轮启动提示词](STARTER_PROMPTS.zh-CN.md)。客户端无法清除历史记忆或限制读取时，如实记录；安装不等于隔离。

可选准备空目录，父目录须已存在，目标须不存在：

```sh
mkdir -p ./runs
python skills/research-discovery-workflow/scripts/prepare_run.py \
  --root ./runs/pass-1 --brief ./my-neutral-brief.md --pass-number 1
```

将 `my-neutral-brief.md` 替换为你实际填写的文件。命令结束仅表示准备完成，**调研尚未启动**。独立第二轮须用另一个干净工作根及新对话；第一轮成果到第二轮 Q5-R 后才交接。没有旧材料时正常跳过 Q6。

## 更新与保留旧版本

仓库 v1.1.0 的科研指令与 v1.0.0 完全相同，无需为获得新科研能力更新个人 Skill。新版本只增加仓库使用与分发便利。

若未来确实要更换安装，先检查现有 Skill 是否有个人改动，另存备份，再自行决定新目录和切换方式。当前安装器没有 `--force`，不会替你删除旧目录。可以先用一个新的自定义目标试装；仅改变目录不保证客户端会发现它。

## 维护者：打包与核验

```sh
python scripts/check_repo.py
python -m unittest discover -s tests -v
python scripts/build_release.py --output ./dist/v1.1.0
python scripts/build_release.py --verify ./dist/v1.1.0/research-discovery-workflow-1.1.0.zip
```

打包前自行创建父目录 `dist/`。构建需要 Git、干净的已提交源码和未存在的输出目录；只读取已提交、允许公开的文件，不打包本地运行目录或缓存。版本取自 `VERSION`，输出 ZIP、文件清单和 SHA-256 校验文件。核验检查文件字节与清单一致；不是签名、第三方信任认证或科研质量证明。
