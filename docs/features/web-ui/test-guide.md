# Web UI 测试指南
Last Updated: 2026-01-27

## 准备工作

1. 安装依赖:
   ```bash
   pip install -r requirements.txt
   ```

2. 设置环境变量（可选，用于 SEC API）:
   ```bash
   export SEC_USER_AGENT="YourApp your@email.com"
   ```

## 测试步骤

### 测试 1: 启动 Web UI

1. 运行命令:
   ```bash
   streamlit run app.py
   ```

2. 预期结果:
   - 浏览器自动打开 `http://localhost:8501`
   - 看到 "Stock Report Hunter" 页面
   - 有输入框和下载选项

### 测试 2: 股票代码输入

1. 在输入框输入 `AAPL`
2. 预期结果:
   - 直接识别为 Apple Inc.

### 测试 3: 公司名称模糊匹配

1. 在输入框输入 `Apple`
2. 预期结果:
   - 显示 "匹配到: AAPL - Apple Inc."
   - 可展开查看其他匹配结果

### 测试 4: 下载功能

1. 输入 `AAPL`
2. 勾选 "SEC 财报" 和 "Earnings Call"
3. 点击 "开始下载"
4. 预期结果:
   - 显示下载进度
   - 完成后显示文件列表和日期
   - 显示文件保存路径

### 测试 5: CLI 报告时间输出

1. 运行命令:
   ```bash
   python main.py AAPL --earnings
   ```

2. 预期结果:
   - 下载完成后显示 "报告时间摘要"
   - 列出 10-K/10-Q 发布日期
   - 列出 Earnings Call 日期

## 常见问题

- **SEC API 访问失败**: 确保设置了 `SEC_USER_AGENT` 环境变量
- **Streamlit 启动失败**: 确保安装了 `streamlit>=1.30.0`
