# S0003 - Earnings Call 抓取
Last Updated: 2025-01-27

## 状态
Todo → Doing → Blocked → **Done**

## 完成时间
2025-01-27

## 目标
给定股票代码，自动抓取公司最新的 Earnings Call（财报电话会）文件，包括 transcript、音频或 PPT。

## 背景
- v0.2 已实现 SEC 财报（10-K/10-Q）下载
- 用户还需要 Earnings Call 来了解管理层对业绩的解读
- Earnings Call 不在 SEC，而是在公司 Investor Relations 页面

## 调研结论 (2025-01-27)

### 数据源选择: Financial Modeling Prep (FMP)
- 覆盖 8000+ 美股公司
- 有免费 tier
- 返回完整 transcript 文本
- API: `https://financialmodelingprep.com/api/v3/earning_call_transcript/{symbol}?quarter=X&year=YYYY`

### 文件类型: 只下载 Transcript
- 文字稿最有用，可直接喂给 AI 分析

## 验收标准
- [x] 运行 `python main.py AAPL --earnings`
- [x] 终端显示找到的 Earnings Call 信息
- [x] 下载文件到 `downloads/AAPL/` (50KB Markdown)
- [x] 文件夹自动打开
- [x] 下载完整 transcript (含 Takeaways, Summary, CEO 引用)

## 涉及文件
- `main.py` - 添加 `--earnings` 参数
- `earnings.py` (新建) - Earnings Call 抓取逻辑
- `requirements.txt` - 可能需要新依赖

## 验收记录
（完成后填写）
