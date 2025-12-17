# 用户故事：实现文本提取核心功能 (FR3)

**状态**: 已完成 (Completed)
**故事 ID**: story-1-text-extraction
**优先级**: 高 (High)

## 1. 背景 (Context)
我们需要为文本类平台（知乎、微信公众号、今日头条）实现核心的文本提取逻辑。这涉及到实现继承自 `BaseExtractor` 的具体提取器类。

## 2. 需求 (Requirements)
- **FR3.1**: 实现 `ZhihuExtractor` 以解析知乎的问题/回答/文章。
    - 提取内容：标题、正文（需清洗为纯文本）。
    - 处理逻辑：处理“阅读更多”展开逻辑（如果可能），或在 MVP 阶段获取初始加载内容。
- **FR3.2**: 实现 `WeChatExtractor` 以解析微信公众号文章。
    - 提取内容：标题、作者、发布时间、正文。
    - 清洗逻辑：必须移除二维码、广告图片占位符等干扰信息。
- **FR3.3**: 实现 `ToutiaoExtractor` 以解析今日头条新闻。
    - 提取内容：标题、正文。
- **FR3.4**: 确保所有提取器都使用 `requests` 库，并注入 `BaseExtractor` 中提供的 `cookies`。
- **FR3.5**: 确保使用 `BeautifulSoup` 进行 HTML 解析和清洗。

## 3. 技术实现策略 (Technical Implementation Strategy)
- **文件位置**:
    - `knowledge-collection/src/extractors/text_extractor.py`
- **类结构**:
    - `TextExtractor(BaseExtractor)`: 通用逻辑（例如通用的 HTML 清洗方法）。
    - `ZhihuExtractor(TextExtractor)`: 针对知乎的特定 CSS 选择器。
    - `WeChatExtractor(TextExtractor)`: 针对公众号的特定 CSS 选择器。
    - `ToutiaoExtractor(TextExtractor)`: 针对头条的特定 CSS 选择器。
- **依赖库**:
    - `requests`, `beautifulsoup4`

## 4. 验收标准 (DoD)
- [ ] `ZhihuExtractor` 能从给定的知乎 URL 中提取标题和正文。
- [ ] `WeChatExtractor` 能从给定的公众号 URL 中提取标题和正文。
- [ ] `ToutiaoExtractor` 能从给定的头条 URL 中提取标题和正文。
- [ ] 提取的内容不包含 HTML 标签（纯文本）。
- [ ] 单元测试或简单的运行脚本能验证从样例 URL（模拟或真实）的提取功能。

## 5. 参考资源
- PRD: `knowledge-collection/docs/prd.md` (FR3)
- 架构文档: `knowledge-collection/docs/architecture.md` (第 4.1 节)
