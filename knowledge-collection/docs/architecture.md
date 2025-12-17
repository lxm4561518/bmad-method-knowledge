# 项目技术架构文档 (Architecture Document)

## 1. 简介 (Introduction)

本文档详细描述了 **内容提取与转录工具 (Content Extractor & Transcriber)** 的技术架构。该项目旨在提供一个统一的命令行接口 (CLI)，用于从多种网络平台（知乎、Bilibili、抖音等）高效提取内容并转换为结构化文本。

### 变更日志 (Change Log)
| Date | Version | Description | Author |
| :--- | :--- | :--- | :--- |
| 2025-12-17 | 1.0 | Initial Architecture Design | Winston (Architect) |

## 2. 高层架构 (High Level Architecture)

### 技术摘要 (Technical Summary)
本项目采用 **模块化单体 (Modular Monolith)** 架构，以 Python 为核心语言。系统遵循 **策略模式 (Strategy Pattern)** 来管理不同平台的提取逻辑，利用 **工厂模式 (Factory Pattern)** 进行动态分发。核心依赖包括 `BeautifulSoup4`（文本解析）、`yt-dlp`（媒体下载）和 `OpenAI Whisper`（语音转录）。

### 高层概览 (High Level Overview)
1.  **架构风格**: 命令行驱动的模块化应用。
2.  **仓库结构**: 单一仓库 (Monorepo)，源代码位于 `src/`。
3.  **核心流程**: URL 输入 -> 策略路由 -> Cookie 注入 -> 提取/下载 -> 转录 (可选) -> JSON 输出。
4.  **关键决策**:
    - **本地优先**: 转录在本地运行（Whisper），确保隐私且无需 API 成本（但也支持未来扩展 API）。
    - **插件化提取器**: 每个平台对应一个独立的 `Extractor` 类，便于扩展。

### 高层架构图 (High Level Project Diagram)
```mermaid
graph TD
    User[用户] -->|输入 URL| CLI[命令行入口 (main.py)]
    CLI -->|请求| Factory[Extractor Factory]
    Factory -->|匹配域名| Strategy{选择策略}
    
    Strategy -->|知乎/公众号/头条| TextExt[Text Extractor]
    Strategy -->|B站/抖音| VideoExt[Video Extractor]
    
    Config[Cookie Manager] -->|注入 Cookies| TextExt
    Config -->|注入 Cookies| VideoExt
    
    TextExt -->|HTTP 请求| Web[目标网站]
    VideoExt -->|yt-dlp| Media[媒体服务器]
    
    VideoExt -->|音频流| Whisper[Whisper ASR 模型]
    Whisper -->|转录文本| Result
    TextExt -->|清洗文本| Result
    
    Result[结构化数据] -->|保存| JSON[JSON 文件]
```

## 3. 技术栈 (Tech Stack)

### 核心编程语言
- **Python 3.8+**: 考虑到 AI 库（Whisper, Torch）的兼容性和丰富的爬虫生态。

### 关键库与框架
- **CLI**: `argparse` (标准库) - 保持轻量级。
- **HTTP/爬虫**: `requests`, `beautifulsoup4` - 处理静态文本。
- **媒体处理**: `yt-dlp` - 强大的视频下载工具。
- **AI/ML**: `openai-whisper`, `torch` - 语音转文字。
- **鉴权**: `browser-cookie3` (可选) 或原生 `json` 加载 - 管理 Cookies。

### 数据存储
- **文件系统**: JSON 文件作为最终输出，无需数据库。

## 4. 详细组件设计 (Detailed Component Design)

### 4.1 提取器模块 (Extractors)
遵循 `BaseExtractor` 抽象基类，所有具体提取器必须实现 `extract(url) -> dict` 方法。

- **BaseExtractor**: 定义接口和通用工具（如请求头生成）。
- **TextExtractor (通用文本)**:
    - `ZhihuExtractor`: 专门处理知乎问答结构。
    - `WeChatExtractor`: 去除公众号特有的干扰元素。
    - `ToutiaoExtractor`: 解析头条新闻接口。
- **VideoExtractor (通用视频)**:
    - 负责调用 `yt-dlp` 获取音频流。
    - 负责初始化和调用 `Whisper` 模型。

### 4.2 Cookie 管理器 (Cookie Manager)
- 负责读取 `cookies.json`。
- 提供 `get_cookies(domain)` 方法，根据 URL 自动匹配最长前缀域名的 Cookie。

### 4.3 转录引擎 (Transcription Engine)
- 封装 Whisper 模型调用。
- 提供简单的缓存机制（如果音频文件已存在则跳过下载）。
- 支持模型大小配置（base/small/medium），平衡速度与精度。

## 5. 数据流 (Data Flow)

1.  **初始化**: CLI 启动，加载 `cookies.json` 到内存。
2.  **路由**: `ExtractorFactory` 解析输入 URL，实例化对应的 `Extractor` 子类。
3.  **执行**:
    - **文本流**: `requests.get` -> `BeautifulSoup` 解析 -> 清洗 -> 提取 Title/Content。
    - **视频流**: `yt-dlp` 下载音频 (mp3/wav) -> `Whisper` 加载音频 -> 推理 -> 生成 Text。
4.  **输出**: 结果字典序列化为 JSON，写入 `outputs/` 目录。

## 6. 安全与隐私 (Security and Privacy)
- **Cookie 安全**: `cookies.json` 包含敏感信息，应添加 `.gitignore` 防止意外提交。
- **本地处理**: 音频转录在本地完成，不上传第三方服务器。

## 7. 项目目录结构 (Project Directory Structure)
```
/
├── .bmad-core/          # BMAD 方法论核心文件
└── knowledge-collection/             # 项目主目录
    ├── docs/            # 文档目录
    │   ├── brief.md     # 项目简报
    │   ├── prd.md       # 产品需求文档
    │   └── architecture.md # 架构文档
    ├── src/             # 源代码目录
    │   ├── extractors/  # 提取器模块
    │   │   ├── __init__.py
    │   │   ├── base.py  # 提取器基类
    │   │   ├── factory.py # 提取器工厂
    │   │   ├── text_extractor.py # 文本类提取器
    │   │   └── video_extractor.py # 视频类提取器
    │   ├── cookie_manager.py # Cookie 管理器
    │   └── main.py      # 程序入口 (CLI)
    ├── outputs/         # 输出文件目录 (自动创建)
    ├── cookies.json     # 用户 Cookie 配置文件 (需手动创建)
    ├── requirements.txt # 项目依赖
    └── README.md        # 项目说明
```

## 8. 部署与运维 (Deployment)
- **环境**: 推荐使用 `venv` 或 `conda` 管理依赖。
- **安装**: `pip install -r requirements.txt`。
- **模型**: 初次运行会自动下载 Whisper 模型权重（约 100MB - 3GB，取决于选择的模型）。
