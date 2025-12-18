# Story 1.8: 配置 Whisper 模型大小

## 状态 (Status)
Done

## 故事 (Story)
**作为一个** 高级用户，
**我希望** 能够配置 Whisper 转录模型的大小（base, small, medium, large），
**以便** 我可以在处理重要视频时，以牺牲速度为代价获得更高的转录准确性。

## 验收标准 (Acceptance Criteria)
1.  **CLI 参数**：CLI (`main.py`) 应接受一个新的参数 `--model-size`。
2.  **默认值**：如果未指定，默认值应保持为 `base`。
3.  **传递机制**：该参数应通过 `ExtractorFactory` 正确传递给 `VideoExtractor` 及其子类 (`DouyinExtractor`)。
4.  **验证**：使用 `--model-size medium` 运行提取应加载 medium 模型（在日志中可见）。

## 任务 / 子任务 (Tasks / Subtasks)
- [x] 更新 `ExtractorFactory`
    - [x] 修改 `get_extractor` 方法签名以接受 `model_size: str = "base"`。
    - [x] 将 `model_size` 传递给 `VideoExtractor` 和 `DouyinExtractor` 的构造函数。
- [x] 更新 CLI (`main.py`)
    - [x] 添加 `--model-size` 参数 (choices: tiny, base, small, medium, large, large-v3)。
    - [x] 在调用 `get_extractor` 时传递解析出的参数。
- [x] 验证
    - [x] 运行带有 `--model-size medium` 的测试命令。
    - [x] 检查日志确认 "Loading Whisper model: medium..."。

## 开发说明 (Dev Notes)
- `VideoExtractor` 已经支持 `model_size` 参数，只需确保它从入口点一直传递到底层即可。
- 注意 `ExtractorFactory` 中对不同域名的处理，只有视频相关的 extractor 需要这个参数。
