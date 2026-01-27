# 测试指南：HTML 转 Markdown
Last Updated: 2025-01-27

## 测试步骤

### 测试 1：验证转换效果
1. 运行：`python main.py AAPL`
2. 打开 `downloads/AAPL/AAPL_10-K_*.md`
3. **预期结果**：
   - 文件大小 < 500KB
   - 内容是纯文本和 Markdown 表格
   - 没有 `<div>`、`<span>` 等 HTML 标签

### 测试 2：验证表格保留
1. 在 Markdown 文件中搜索 `|`（表格分隔符）
2. **预期结果**：
   - 财务数据表格以 Markdown 格式呈现
   - 如：`| Revenue | $100M |`

### 测试 3：ChatBot 兼容性
1. 将 `.md` 文件拖入 ChatGPT 或 Claude
2. 问："总结这份财报的关键数据"
3. **预期结果**：
   - AI 能正常解析内容
   - 能提取出财务数据
