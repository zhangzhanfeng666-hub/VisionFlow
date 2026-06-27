# Repo Scope

## What This Repository Is

这是 `HDR Creator` 第一阶段 MVP 的 Resolve 插件/脚本研发工作区，也是团队和 AI agent 的上下文同步入口。

它负责：

- HDR 工作流验证
- Resolve 插件/脚本工作流研发
- DCTL 研发
- HDR 发布逻辑实验
- 最小验证资产管理
- 面向新开发者和 agent 的上下文传递

## What This Repository Is Not

它不是：

- 完整 GUI 产品仓
- 通用 LUT 商店
- 色彩理论百科
- 原始视频素材仓
- Resolve 外挂或插件系统仓

## Out Of Scope For The Current Phase

当前阶段不做：

- `HDR -> SDR` 兼容主线
- 复杂自动化平台
- 脱离 Resolve 的独立成品应用
- AI 增强、模板、风格包生态

## Why This Boundary Exists

这个项目的核心不是“展示 HDR 技术复杂度”，而是帮助用户把已经拥有的拍摄设备能力，稳定转化为最终发布效果。

因此产品外壳优先做成 Resolve 内可操作的插件/脚本工作流，而不是试图让 DCTL 独自承担素材识别、输出控制和交互。

因此仓库必须保持聚焦：

- 围绕结果
- 围绕发布链路
- 围绕第一阶段 MVP
