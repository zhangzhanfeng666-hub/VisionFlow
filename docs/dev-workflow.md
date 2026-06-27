# Development Workflow

## Core Rule

优先改 `src/`，不要把临时实验直接堆在 `release/`。

当前主开发顺序是：

1. `src/plugin/` 外壳
2. `src/workflow/` 识别与规划
3. `src/dctl/` 颜色模块

## Normal Flow

1. 从 `main` 拉出分支
2. 在 `src/plugin/`、`src/workflow/`、`src/dctl/` 或 `src/common/` 做改动
3. 如有需要，同步更新 `release/dctl/`
4. 补充文档或验证截图
5. 合并回 `main`

## Branching

推荐分支：

- `feature/<topic>`
- `fix/<topic>`
- `exp/<topic>`

## Validation Expectations

每次改动至少应说明：

- 改动目标是什么
- 预期改善的结果是什么
- 用什么设备或场景验证

如果已有截图或对比，应放入 `tests/stills/`。

## Release Handling

- `src/plugin/` 保持插件/脚本入口清晰
- `src/workflow/` 保持识别、规划、输出逻辑清晰
- `src/dctl/` 保持可读、可维护
- `release/dctl/` 保持可投放到 Resolve
- 发布副本命名统一使用 `HDRC_` 前缀

## Scope Guardrails

未经确认，不要顺手把工作扩展到：

- GUI 产品
- 自动剪辑
- 风格 LUT 商店
- 原始视频资产管理

## Shared Assumption

当前共同环境假设为：

- Windows
- VS Code
- DaVinci Resolve

如果新增依赖、脚本或流程，应同步写入文档，避免 agent 只能从聊天记录获取信息。
