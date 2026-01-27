# Earnings Call Transcript 下载功能
Last Updated: 2025-01-27

## 这是什么
输入美股代码，自动下载最新的 Earnings Call（财报电话会）文字稿。

## 给谁用
需要了解管理层对业绩解读的投资研究者。

## 怎么用
```bash
# 只下载 Earnings Call
python main.py AAPL --earnings --no-sec

# 同时下载 SEC 财报和 Earnings Call
python main.py AAPL --earnings
```

## 会发生什么
1. 工具从 Motley Fool 查找最新的 transcript
2. 下载并转换成 Markdown 格式
3. 自动打开下载文件夹
4. 显示你的分析 prompt

## 文件内容
下载的 Markdown 包含：
- **Takeaways** - 关键财务数据摘要
- **Summary** - 电话会总结
- **Call participants** - 参与者名单
- **CEO/CFO 引用** - 重要发言

## 数据源
The Motley Fool (免费，无需 API Key)

## 限制
- 只能下载 Motley Fool 收录的公司
- 新财报可能需要等待几小时才会被收录
