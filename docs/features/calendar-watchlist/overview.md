# 日历 + Watchlist 功能说明
Last Updated: 2026-01-27

## 这是什么

管理你关注的股票列表，在日历视图中查看所有股票的财报和 Earnings Call 日期。

## 主要功能

### Watchlist 管理
- 在侧边栏添加/删除关注的股票
- 配置文件 `watchlist.txt` 持久保存
- 支持多种格式（每行一个、逗号分隔）

### 日历视图
- **即将到来**: 显示未来已确定的 Earnings 日期（前瞻性）
- **历史记录**: 按月份展示过去的事件
- 数据源: Nasdaq API (未来日期) + SEC (历史财报) + Motley Fool (历史 Earnings Call)

### 批量下载
- 一键下载 Watchlist 中所有股票的资料
- 可选择下载 SEC 财报和/或 Earnings Call

## 如何使用

### 1. 添加股票到 Watchlist
- 方法一：在侧边栏输入股票代码，点击「添加」
- 方法二：在单股票查询页面下载时勾选「添加到 Watchlist」
- 方法三：直接编辑 `watchlist.txt` 文件

### 2. 查看日历
- 点击「财报日历」标签页
- 查看按月份分组的财报事件

### 3. 批量下载
- 在日历页面底部
- 勾选要下载的内容类型
- 点击「下载全部 Watchlist」

## watchlist.txt 格式

```
# 注释行（以 # 开头）
AAPL
NVDA
MSFT, GOOGL, AMZN
```
