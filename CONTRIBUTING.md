# Contributing

## Before You Start

开始任何改动前，先阅读：

1. `README.md`
2. `docs/repo-scope.md`
3. `docs/current-priority.md`
4. `docs/dev-workflow.md`

## Branches

分支命名规则：

- `feature/<topic>`
- `fix/<topic>`
- `exp/<topic>`

示例：

- `feature/hdr-publish-pocket`
- `fix/highlight-rolloff`
- `exp/iphone-normalize-pass-1`

## Commit Style

保持提交信息简洁、可扫描：

- `init: scaffold hdr creator workspace`
- `feat: add pocket hdr publish dctl`
- `docs: clarify validation baseline`
- `fix: adjust release dctl naming`

## Source Of Truth

- `src/` 是源码真源
- `release/dctl/` 是给 Resolve 的投放副本
- 不要只改 `release/` 而忘记同步 `src/`

## Validation Evidence

代码改动后至少补下面之一：

- 更新相关文档，说明目标和假设
- 增加一张关键截图到 `tests/stills/`

截图命名：

- `<device>_<scene>_<variant>_<date>.png`

## How To Describe Work

在文档或提交中尽量显式写出：

- 这次改动服务的结果目标
- 当前假设是什么
- 已验证了什么
- 还有什么未验证

## Scope Control

未经明确确认，不要主动把仓库扩展到：

- GUI 产品
- 自动剪辑流程
- 风格 LUT 商店
- 原始视频托管
