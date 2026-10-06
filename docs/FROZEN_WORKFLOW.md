# Workflow 冻结与仓库版本

**科研 Workflow 冻结在 v1.0.0。仓库 v1.2.0 只完善使用、示例与分发。**

基准是 [v1.0.0](https://github.com/heisenberg0020/research-discovery-workflow/tree/v1.0.0)，提交 `894b429b51d2f3aeb35e5e4606260dbc91376e70`。本次不是流程迭代，也没有增加科研门槛。

## 哪些内容不变

- `skills/research-discovery-workflow/` 中的全部文件：Skill 入口、八份引用指令、UI 元数据和准备器。
- [中文双轮启动提示词](STARTER_PROMPTS.zh-CN.md)与[原始英文快速指南](QUICKSTART.en.md)。
- 隔离、Q0–Q5、Q5-R、条件 Q6、可选 Q6-P、Q7-A → Q7-B 的现有行为与授权边界。

[冻结清单](workflow-freeze.json)保存这 13 个文件的字节摘要。仓库检查会核对摘要和 Skill 文件集合；新增或遗漏指令文件也会报告。它用于发现意外改动，不是签名、访问控制或科学正确性认证。

## 哪些内容可以完善

首页、原创图示、安装/兼容说明、公开示例、贡献入口、仓库测试和发行包。在 Skill 外增加的安装与打包脚本是可选工具，不构成新阶段，也不替代宿主 Agent。

新旧版本中的科研指令相同。已有 v1.0.0 Skill 不需要为了获得新科研能力而更新；需要新使用说明和发行工具时，再获取新版仓库。

## 如何核对

在仓库或解压后的发行包根目录，先按[安装说明](installation.md#2-选择并核对-python)选择并核对 Python 3.10+，在同一终端执行：

```sh
"$RDW_PYTHON" scripts/check_repo.py
```

在包含旧标签的源码仓库还可直接核对：

```sh
git diff --exit-code v1.0.0 -- skills/research-discovery-workflow docs/STARTER_PROMPTS.zh-CN.md docs/QUICKSTART.en.md
```

未来只有用户明确要求修改 Workflow 才能讨论新的流程版本。不能调整冻结清单来掩盖意外改动。
