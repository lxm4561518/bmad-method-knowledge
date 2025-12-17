# 用户故事：重构 Cookie 管理 - 支持目录读取 (Story 4)

**状态**: 待定 (Pending)
**故事 ID**: story-4-cookie-refactor
**优先级**: 高 (High)

## 1. 背景 (Context)
用户反馈将所有 Cookie 存储在单个 `cookies.json` 中过于杂乱。用户已将 Cookie 按平台拆分为单独的 `.txt` 文件（Netscape 格式），存放在 `knowledge-collection/cookies/` 目录下。

## 2. 需求 (Requirements)
- **FR7**: `CookieManager` 需支持从指定目录读取所有 Cookie 文件。
- **FR8**: 识别 Netscape 格式的 Cookie 文件（如 `zhihu.txt`, `bilibili.txt`）。
- **FR9**: 根据文件名（无扩展名）作为 Domain Key（如 `zhihu`, `bilibili`）存储和检索 Cookie。
- **NFR5**: 保持与现有 `extractors` 的兼容性（即最终提供给 extractor 的仍是 dict 格式）。

## 3. 技术实现策略
- **CookieManager**:
    - 构造函数接受 `cookie_dir` 参数。
    - 使用 `glob` 遍历目录下所有 `.txt` 文件。
    - 使用 `http.cookiejar.MozillaCookieJar` 解析 Netscape 格式文件。
    - 将解析后的 Cookie 转换为 Dict 格式存储。
- **Main CLI**:
    - 更新参数 `--cookie-file` 为 `--cookie-dir` (或自适应)。
    - 默认路径指向 `cookies/`。

## 4. 验收标准 (DoD)
- [x] 能正确读取 `cookies/` 目录下的 `zhihu.txt` 等文件。
- [x] 能正确解析 Netscape 格式的 Cookie 内容。
- [x] 运行 CLI 时能自动加载对应平台的 Cookie。
