# Installation-path calibration / 安装路径校准

2026-10-06，外层安装器默认目标改为 `$HOME/.agents/skills`，依据 [Codex 专用 Skill 加载路径表](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills)。`--dest` 仍支持自定义或旧位置；不自动迁移、删除或覆盖安装。Workflow v1.0.0 未变。

当前 CLI 为 0.160.0。使用该版本自己的 `app-server generate-json-schema` 做了无模型的接口检查。其 `SkillsListParams` 只有 `cwds`、`forceReload`，未发现排除个人 roots 的参数。为保持“只检查本仓库/临时测试范围”的边界，没有实际启动 app-server 或调用 `initialize` / `skills/list`，也没有个人 Skill 安装。官方 [app-server Skill 接口说明](https://learn.chatgpt.com/docs/app-server#skills)不等于本机执行回执。

22 项分发测试在临时虚构 fixture 中通过。它们验证目标选择、显式旧位置、拒绝覆盖及复制行为，不验证宿主加载。旧路径与新 user 路径的实际发现均未实测；不据此声称旧位置失效。之前 v1.3.0 的[显式 CLI 读取证据](../2026-10-06-codex-cli/README.md)仍保留其原有范围，不能转换成新默认安装的加载认证。

The installer follows the current documented user-skill location. Custom/legacy destinations remain explicit and non-overwriting. The version-matched CLI schema was inspected without starting an app-server or model call. Distribution fixtures passed; actual discovery from the new user location and legacy locations was not tested. These are separate claims, not a host-compatibility certification.

最小命令与范围记录见 [receipt.json](receipt.json)。第四批全部外层工具的 94 项回归结果及早期测试问题见 [OUTER_CHECKS.json](OUTER_CHECKS.json)；它与上面的 22 项分发子集不是两份独立效果证据。本地完整 schema 属于可重建工具输出，不作为公开科研证据。

2026-10-07 收尾复核补修了六类实际边界问题，并增加 11 项合成回归。最终 **105 项测试通过**；单独复核的 48 项子集不是另一份效果证据。旧 74 份公开 CLI 科学证据原样保留；新的测试、阅读和导出修复不补成用户级宿主加载、科研质量或强隔离认证。原 94 项回执及中间失败均保留在同一记录中。
