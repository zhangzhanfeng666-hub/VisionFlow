# Resolve Plugin V1

## Interface Names

DaVinci Resolve 当前最 relevant 的插件/扩展接口有三类：

### 1. Workflow Integrations

适合：

- 带 UI 的工作流插件
- 更接近真正产品外壳
- 适合后续做更正式的交互层

本机示例目录：

- `C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Workflow Integrations\Examples`

### 2. DaVinci Resolve Scripting API

适合：

- Python / Lua 自动化
- 媒体池、时间线、项目、渲染流程控制
- 第一版原型验证

本机模块：

- `C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules\DaVinciResolveScript.py`

### 3. DCTL

适合：

- 像素级颜色变换
- 输入归一
- 发布前颜色处理

不适合独立承担完整产品工作流。

## V1 Choice

第一版选择：

- 用 `Scripting API` 做 Resolve 内工具窗口
- 用 `workflow engine` 做识别和规划
- 用 `DCTL` 做颜色模块

原因：

- 比 Workflow Integrations/Electron 更轻
- 能更快跑通素材识别和导入流程
- 更容易在现有仓库里快速迭代

## V1 Capabilities

当前脚本插件原型支持：

- 选择素材路径
- 指定设备识别模式或自动识别
- 生成 HDR 发布工作流计划
- 可选把素材导入目标 bin
- 从目标 bin 创建 timeline
- 生成 render job 到当前项目的渲染队列

## Installed Script Location

Resolve 用户脚本目录：

- `C:\Users\wuche\AppData\Roaming\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Utility`

安装后的脚本名：

- `HDR_Creator_Workflow.py`

## How To Run

在 Resolve 中打开：

- `Workspace > Scripts > Utility > HDR_Creator_Workflow`

如果脚本没有出现，重启 Resolve 一次最稳。

## Current UI Actions

当前窗口里的关键动作：

- `Generate Plan`
- `Import To Bin`
- `Create Timeline`
- `Queue Render Job`

它现在已经可以作为插件第一版原型使用，而不只是一个静态计划查看器。
