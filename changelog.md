# Changelog
Last Updated: 2026-01-27

## [v1.0] - 2026-01-27
### Added
- Watchlist 管理 (`watchlist.py`)
- 日历视图显示财报/Earnings Call 日期 (`calendar_data.py`)
- **未来 Earnings 日期获取** (yfinance，含精确时间和盘前/盘后 BMO/AMC)
- 批量下载 Watchlist 中所有股票
- 侧边栏 Watchlist 管理界面

### Changed
- `app.py` - 重构为多页面结构（单股票查询 / 日历视图）
- 日历视图分离「即将到来」和「历史记录」
- 布局改为 wide 模式

### Files Changed
- `watchlist.py` - 新建，Watchlist 管理
- `calendar_data.py` - 新建，日历数据获取（含未来日期）
- `app.py` - 添加日历视图和侧边栏

## [v0.4] - 2026-01-27
### Added
- Streamlit Web UI (`app.py`)
- 公司名称模糊匹配 (`ticker_lookup.py`)
- CLI 报告时间摘要输出

### Changed
- `main.py` - `download_and_convert` 返回文件信息
- `requirements.txt` - 添加 streamlit

### Files Changed
- `app.py` - 新建，Streamlit Web UI
- `ticker_lookup.py` - 新建，SEC 公司名称查询
- `main.py` - 添加报告时间输出

## [v0.3] - 2025-01-27
### Added
- Earnings Call transcript 下载功能 (`--earnings` 参数)
- Motley Fool 爬虫 (免费数据源)
- 输出包含 Takeaways, Summary, CEO 引用

### Files Changed
- `main.py` - 添加 `--earnings` 和 `--no-sec` 参数
- `earnings.py` - 新建，Motley Fool 爬虫逻辑

## [v0.2] - 2025-01-26
### Added
- 直接调用 SEC API 获取 filing 信息
- HTML 转 Markdown 功能 (markdownify)
- 自动提取 Primary Document

### Changed
- 移除 sec-edgar-downloader 依赖
- 输出格式从乱码 .txt 改为干净 .md

### Files Changed
- `main.py` - 完全重写
- `requirements.txt` - 更新依赖

## [v0.1] - 2025-01-26
### Added
- 基础下载功能 (sec-edgar-downloader)
- 自动打开文件夹
- 显示 my_prompt.txt 内容
