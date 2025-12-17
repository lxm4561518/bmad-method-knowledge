# 抖音采集技术总结 (Douyin Extraction Technical Summary)

## 1. 抖音采集遇到的问题 (Problems Encountered)

在实现抖音视频音频采集功能时，我们遇到了以下主要技术障碍：

### 1.1 `yt-dlp` 原生提取器失效
- **错误信息**: `[Douyin] Fresh cookies (not necessarily logged in) are needed`
- **原因**: 抖音加强了桌面端网页（`douyin.com`）的风控（WAF），即使提供了有效的 Netscape 格式 Cookie，`yt-dlp` 的原生提取逻辑（尝试获取 `web detail JSON`）经常因为签名验证或环境检测而失败。

### 1.2 严格的反爬虫策略 (Anti-Crawl & WAF)
- **现象**: 使用桌面版 User-Agent 访问时，请求常被重定向至验证页面或直接返回 403/412 错误。
- **Cookie 限制**: 即使通过 `cookiefile` 传递了物理 Cookie 文件，由于 IP 变动或指纹不匹配，Cookie 很快失效。

### 1.3 `yt-dlp` URL 支持限制
- **现象**: 尝试直接传递解析后的移动端 URL（`iesdouyin.com`）给 `yt-dlp` 时，报错 `Unsupported URL`。
- **原因**: `yt-dlp` 主要支持标准的 `douyin.com` 链接，对移动端 API 域名支持不佳。

---

## 2. 详细的技术解决方案 (Detailed Technical Solution)

为了解决上述问题，我们采取了**“模拟移动端 + 手动降级解析”**的混合策略，具体实现如下：

### 2.1 架构隔离 (`DouyinExtractor`)
- **继承扩展**: 创建了独立的 `DouyinExtractor` 类（继承自 `VideoExtractor`），确保针对抖音的特殊修改不会影响 Bilibili、知乎等其他平台的采集逻辑。
- **独立配置**: 为抖音提取器配置了独立的 User-Agent 和 Cookie 处理逻辑。

### 2.2 模拟移动端访问 (Mobile Simulation)
- **策略**: 放弃攻克桌面端 WAF，转而模拟 Android 移动设备。
- **实现**:
  ```python
  self.mobile_ua = 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 ...'
  ```
  使用此 UA 访问短链接（如 `v.douyin.com`）会重定向至 `iesdouyin.com` 的移动分享页，该页面的风控相对较宽松，且包含完整的视频元数据。

### 2.3 手动降级解析 (Manual Fallback Parsing)
由于 `yt-dlp` 无法解析移动端页面，我们实现了手动解析逻辑：
1.  **HTML 获取**: 使用 `requests` 库（带 Mobile UA）获取页面 HTML。
2.  **数据提取**: 使用正则表达式提取页面中内嵌的 JSON 数据块 `window._ROUTER_DATA`。
    ```python
    match = re.search(r'window\._ROUTER_DATA\s*=\s*(\{.*?\})(?:;|\s*</script>)', html, re.DOTALL)
    ```
3.  **JSON 遍历**: 解析 JSON，递归查找 `video` -> `play_addr` -> `url_list` 路径，获取视频直链。
4.  **去水印处理**: 自动将 URL 中的 `playwm`（带水印）替换为 `play`（无水印），提升内容质量。

### 2.4 直链下载集成
- **最终执行**: 将手动解析得到的**视频直链（.mp4 URL）**直接传递给 `yt-dlp`。
- **优势**: `yt-dlp` 对直链下载的支持非常稳定，不再需要处理复杂的页面解析和签名验证，从而彻底绕过了“Fresh cookies”错误。

### 2.5 完整流程图
```mermaid
graph TD
    A[输入 v.douyin.com 链接] --> B{DouyinExtractor}
    B -->|1. 尝试| C[模拟移动端请求 (Mobile UA)]
    C --> D[解析 window._ROUTER_DATA]
    D -->|成功| E[获取无水印直链]
    D -->|失败| F[回退至 yt-dlp 原生逻辑]
    E --> G[yt-dlp 下载音频]
    F --> G
    G --> H[Whisper 转录]
```
