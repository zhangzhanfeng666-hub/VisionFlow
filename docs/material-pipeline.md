# Material Pipeline

## Goal

第一阶段先把下面三件事统一封装成一个可扩展的工作流层：

- 素材识别
- 色彩转换规划
- 输出规划

这层封装的目标不是立刻替代 Resolve，而是先把“识别逻辑”和“发布逻辑”的决策收口到同一个接口里，作为插件/脚本外壳的后端决策层，避免后续脚本、DCTL、导出规则各写各的。

## Current Implementation

当前新增了一个 Python 工作流包：

- `src/workflow/asset_probe.py`
- `src/workflow/material_recognizer.py`
- `src/workflow/color_pipeline.py`
- `src/workflow/output_planner.py`
- `src/workflow/service.py`
- `src/workflow/cli.py`

统一入口是 `HDRWorkflowService`。

它应被插件外壳调用，而不是被当成最终产品界面本身。

## Encapsulation Boundary

### 1. Asset Probe

负责：

- 文件是否存在
- 扩展名
- 文件名
- 大小
- 是否可用 `ffprobe`
- 可选 metadata 抽取

当前如果机器上没有 `ffprobe`，会自动退回到基于文件名和扩展名的启发式识别。

### 2. Material Recognition

负责：

- 判断素材更接近 `Pocket`、`iPhone` 还是 `generic-hdr`
- 给出置信度
- 给出命中的原因
- 绑定对应输入归一 DCTL

### 3. Color Transform Plan

负责输出统一的颜色处理计划：

- 是否做输入归一
- 使用哪个 normalization DCTL
- 工作域 transfer / gamut
- 使用哪个 publish DCTL
- 目标输出 transfer / gamut
- metadata 策略

### 4. Output Plan

负责：

- 输出平台
- 容器
- 编码器
- 输出文件名
- 输出相对目录

## Current Profiles

设备 profile 放在：

- `profiles/devices/profiles.json`

平台 profile 放在：

- `profiles/platforms/profiles.json`

当前只正式支持一条平台主线：

- `douyin-hdr`

## CLI

当前可通过下面的命令生成工作流计划：

```bash
python -m src.workflow.cli plan path/to/asset.mov
python -m src.workflow.cli plan path/to/asset.mov --device-family pocket
```

输出是 JSON，适合：

- 人直接看
- 另一位开发的 agent 直接消费
- 后续接自动导出器

## Next Step

这次实现的是“决策封装层”。下一步应按这个边界继续往下补：

1. 用真实素材和命名规则校正识别逻辑
2. 把 DCTL scaffold 替换成真实的归一和发布逻辑
3. 增加 Resolve 插件/脚本侧的执行 backend
4. 明确 Pocket / iPhone 的输入特性差异
