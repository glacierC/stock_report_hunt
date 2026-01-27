# 测试指南：Earnings Call 下载
Last Updated: 2025-01-27

## 前置条件
1. 已安装 Python 3.11+
2. 已安装依赖：`pip install -r requirements.txt`

## 测试步骤

### 测试 1：下载 Apple Earnings Call
1. 运行：`python main.py AAPL --earnings --no-sec`
2. **预期结果**：
   - 终端显示 "搜索 Motley Fool..."
   - 文件夹自动打开
   - 看到 `AAPL_earnings_YYYYMMDD.md` (~50KB)

### 测试 2：验证内容质量
1. 打开下载的 `.md` 文件
2. **预期结果**：
   - 有 "Takeaways" 部分
   - 有 "Summary" 部分
   - 有 CEO/CFO 引用

### 测试 3：同时下载 SEC + Earnings
1. 运行：`python main.py NVDA --earnings`
2. **预期结果**：
   - 下载 10-K, 10-Q (SEC)
   - 下载 Earnings Call transcript
   - 所有文件在 `downloads/NVDA/`
