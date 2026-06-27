# HDR Creator Workspace

GitHub 仓库名当前为 `VisionFlow`。在这个仓库里，我们把它作为 `HDR Creator` 第一阶段 DCTL 研发工作区来使用和维护。

这是 `HDR Creator` 的 DCTL 研发仓，用来验证 `Pocket + iPhone` 的 `拍摄HDR -> 正确发布HDR` 工作流。

这个仓库不是通用 HDR/LUT 实验仓，不是最终产品应用仓，也不是原始视频素材仓。它的职责是为第一阶段 MVP 提供清晰、可协作、可复现的 DCTL 研发环境。

## Current Stage

当前阶段只做一条主线：`拍摄HDR -> 发布HDR`。

- 目标用户是 Apple Creator，而不是专业调色师
- 成功标准是“最终效果被正确保留下来”
- 重点是发布结果，不是技术概念教育

## Read This First

无论是开发者还是 AI agent，进入仓库后按这个顺序阅读：

1. `README.md`
2. [`AGENTS.md`](AGENTS.md)
3. [`docs/repo-scope.md`](docs/repo-scope.md)
4. [`docs/product-intent.md`](docs/product-intent.md)
5. [`docs/current-priority.md`](docs/current-priority.md)
6. [`docs/dev-workflow.md`](docs/dev-workflow.md)
7. 再进入 `src/`

## Repo Layout

```text
.vscode/                 Shared workspace settings and tasks
docs/                    Product intent, scope, workflow, validation docs
docs/reports/            Archived product and business background documents
release/dctl/            DCTL files prepared for Resolve deployment
src/dctl/                Source DCTL files
src/common/              Shared notes, constants, math/color helpers
tests/fixtures/          Fixture policy only; raw video does not go into Git
tests/stills/            Small validation screenshots and stills
tests/exports/           Local export outputs, ignored by Git
```

## Background Docs

长期背景材料单独归档在 `docs/reports/`。

当前报告：

- [`docs/reports/HDR Creator 项目商业分析报告（V1）.md`](docs/reports/HDR%20Creator%20项目商业分析报告（V1）.md)

## Working Rules

- 源码优先放在 `src/`，不要直接把实验改动留在 `release/`
- 一个任务一个分支，例如 `feature/hdr-publish-pocket`
- 代码改动应补充文档或验证截图
- 未经确认不要扩展到 GUI、自动剪辑、风格 LUT 生态

## Quick Start

1. 阅读上面的入口文档顺序
2. 从 `src/dctl/` 查看当前 DCTL 结构
3. 从 [`docs/material-pipeline.md`](docs/material-pipeline.md) 了解素材识别与输出封装
4. 在 `release/dctl/` 查看当前可投放版本
5. 按 [`docs/validation-playbook.md`](docs/validation-playbook.md) 进行验证

## Git Scope

提交到 Git 的内容应保持轻量且可复现：

- 提交：DCTL、Markdown 文档、必要配置、小体积截图
- 不提交：原始视频、导出视频、缓存、Resolve 用户目录内容
