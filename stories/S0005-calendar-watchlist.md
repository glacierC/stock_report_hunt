# S0005 - 日历 + Watchlist
Last Updated: 2026-01-27

## 状态: Done
## 完成时间: 2026-01-27

## 目标
可视化追踪关注股票的财报和 Earnings Call 日期，支持批量下载。

**重要补充**: 日历需显示**未来**已确定的财报/Earnings Call 日期（前瞻性），不仅是历史记录。

## 验收标准
- [x] 创建 `watchlist.txt`，写入 AAPL, NVDA, MSFT
- [x] 打开 Web UI，看到日历视图
- [x] 日历上标注各股票的财报日期和 Earnings Call 日期
- [x] 支持一键批量下载 Watchlist 中所有股票

## 涉及文件

### 代码
- `watchlist.py` (新建) - Watchlist 管理
- `calendar_data.py` (新建) - 获取财报/Earnings Call 日期
- `app.py` (修改) - 添加日历视图页面
- `watchlist.txt` (示例) - 股票列表配置

### 文档
- `docs/features/calendar-watchlist/overview.md`
- `docs/features/calendar-watchlist/test-guide.md`

## 技术方案
1. **Watchlist**: 简单文本文件，每行一个 ticker
2. **日期数据**:
   - SEC 财报日期: 已有 `get_latest_filing` 返回日期
   - Earnings Call 日期: 从 Motley Fool 解析
3. **日历 UI**: Streamlit + streamlit-calendar 或自定义表格视图

## 验收记录
- 2026-01-27: 代码实现完成
- watchlist.py: Watchlist 管理（增删改查）
- calendar_data.py: 获取 SEC 和 Earnings Call 日期
- app.py: 日历视图 + 侧边栏管理 + 批量下载
