# Changelog
Last Updated: 2026-01-27

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
