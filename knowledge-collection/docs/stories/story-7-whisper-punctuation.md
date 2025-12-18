# Story 1.7: 增强视频转录的可读性

## 状态 (Status)
Done

## 故事 (Story)
**作为一个** 内容消费者，
**我希望** 视频转录的文本包含正确的标点符号和句子分段，
**以便** 我可以轻松阅读和理解内容，而不会因为非结构化的文本块而感到精神疲劳。

## 验收标准 (Acceptance Criteria)
1.  **标点符号**：转录输出必须包含适用于口语（特别是中文）的标准标点符号（逗号、句号、问号）。
2.  **分段**：输出文本应具有视觉结构（例如，使用换行符或段落），而不是单个连续的字符串。
3.  **配置**：该解决方案应在现有的 `VideoExtractor` 中工作，无需外部 API 调用（除非必须使用本地轻量级标点符号模型）。
4.  **验证**：使用用户提供的示例文本（或类似音频）进行的测试运行应产生可读的输出。

## 任务 / 子任务 (Tasks / Subtasks)
- [ ] 研究 Whisper 的标点符号能力
    - [ ] 调查 Whisper API 中的 `initial_prompt` 参数以鼓励使用标点符号。
    - [ ] 调查利用 Whisper 响应中的 `segments` 来实现自然换行。
- [ ] 在 `VideoExtractor` 中实现标点/分段逻辑
    - [ ] 更新 `_transcribe_audio` 方法以使用 `initial_prompt`（例如，“这是一段中文对话，包括标点符号。”）。
    - [ ] 如果 `result['text']` 仍然没有标点符号，则重构返回值以从带有换行符的 `segments` 构建文本。
- [ ] 使用测试用例进行验证
    - [ ] 对示例视频（例如上一个故事中的抖音链接）运行提取。
    - [ ] 检查输出 JSON 的标点符号和可读性。

## 开发说明 (Dev Notes)
### 技术背景
- **当前实现**：`VideoExtractor` 使用 `self.model.transcribe(filepath, language='zh')` 并返回 `result['text']`。
- **Whisper 行为**：OpenAI Whisper 模型（尤其是像 `base` 这样的小型模型）在中文标点符号方面可能会遇到困难，除非经过提示或后处理。
- **优化策略**：
    1.  **提示 (Prompting)**：传递 `initial_prompt="这是一段中文对话，包括标点符号。"` 告诉解码器模仿该风格，通常会诱导生成标点符号。
    2.  **分段 (Segments)**：`result['segments']` 包含具有开始/结束时间和文本的分段列表。用 `\n` 连接这些分段是提高可读性的简单方法。
    
### 来源参考
- `knowledge-collection/src/extractors/video_extractor.py`：需要修改 `_transcribe_audio` 方法（第 60 行）。
- `knowledge-collection/docs/prd.md`：FR5（自动转录）和 NFR3（易用性 - 隐含的可读性）。

### 项目结构
- 修改 `knowledge-collection/src/extractors/video_extractor.py`。
- 除非创建一个单独的 `text_processor.py` 实用程序（对于此 MVP 来说可能是不必要的），否则不需要新文件。

## 变更日志 (Change Log)
| 日期 | 版本 | 描述 | 作者 |
| :--- | :--- | :--- | :--- |
| 2025-12-18 | 1.0 | 基于用户反馈的初稿 | Bob (SM) |
