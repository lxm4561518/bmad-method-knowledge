# 用户故事：CLI 集成与 Cookie 管理 (FR1, FR2, FR6)

**状态**: 待定 (Pending)
**故事 ID**: story-3-cli-integration
**优先级**: 中 (Medium)

## 1. 背景 (Context)
将各个提取器连接到主 CLI 入口点，确保 Cookie 能正确加载，并生成格式化的 JSON 输出。

## 2. 需求 (Requirements)
- **FR1**: 完成 `ExtractorFactory`，将 URL 正确路由到新的 `Zhihu/WeChat/Toutiao/Video` 提取器。
- **FR2**: 确保 `CookieManager` 正确加载 `cookies.json` 并将特定域名的 Cookie 传递给提取器。
- **FR6**: 确保 `main.py` 将结果保存为 `outputs/` 目录下格式正确的 JSON 文件。
- **NFR3**: 在 CLI 中添加基本的错误处理和用户反馈（打印语句）。

## 3. 技术实现策略 (Technical Implementation Strategy)
- **文件位置**:
    - `knowledge-collection/src/main.py`
    - `knowledge-collection/src/cookie_manager.py`
    - `knowledge-collection/src/extractors/factory.py`
- **任务**:
    - 更新 `factory.py` 的路由逻辑。
    - 增强 `cookie_manager.py` 的域名匹配逻辑（MVP 阶段简单的字符串匹配即可）。
    - 完善 `main.py` 的参数解析和输出日志。

## 4. 验收标准 (DoD)
- [x] 运行 `python main.py <url>` 能成功识别平台。
- [x] Cookie 能被传递给提取器。
- [x] 在 `outputs/` 目录下生成 JSON 文件，包含键：`title`, `content`, `url`, `timestamp`。
- [x] 系统能优雅地处理不支持的 URL。

## 5. 参考资源
- PRD: `knowledge-collection/docs/prd.md`
- 架构文档: `knowledge-collection/docs/architecture.md`
