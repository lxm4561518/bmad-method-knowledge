# 用户故事：实现视频提取与转录 (FR4, FR5)

**状态**: 已完成 (Completed)
**故事 ID**: story-2-video-extraction
**优先级**: 高 (High)

## 1. 背景 (Context)
我们需要为 Bilibili 和抖音等视频平台实现内容处理能力。这包括下载音频流并使用 OpenAI Whisper 进行转录。

## 2. 需求 (Requirements)
- **FR4**: 实现 `VideoExtractor` 逻辑以下载音频。
    - 使用 `yt-dlp` 库（通过 Python 包装器或子进程）获取音频流（仅下载最佳质量音频）。
    - 支持 Bilibili 和抖音的 URL。
- **FR5**: 实现基于 `openai-whisper` 的转录逻辑。
    - 加载 Whisper 模型（默认为 'base' 或 'small'）。
    - 将下载的音频文件转录为文本。
    - 必须支持中文识别 (`language='zh'`)。
- **输出**: 返回包含标题（来自视频元数据）和内容（转录文本）的结构化字典。

## 3. 技术实现策略 (Technical Implementation Strategy)
- **文件位置**:
    - `knowledge-collection/src/extractors/video_extractor.py`
- **类结构**:
    - `VideoExtractor(BaseExtractor)`
- **依赖库**:
    - `yt-dlp`, `openai-whisper`, `torch`
- **流程**:
    1. `extract(url)` 调用内部方法 `_download_audio(url)` -> 返回 .mp3/.wav 文件路径。
    2. 调用内部方法 `_transcribe_audio(path)` -> 返回文本。
    3. 返回字典结果。

## 4. 验收标准 (DoD)
- [ ] `VideoExtractor` 能成功从有效的 Bilibili/抖音 URL 下载音频。
- [ ] Whisper 模型能正确加载并转录音频。
- [ ] 转录后的文本正确包含在返回结果的 `content` 字段中。
- [ ] 临时音频文件在处理后被清理（推荐）或缓存。

## 5. 参考资源
- PRD: `knowledge-collection/docs/prd.md` (FR4, FR5)
- 架构文档: `knowledge-collection/docs/architecture.md` (第 4.1, 4.3 节)
