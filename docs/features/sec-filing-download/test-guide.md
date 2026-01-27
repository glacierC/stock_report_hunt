# 测试指南：SEC 财报下载
Last Updated: 2025-01-27

## 前置条件
1. 已安装 Python 3.11+
2. 已安装依赖：`pip install -r requirements.txt`

## 测试步骤

### 测试 1：基本下载
1. 打开终端，进入项目目录
2. 运行：`python main.py NVDA`
3. **预期结果**：
   - 终端显示下载进度
   - Finder 自动打开 `downloads/NVDA/` 文件夹
   - 文件夹内有 `.md` 文件

### 测试 2：验证文件可读
1. 双击打开下载的 `.md` 文件
2. **预期结果**：
   - 看到清晰的段落和表格
   - 没有 XML 代码或乱码

### 测试 3：Prompt 显示
1. 在项目根目录创建 `my_prompt.txt`，写入任意内容
2. 运行：`python main.py AAPL`
3. **预期结果**：
   - 终端最后显示 `my_prompt.txt` 的内容
