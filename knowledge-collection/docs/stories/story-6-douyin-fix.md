# 用户故事：抖音采集修复与优化 (Story 6)

**状态**: Draft
**故事 ID**: story-6-douyin-fix
**优先级**: High

## 1. 背景 (Context)
在 `story-5-api-service` 的验收测试中，发现抖音视频采集功能失效，报错 `Fresh cookies (not necessarily logged in) are needed`。这表明现有的 `yt-dlp` 集成或 Cookie 处理逻辑无法通过抖音最新的反爬验证。

## 2. 需求 (Requirements)
- **FR14 (抖音专用采集策略)**: 针对抖音平台实现独立的采集优化逻辑，解决 Cookie 验证失败的问题。
- **FR15 (yt-dlp 配置优化)**: 调整 `yt-dlp` 的调用参数（如 User-Agent, Referer 等）以匹配采集 Cookie 时的环境。
- **FR16 (版本兼容性)**: 确保升级或修改配置不影响 Bilibili、知乎等其他平台的现有采集功能。
- **FR17 (调研优先)**: 在编码前，必须先在 GitHub 或技术社区搜索当前成熟的抖音采集/文案提取方案，优先复用验证过的方案，避免无效尝试。
- **NFR6 (调试能力)**: 提供更详细的错误日志，以便快速定位 Cookie 或签名问题。

## 3. 技术实现策略 (Technical Strategy)
- **前置调研 (Research First)**:
    - 搜索关键词: `douyin extractor`, `yt-dlp douyin fix`, `douyin scraper 2024`, `抖音 视频 提取 开源`。
    - 评估维度: 最近更新时间、Star 数、Issue 活跃度、是否明确支持最新风控。
    - 验证流程: 选取 2-3 个最有希望的方案（如特定的 yt-dlp 分支、专门的 Python 库），编写简单的 POC 脚本逐一验证。
- **独立 Extractor**: 检查 `VideoExtractor`，如果有必要，为抖音拆分出独立的 `DouyinExtractor`，继承自 `VideoExtractor` 或 `BaseExtractor`。
- **Cookie 传递**: 验证 `yt-dlp` 的 `cookiefile` 参数是否正确指向了物理文件（`yt-dlp` 有时对内存中的 cookie dict 支持不佳，更偏好文件路径）。
- **User-Agent 统一**: 确保代码中请求使用的 UA 与 Cookie 文件中的 UA 一致（或使用通用的高兼容性 UA）。
- **依赖升级**: 尝试升级 `yt-dlp` 到最新版本。
- **临时文件**: 如果 `yt-dlp` 需要物理 Cookie 文件，考虑在运行时将内存中的 Cookie 写入临时文件供其调用。

## 4. 验收标准 (DoD)
- [ ] **抖音采集成功**: 使用最新的 `douyin.txt` Cookie，能够成功采集抖音视频（如下载音频并转录）。
- [ ] **B站采集回归**: Bilibili 视频采集功能依然正常，不受抖音修复的影响。
- [ ] **知乎采集回归**: 知乎文本采集功能依然正常。
- [ ] **API 响应**: `/extract` 接口针对抖音 URL 返回 200 及正确的 JSON 数据。

## 6. Tasks
- [x] Task 1: Research and POC Douyin extraction with `cookiefile` and `yt-dlp` upgrade.
- [x] Task 2: Implement `DouyinExtractor` class in `src/extractors/douyin_extractor.py`.
- [x] Task 3: Integrate `DouyinExtractor` into `ExtractorFactory` and `CookieManager`.
- [x] Task 4: Verify Douyin extraction (Manual & Automated).
- [x] Task 5: Regression test (Bilibili/Zhihu).

## 5. 开发笔记 (Dev Notes)
- **风险**: 抖音风控变化极快，可能需要反复调试参数。
- **隔离**: 尽量不要修改 `VideoExtractor` 的核心逻辑，而是通过子类重写或条件判断来隔离抖音的特殊逻辑。
- **Cookie 路径**: `yt-dlp` 的 Python 接口 `ydl_opts` 中，`cookiefile` 参数通常比通过 header 传递 cookie 更稳定。
- **2025-12-17**: Initial analysis showed `yt-dlp` fails with "Fresh cookies needed".
- **2025-12-17**: Implemented `DouyinExtractor` with `cookiefile` support.
- **2025-12-17**: `yt-dlp` native extraction still failed due to WAF/Anti-Crawl on desktop site.
- **2025-12-17**: Implemented **Manual Fallback Strategy**:
    - Use Mobile User-Agent to access `iesdouyin.com` share page.
    - Parse `window._ROUTER_DATA` JSON from HTML.
    - Extract direct video URL (replacing `playwm` -> `play`).
    - Pass direct URL to `yt-dlp`.
    - **Result**: Successfully extracted and transcribed video without fresh cookies.
