# Plugin Architecture

## Goal

当前产品方向调整为：

- `Resolve 插件/脚本外壳` 负责流程
- `workflow engine` 负责识别与决策
- `DCTL` 负责颜色处理

## Why Not DCTL Alone

`DCTL` 适合：

- 输入归一
- HDR 发布前的颜色变换
- 高光、对比度、饱和度等像素级处理

`DCTL` 不适合独立承担：

- 素材识别
- 元数据决策
- 输出控制
- 一键式用户流程
- 产品级 UI 和状态管理

## Layered Design

### 1. Plugin / Script Shell

位置：

- `src/plugin/`

职责：

- 在 Resolve 内暴露操作入口
- 收集用户选择
- 调用 workflow engine
- 选择对应 DCTL
- 组织导出参数

### 2. Workflow Engine

位置：

- `src/workflow/`

职责：

- 探测素材
- 识别设备来源
- 构建色彩处理计划
- 构建输出计划

### 3. DCTL Modules

位置：

- `src/dctl/`

职责：

- 输入归一
- HDR 发布颜色处理
- 设备差异的颜色层修正

## First Build Direction

第一阶段不急着做 OFX 级复杂插件，先优先做：

- Resolve 脚本/插件外壳原型
- 调用 `HDRWorkflowService`
- 输出统一计划
- 手动或半自动套用 DCTL / 输出设置

## Current Constraint

当前仓库已经有：

- workflow 决策层
- DCTL scaffold

下一步应补：

- `src/plugin/` 入口
- Resolve 调用约定
- 插件侧的执行链路
