# 用户故事：HTTP API 服务支持 (Story 5)

**状态**: Draft
**故事 ID**: story-5-api-service
**优先级**: High

## 1. 背景 (Context)
目前工具仅提供 CLI 接口。用户希望通过 HTTP 接口调用文案提取逻辑，以便于外部工具（如 Postman）集成或自动化调用。

## 2. 需求 (Requirements)
- **FR10 (API Endpoint)**: 提供一个 HTTP POST 接口（如 `/extract` 或 `/api/extract`）。
- **FR11 (输入格式)**: 接口接收 JSON 格式的 Body，包含 `url` 字段。
- **FR12 (输出格式)**: 接口返回 JSON 格式结果，包含 `title`, `content`, `url`, `timestamp`。
- **FR13 (逻辑复用)**: 复用现有的 `TextExtractor` 和 `VideoExtractor` 逻辑（包括 Cookie 处理）。

## 3. 技术实现策略 (Technical Strategy)
- **技术栈**: 使用 `FastAPI` 作为 Web 框架，`Uvicorn` 作为服务器。
- **新增模块**: 创建 `src/server.py` 或 `src/api.py`。
- **依赖管理**: 在 `requirements.txt` 中添加 `fastapi`, `uvicorn`, `pydantic`。
- **流程**:
    1.  接收 POST 请求。
    2.  解析 Body 中的 `url`。
    3.  调用 `ExtractorFactory.create_extractor(url)`。
    4.  执行 `extractor.extract(url)`。
    5.  构造标准 JSON 响应。
    6.  处理异常并返回适当的 HTTP 状态码（400/500）。

## 4. 验收标准 (DoD)
- [ ] **API 可用性**: 启动服务后，可以通过 Postman 访问接口。
- [ ] **输入处理**: 发送 `{ "url": "..." }` 能被正确解析。
- [ ] **输出一致性**: 返回的 JSON 结构与 CLI 输出一致，且符合用户提供的示例：
    ```json
    {
        "title": "示例标题",
        "content": "示例内容...",
        "url": "https://...",
        "timestamp": "2025-12-17T..."
    }
    ```
- [ ] **功能覆盖**: 支持文本（知乎等）和视频（Bilibili等）链接的提取。
- [ ] **异常处理**: 对于不支持的 URL 或提取失败的情况，返回包含错误信息的 JSON 和对应 HTTP 状态码。

## 5. 开发笔记 (Dev Notes)
- **架构变更**: 引入 Web Server 层。
- **性能注意**: 视频提取涉及下载和转录，可能耗时较长。MVP 阶段可接受同步阻塞，但需注意设置合理的超时时间。
- **复用性**: 确保直接复用 `src/extractors` 中的逻辑，避免代码重复。
- **Cookie**: API 服务启动时也需加载 `cookies.json` (或通过 CookieManager 自动处理)。
