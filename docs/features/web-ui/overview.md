# Web UI 功能说明
Last Updated: 2026-01-27

## 这是什么

Stock Report Hunter 的本地网页界面，让你通过浏览器下载美股财报和 Earnings Call。

## 主要功能

1. **智能搜索**: 输入公司名称（如 "Apple"）或股票代码（如 "AAPL"），自动识别
2. **一键下载**: 同时下载 SEC 财报和 Earnings Call Transcript
3. **结果展示**: 显示下载的文件和报告发布日期

## 如何启动

```bash
cd stock_report_hunt
streamlit run app.py
```

浏览器会自动打开 `http://localhost:8501`

## 界面说明

1. **输入框**: 输入股票代码或公司名称
2. **匹配提示**: 如果输入公司名称，会显示匹配到的股票代码
3. **下载选项**: 选择要下载的内容（SEC 财报 / Earnings Call）
4. **下载按钮**: 点击开始下载
5. **结果区**: 显示下载的文件列表和日期
