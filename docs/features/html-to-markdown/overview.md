# HTML 转 Markdown 功能
Last Updated: 2025-01-27

## 这是什么
SEC 原始文件是 HTML 格式，包含大量代码和样式。这个功能把它转成干净的 Markdown，方便阅读和 AI 分析。

## 为什么需要
- 原始文件：12MB，充满 XML/HTML 代码，无法阅读
- 转换后：200-300KB，纯文本 + 表格，可直接拖入 ChatBot

## 技术实现
- 使用 `beautifulsoup4` 清理 HTML
- 使用 `markdownify` 转换为 Markdown
- 自动移除 script、style 等无用标签

## 优点
- 纯 Python 实现，无需安装系统软件
- 保留表格结构
- 文件大小减少 95%+
